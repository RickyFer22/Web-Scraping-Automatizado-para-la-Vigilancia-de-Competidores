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

base_urls = [
    "https://www.electromisiones.com.ar/3-materiales_electricos",
    "https://www.electromisiones.com.ar/4-iluminacion?order=product.date_add.desc",
    "https://www.electromisiones.com.ar/11-cables",
    "https://www.electromisiones.com.ar/471-cajas?categoria=derivacion,tapas",
    "https://www.electromisiones.com.ar/34-termicas_y_disyuntores"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Crear una tabla para almacenar los datos
tabla_nombre = 'electromisiones'
c.execute(f'''CREATE TABLE IF NOT EXISTS {tabla_nombre}
                (Fecha TEXT, Descripcion TEXT, Precio TEXT)''')

for base_url in base_urls:
    response = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encuentra todos los divs de los productos
    product_divs = soup.select("#category-description > div > div > section > div > div > div > div > div > div.elementor-element.elementor-element-51421d9.elementor-atc--align-justify.elementor-widget.elementor-widget-product-grid.elementor-widget-heading.elementor-widget-product-box > div > div > article") + \
                   soup.select("#js-product-list > div > div > article")

    for product_div in product_divs:
        # Obtiene la fecha actual
        fecha_actual = datetime.now().strftime("%d/%m/%Y")

        # Obtiene el nombre del producto
        product_name_element = product_div.select_one("a > div.elementor-content > h3, div.tvproduct-wrapper.grid > div.tvproduct-info-box-wrapper > div > div.tvproduct-name.product-title > a > h6")
        product_name = product_name_element.text.strip() if product_name_element else "No disponible"

        # Obtiene el precio del producto
        price_element = product_div.select_one("a > div.elementor-content > div > span, div.tvproduct-wrapper.grid > div.tvproduct-info-box-wrapper > div > div.tv-product-price.tvproduct-name-price-wrapper > div > span")
        product_price = price_element.text.strip() if price_element else "No disponible"

        # Insertar los datos en la tabla
        c.execute(f"INSERT INTO {tabla_nombre} (Fecha, Descripcion, Precio) VALUES (?, ?, ?)", (fecha_actual, product_name, product_price))
        conn.commit()

# Cerrar la conexión con la base de datos
conn.close()
