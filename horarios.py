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