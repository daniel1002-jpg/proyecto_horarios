# Proyecto Automatización de Horarios

Sistema de gestión de horarios académicos con generación de HTML.

## Características

- ✅ Lectura y validación de datos JSON
- ✅ Organización automática por días de la semana
- ✅ Generación de HTML responsive con diseño profesional
- ✅ Tabla de horarios con colores por modalidad
- ✅ Íconos Font Awesome para cada modalidad
- ✅ Exportación como imagen PNG de alta calidad
- ✅ Resumen estadístico de materias
- ✅ 21 tests unitarios completos

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

# Visualizar resultado
# Abrir output/horario.html en el navegador
# O usar servidor local: python3 -m http.server 8000 en carpeta output/
```

## Modalidades soportadas

- 🟢 **Virtual**: Clases en línea
- 🔴 **Presencial**: Clases en aula física  
- 🟡 **Mixta**: Combinación de ambas modalidades

## Exportación de imágenes

El sistema incluye funcionalidad para exportar el horario como imagen PNG:

1. Abre el archivo HTML generado
2. Haz clic en "Exportar como imagen"
3. La imagen se descarga automáticamente

## Estructura del proyecto

```
proyecto_horarios/
├── data/
│   └── horarios.json       # Datos de entrada
├── output/
│   ├── template.html       # Plantilla HTML
│   ├── styles.css          # Estilos CSS
|   ├── export.js           # Funcionalidad de exportación
│   └── horario.html        # HTML generado
├── tests/
│   └── test_horarios.py    # Tests unitarios
├── horarios.py             # Módulo principal
├── main.py                 # Script ejecutable
└── requirements.txt        # Dependencias
```

## Formato de datos JSON

```json
[
  {
    "nombre": "Nombre de la materia",
    "horario": {
      "inicio": "HH:MM",
      "fin": "HH:MM"
    },
    "dias": ["Lunes", "Martes"],
    "modalidad": "virtual|presencial|mixta"
  }
]
```

## Tecnologías utilizadas

- **Python 3**: Lógica principal
- **Jinja2**: Generación de templates
- **HTML5/CSS3**: Interfaz responsive
- **Font Awesome**: Iconografía
- **html2canvas**: Exportación de imágenes
- **unittest**: Testing framework