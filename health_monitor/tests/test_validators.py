"""
Testy jednostkowe dla walidatorów
"""

import sys
import os

# Dodaj ścieżkę do modułu src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import unittest
from utils.validators import (
    validate_weight,
    validate_pressure,
    validate_heartrate,
    validate_glucose,
    ValidationError,
)


class TestWeightValidator(unittest.TestCase):
    """Testy walidatora wagi"""

    def test_valid_weight(self):
        """Test poprawnej wagi"""
        self.assertEqual(validate_weight("70.5"), 70.5)
        self.assertEqual(validate_weight("100"), 100.0)

    def test_invalid_weight_not_number(self):
        """Test błędnej wagi - nie liczba"""
        with self.assertRaises(ValidationError) as context:
            validate_weight("abc")
        self.assertIn("musi być liczbą", str(context.exception))

    def test_invalid_weight_negative(self):
        """Test błędnej wagi - wartość ujemna"""
        with self.assertRaises(ValidationError) as context:
            validate_weight("-10")
        self.assertIn("Nieprawidłowa wartość", str(context.exception))

    def test_invalid_weight_too_high(self):
        """Test błędnej wagi - wartość za duża"""
        with self.assertRaises(ValidationError) as context:
            validate_weight("600")
        self.assertIn("Nieprawidłowa wartość", str(context.exception))


class TestPressureValidator(unittest.TestCase):
    """Testy walidatora ciśnienia"""

    def test_valid_pressure(self):
        """Test poprawnego ciśnienia"""
        sys, dia = validate_pressure("120", "80")
        self.assertEqual(sys, 120)
        self.assertEqual(dia, 80)

    def test_invalid_pressure_not_number(self):
        """Test błędnego ciśnienia - nie liczba"""
        with self.assertRaises(ValidationError) as context:
            validate_pressure("abc", "80")
        self.assertIn("musi być liczbą", str(context.exception))

    def test_invalid_pressure_systolic_too_low(self):
        """Test błędnego ciśnienia - skurczowe za niskie"""
        with self.assertRaises(ValidationError) as context:
            validate_pressure("40", "80")
        self.assertIn("Nieprawidłowe ciśnienie", str(context.exception))

    def test_invalid_pressure_diastolic_greater_than_systolic(self):
        """Test błędnego ciśnienia - rozkurczowe większe niż skurczowe"""
        with self.assertRaises(ValidationError) as context:
            validate_pressure("80", "90")
        self.assertIn("większe od rozkurczowego", str(context.exception))


class TestHeartRateValidator(unittest.TestCase):
    """Testy walidatora tętna"""

    def test_valid_heartrate(self):
        """Test poprawnego tętna"""
        self.assertEqual(validate_heartrate("70"), 70)
        self.assertEqual(validate_heartrate("100"), 100)

    def test_invalid_heartrate_not_number(self):
        """Test błędnego tętna - nie liczba"""
        with self.assertRaises(ValidationError) as context:
            validate_heartrate("abc")
        self.assertIn("musi być liczbą", str(context.exception))

    def test_invalid_heartrate_negative(self):
        """Test błędnego tętna - wartość ujemna"""
        with self.assertRaises(ValidationError) as context:
            validate_heartrate("-10")
        self.assertIn("Nieprawidłowa wartość", str(context.exception))

    def test_invalid_heartrate_too_high(self):
        """Test błędnego tętna - wartość za wysoka"""
        with self.assertRaises(ValidationError) as context:
            validate_heartrate("400")
        self.assertIn("Nieprawidłowa wartość", str(context.exception))


class TestGlucoseValidator(unittest.TestCase):
    """Testy walidatora glukozy"""

    def test_valid_glucose(self):
        """Test poprawnej glukozy"""
        self.assertEqual(validate_glucose("100"), 100)
        self.assertEqual(validate_glucose("150"), 150)

    def test_invalid_glucose_not_number(self):
        """Test błędnej glukozy - nie liczba"""
        with self.assertRaises(ValidationError) as context:
            validate_glucose("abc")
        self.assertIn("musi być liczbą", str(context.exception))

    def test_invalid_glucose_negative(self):
        """Test błędnej glukozy - wartość ujemna"""
        with self.assertRaises(ValidationError) as context:
            validate_glucose("-10")
        self.assertIn("Nieprawidłowa wartość", str(context.exception))

    def test_invalid_glucose_too_high(self):
        """Test błędnej glukozy - wartość za wysoka"""
        with self.assertRaises(ValidationError) as context:
            validate_glucose("700")
        self.assertIn("Nieprawidłowa wartość", str(context.exception))


if __name__ == "__main__":
    unittest.main()
