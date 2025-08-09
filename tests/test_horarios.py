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

    

def get_invalid_data():
    invalid_data = {"materias_incorrectas": []}
    
    with open("invalid_data.json", "w") as f:
        json.dump(invalid_data, f)

    return invalid_data