import time
from selenium import webdriver
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
    "https://www.lacasadelaslamparas.com.ar/productos"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}
# Configurar Selenium con Firefox
options = webdriver.FirefoxOptions()
options.headless = True  # Para ejecutar en segundo plano sin abrir el navegador
driver = webdriver.Firefox(options=options)

# Crear una tabla para almacenar los datos
tabla_nombre = 'lacasadelaslamparas'
c.execute(f'''CREATE TABLE IF NOT EXISTS {tabla_nombre}
                (Fecha TEXT, Descripcion TEXT, Precio TEXT)''')

for url in urls:
    driver.get(url)
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll hacia abajo hasta el final de la página
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Esperar a que carguen los productos
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Obtener el HTML de la página completa
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Encuentra todos los divs de los productos
    product_divs = soup.find_all("div", class_="item-description py-4 px-1")

    for product_div in product_divs:
        # Obtiene la fecha actual
        fecha_actual = datetime.now().strftime("%d/%m/%Y")

        # Obtiene el nombre del producto
        product_name_div = product_div.find("a").find("div", class_="js-item-name item-name mb-3")
        product_name = product_name_div.text.strip() if product_name_div else "No disponible"

        # Obtiene el precio del producto
        price_container = product_div.find("a").find("div", class_="item-price-container mb-1").find("span", class_="js-price-display item-price")
        product_price = price_container.text.strip() if price_container else "No disponible"

        # Insertar los datos en la tabla
        c.execute(f"INSERT INTO {tabla_nombre} (Fecha, Descripcion, Precio) VALUES (?, ?, ?)", (fecha_actual, product_name, product_price))
        conn.commit()

# Cerrar el navegador y la conexión con la base de datos
driver.quit()
conn.close()
