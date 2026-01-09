#!/bin/bash

# ------------------------------
# Load environment variables
# ------------------------------
# Go to project root (two levels up from this script)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
ENV_FILE="$ROOT_DIR/.env"

if [ -f "$ENV_FILE" ]; then
    set -a  # automatically export all vars
    source "$ENV_FILE"
    set +a
else
    echo "❌ Configuration file not found: $ENV_FILE"
    exit 1
fi

#------------------------------------
# Configure relative paths
#------------------------------------

BASE_DIR="$ROOT_DIR/Imputación de Horas"
PYTHON_DIR="$ROOT_DIR/Archivos/Python"
VENV_DIR="$ROOT_DIR/Archivos/venv"
STATE_FILE="$ROOT_DIR/Archivos/ultimo_mes.txt"


#------------------------------------
# Initialize if it doesn't exist
#------------------------------------
if [ ! -f "$STATE_FILE" ]; then
    echo "2025-01" > "$STATE_FILE"
fi

# Read current year and month
CURRENT=$(cat "$STATE_FILE")
ANIO=$(echo "$CURRENT" | cut -d'-' -f1)
MES=$(echo "$CURRENT" | cut -d'-' -f2)

ARCHIVO_ODS="$BASE_DIR/$ANIO/${MES}_redmine.ods"


#------------------------------------
# Check if the month is in the future
#------------------------------------
HOY_ANIO=$(date +%Y)
HOY_MES=$(date +%m)

if [ $ANIO -gt $HOY_ANIO ] || { [ $ANIO -eq $HOY_ANIO ] && [ $MES -gt $HOY_MES ]; }; then
    echo "⚠ The file $ARCHIVO_ODS corresponds to a future month. Skipping load."
    exit 0
fi


#------------------------------------
# Execute the Python script (load hours to Redmine)
#------------------------------------
if [ ! -f "$ARCHIVO_ODS" ]; then
    echo "❌ File does not exist: $ARCHIVO_ODS"
    exit 1
fi

echo "▶ Loading hours with $ARCHIVO_ODS"

source "$VENV_DIR/bin/activate"
python3 "$PYTHON_DIR/cargar_horas.py" "$ARCHIVO_ODS"
RESULTADO=$?

#------------------------------------
# Check if the hour loading was successful
#------------------------------------
if [ $RESULTADO -ne 0 ]; then
    echo "⚠ There were errors loading hours."
    exit 1
fi

echo "✅ Hours loaded successfully."
echo ""
echo "📧 To send the report email, run: ./enviar_mail_script.sh"
echo "⏭  To advance to the next month, run: ./enviar_mail_script.sh (it will advance automatically after sending)"

