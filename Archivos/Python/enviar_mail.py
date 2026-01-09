import pandas as pd
from redminelib import Redmine
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os
import sys
import locale

# Configurar locale para nombres de meses en español
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')
    except:
        # Fallback si no se puede configurar locale
        pass

# -------------------------
# Variables de Entorno
# -------------------------
DE = os.environ.get("DE")
DE_NAME = os.environ.get("DE_NAME", "Matías Dellafiore")

# Procesar destinatarios con formato "Nombre <email>"
PARA_RAW = os.environ.get("PARA", "").split(",")
CC_RAW = os.environ.get("CC", "").split(",")

# Función para procesar destinatarios
def procesar_destinatarios(destinatarios_raw):
    destinatarios = []
    for dest in destinatarios_raw:
        dest = dest.strip()
        if dest:
            if "<" in dest and ">" in dest:
                # Formato "Nombre <email>" - guardar tal como viene
                destinatarios.append(dest)
            else:
                # Solo email
                destinatarios.append(dest)
    return destinatarios

# Función para extraer solo emails
def extraer_emails(destinatarios):
    emails = []
    for dest in destinatarios:
        if "<" in dest and ">" in dest:
            email = dest.split("<")[1].split(">")[0].strip()
            emails.append(email)
        else:
            emails.append(dest)
    return emails

PARA = procesar_destinatarios(PARA_RAW)
CC = procesar_destinatarios(CC_RAW)
SMTP_SERVER = os.environ.get("SMTP_SERVER")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
SMTP_PASS = os.environ.get("SMTP_PASS")  # se toma del entorno
REDMINE_URL = os.environ.get("REDMINE_URL")
API_KEY = os.environ.get("API_KEY")

# -------------------------
# Leer parámetros
# -------------------------
if len(sys.argv) < 2:
    print("Uso: python enviar_mail.py archivo.csv")
    sys.exit(1)

archivo_csv = sys.argv[1]
if not os.path.isfile(archivo_csv):
    print(f"❌ No existe el archivo: {archivo_csv}")
    sys.exit(1)

# -------------------------
# Leer CSV
# -------------------------
try:
    df = pd.read_csv(archivo_csv)
except Exception as e:
    print(f"❌ Error leyendo CSV {archivo_csv}: {e}")
    sys.exit(1)

# -------------------------
# Año y mes para guardado
# -------------------------
ANIO_MAIL = df['Fecha'].iloc[0][:4]
MES_NUM = df['Fecha'].iloc[0][5:7]

# Obtener nombre del mes
try:
    fecha_obj = datetime.datetime.strptime(f"{ANIO_MAIL}-{MES_NUM}-01", "%Y-%m-%d")
    NOMBRE_MES = fecha_obj.strftime("%B").capitalize()
except:
    # Fallback si no funciona locale
    meses = {
        "01": "Enero", "02": "Febrero", "03": "Marzo", "04": "Abril",
        "05": "Mayo", "06": "Junio", "07": "Julio", "08": "Agosto",
        "09": "Septiembre", "10": "Octubre", "11": "Noviembre", "12": "Diciembre"
    }
    NOMBRE_MES = meses.get(MES_NUM, MES_NUM)

# Definir carpeta base de mails relativa al CSV
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIL_DIR_BASE = os.path.join(ROOT_DIR, "Mails")
MAIL_DIR = os.path.join(MAIL_DIR_BASE, ANIO_MAIL)
os.makedirs(MAIL_DIR, exist_ok=True)

# -------------------------
# Cálculo de Totales
# -------------------------
total_dias = df['Fecha'].nunique()
total_horas = df['Horas'].sum()

# Conectar a Redmine
redmine = Redmine(REDMINE_URL, key=API_KEY)

# Agrupar por proyecto y ticket
resumen_proyectos = ""
for proyecto, df_proj in df.groupby("Proyecto"):
    # Calcular la suma total de porcentajes para este proyecto
    porcentaje_total_proyecto = 0
    for ticket_id, df_ticket in df_proj.groupby("Ticket_ID"):
        horas_ticket = df_ticket["Horas"].sum()
        porcentaje = (horas_ticket / total_horas) * 100
        porcentaje_total_proyecto += porcentaje
    
    resumen_proyectos += f"<h2>{proyecto} [{porcentaje_total_proyecto:.1f}%]</h2>"
    for ticket_id, df_ticket in df_proj.groupby("Ticket_ID"):
        try:
            issue = redmine.issue.get(ticket_id)
            titulo_ticket = issue.subject
        except Exception:
            titulo_ticket = f"Ticket {ticket_id}"
        horas_ticket = df_ticket["Horas"].sum()
        porcentaje = (horas_ticket / total_horas) * 100
        resumen_proyectos += f"<p><a href='{REDMINE_URL}/issues/{ticket_id}'>{titulo_ticket}</a></p>" \
                             f"<p>• Total de horas: <strong>{horas_ticket}h</strong><br>" \
                             f"• Porcentaje: <strong>{porcentaje:.1f}%</strong></p>"

