"""
Testy bazy danych
"""

import sys
import os
import tempfile
import unittest

# Dodaj ścieżkę do modułu src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from db.database import Database
from datetime import datetime


class TestDatabase(unittest.TestCase):
    """Testy operacji na bazie danych"""

    def setUp(self):
        """Przygotowanie - tworzenie tymczasowej bazy danych"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()

        # Mockowanie ścieżki bazy danych
        import utils.paths

        self.original_get_db_path = utils.paths.get_db_path
        utils.paths.get_db_path = lambda: self.temp_db.name

        self.db = Database()

    def tearDown(self):
        """Czyszczenie - usunięcie tymczasowej bazy"""
        import utils.paths

        utils.paths.get_db_path = self.original_get_db_path

        if hasattr(self, "db"):
            self.db.conn.close()

        try:
            os.unlink(self.temp_db.name)
        except:
            pass

    def test_add_and_get_weight(self):
        """Test dodawania i pobierania wagi"""
        self.db.add_weight(75.5)
        weights = self.db.get_weights(limit=1)

        self.assertEqual(len(weights), 1)
        self.assertEqual(weights[0][0], 75.5)

    def test_add_and_get_pressure(self):
        """Test dodawania i pobierania ciśnienia"""
        self.db.add_pressure(120, 80)
        pressures = self.db.get_pressures(limit=1)

        self.assertEqual(len(pressures), 1)
        self.assertEqual(pressures[0][0], 120)
        self.assertEqual(pressures[0][1], 80)

    def test_add_and_get_heartrate(self):
        """Test dodawania i pobierania tętna"""
        self.db.add_heartrate(72)
        heartrates = self.db.get_heartrates(limit=1)

        self.assertEqual(len(heartrates), 1)
        self.assertEqual(heartrates[0][0], 72)

    def test_add_and_get_glucose(self):
        """Test dodawania i pobierania glukozy"""
        self.db.add_glucose(
            100, measurement_time="2026-01-08 10:00", meal_timing="na czczo"
        )
        glucose_records = self.db.get_glucose(limit=1)

        self.assertEqual(len(glucose_records), 1)
        self.assertEqual(glucose_records[0][0], 100)
        self.assertEqual(glucose_records[0][3], "na czczo")

    def test_settings(self):
        """Test zapisywania i odczytywania ustawień"""
        self.db.set_setting("test_key", "test_value")
        value = self.db.get_setting("test_key")

        self.assertEqual(value, "test_value")

    def test_settings_default(self):
        """Test domyślnej wartości ustawienia"""
        value = self.db.get_setting("nonexistent_key", "default")
        self.assertEqual(value, "default")

    def test_multiple_weights(self):
        """Test dodawania wielu pomiarów wagi"""
        # Sprawdź ile mamy na start
        initial_count = len(self.db.get_weights(limit=1000))

        self.db.add_weight(70.0)
        self.db.add_weight(71.5)
        self.db.add_weight(72.0)

        weights = self.db.get_weights(limit=1000)
        self.assertEqual(len(weights), initial_count + 3)

    def test_glucose_migration(self):
        """Test migracji tabeli glucose"""
        # Sprawdź czy tabela glucose ma wszystkie kolumny
        cur = self.db.conn.cursor()
        cur.execute("PRAGMA table_info(glucose)")
        columns = [row[1] for row in cur.fetchall()]

        self.assertIn("value", columns)
        self.assertIn("date", columns)
        self.assertIn("measurement_time", columns)
        self.assertIn("meal_timing", columns)


if __name__ == "__main__":
    unittest.main()
