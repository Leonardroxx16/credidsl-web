# CrediDSL Web (prototipo académico)

Interfaz web mínima para probar el analizador CrediDSL con datos sintéticos o de ejemplo. No usar para decisiones crediticias reales.

## Probar localmente en Windows

1. Instala Python 3.11 o 3.12 desde https://www.python.org/downloads/ y marca **Add Python to PATH**.
2. Abre PowerShell dentro de esta carpeta.
3. Ejecuta:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

4. Abre http://127.0.0.1:5000

Si PowerShell bloquea la activación, puedes ejecutar sin activar el entorno:

```powershell
py -m pip install -r requirements.txt
py app.py
```

## Publicar en Render

1. Sube esta carpeta a un repositorio GitHub.
2. En Render: **New + → Web Service**, conecta el repositorio.
3. Configura:
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Plan: Free para pruebas, si está disponible en tu cuenta.
4. Pulsa **Create Web Service** y revisa los logs del despliegue.

Endpoints de comprobación:
- `/` interfaz web
- `/api/health` estado del servicio
- `/api/demo` resumen de 100 casos sintéticos

## Seguridad y limitaciones

- No introduzcas datos personales, financieros reales ni credenciales.
- Este es un prototipo académico sin autenticación ni persistencia.
- El servicio gratuito puede suspenderse por inactividad y no debe usarse como producción.
