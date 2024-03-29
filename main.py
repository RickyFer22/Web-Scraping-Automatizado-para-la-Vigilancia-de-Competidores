import os
import subprocess

# Lista de scripts a ejecutar
scripts = [
    "1electropunto.py",
    "2casadelaslamparas.py",
    "3iluminar.py",
    "4electrolineas.py",
    "5electromisiones.py",
    "6listas_en_excel.py",
    "7envio_email.py"
]

# Ejecutar cada script
for script in scripts:
    print(f"Ejecutando {script}...")
    try:
        subprocess.run(["python", script], check=True)
        print(f"{script} ejecutado exitosamente.")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar {script}: {e}")
