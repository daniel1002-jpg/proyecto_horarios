import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import horarios

class TestReadHorarios(unittest.TestCase):
    
    def test_read_existing_file(self):
        # Arrange
        file_path = "data/horarios.json"

        # Act
        data = horarios.read_horarios(file_path)

        # Assert
        self.assertIsInstance(data, list) # Revised if is necessary
        self.assertGreater(len(data), 0)

    def test_read_nonexisting_file(self):
        # Arrange
        file_path = "data/non_existent_file.json"

        # Act & Assert
        with self.assertRaises(FileNotFoundError):
            horarios.read_horarios(file_path)

class TestValidateFormat(unittest.TestCase):

    def test_valid_format(self):
        # Arrange
        valid_data = [
            {
                "nombre": "Test subject",
                "horario": {"inicio": "10:00", "fin": "12:00"},
                "dias": ["Lunes", "Miércoles"],
                "modalidad": "mixta"
            }
        ]

        # Act & Assert
        try:
            horarios.validate_format(valid_data)
        except (KeyError, ValueError):
            self.fail("validate_format raised an exception with valid data")

    def test_missing_nombre_key(self):
        # Arrange
        invalid_data = [
            {
                "horario": {"inicio": "10:00", "fin": "12:00"},
                "dias": ["Lunes", "Miércoles"],
                "modalidad": "mixta"
            }
        ]

        # Act & Assert
        with self.assertRaises(KeyError):
            horarios.validate_format(invalid_data)

    def test_missing_horario_key(self):
        # Arrange
        invalid_data = [
            {
                "nombre": "Test subject",
                "dias": ["Lunes", "Miércoles"],
                "modalidad": "mixta"
            }
        ]

        # Act & Assert
        with self.assertRaises(KeyError):
            horarios.validate_format(invalid_data)

    def test_invalid_horario_structure(self):
        # Arrange
        invalid_data = [
            {
                "nombre": "Test subject",
                "horario": "18:00 - 12:00",
                "dias": ["Lunes", "Miércoles"],
                "modalidad": "mixta"
            }
        ]

        # Act & Assert
        with self.assertRaises(ValueError):
            horarios.validate_format(invalid_data)

    def test_missing_horario_inicio(self):
        # Arrange
        invalid_data = [
            {
                "nombre": "Test subject",
                "horario": {"fin": "12:00"},
                "dias": ["Lunes", "Miércoles"],
                "modalidad": "mixta"
            }
        ]

        # Act & Assert
        with self.assertRaises(KeyError):
            horarios.validate_format(invalid_data)

    def test_non_list_data(self):
        # Arrange
        invalid_data = {"nombre": "Test subject"}

        # Act & Assert
        with self.assertRaises(ValueError):
            horarios.validate_format(invalid_data)

class TestOrganizeHorarios(unittest.TestCase):

    """ Common setup for tests """
    def setUp(self):
        self.sample_data = [
            {"nombre": "Teoría de Algoritmos", "horario": {"inicio": "19:00", "fin": "22:00"}, "dias": ["Lunes", "Jueves"], "modalidad": "mixta"},
            {"nombre": "Taller de programación 1", "horario": {"inicio": "18:00", "fin": "22:00"}, "dias": ["Lunes", "Jueves"], "modalidad": "virtual"},
            {"nombre": "Probabilidad y Estadística", "horario": {"inicio": "18:00", "fin": "21:00"}, "dias": ["Martes", "Miércoles"], "modalidad": "presencial"},
        ]

    def test_organize_by_days(self):
        # Act
        organized_data = horarios.organize_horarios(self.sample_data)

        # Assert
        expected_days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
        for day in expected_days:
            self.assertIn(day, organized_data)

    def test_correct_subject_count_per_day(self):
        # Act
        organized_data = horarios.organize_horarios(self.sample_data)

        # Assert
        self.assertEqual(len(organized_data["Lunes"]), 2)
        self.assertEqual(len(organized_data["Martes"]), 1)
        self.assertEqual(len(organized_data["Miércoles"]), 1)
        self.assertEqual(len(organized_data["Jueves"]), 2)
        self.assertEqual(len(organized_data["Viernes"]), 0)

    def test_time_sorting_within_days(self):
        # Act
        organized_data = horarios.organize_horarios(self.sample_data)

        # Assert
        lunes_subjects = organized_data["Lunes"]
        self.assertEqual(lunes_subjects[0]["nombre"], "Taller de programación 1")
        self.assertEqual(lunes_subjects[1]["nombre"], "Teoría de Algoritmos")

    def test_empty_data(self):
        # Act
        organized_data = horarios.organize_horarios([])

        # Assert
        expected_days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
        for day in expected_days:
            self.assertIn(day, organized_data)
            self.assertEqual(len(organized_data[day]), 0)

class TestIntegration(unittest.TestCase):

    def test_read_and_organize_real_data(self):
        # Arrange
        file_path = "data/horarios.json"
        
        # Act
        data = horarios.read_horarios(file_path)
        organized_data = horarios.organize_horarios(data)

        # Assert
        self.assertIsInstance(organized_data, dict)
        self.assertGreater(len(organized_data["Lunes"]), 0)
        self.assertGreater(len(organized_data["Martes"]), 0)


if __name__ == "__main__":
    unittest.main()