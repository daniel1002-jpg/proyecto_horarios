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

class TestGenerateHTML(unittest.TestCase):
    
    def setUp(self):
        self.sample_data = [
            {"nombre": "Teoría de Algoritmos", "horario": {"inicio": "19:00", "fin": "22:00"}, "dias": ["Lunes", "Jueves"], "modalidad": "mixta"},
        ]
        self.organized_data = horarios.organize_horarios(self.sample_data)

    def test_generate_html_creates_file(self):
        # Arrange
        output_path = "output/test_horario.html"

        # Act
        horarios.generate_html(self.organized_data, output_path)

        # Assert
        self.assertTrue(os.path.exists(output_path))

        # Clean up
        if os.path.exists(output_path):
            os.remove(output_path)

    def test_generate_html_contains_subject_name(self):
        # Arrange
        output_path = "output/test_horario.html"

        # Act
        horarios.generate_html(self.organized_data, output_path)

        # Assert
        with open(output_path, 'r') as file:
            content = file.read()
            self.assertIn(self.organized_data["Lunes"][0]["nombre"], content)

        # Clean up
        os.remove(output_path)

    def test_generate_html_contains_schedule_info(self):
        # Arrange
        output_path = "output/test_horario.html"

        # Act
        horarios.generate_html(self.organized_data, output_path)

        # Assert
        schedule = format(self.organized_data["Lunes"][0]["horario"]["inicio"]) + " - " + format(self.organized_data["Lunes"][0]["horario"]["fin"])
        modality = self.organized_data["Lunes"][0]["modalidad"]
        with open(output_path, 'r') as file:
            content = file.read()
            self.assertIn(schedule, content)
            self.assertIn(modality, content)

        # Clean up
        os.remove(output_path)

    def test_generated_html_has_valid_structure(self):
        # Arrange
        output_path = "output/test_horario.html"

        # Act
        horarios.generate_html(self.organized_data, output_path)

        # Assert
        with open(output_path, 'r') as file:
            content = file.read()
            self.assertTrue("<!DOCTYPE html>" in content)
            self.assertTrue("<html lang=\"es\">" in content)
            self.assertTrue("</html>" in content)

        # Clean up
        os.remove(output_path)

    def test_generate_html_contains_summary_statistics(self):
        # Arrange
        output_path = "output/test_horario.html"

        # Act
        horarios.generate_html(self.organized_data, output_path)

        # Assert
        with open(output_path, 'r') as file:
            content = file.read()
            self.assertIn("<strong>Total de materias:</strong> 1", content)
            self.assertIn("Presencial: 0", content)
            self.assertIn("Virtual: 0", content)
            self.assertIn("Mixta: 1", content)

        # Clean up
        os.remove(output_path)

class TestGenerateTableData(unittest.TestCase):
    
    def setUp(self):
        self.sample_data = [
            {"nombre": "Teoría de Algoritmos", "horario": {"inicio": "19:00", "fin": "22:00"}, "dias": ["Lunes", "Jueves"], "modalidad": "mixta"},
            {"nombre": "Matemáticas Discretas", "horario": {"inicio": "18:00", "fin": "21:00"}, "dias": ["Martes", "Viernes"], "modalidad": "presencial"}
        ]
        self.organized_data = horarios.organize_horarios(self.sample_data)

    def test_generate_table_data_creates_time_slots(self):
        # Act
        table_data = horarios.generate_table_data(self.organized_data)

        # Assert
        self.assertEqual(len(table_data), 2)
        self.assertIn("time_range", table_data[0])

    def test_generate_table_data_sorts_time_ranges(self):
        # Act
        table_data = horarios.generate_table_data(self.organized_data)

        # Assert
        self.assertEqual(table_data[0]["time_range"], "18:00 - 21:00")
        self.assertEqual(table_data[1]["time_range"], "19:00 - 22:00")

    def test_generate_table_data_assigns_subjects_to_names(self):
        # Act
        table_data = horarios.generate_table_data(self.organized_data)

        # Assert
        first_row = table_data[0]
        self.assertEqual(first_row["Martes"]["nombre"], "Matemáticas Discretas")
        self.assertEqual(first_row["Viernes"]["nombre"], "Matemáticas Discretas")
        self.assertIsNone(first_row["Miércoles"])

        second_row = table_data[1]
        self.assertEqual(second_row["Lunes"]["nombre"], "Teoría de Algoritmos")
        self.assertEqual(second_row["Jueves"]["nombre"], "Teoría de Algoritmos")

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