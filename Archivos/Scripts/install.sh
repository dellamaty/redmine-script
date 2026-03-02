#!/bin/bash

echo "🚀 Redmine Hours System Installer"
echo "=================================================="

# Get project root (two levels up from this script)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$ROOT_DIR"

# Verify Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install it first."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv Archivos/venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source Archivos/venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install --break-system-packages pandas python-redmine odfpy

# Set execution permissions
echo "🔐 Setting execution permissions..."
chmod +x redmine.sh
chmod +x Archivos/Scripts/*.sh

# Initialize ultimo_mes.txt with interactive confirmation
echo ""
echo "📅 Initial month setup (Archivos/ultimo_mes.txt)"
CURRENT_PERIOD="$(date +%Y-%m)"
START_PERIOD="$CURRENT_PERIOD"
echo "Detected current period: $CURRENT_PERIOD"

read -r -p "Is this the correct starting period? [Y/n]: " PERIOD_CONFIRMATION
if [[ "$PERIOD_CONFIRMATION" =~ ^([Nn]|[Nn][Oo])$ ]]; then
    while true; do
        read -r -p "Enter the starting period (YYYY-MM): " USER_PERIOD
        if [[ "$USER_PERIOD" =~ ^[0-9]{4}-(0[1-9]|1[0-2])$ ]]; then
            START_PERIOD="$USER_PERIOD"
            break
        fi
        echo "❌ Invalid format. Please use YYYY-MM (example: 2026-03)."
    done
fi

echo "$START_PERIOD" > Archivos/ultimo_mes.txt
echo "✅ Archivos/ultimo_mes.txt initialized with: $START_PERIOD"

# Create .env.example if it doesn't exist
echo "📝 Creating .env.example file..."
if [ ! -f ".env.example" ]; then
    cat > .env.example << 'EOF'
#---------------------------
# Carga de Horas en Redmine
#---------------------------

REDMINE_URL=https://redmine.empresa.com
API_KEY=tu_api_key_aqui


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
# Para Gmail: usar contraseña de aplicación, no la contraseña normal
# Ver: https://support.google.com/mail/answer/185833?hl=es-419
EOF
fi

echo ""
echo "✅ Installation completed!"
echo ""
echo "📋 Next steps:"
echo "1. Copy .env.example to .env:"
echo "   cp .env.example .env"
echo ""
echo "2. Edit .env with your data:"
echo "   - Your email and name"
echo "   - Recipients"
echo "   - Redmine API key"
echo "   - SMTP password"
echo ""
echo "🚀 To run: ./redmine.sh"
echo ""
echo "📁 Required folder structure:"
echo "   - Imputación de Horas/YYYY/MM_redmine.ods"
echo "   - firma_digital.png (optional)"
