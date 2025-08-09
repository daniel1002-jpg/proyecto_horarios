import json

def read_horarios(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def validate_format(data: dict):
    if "materias" not in data:
        raise KeyError("Missing 'materias' key in json data")
    
    for materia in data['materias']:
        if 'Nombre' not in materia or 'Horario' not in materia or 'Días' not in materia or 'Modalidad' not in materia:
            raise ValueError("Missing required keys in materia data")

def organize_horarios(horarios_data):
    days_of_week = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    organized = {day: [] for day in days_of_week}

    for materia in horarios_data:
        for day in materia["Días"]:
            organized[day].append(materia)

    for day in organized:
        organized[day].sort(key=lambda x: x["Horario"].split(" - ")[0])

    return organized