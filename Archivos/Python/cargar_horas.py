import pandas as pd
from redminelib import Redmine
import sys
import os

#--------------------------------------------
# Variables de Entorno
#--------------------------------------------
REDMINE_URL = os.environ.get("REDMINE_URL")
API_KEY = os.environ.get("API_KEY")
CSV_DIR_NAME = os.environ.get("CSV_DIR_NAME", "CSV Files for Script")  # nombre de carpeta por defecto

#--------------------------------------------
# Leer Parámetros
#--------------------------------------------
if len(sys.argv) < 2:
    print("Uso: python cargar_horas.py archivo.ods")
    sys.exit(1)

archivo_ods = sys.argv[1]
if not os.path.isfile(archivo_ods):
    print(f"❌ No existe el archivo: {archivo_ods}")
    sys.exit(1)

# Nombre temporal del CSV (temporal en /tmp)
nombre_csv = os.path.splitext(os.path.basename(archivo_ods))[0] + ".csv"
archivo_csv_tmp = os.path.join("/tmp", nombre_csv)

#--------------------------------------------
# Convertir ODS → CSV
#--------------------------------------------
try:
    # Leer solo las primeras filas para evitar problemas con secciones adicionales
    df_ods = pd.read_excel(archivo_ods, engine="odf")
    
    # Filtrar solo las filas que tienen datos válidos en las columnas principales
    # Esto evita problemas con secciones como "Estadísticas del Mes"
    columnas_principales = ["Fecha", "Proyecto", "Ticket_ID", "Horas", "Comentario", "Cargada?"]
    df_ods = df_ods.dropna(subset=["Fecha"])  # Eliminar filas sin fecha
    
    df_ods.to_csv(archivo_csv_tmp, index=False)
    print(f"✔ Convertido {archivo_ods} → {archivo_csv_tmp}")
    print(f"ℹ Filas procesadas: {len(df_ods)} (secciones adicionales ignoradas)")
except Exception as e:
    print(f"❌ Error convirtiendo ODS a CSV: {e}")
    sys.exit(1)

#--------------------------------------------
# Leer CSV
#--------------------------------------------
try:
    df = pd.read_csv(archivo_csv_tmp)
except Exception as e:
    print(f"❌ Error leyendo CSV {archivo_csv_tmp}: {e}")
    sys.exit(1)

#--------------------------------------------
# Procesar fechas: convertir solo día a fecha completa
#--------------------------------------------
# Leer año y mes del archivo ultimo_mes.txt
# El archivo está en Archivos/ultimo_mes.txt
proyecto_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(archivo_ods))))
ultimo_mes_file = os.path.join(proyecto_root, "Archivos", "ultimo_mes.txt")
try:
    with open(ultimo_mes_file, 'r') as f:
        ultimo_mes = f.read().strip()
    ANIO_ACTUAL = ultimo_mes[:4]
    MES_ACTUAL = ultimo_mes[5:7]
    print(f"📅 Usando año: {ANIO_ACTUAL}, mes: {MES_ACTUAL}")
except Exception as e:
    print(f"❌ Error leyendo ultimo_mes.txt: {e}")
    sys.exit(1)

# Convertir días a fechas completas
def convertir_fecha(dia):
    if pd.isna(dia) or dia == '':
        return dia
    # Asegurar que el día tenga 2 dígitos
    dia_str = str(int(float(dia))).zfill(2)
    return f"{ANIO_ACTUAL}-{MES_ACTUAL}-{dia_str}"

# Aplicar conversión a la columna Fecha
df['Fecha'] = df['Fecha'].apply(convertir_fecha)
print(f"✔ Fechas convertidas usando año {ANIO_ACTUAL} y mes {MES_ACTUAL}")

# Validación básica - verificar columnas principales
columnas_principales = {"Fecha", "Proyecto", "Ticket_ID", "Horas", "Comentario"}
if not columnas_principales.issubset(df.columns):
    print(f"❌ Error: el CSV debe contener las columnas: {columnas_principales}")
    sys.exit(1)

# Verificar si existe columna de control (puede ser "Cargada?" o "Subir?")
columna_control = None
if "Subir?" in df.columns:
    columna_control = "Subir?"
elif "Cargada?" in df.columns:
    columna_control = "Cargada?"
    print("ℹ Usando columna 'Cargada?' (considera cambiar a 'Subir?' en el futuro)")
else:
    print("❌ Error: debe existir una columna 'Subir?' o 'Cargada?' para controlar qué filas procesar")
    sys.exit(1)

#--------------------------------------------
# Crear CSV solo si se especifica --create-csv
#--------------------------------------------
CREATE_CSV = "--create-csv" in sys.argv

if CREATE_CSV:
    # Usar el año y mes que ya leímos del ultimo_mes.txt
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(archivo_ods)))  # carpeta "Imputación de Horas"
    CSV_DIR = os.path.join(BASE_DIR, ANIO_ACTUAL, CSV_DIR_NAME)
    os.makedirs(CSV_DIR, exist_ok=True)

    archivo_csv = os.path.join(CSV_DIR, nombre_csv)
    df.to_csv(archivo_csv, index=False)  # crear CSV temporal
    print(f"✔ Creado CSV temporal en {archivo_csv}")
    print("ℹ Modo --create-csv: solo se creó el CSV, no se cargaron horas a Redmine")
    sys.exit(0)  # Salir sin cargar horas a Redmine

#--------------------------------------------
# Conectar a Redmine
#--------------------------------------------
redmine = Redmine(REDMINE_URL, key=API_KEY)

#--------------------------------------------
# Filtrar filas a cargar (solo las que tienen "SI" en la columna de control)
#--------------------------------------------
df_a_cargar = df[df[columna_control].str.upper().str.strip().isin(["SI", "SÍ"])]
filas_total = len(df)
filas_a_cargar = len(df_a_cargar)

print(f"📊 Total de filas en el archivo: {filas_total}")
print(f"📊 Filas marcadas para cargar: {filas_a_cargar}")

if filas_a_cargar == 0:
    print(f"⚠ No hay filas marcadas para cargar (todas tienen 'NO' en {columna_control})")
    sys.exit(0)

#--------------------------------------------
# Cargar las Horas
#--------------------------------------------
hubo_errores = False

for _, row in df_a_cargar.iterrows():
    try:
        # Asegurar que la fecha esté en formato correcto para Redmine (YYYY-MM-DD)
        fecha_redmine = str(row["Fecha"])
        print(f"🔄 Cargando: {fecha_redmine} | Ticket {row['Ticket_ID']} | {row['Horas']}h")
        
        redmine.time_entry.create(
            issue_id=int(row["Ticket_ID"]),
            hours=float(row["Horas"]),
            spent_on=fecha_redmine,
            comments=str(row["Comentario"])
        )
        print(f"✔ Cargado exitosamente: {fecha_redmine} | Ticket {row['Ticket_ID']} | {row['Horas']}h")
    except Exception as e:
        print(f"❌ Error con ticket {row['Ticket_ID']} en {row['Fecha']}: {e}")
        hubo_errores = True

#--------------------------------------------
# No modificar el archivo ODS para evitar problemas
#--------------------------------------------
print("ℹ Archivo ODS no modificado (para evitar columnas adicionales)")

#--------------------------------------------
# Salir con código de error si hubo fallos
#--------------------------------------------
if hubo_errores:
    print("⚠ Se detectaron errores al cargar las horas. Finalizando")
    sys.exit(1)
else:
    sys.exit(0)