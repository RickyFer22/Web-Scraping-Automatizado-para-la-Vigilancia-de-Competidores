import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import sqlite3
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import os

# Configurar las reintentos para las solicitudes
session = requests.Session()
retry = Retry(total=5, backoff_factor=0.3, status_forcelist=[500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

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

# Configurar opciones de Selenium para evitar errores de ejecución
options = Options()
options.headless = True  # Ejecutar en modo sin interfaz gráfica

# Iniciar el controlador del navegador
try:
    driver = webdriver.Firefox(options=options)
except Exception as e:
    print(f"Error al iniciar el navegador: {e}")
    conn.close()
    exit()

# Obtener las URLs de las páginas adicionales
additional_pages = [f"{base_url}page/{i}/" for base_url in base_urls for i in range(2, 100)]  # Ajusta el rango si es necesario

# Función para procesar productos en una página
def process_products(soup):
    product_divs = soup.select("div.product-small.col.has-hover.product")

    if not product_divs:
        print("No se encontraron productos en la página.")
        return

    for product_div in product_divs:
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        product_name_element = product_div.select_one("p.name.product-title.woocommerce-loop-product__title > a")
        product_name = product_name_element.text.strip() if product_name_element else "No disponible"
        price_element = product_div.select_one("div.price-wrapper > span > span > bdi")
        product_price = price_element.text.strip() if price_element else "No disponible"

        # Insertar los datos en la tabla
        c.execute(f"INSERT INTO {tabla_nombre} (Fecha, Descripcion, Precio) VALUES (?, ?, ?)", (fecha_actual, product_name, product_price))
        conn.commit()

try:
    for base_url in base_urls:
        try:
            print(f"Accediendo a: {base_url}")
            driver.get(base_url)

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)

                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # Verificar si la página contiene un mensaje de error
            error_message = soup.find(string="¡Ups! No pudimos encontrar esa página.")
            if error_message:
                print(f"Página no encontrada: {base_url}")
                continue

            process_products(soup)

            # Visitar páginas adicionales si existen
            for page_url in additional_pages:
                try:
                    driver.get(page_url)
                    time.sleep(3)

                    html = driver.page_source
                    soup = BeautifulSoup(html, 'html.parser')

                    error_message = soup.find(string="¡Ups! No pudimos encontrar esa página.")
                    if error_message:
                        print(f"Página no encontrada: {page_url}")
                        break

                    process_products(soup)
                except Exception as e:
                    print(f"Error al procesar {page_url}: {e}")
                    continue

        except Exception as e:
            print(f"Error al acceder a {base_url}: {e}")
            continue
finally:
    # Cerrar la conexión con la base de datos y el navegador
    conn.close()
    driver.quit()
    print("Conexión cerrada y navegador terminado.")


