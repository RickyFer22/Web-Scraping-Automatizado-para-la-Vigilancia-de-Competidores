import requests
from bs4 import BeautifulSoup
import sqlite3
import time
from selenium import webdriver
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
    "https://iluminar.ar/product-category/electricidad/",
    "https://iluminar.ar/product-category/iluminacion/"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Crear una tabla para almacenar los datos
tabla_nombre = 'iluminar'
c.execute(f'''CREATE TABLE IF NOT EXISTS {tabla_nombre}
                (Fecha TEXT, Descripcion TEXT, Precio TEXT)''')

# Iniciar el controlador de navegador (en este caso, Firefox)
driver = webdriver.Firefox()

# Obtener las URLs de las páginas adicionales
additional_pages = [f"{base_url}page/{i}/" for base_url in base_urls for i in range(2, 100)]  # Cambia el rango si es necesario

# Función para procesar productos en una página
def process_products(soup):
    product_divs = soup.select("#main > div > div.col.large-9 > div > div.products.row.row-small.large-columns-4.medium-columns-3.small-columns-2.has-shadow.row-box-shadow-1.row-box-shadow-3-hover > div.product-small.col.has-hover.product")

    for product_div in product_divs:
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        product_name_element = product_div.select_one("div.box-text.box-text-products.text-center.grid-style-2 > div.title-wrapper > p.name.product-title.woocommerce-loop-product__title > a")
        product_name = product_name_element.text.strip() if product_name_element else "No disponible"
        price_element = product_div.select_one("div.box-text.box-text-products.text-center.grid-style-2 > div.price-wrapper > span > span > bdi")
        product_price = price_element.text.strip() if price_element else "No disponible"

        # Insertar los datos en la tabla
        c.execute(f"INSERT INTO {tabla_nombre} (Fecha, Descripcion, Precio) VALUES (?, ?, ?)", (fecha_actual, product_name, product_price))
        conn.commit()

for base_url in base_urls:
    try:
        # Visitar la página principal de la categoría
        driver.get(base_url)

        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Desplazarse hacia abajo
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Esperar a que se cargue el nuevo contenido
            time.sleep(5)

            # Calcular la nueva altura y mover el scroll
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Procesar la página actual
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Verificar si la página contiene el mensaje de error
        error_message = soup.find(string="¡Ups! No pudimos encontrar esa página.")
        if error_message:
            print(f"¡Se encontró un error en la página {base_url}! Saltando a la siguiente página.")
            continue

        process_products(soup)

        # Visitar páginas adicionales si existen
        for page_url in additional_pages:
            driver.get(page_url)
            time.sleep(5)  # Esperar a que se cargue la página

            # Procesar la página adicional
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # Verificar si la página contiene el mensaje de error
            error_message = soup.find(string="¡Ups! No pudimos encontrar esa página.")
            if error_message:
                print(f"¡Se encontró un error en la página {page_url}! Saltando a la siguiente página.")
                break

            process_products(soup)
    except Exception as e:
        print(f"Ocurrió un error al procesar la página {base_url}: {str(e)}. Saltando a la siguiente página.")


# Cerrar la conexión con la base de datos
conn.close()

# Cerrar el controlador del navegador
driver.quit()

