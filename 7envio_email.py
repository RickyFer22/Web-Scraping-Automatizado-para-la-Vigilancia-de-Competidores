import os
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Obtener la ruta de la carpeta actual
current_folder = os.path.dirname(os.path.abspath(__file__))

# Configuración de la conexión SMTP
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("tu_correo@gmail.com", "tu_contraseña")

# Creación del mensaje
msg = MIMEMultipart()
msg['From'] = "tu_correo@gmail.com"
msg['To'] = "destinatario1@correo.com, destinatario2@correo.com"
msg['Subject'] = "Lista de Precios de la competencia"

# Obtención de la fecha y hora actuales
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

# Creación del cuerpo del mensaje
body = f"Se ha ejecutado y actualizado con éxito la base de datos de los Precios de las Competencias. Fecha y hora de actualización: {dt_string}"
msg.attach(MIMEText(body, 'plain'))

# Adjuntar el archivo
filename = "precios_competencia.xlsx"
file_path = os.path.join(current_folder, filename)  # Construir la ruta completa al archivo
with open(file_path, "rb") as attachment:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(part)

# Envío del correo electrónico
server.sendmail("tu_correo@gmail.com", ["destinatario@correo.com"], msg.as_string())

# Cierre de la conexión SMTP
server.quit()


