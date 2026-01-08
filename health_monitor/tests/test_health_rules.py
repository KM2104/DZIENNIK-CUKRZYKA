"""
Testy jednostkowe dla reguł zdrowotnych
"""

import sys
import os

# Dodaj ścieżkę do modułu src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import unittest
from utils.health_rules import (
    weight_alert,
    pressure_alert,
    heartrate_alert,
    glucose_alert,
    AlertLevel,
)


class TestWeightAlerts(unittest.TestCase):
    """Testy alertów dla wagi"""

    def test_weight_ok(self):
        """Test wagi w normie"""
        # Domyślne limity: 50-150 kg
        result = weight_alert(70)
        self.assertEqual(result, AlertLevel.OK)

    def test_weight_warning_low(self):
        """Test wagi - ostrzeżenie (poniżej minimum)"""
        result = weight_alert(48)  # Poniżej 50 kg
        self.assertEqual(result, AlertLevel.WARNING)

    def test_weight_warning_high(self):
        """Test wagi - ostrzeżenie (powyżej maksimum)"""
        result = weight_alert(155)  # Powyżej 150 kg
        self.assertEqual(result, AlertLevel.WARNING)

    def test_weight_danger_low(self):
        """Test wagi - niebezpieczna (znacznie poniżej minimum)"""
        result = weight_alert(35)  # Poniżej 50*0.8 = 40 kg
        self.assertEqual(result, AlertLevel.DANGER)

    def test_weight_danger_high(self):
        """Test wagi - niebezpieczna (znacznie powyżej maksimum)"""
        result = weight_alert(200)  # Powyżej 150*1.2 = 180 kg
        self.assertEqual(result, AlertLevel.DANGER)


class TestPressureAlerts(unittest.TestCase):
    """Testy alertów dla ciśnienia"""

    def test_pressure_ok(self):
        """Test ciśnienia w normie"""
        result = pressure_alert(120, 80)
        self.assertEqual(result, AlertLevel.OK)

    def test_pressure_warning_systolic(self):
        """Test ciśnienia - ostrzeżenie (skurczowe podwyższone)"""
        result = pressure_alert(145, 80)
        self.assertEqual(result, AlertLevel.WARNING)

    def test_pressure_warning_diastolic(self):
        """Test ciśnienia - ostrzeżenie (rozkurczowe podwyższone)"""
        result = pressure_alert(120, 95)
        self.assertEqual(result, AlertLevel.WARNING)

    def test_pressure_danger_systolic(self):
        """Test ciśnienia - niebezpieczne (skurczowe wysokie)"""
        result = pressure_alert(190, 80)
        self.assertEqual(result, AlertLevel.DANGER)

    def test_pressure_danger_diastolic(self):
        """Test ciśnienia - niebezpieczne (rozkurczowe wysokie)"""
        result = pressure_alert(120, 125)
        self.assertEqual(result, AlertLevel.DANGER)


class TestHeartRateAlerts(unittest.TestCase):
    """Testy alertów dla tętna"""

    def test_heartrate_ok(self):
        """Test tętna w normie (60-100 bpm)"""
        result = heartrate_alert(75)
        self.assertEqual(result, AlertLevel.OK)

    def test_heartrate_warning_low(self):
        """Test tętna - ostrzeżenie (50-59 bpm)"""
        result = heartrate_alert(55)
        self.assertEqual(result, AlertLevel.WARNING)

    def test_heartrate_warning_high(self):
        """Test tętna - ostrzeżenie (101-120 bpm)"""
        result = heartrate_alert(110)
        self.assertEqual(result, AlertLevel.WARNING)

    def test_heartrate_danger_low(self):
        """Test tętna - niebezpieczne (<50 bpm)"""
        result = heartrate_alert(45)
        self.assertEqual(result, AlertLevel.DANGER)

    def test_heartrate_danger_high(self):
        """Test tętna - niebezpieczne (>120 bpm)"""
        result = heartrate_alert(140)
        self.assertEqual(result, AlertLevel.DANGER)


class TestGlucoseAlerts(unittest.TestCase):
    """Testy alertów dla glukozy"""

    def test_glucose_ok(self):
        """Test glukozy w normie (70-140 mg/dL)"""
        result = glucose_alert(100)
        self.assertEqual(result, AlertLevel.OK)

    def test_glucose_warning_low(self):
        """Test glukozy - ostrzeżenie (50-69 mg/dL)"""
        result = glucose_alert(65)
        self.assertEqual(result, AlertLevel.WARNING)

    def test_glucose_warning_high(self):
        """Test glukozy - ostrzeżenie (141-200 mg/dL)"""
        result = glucose_alert(180)
        self.assertEqual(result, AlertLevel.WARNING)

    def test_glucose_danger_low(self):
        """Test glukozy - niebezpieczne (<50 mg/dL)"""
        result = glucose_alert(40)
        self.assertEqual(result, AlertLevel.DANGER)

    def test_glucose_danger_high(self):
        """Test glukozy - niebezpieczne (>200 mg/dL)"""
        result = glucose_alert(250)
        self.assertEqual(result, AlertLevel.DANGER)


if __name__ == "__main__":
    unittest.main()
