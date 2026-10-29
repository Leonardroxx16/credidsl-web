# CrediDSL Web — rediseño de interfaz

Prototipo académico para experimentar con el lenguaje CrediDSL usando valores sintéticos. Esta versión reorganiza la pantalla como un pequeño laboratorio: editor de reglas, datos de entrada, salida del analizador y referencia de sintaxis.

## Probar localmente en Windows

1. Instala Python 3.11 o 3.12 desde https://www.python.org/downloads/ y marca **Add Python to PATH**.
2. Abre PowerShell dentro de la carpeta `CrediDSL_Web`.
3. Ejecuta:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

4. Abre http://127.0.0.1:5000

## Publicar en Render

1. Sube el contenido de esta carpeta a GitHub.
2. En Render: **New + → Web Service**, conecta el repositorio.
3. Configura Runtime `Python 3`, Build Command `pip install -r requirements.txt` y Start Command `gunicorn app:app`.

## Endpoints

- `/` — interfaz web.
- `/evaluate` — compila y evalúa la regla enviada.
- `/api/health` — estado del servicio.
- `/api/demo` — resumen de 100 casos sintéticos.

## Alcance y seguridad

- No ingresar datos personales, credenciales ni información financiera real.
- No tiene autenticación ni persistencia de datos.
- El prototipo devuelve `REVISION_MANUAL` cuando la condición de la regla no se cumple.
- Esta demostración no es una herramienta para aprobar o rechazar solicitudes crediticias reales.
