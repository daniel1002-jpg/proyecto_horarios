import json
import os
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

def read_horarios(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def validate_format(data):
    if not isinstance(data, list):
        raise ValueError("data should be a list of subjects")

    required_keys = ["nombre", "horario", "dias", "modalidad"]
    horario_keys = ["inicio", "fin"]

    for materia in data:
        for key in required_keys:
            if key not in materia:
                raise KeyError(f"Missing {key} key in subject data")

        if not isinstance(materia["horario"], dict):
            raise ValueError("horario should be a object")

        for key in horario_keys:
            if key not in materia["horario"]:
                raise KeyError(f"Missing {key} key in horario data")

def organize_horarios(horarios_data):
    days_of_week = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    organized = {day: [] for day in days_of_week}

    for materia in horarios_data:
        for day in materia["dias"]:
            organized[day].append(materia)

    for day in organized:
        organized[day].sort(key=lambda x: x["horario"]["inicio"])

    return organized

def generate_html(data, path_file):
    os.makedirs(os.path.dirname(path_file), exist_ok=True)

    env = Environment(loader=FileSystemLoader('output'))
    template = env.get_template('template.html')

    total_subjects = sum(len(subjects) for subjects in data.values())
    modalitys = {"virtual": 0, "presencial": 0, "mixta": 0}
    unic_subjects = set()

    for subjects in data.values():
        for subject in subjects:
            if subject["nombre"] not in unic_subjects:
                unic_subjects.add(subject["nombre"])
                modality = subject["modalidad"]
                if modality in modalitys:
                    modalitys[modality] += 1

    template_data = {
        "cuatrimestre": "2° 2024",
        "horarios_por_dia": data,
        "fecha_generacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_materias": len(unic_subjects),
        "modalidades": modalitys
    }

    content = template.render(template_data)

    with open(path_file, 'w', encoding='utf-8') as file:
        file.write(content)