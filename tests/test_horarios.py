import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import json
import horarios

class TestReadHorarios(unittest.TestCase):
    
    def test_read_horarios_correctly(self):
        # Arrange
        file_path = "data/horarios.json"

        # Act
        data = horarios.read_horarios(file_path)

        # Assert
        self.assertGreater(len(data), 0)
        for item in data:
            self.assertIn("Nombre", item)
            self.assertIn("Horario", item)
            self.assertIn("Días", item)
            self.assertIn("Modalidad", item)

    def test_read_horarios_file_not_found(self):
        # Arrange
        file_path = "data/non_existent_file.json"

        # Act & Assert
        with self.assertRaises(FileNotFoundError):
            horarios.read_horarios(file_path)

    def test_read_correct_data_with_invalid_keys(self):
        # Arrange
        invalid_data = get_invalid_data()

        # Act & Assert
        with self.assertRaises(KeyError):
            horarios.validate_format(invalid_data)

    def test_read_correct_data_with_missing_keys(self):
        # Arrange
        invalid_data = json.dumps({"materias": [{"Nombre": "Algoritmos"}]})
        with open("invalid_data.json", "w") as f:
            f.write(invalid_data)

        # Act & Assert
        data = horarios.read_horarios("invalid_data.json")
        with self.assertRaises(ValueError):
            horarios.validate_format(data)

        os.remove("invalid_data.json")

    def test_organize_horarios(self):
        # Arrange
        horarios_data = [
            {"Nombre": "Teoría de Algoritmos", "Horario": "19:00 - 22:00", "Días": ["Lunes", "Jueves"], "Modalidad": "Mixta"},
            {"Nombre": "Taller de programación 1", "Horario": "18:00 - 22:00", "Días": ["Lunes", "Jueves"], "Modalidad": "Virtual"},
            {"Nombre": "Probabilidad y Estadística", "Horario": "18:00 - 21:00", "Días": ["Martes", "Miércoles"], "Modalidad": "Presencial"},
        ]

        # Act
        organized_data = horarios.organize_horarios(horarios_data)

        # Assert
        self.assertIn("Lunes", organized_data)
        self.assertIn("Martes", organized_data)
        self.assertIn("Miércoles", organized_data)
        self.assertIn("Jueves", organized_data)

        self.assertEqual(len(organized_data["Lunes"]), 2)
        self.assertEqual(len(organized_data["Martes"]), 1)
        self.assertEqual(len(organized_data["Miércoles"]), 1)
        self.assertEqual(len(organized_data["Jueves"]), 2)

        lunes_materias = organized_data["Lunes"]
        self.assertEqual(lunes_materias[0]["Nombre"], "Taller de programación 1")
        self.assertEqual(lunes_materias[1]["Nombre"], "Teoría de Algoritmos")

        jueves_materias = organized_data["Jueves"]
        self.assertEqual(jueves_materias[0]["Nombre"], "Taller de programación 1")
        self.assertEqual(jueves_materias[1]["Nombre"], "Teoría de Algoritmos")

def get_invalid_data():
    invalid_data = {"materias_incorrectas": []}
    
    with open("invalid_data.json", "w") as f:
        json.dump(invalid_data, f)

    return invalid_data

def get_horarios_data(data_path):
    return horarios.read_horarios(data_path)