# -------------------------
# Construir cuerpo del mail
# -------------------------
mes = df['Fecha'].iloc[0][:7]
cuerpo = f"""
<p>Buenas, ¿cómo va? Adjunto a continuación mi distribución de horas/proyectos del mes {NOMBRE_MES}.</p>

<h1>Tiempo Dedicado</h1>
<p>Total de días trabajados: <strong>{total_dias} días</strong><br>
Total de horas trabajadas: <strong>{total_horas} horas</strong></p>

<h1>Proyectos</h1>
{resumen_proyectos}
<p>Saludos!</p>

<p><img src="cid:firma_digital" alt="Firma Digital" style="max-width: 300px;"></p>
"""

# -------------------------
# Enviar correo
# -------------------------
try:
    msg = MIMEMultipart('related')
    msg['From'] = f"{DE_NAME} <{DE}>"
    
    # Formatear destinatarios (ya vienen formateados)
    msg['To'] = ", ".join(PARA)
    msg['CC'] = ", ".join(CC)
    msg['Subject'] = f"Imputación Horas/Proyecto - {NOMBRE_MES} {ANIO_MAIL}"
    
    # Crear parte HTML
    html_part = MIMEMultipart('alternative')
    html_part.attach(MIMEText(cuerpo, 'html', 'utf-8'))
    msg.attach(html_part)
    
    # Agregar firma digital como imagen embebida
    firma_path = os.path.join(ROOT_DIR, "firma_digital.png")
    if os.path.exists(firma_path):
        with open(firma_path, 'rb') as f:
            firma_img = MIMEImage(f.read())
            firma_img.add_header('Content-ID', '<firma_digital>')
            firma_img.add_header('Content-Disposition', 'inline', filename='firma_digital.png')
            msg.attach(firma_img)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(DE, SMTP_PASS)
        # Extraer solo los emails para el envío
        para_emails = extraer_emails(PARA)
        cc_emails = extraer_emails(CC)
        server.sendmail(DE, para_emails + cc_emails, msg.as_string())

    # Formatear destinatarios para el print
    print(f"✔ Mail enviado a {', '.join(PARA + CC)}")

    # Guardar copia del mail en formato Markdown
    archivo_mail = os.path.join(MAIL_DIR, f"{MES_NUM}_mail_redmine.md")
    
    # Convertir HTML a Markdown para mejor legibilidad
    cuerpo_md = cuerpo.replace("<h1>", "\n# ").replace("</h1>", "")
    cuerpo_md = cuerpo_md.replace("<h2>", "\n## ").replace("</h2>", "")
    cuerpo_md = cuerpo_md.replace("<p>", "").replace("</p>", "\n")
    cuerpo_md = cuerpo_md.replace("<br>", "  \n")
    cuerpo_md = cuerpo_md.replace("<strong>", "**").replace("</strong>", "**")
    # Convertir links con regex para mejor manejo
    import re
    cuerpo_md = re.sub(r'<a href=\'(.*?)\'>(.*?)</a>', r'[\2](\1)', cuerpo_md)
    # Remover la imagen de la firma del markdown
    cuerpo_md = re.sub(r'<img.*?firma_digital.*?>', '', cuerpo_md)
    # Limpiar líneas vacías múltiples
    cuerpo_md = re.sub(r'\n\s*\n', '\n\n', cuerpo_md).strip()
    
    with open(archivo_mail, "w", encoding="utf-8") as f:
        f.write(f"**Para:** {', '.join(PARA)}\n")
        f.write(f"**CC:** {', '.join(CC)}\n")
        f.write(f"**Asunto:** Imputación Horas/Proyecto - {NOMBRE_MES} {ANIO_MAIL}\n\n")
        f.write(cuerpo_md)

    print(f"✔ Mail guardado en: {archivo_mail}")

    sys.exit(0)

except Exception as e:
    print(f"❌ Error enviando mail: {e}")
    sys.exit(1)

