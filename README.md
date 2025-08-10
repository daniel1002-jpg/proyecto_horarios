# Proyecto Automatización de Horarios

Sistema de gestión de horarios académicos con generación de HTML.

## Intalación

```bash
# Crear entorno virtual
python3 -m venv env

# Activar entorno virtual
source venv/bin/activate

# Intalar dependencias
pip install -r requirements.txt
```
## Uso

```bash
# Ejecutar tests
pyhton3 -m unittest

# Generar horario HTML
python3 main.py
```

## Estructura del proyecto

```
proyecto_horarios/
├── data/
│   └── horarios.json       # Datos de entrada
├── output/
│   ├── template.html       # Plantilla HTML
│   └── horario.html        # HTML generado
├── tests/
│   └── test_horarios.py    # Tests unitarios
├── horarios.py             # Módulo principal
├── main.py                 # Script ejecutable
└── requirements.txt        # Dependencias
```