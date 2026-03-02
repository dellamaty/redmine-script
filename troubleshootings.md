## 🔧 Solución de problemas

### Instalación manual del entorno virtual (sólo si el automático falla)

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

