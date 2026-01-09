# Sistema de Imputación de Horas Redmine

Sistema automatizado para cargar horas en Redmine y enviar reportes por email.

## 🚀 Instalación Rápida

**¡Solo necesitas ejecutar el instalador automático!**

```bash
chmod +x Archivos/Scripts/install.sh
./Archivos/Scripts/install.sh
```

El instalador automático:
- ✅ Crea el entorno virtual de Python
- ✅ Instala todas las dependencias necesarias
- ✅ Configura los permisos de ejecución
- ✅ Crea el archivo de configuración de ejemplo
- ✅ Te guía con los próximos pasos

### Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con tus datos
```

**⚠️ Importante para Gmail:**
Si usas Gmail, necesitas configurar una contraseña de aplicación:

1. **Activar verificación en 2 pasos** en tu cuenta de Google
2. **Generar contraseña de aplicación**: [Configurar contraseña de aplicación en Gmail](https://support.google.com/mail/answer/185833?hl=es-419)
3. **Configurar en bash** (opcional, para mayor seguridad):
```bash
vim ~/.bashrc
# Agregar al final del archivo:
export SMTP_PASS="tu_contraseña_de_aplicacion"
# Guardar y recargar:
source ~/.bashrc
```

**Nota**: Si configuras SMTP_PASS en bash, déjalo vacío en .env para mayor seguridad.

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

### Instalación manual (solo si el automático falla)

Si por alguna razón el instalador automático no funciona, puedes hacer estos pasos manualmente:

1. **Crear entorno virtual:**
```bash
python3 -m venv Archivos/venv
source Archivos/venv/bin/activate  # Linux/Mac
```

2. **Instalar dependencias:**
```bash
pip install --break-system-packages pandas python-redmine odfpy
```

3. **Configurar archivo .env:**
```bash
# Copiar ejemplo
cp .env.example .env

