import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import os

# Obtener la ruta de la carpeta actual
current_folder = os.getcwd()

# Crear la conexión con la base de datos SQLite
db_filename = 'precios_competencia.db'
db_path = os.path.join(current_folder, db_filename)
conn = sqlite3.connect(db_path)
c = conn.cursor()

urls = [
    "https://electropunto.com.ar/search/?q=cable+",
    "https://electropunto.com.ar/protecciones/",
    "https://electropunto.com.ar/cajas-y-canerias/",
    "https://electropunto.com.ar/accesorios-de-electricidad/"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Crear una tabla para almacenar los datos
tabla_nombre = 'electropunto'
c.execute(f'''CREATE TABLE IF NOT EXISTS {tabla_nombre}
                (Fecha TEXT, Descripcion TEXT, Precio TEXT)''')

for url in urls:
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encuentra todos los divs de los productos
    product_divs = soup.find_all("div", class_="js-item-name h2 item-name")

    for product_div in product_divs:
        # Obtiene la fecha actual
        fecha_actual = datetime.now().strftime("%d/%m/%Y")

        # Obtiene el nombre del producto
        product_name = product_div.text.strip()

        # Obtiene el identificador del producto
        product_id = product_div.attrs["data-store"].replace("product-item-name-", "")

        # Busca el precio del producto
        price_container = product_div.find_next_sibling("div", class_="item-price-container").find("div", class_="js-price-display price item-price")
        if price_container:
            product_price = price_container.text.strip()
        else:
            product_price = "No disponible"

        # Insertar los datos en la tabla
        c.execute(f"INSERT INTO {tabla_nombre} (Fecha, Descripcion, Precio) VALUES (?, ?, ?)", (fecha_actual, product_name, product_price))
        conn.commit()

# Cerrar la conexión con la base de datos
conn.close()
