#!/bin/bash

# ==========================================
# Main Redmine Script - Orchestrator
# ==========================================
# This script coordinates the hour loading and email sending process.
# It calls two separate scripts to avoid duplicate hour entries:
#   1. cargar_horas_script.sh - Loads hours to Redmine
#   2. enviar_mail_script.sh - Sends email report and advances to next month
# ==========================================

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
SCRIPTS_DIR="$ROOT_DIR/Archivos/Scripts"

echo "======================================"
echo "   Redmine Hours & Email Manager"
echo "======================================"
echo ""
echo "What would you like to do?"
echo ""
echo "  1) Load hours to Redmine"
echo "  2) Send email report"
echo "  3) Both (load hours + send email)"
echo "  0) Exit"
echo ""
echo -n "Select an option [0-3]: "
read -r opcion

echo ""

#------------------------------------
# Process selected option
#------------------------------------
case $opcion in
    1)
        echo "======================================"
        echo "📊 Loading hours to Redmine"
        echo "======================================"
        echo ""
        
        "$SCRIPTS_DIR/cargar_horas_script.sh"
        LOAD_RESULT=$?
        
        if [ $LOAD_RESULT -ne 0 ]; then
            echo ""
            echo "❌ Error loading hours."
            exit 1
        fi
        
        echo ""
        echo "======================================"
        echo "   Process completed successfully"
        echo "======================================"
        ;;
        
    2)
        echo "======================================"
        echo "📧 Sending email report"
        echo "======================================"
        echo ""
        
        "$SCRIPTS_DIR/enviar_mail_script.sh"
        MAIL_RESULT=$?
        
        if [ $MAIL_RESULT -ne 0 ]; then
            echo ""
            echo "❌ Error sending email."
            exit 1
        fi
        
        echo ""
        echo "======================================"
        echo "   Process completed successfully"
        echo "======================================"
        ;;
        
    3)
        echo "======================================"
        echo "📊 STEP 1: Loading hours to Redmine"
        echo "======================================"
        echo ""
        
        "$SCRIPTS_DIR/cargar_horas_script.sh"
        LOAD_RESULT=$?
        
        if [ $LOAD_RESULT -ne 0 ]; then
            echo ""
            echo "❌ Error loading hours. Process stopped."
            exit 1
        fi
        
        echo ""
        echo "======================================"
        echo "📧 STEP 2: Sending email report"
        echo "======================================"
        echo ""
        
        "$SCRIPTS_DIR/enviar_mail_script.sh"
        MAIL_RESULT=$?
        
        if [ $MAIL_RESULT -ne 0 ]; then
            echo ""
            echo "⚠ There were errors sending the email, but hours were already loaded."
            exit 1
        fi
        
        echo ""
        echo "======================================"
        echo "   Process completed successfully"
        echo "======================================"
        ;;
        
    0)
        echo "👋 Exiting..."
        exit 0
        ;;
        
    *)
        echo "❌ Invalid option. Please select a number between 0 and 3."
        exit 1
        ;;
esac
