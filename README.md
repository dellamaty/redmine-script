# Redmine Time Tracking System

Automated system to upload worked hours to Redmine and send email reports.

## 🚀 Initial Setup

### Dependency installer

Run the automatic installer first:

```bash
chmod +x Archivos/Scripts/install.sh
./Archivos/Scripts/install.sh
```

The installer will:
- ✅ Create the Python virtual environment
- ✅ Install all required dependencies
- ✅ Set execution permissions
- ✅ Create the sample configuration file (`.env.example`)
- ✅ Initialize `Archivos/ultimo_mes.txt` with the current period (manual confirmation)
- ✅ Show the next setup steps

### Environment variables (`.env`)

Create your local configuration file:

```bash
cp .env.example .env
# Edit .env with your values
```

Then update `.env` with your Redmine and SMTP credentials.

#### Mail sender considerations

Email settings are only needed if you use options that send reports (`Send email report` or `Both`).
If you only upload hours, SMTP settings are not used in that run.

## 🚀 Usage

### Main execution

After the initial setup, run:

```bash
./redmine.sh
```

The script shows this menu:

1. **Load hours to Redmine** - Uploads hours only
2. **Send email report** - Sends the report only (assumes data already prepared)
3. **Both** - Uploads hours and then sends the report
0. **Exit** - Exits the script

### Input files and output behavior

- The working-hours source file is an `.ods` spreadsheet in `Imputación de Horas/YYYY/`.
- A CSV file is generated in `CSV Files for Script/` for processing.
- If `Archivos/firma_digital.png` exists, it is included in the email signature.
- After a successful email send, the system advances to the next month automatically.

## 📁 Folder structure

```text
Redmine/
├── redmine.sh                    # Main script (interactive menu)
├── .env                          # Local configuration (create from .env.example)
├── .env.example                  # Configuration template
├── .gitignore                    # Git ignored files
├── Archivos/
│   ├── ultimo_mes.txt            # Current period tracker (auto-updated)
│   ├── firma_digital.png         # Digital signature (optional)
│   ├── Python/
│   │   ├── cargar_horas.py       # Redmine upload script
│   │   └── enviar_mail.py        # Email sending script
│   ├── Scripts/
│   │   ├── cargar_horas_script.sh
│   │   ├── enviar_mail_script.sh
│   │   └── install.sh
│   └── venv/                     # Python virtual environment
├── Imputación de Horas/
│   └── 2025/
│       ├── 01_redmine.ods
│       └── CSV Files for Script/
│           └── 01_redmine.csv
└── Mails/
    └── 2025/
        └── 01_mail_redmine.md    # Saved copy of sent email
```

## ⚙️ Detailed Configuration

### Gmail-specific setup

If you use Gmail as SMTP server, create an **App Password**:

1. Enable **2-Step Verification** in your Google account
2. Generate an App Password: [Set up Gmail App Password](https://support.google.com/mail/answer/185833?hl=es-419)
3. Use that App Password instead of your normal password

Optional (more secure): store `SMTP_PASS` in your shell environment.

```bash
# Edit bash file
vim ~/.bashrc

# Add at the end of the file
export SMTP_PASS="your_application_password"

# Save and reload configuration
source ~/.bashrc
```

If `SMTP_PASS` is defined in bash, leave it empty in `.env`:

```bash
SMTP_PASS=
```

### Multiple recipients example

```bash
PARA="Juan <juan@company.com>, Ana <ana@company.com>, pedro@company.com"
CC="Director <director@company.com>, Manager <manager@company.com>"
```

## 📝 Important Notes

- **`ultimo_mes.txt` initial value**: during installation, the script detects `YYYY-MM` and asks for manual confirmation. You can change it if needed.
- The script automatically processes the next month after sending an email.
- **Function split**:
  - `cargar_horas_script.sh`: uploads hours only (no email, no month advance)
  - `enviar_mail_script.sh`: sends email and advances month (no Redmine upload)
- **Duplicate prevention**: `enviar_mail_script.sh` can generate CSV without uploading hours to Redmine.
- **`Mails/` folder**: every sent email is stored as Markdown in `Mails/YYYY/MM_mail_redmine.md`.
- Avoid accents in `.env` names to prevent encoding issues.
- `.env` is ignored by Git to protect credentials.

## 📚 References

- [Technical details](technical-details.md)
- [Troubleshooting](troubleshootings.md)