import paramiko
import os
import zipfile
import datetime
from email.message import EmailMessage
import smtplib
import shutil

# Datos para la conexión SSH
hostname = '192.168.100.38'
username = 'sqo21'
password = 'Sebas1234'
port = 22
transport = paramiko.Transport((hostname, port))
transport.connect(username=username, password=password)
sftp = transport.open_sftp_client()

# Directorio y tiempo de los archivos
local_dir = '/home/sqo21/ArchCopia' # Repositorio Equipo A
remote_dir = '/home/sqo21/PruebaArch' # Repositorio Equipo B
max_time_delta = datetime.timedelta(hours=24)  # Se buscan archivos creados en las últimas 24 horas


# Se buscan los archivos en base a los requerimientos
selected_files = []
for file_name in sftp.listdir(remote_dir):
    file_path = os.path.join(remote_dir, file_name)
    attrs = sftp.stat(file_path)
    file_created_time = datetime.datetime.fromtimestamp(attrs.st_mtime)
    time_delta = datetime.datetime.now() - file_created_time
    if time_delta <= max_time_delta:
        selected_files.append(file_path)
        print("Se encontro el archivo: " + file_name)

# NOTA: La funciona de comprimir archivos no funciona ya que indica que no existen archivos, pero
# al buscar estos archivos si los reconoce

# Comprimimos los archivos seleccionados en un archivo ZIP
# backup_name = 'respaldo_{}.zip'.format(datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
# backup_path = os.path.join(local_dir, backup_name)
# with zipfile.ZipFile(backup_path, 'w') as backup_file:
#     for file_path in selected_files:
#         filename = os.path.basename(file_path)
#         backup_file.write(file_path, arcname=file_name)

# Trasladamos el archivo de respaldo al equipo local
# shutil.copy2(backup_path, local_dir)

# Se cierra la conexión SSH
sftp.close()
transport.close()


# Se envia correo 
remitente = "sqo21dev@gmail.com"
destinatario = "sebastianquesadaocampo@gmail.com"
mensaje = "Se ha generado una Copia de seguridad de los archivos en la carpeta " + remote_dir
email = EmailMessage()
email["From"] = remitente
email["To"] = destinatario
email["Subject"] = "¡ALERTA DE MOVIMIENTO!"
email.set_content(mensaje)
smtp = smtplib.SMTP_SSL("smtp.gmail.com")
#Es necesario crear una Contraseña especial debido a que Google ya no soporta enviar correos electrónicos vía el protocolo SMTP indicando la contraseña de nuestra cuenta
smtp.login(remitente, "ydzzcldskptwxacl")
smtp.sendmail(remitente, destinatario, email.as_string())
smtp.quit()
print('Correo Enviado')


print('Archivos Guardados')