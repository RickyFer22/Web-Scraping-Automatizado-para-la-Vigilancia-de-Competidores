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
    "https://electrolineas.com.ar/categoria-producto/cables-categorias/?v=c838c18b91bc",
    "https://electrolineas.com.ar/categoria-producto/proteccion-electrica-categorias/?v=c838c18b91bc",
    "https://electrolineas.com.ar/categoria-producto/canos-y-accesorios-categorias/?v=c838c18b91bc",
    "https://electrolineas.com.ar/categoria-producto/iluminacion-categorias/?v=c838c18b91bc"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Crear una tabla para almacenar los datos
tabla_nombre = 'electrolineas'
c.execute(f'''CREATE TABLE IF NOT EXISTS {tabla_nombre}
                (Fecha TEXT, Descripcion TEXT, Precio TEXT)''')

for base_url in base_urls:
    response = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Obtener todas las páginas de la categoría
    pagination_nav = soup.select_one("body > div.website-wrapper > div.main-page-wrapper > div > div > div > div > section.wd-negative-gap.elementor-section.elementor-top-section.elementor-element.elementor-element-467f0e8.elementor-section-boxed.elementor-section-height-default.elementor-section-height-default.wd-section-disabled > div > div.elementor-column.elementor-col-50.elementor-top-column.elementor-element.elementor-element-5c2c826 > div > div.elementor-element.elementor-element-26dfe0a.wd-shop-product.elementor-widget.elementor-widget-wd_archive_products > div > div.wd-loop-footer.products-footer > nav")
    if pagination_nav:
        pages = [a['href'] for a in pagination_nav.select('a')]
    else:
        pages = [base_url]

    for page_url in pages:
        response = requests.get(page_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Encuentra todos los divs de los productos
        product_divs = soup.select("body > div.website-wrapper > div.main-page-wrapper > div > div > div > div > section.wd-negative-gap.elementor-section.elementor-top-section.elementor-element.elementor-element-467f0e8.elementor-section-boxed.elementor-section-height-default.elementor-section-height-default.wd-section-disabled > div > div.elementor-column.elementor-col-50.elementor-top-column.elementor-element.elementor-element-5c2c826 > div > div.elementor-element.elementor-element-26dfe0a.wd-shop-product.elementor-widget.elementor-widget-wd_archive_products > div > div.products.elements-grid.wd-products-holder.wd-spacing-20.grid-columns-4.pagination-pagination.title-line-one.wd-stretch-cont-lg.align-items-start.wd-products-with-bg.row > div.product-grid-item.product")

        for product_div in product_divs:
            # Obtiene la fecha actual
            fecha_actual = datetime.now().strftime("%d/%m/%Y")

            # Obtiene el nombre del producto
            product_name_element = product_div.select_one("div.product-element-bottom > h3 > a")
            product_name = product_name_element.text.strip() if product_name_element else "No disponible"

            # Obtiene el precio del producto
            price_element = product_div.select_one("div.product-element-bottom > div.wrap-price > span > span > bdi")
            product_price = price_element.text.strip() if price_element else "No disponible"

            # Insertar los datos en la tabla
            c.execute(f"INSERT INTO {tabla_nombre} (Fecha, Descripcion, Precio) VALUES (?, ?, ?)", (fecha_actual, product_name, product_price))
            conn.commit()

# Cerrar la conexión con la base de datos
conn.close()
