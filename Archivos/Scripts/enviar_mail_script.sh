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
# Check if the ODS file exists
#------------------------------------
if [ ! -f "$ARCHIVO_ODS" ]; then
    echo "❌ File does not exist: $ARCHIVO_ODS"
    exit 1
fi


#------------------------------------
# Ask if user wants to send the mail
#------------------------------------
echo "📧 This will send the report email for ${ANIO}-${MES}"
echo ""
echo "⚠️  IMPORTANT: Make sure you have already loaded the hours to Redmine!"
echo "   If you haven't loaded the hours yet, run: ./cargar_horas_script.sh"
echo ""
echo "Do you want to continue and send the email? (s/n)"
read -r respuesta

if [[ ! "$respuesta" =~ ^[Ss]$ ]]; then
    echo "⏭ Email sending cancelled."
    exit 0
fi


#------------------------------------
# Create temporary CSV for the email
#------------------------------------
echo "▶ Creating temporary CSV for the email..."

source "$VENV_DIR/bin/activate"
python3 "$PYTHON_DIR/cargar_horas.py" "$ARCHIVO_ODS" --create-csv
CSV_RESULT=$?

if [ $CSV_RESULT -ne 0 ]; then
    echo "❌ Error creating CSV for the email"
    exit 1
fi


#------------------------------------
# Execute email sending
#------------------------------------
CSV_DIR="$BASE_DIR/$ANIO/CSV Files for Script"
ARCHIVO_CSV="$CSV_DIR/${MES}_redmine.csv"

if [ ! -f "$ARCHIVO_CSV" ]; then
    echo "❌ Generated CSV not found at $ARCHIVO_CSV"
    exit 1
fi

echo "▶ Sending email with $ARCHIVO_CSV"
python3 "$PYTHON_DIR/enviar_mail.py" "$ARCHIVO_CSV"
MAIL_RESULT=$?

if [ $MAIL_RESULT -ne 0 ]; then
    echo "⚠ There were errors sending the email."
    exit 1
fi

echo "✅ Email sent successfully."


#------------------------------------
# Clean up temporary CSV and folder
#------------------------------------
echo "▶ Cleaning up temporary files..."
rm -f "$ARCHIVO_CSV"
rmdir "$CSV_DIR" 2>/dev/null || true  # Remove folder if empty
echo "✔ Temporary files removed"


#------------------------------------
# Calculate next month and update state
#------------------------------------
MES_SIG=$((10#$MES + 1))
ANIO_SIG=$ANIO

if [ $MES_SIG -gt 12 ]; then
    MES_SIG=1
    ANIO_SIG=$((ANIO + 1))
fi

# Save new value with two digits
printf "%04d-%02d\n" $ANIO_SIG $MES_SIG > "$STATE_FILE"

echo "✔ Process completed. Next execution will use ${ANIO_SIG}-$(printf '%02d' $MES_SIG)_redmine.ods"

