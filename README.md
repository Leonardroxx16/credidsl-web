# CrediDSL Web

Laboratorio académico para validar políticas crediticias y simularlas sobre solicitudes ficticias. Esta versión implementa el diseño de la Parte 2 del informe.

## Abrir en Windows

En el equipo donde se preparó el proyecto, abre iniciar.cmd y visita http://127.0.0.1:5000. Deja abierta la ventana de la aplicación durante la demostración. Para detenerla, pulsa Ctrl+C en esa ventana.

Para preparar el proyecto en otro equipo con Python 3.10 o posterior:

~~~powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
~~~

La aplicación se ejecuta en la dirección local. Java solo se requiere para regenerar los analizadores. Se incluye el código Python generado para ejecutar la aplicación sin el JAR.

## Demostración

1. **Validar política A** muestra diagnósticos por etapa, línea y columna. Las secciones desplegables muestran los tokens y el árbol sintáctico.
2. **Evaluar solicitud con A** aplica la política al caso ingresado. Muestra la decisión y las reglas de mayor prioridad que la explican.
3. **Simular con A** o **Comparar A y B** ejecuta las políticas sobre el mismo lote. Sin archivo se usan 100 solicitudes sintéticas. Con un CSV, utiliza el formato del archivo de ejemplo disponible en la interfaz.
4. **Comparar validadores** contrasta, sobre políticas con errores conocidos, el reconocimiento léxico y sintáctico con la validación completa.

### Ejemplo de política

~~~text
REGLA deuda_alta PRIORIDAD 20
SI ratio_deuda > 0.50 ENTONCES RECHAZAR

REGLA perfil_elegible PRIORIDAD 10
SI puntaje >= 650 Y ingreso_mensual >= 1800 Y ratio_deuda <= 0.35
ENTONCES APROBAR

POR_DEFECTO REVISION_MANUAL
~~~

El formato anterior usaba una regla con AND y OR. Para trasladarla, agrega PRIORIDAD con un entero positivo, usa Y y O, y termina la política con POR_DEFECTO. Los nombres del catálogo son puntaje, ingreso_mensual y ratio_deuda. La nueva gramática distingue mayúsculas y no usa punto y coma.

El CSV debe incluir las columnas id, puntaje, ingreso_mensual y ratio_deuda, codificación UTF-8 y punto decimal. El puntaje es un entero de 0 a 1000, el ingreso es un decimal no negativo y la proporción de deuda va de 0 a 1. Se admiten hasta 1000 solicitudes por archivo y 128 KB. Usar exclusivamente datos ficticios.

## Implementación y pruebas

- CrediDSL.g4 especifica las reglas léxicas y sintácticas. ANTLR 4.13.2 genera el lexer y el parser.
- credidsl.py separa el análisis léxico, sintáctico y semántico y construye la política ejecutable.
- simulation.py carga solicitudes, calcula resultados y realiza la comparación.
- app.py conserva Flask para reutilizar el proyecto original. En el informe se había planteado Java y JUnit. La versión implementada conserva ANTLR y usa su destino Python 3 con unittest para integrar el analizador en Flask.

Para regenerar después de cambiar la gramática, descarga el [JAR oficial de ANTLR 4.13.2](https://www.antlr.org/download/antlr-4.13.2-complete.jar), colócalo en .tools y ejecuta:

~~~powershell
java -jar .tools\antlr-4.13.2-complete.jar -Dlanguage=Python3 -no-listener -o generated CrediDSL.g4
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
~~~

Los casos automatizados comprueban precedencia, límites, diagnósticos, conflictos, CSV y las 100 decisiones de cada política contra un cálculo de referencia. La comparación del ejemplo cambia el umbral de puntaje de 650 a 700.

| Política | Aprobar | Rechazar | Revisión manual |
|---|---:|---:|---:|
| A | 19 | 37 | 44 |
| B | 16 | 37 | 47 |

Tres solicitudes cambian de aprobación a revisión manual. En el lote de 10 políticas de prueba hay 8 inválidas. El lexer y el parser detectan 3, la validación completa detecta 8 y ambas configuraciones aceptan las 2 válidas. Las cifras corresponden a los ejemplos reproducibles del proyecto.

## Rutas

- / abre la interfaz.
- POST /evaluate ejecuta la operación del formulario.
- /api/health devuelve el estado del servicio.
- /api/demo resume la simulación de 100 casos.
- /api/validation-study devuelve la comparación de detección.
- /demo.csv descarga las solicitudes ficticias.

En un servidor Linux con las dependencias instaladas se puede iniciar con gunicorn app:app.
