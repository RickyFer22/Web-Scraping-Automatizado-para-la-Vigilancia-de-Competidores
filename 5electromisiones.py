import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

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

# Configurar los reintentos para las solicitudes HTTP
session = requests.Session()
retry = Retry(total=5, backoff_factor=0.3, status_forcelist=[500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

# Crear la tabla en SQLite
tabla_nombre = 'electromisiones'
c.execute(f'''CREATE TABLE IF NOT EXISTS {tabla_nombre}
                (Fecha TEXT, Descripcion TEXT, Precio TEXT)''')

try:
    for base_url in base_urls:
        try:
            print(f"Accediendo a: {base_url}")
            response = session.get(base_url, headers=headers, timeout=10)
            response.raise_for_status()  # Lanza una excepción para códigos de error HTTP

            soup = BeautifulSoup(response.content, 'html.parser')

            # Encuentra los divs de productos con ambos selectores
            product_divs = soup.select(
                "#category-description article, #js-product-list article"
            )

            if not product_divs:
                print(f"No se encontraron productos en: {base_url}")
                continue

            for product_div in product_divs:
                fecha_actual = datetime.now().strftime("%d/%m/%Y")

                # Intentar extraer el nombre del producto con varios selectores
                product_name_element = product_div.select_one("h3, h6")
                product_name = product_name_element.text.strip() if product_name_element else "No disponible"

                # Intentar extraer el precio del producto con varios selectores
                price_element = product_div.select_one("span.price, div.tv-product-price span")
                product_price = price_element.text.strip() if price_element else "No disponible"

                # Insertar los datos en la base de datos
                c.execute(f"INSERT INTO {tabla_nombre} (Fecha, Descripcion, Precio) VALUES (?, ?, ?)", 
                          (fecha_actual, product_name, product_price))
                conn.commit()

        except requests.exceptions.RequestException as e:
            print(f"Error al acceder a {base_url}: {e}")
            continue

finally:
    # Cerrar la conexión con la base de datos
    conn.close()
    print("Conexión con la base de datos cerrada.")


