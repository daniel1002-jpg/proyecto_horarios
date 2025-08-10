# Proyecto Automatización de Horarios

Sistema de gestión de horarios académicos con generación de HTML.

## Instalación

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## Uso

```bash
# Ejecutar tests
python3 -m unittest

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
│   ├── styles.css          # Estilos CSS
│   └── horario.html        # HTML generado
├── tests/
│   └── test_horarios.py    # Tests unitarios
├── horarios.py             # Módulo principal
├── main.py                 # Script ejecutable
└── requirements.txt        # Dependencias
```