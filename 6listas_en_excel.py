import sqlite3
from openpyxl import Workbook
import os

# Obtener la ruta del directorio actual del script
current_folder = os.path.dirname(os.path.abspath(__file__))

# Nombre del archivo de la base de datos
db_filename = 'precios_competencia.db'

# Buscar la base de datos en diferentes directorios
search_paths = [current_folder, os.path.expanduser("~"), os.path.join(os.path.expanduser("~"), "my_project")]
for search_path in search_paths:
    db_path = os.path.join(search_path, db_filename)
    if os.path.isfile(db_path):
        break
else:
    print("No se encontró la base de datos en ninguno de los directorios.")
    exit()

print(f"Se encontró la base de datos en: {db_path}")

# Crear la conexión con la base de datos SQLite
try:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
except sqlite3.Error as e:
    print(f"Error al conectarse a la base de datos: {e}")
    exit()

# Obtener nombres de las tablas en la base de datos
c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
tablas = c.fetchall()

# Eliminar el archivo Excel existente (si existe)
excel_file_path = os.path.join(current_folder, "precios_competencia.xlsx")
if os.path.exists(excel_file_path):
    os.remove(excel_file_path)

# Crear un nuevo archivo Excel
wb = Workbook()

for tabla in tablas:
    nombre_tabla = tabla[0]
    ws = wb.create_sheet(title=nombre_tabla)

    # Obtener los nombres de las columnas
    c.execute(f"PRAGMA table_info({nombre_tabla})")
    column_names = [info[1] for info in c.fetchall()]

    # Verificar si la columna "fecha" existe en la tabla
    if 'fecha' not in column_names:
        print(f"No se encontró una columna de fecha en la tabla {nombre_tabla}.")
        continue

    # Convertir la columna de fecha a tipo date (si no está ya en ese formato)
    c.execute(f"UPDATE {nombre_tabla} SET fecha = date(fecha) WHERE typeof(fecha) != 'date'")

    # Obtener la fila con la fecha más reciente
    c.execute(f"""
        SELECT *
        FROM {nombre_tabla}
        WHERE fecha = (SELECT MAX(fecha) FROM {nombre_tabla})
    """)
    row = c.fetchone()

    # Escribir los nombres de las columnas en la primera fila
    for col_index, col_name in enumerate(column_names):
        ws.cell(row=1, column=col_index+1, value=col_name)

    # Escribir los datos de la fila más reciente en la segunda fila
    if row:
        for col_index, value in enumerate(row):
            ws.cell(row=2, column=col_index+1, value=value)
    else:
        print(f"No se encontraron datos recientes en la tabla {nombre_tabla}.")

    # Ajustar el ancho de las columnas
    for col in ws.columns:
        max_length = 0
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = (max_length + 2) * 1.2
        ws.column_dimensions[col[0].column_letter].width = adjusted_width

# Eliminar la hoja inicial por defecto "Sheet" si hay más de una hoja
if len(wb.sheetnames) > 1:
    wb.remove(wb["Sheet"])

# Guardar el archivo Excel en el mismo directorio que la base de datos
wb.save(excel_file_path)

# Cerrar la conexión con la base de datos
conn.close()