# Editar con tus datos
nano .env
```

4. **Dar permisos de ejecución:**
```bash
chmod +x redmine.sh
chmod +x Archivos/Scripts/*.sh
```

## ⚙️ Configuración

### Configuración específica para Gmail

Si usas Gmail como servidor SMTP, necesitas configurar una **contraseña de aplicación**:

1. **Activar verificación en 2 pasos** en tu cuenta de Google
2. **Generar contraseña de aplicación**: 
   - Ve a [Configurar contraseña de aplicación en Gmail](https://support.google.com/mail/answer/185833?hl=es-419)
   - Selecciona "Otra aplicación" y genera la contraseña
3. **Usar la contraseña de aplicación** en lugar de tu contraseña normal

**Configuración opcional para mayor seguridad:**
```bash
# Editar archivo bash
vim ~/.bashrc

# Agregar al final del archivo:
export SMTP_PASS="tu_contraseña_de_aplicacion"

# Guardar y recargar configuración
source ~/.bashrc
```

Si configuras SMTP_PASS en bash, déjalo vacío en .env:
```bash
SMTP_PASS=
```

### Variables de entorno (.env)

```bash
#---------------------------
# Carga de Horas en Redmine
#---------------------------
REDMINE_URL=https://redmine.empresa.com
API_KEY=tu_api_key_aqui
# API Key: Obtener desde Redmine → Mi cuenta → Token de API (o API access key)
# Es un token de autenticación que permite al script acceder a tu cuenta de Redmine


#---------------------------
# Envío del correo
#---------------------------
# Correo remitente
DE=tu_email@empresa.com
DE_NAME="Tu Nombre"

# Destinatarios (formato: "Nombre <email>")
PARA="Destinatario1 <destinatario1@empresa.com>"
CC="Destinatario2 <destinatario2@empresa.com>"

# Servidor SMTP
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_PASS=tu_password_smtp
```

### Ejemplos de destinatarios múltiples

```bash
# Múltiples destinatarios
PARA="Juan <juan@empresa.com>, Ana <ana@empresa.com>, pedor@empresa.com"
CC="Director <director@empresa.com>, Manager <manager@empresa.com>"
```

## 📁 Estructura de carpetas

```
Redmine/
├── redmine.sh                    # Script principal (menú interactivo)
├── .env                          # Configuración (crear desde .env.example)
├── .env.example                  # Ejemplo de configuración
├── .gitignore                    # Archivos ignorados por Git
├── firma_digital.png             # Firma digital (opcional)
├── Archivos/
│   ├── Python/
│   │   ├── cargar_horas.py      # Script de carga a Redmine
│   │   └── enviar_mail.py       # Script de envío de emails
│   ├── Scripts/
│   │   ├── cargar_horas_script.sh    # Script para cargar horas
│   │   ├── enviar_mail_script.sh    # Script para enviar email
│   │   └── install.sh                # Instalador automático
│   ├── venv/                    # Entorno virtual de Python
│   └── ultimo_mes.txt           # Control de mes actual (se actualiza automáticamente)
├── Imputación de Horas/
│   └── 2025/
│       ├── 08_redmine.ods        # Archivo de horas (formato ODS)
│       └── CSV Files for Script/
│           └── 08_redmine.csv   # CSV generado automáticamente
└── Mails/
    └── 2025/
        └── 01_mail_redmine.md   # Copia del email enviado (Markdown, generado automáticamente)
```

## 🚀 Uso

### Ejecución principal (menú interactivo)

```bash
./redmine.sh
```

El script te mostrará un menú con las siguientes opciones:

1. **Load hours to Redmine** - Solo carga las horas en Redmine
2. **Send email report** - Solo envía el email (asume que ya cargaste las horas)
3. **Both** - Carga horas y luego envía el email
0. **Exit** - Sale del script

### Ejecución manual de componentes

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

## 📊 Formato del archivo ODS

El archivo debe tener las siguientes columnas:
- **Fecha**: Día del mes (1-31) - se convierte automáticamente a fecha completa
- **Ticket_ID**: Número del ticket en Redmine
- **Proyecto**: Nombre del proyecto
- **Horas**: Número de horas trabajadas
- **Comentario**: Descripción de las horas trabajadas
- **Subir?**: Columna de control (SI/NO) para indicar qué filas cargar en redmine. No aplicable para el envío del mail, se enviarán **TODAS** las filas que estén cargadas.

## 🔧 Solución de problemas

### Error de codificación
Si aparece error de codificación con caracteres especiales:
- **NO usar tildes/acentos** en nombres en .env (ej: "Matias" en lugar de "Matías")
- Verificar que el archivo .env esté en UTF-8

### Error de conexión SMTP
- Verificar credenciales en .env
- **Para Gmail**: Usar contraseña de aplicación (no la contraseña normal)
  - [Configurar contraseña de aplicación en Gmail](https://support.google.com/mail/answer/185833?hl=es-419)
  - Requiere verificación en 2 pasos activada
- Verificar que SMTP esté habilitado

### Error de API Redmine
- Verificar API_KEY en .env
- Verificar REDMINE_URL
- Verificar permisos del usuario en Redmine

### Error: "python: command not found"
- Asegúrate de que el entorno virtual esté activado
- Los scripts activan automáticamente el entorno virtual, pero si ejecutas Python directamente, usa:
  ```bash
  source Archivos/venv/bin/activate
  ```

## 📝 Notas importantes

- **Configuración inicial de `ultimo_mes.txt`**: Este archivo se actualiza automáticamente después de enviar cada email, pero **debes configurarlo manualmente la primera vez** para que apunte al mes correcto. El formato es `YYYY-MM` (ej: `2026-01` para enero de 2026). Si clonas el repositorio, ajusta este archivo según el mes actual antes de usar el sistema.
- El script procesa automáticamente el mes siguiente después de enviar el email
- **Separación de funciones**: 
  - `cargar_horas_script.sh` solo carga horas (NO envía email, NO avanza mes)
  - `enviar_mail_script.sh` solo envía email y avanza al siguiente mes (NO carga horas)
- **Prevención de duplicados**: El script `enviar_mail_script.sh` crea el CSV sin cargar horas a Redmine
- **Carpeta Mails/**: Cada vez que se envía un email, se guarda automáticamente una copia en formato Markdown en `Mails/YYYY/MM_mail_redmine.md`. Esto permite tener un historial de todos los reportes enviados.
- La firma digital se incluye automáticamente si existe `firma_digital.png`
- El sistema es portable y funciona en cualquier PC con la configuración correcta
- **NO usar tildes/acentos** en nombres en .env para evitar errores de codificación
- El archivo `.env` está en `.gitignore` para proteger tus credenciales

## 🔒 Seguridad

- El archivo `.env` contiene información sensible y está excluido de Git (ver `.gitignore`)
- Usa `.env.example` como plantilla para configurar tu `.env`
- Para mayor seguridad, puedes configurar `SMTP_PASS` como variable de entorno del sistema en lugar de en `.env`
