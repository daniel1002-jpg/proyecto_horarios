import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
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
            