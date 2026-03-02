## 🔧 Detalles Técnicos

## 📋 ¿Qué hace el instalador automático?

El script `Archivos/Scripts/install.sh` automatiza todos estos pasos:

### Requisitos previos
- Python 3.8 o superior
- Acceso a Redmine con API key
- Cuenta de email con SMTP habilitado

### Pasos que automatiza el instalador:

1. **Verifica Python instalado**
2. **Crea entorno virtual:**
```bash
python3 -m venv Archivos/venv
source Archivos/venv/bin/activate
```

3. **Instala dependencias:**
```bash
pip install --break-system-packages pandas python-redmine odfpy
```

4. **Configura permisos:**
```bash
chmod +x redmine.sh
chmod +x Archivos/Scripts/*.sh
```

5. **Crea archivo de configuración de ejemplo** (.env.example)
6. **Te guía con los próximos pasos**

## 📊 Formato del archivo ODS

El archivo debe tener las siguientes columnas:
- **Fecha**: Día del mes (1-31) - se convierte automáticamente a fecha completa
- **Ticket_ID**: Número del ticket en Redmine
- **Proyecto**: Nombre del proyecto
- **Horas**: Número de horas trabajadas
- **Comentario**: Descripción de las horas trabajadas
- **Subir?**: Columna de control (SI/NO) para indicar qué filas cargar en redmine. No aplicable para el envío del mail, se enviarán **TODAS** las filas que estén cargadas.

## 🔒 Seguridad

- El archivo `.env` contiene información sensible y está excluido de Git (ver `.gitignore`)
- Usa `.env.example` como plantilla para configurar tu `.env`
- Para mayor seguridad, puedes configurar `SMTP_PASS` como variable de entorno del sistema en lugar de en `.env`

## Ejecución manual de componentes
Si no deseas usar directamente el archivo "redmine.sh", a continuación están los comandos a ejecutar por separado cada acción

```bash
# Solo cargar horas
./Archivos/Scripts/cargar_horas_script.sh

# Solo enviar mail
./Archivos/Scripts/enviar_mail_script.sh

# Ejecutar scripts Python directamente
source Archivos/venv/bin/activate
python3 Archivos/Python/cargar_horas.py "Imputación de Horas/2025/08_redmine.ods"
python3 Archivos/Python/enviar_mail.py "Imputación de Horas/2025/CSV Files for Script/08_redmine.csv"
```

