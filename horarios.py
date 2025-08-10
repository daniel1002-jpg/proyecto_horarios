import json

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