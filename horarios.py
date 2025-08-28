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

    modalities = {"virtual": 0, "presencial": 0, "mixta": 0}
    unique_subjects = set()

    for subjects in data.values():
        for subject in subjects:
            if subject["nombre"] not in unique_subjects:
                unique_subjects.add(subject["nombre"])
                modality = subject["modalidad"]
                if modality in modalities:
                    modalities[modality] += 1

    table_data = generate_table_data(data)

    template_data = {
        "cuatrimestre": "2° 2025",
        "horarios_por_dia": data,
        "horarios_tabla": table_data,
        "fecha_generacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_materias": len(unique_subjects),
        "modalidades": modalities
    }

    content = template.render(template_data)

    with open(path_file, 'w', encoding='utf-8') as file:
        file.write(content)

def generate_table_data(organized_data):
    times = set()

    for day_subjects in organized_data.values():
        for subject in day_subjects:
            time_range = f"{subject['horario']['inicio']} - {subject['horario']['fin']}"
            times.add(time_range)

    sorted_times = sorted(list(times), key=lambda x: x.split(" - ")[0])

    table_rows = []
    for time_range in sorted_times:
        row = {"time_range": time_range}
        for day in ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]:
            day_subject = None
            if day in organized_data:
                for subject in organized_data[day]:
                    subject_time = f"{subject['horario']['inicio']} - {subject['horario']['fin']}"
                    if subject_time == time_range:
                        day_subject = subject
                        break
            row[day] = day_subject
        table_rows.append(row)

    return table_rows