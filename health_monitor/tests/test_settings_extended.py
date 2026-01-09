"""
Testy rozszerzonych ustawień (limity ciśnienia, tętna, glukozy)
"""

import sys
import os
import tempfile
import unittest

# Dodaj ścieżkę do modułu src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from utils.settings import Settings


class TestExtendedSettings(unittest.TestCase):
    """Testy rozszerzonych ustawień"""

    def setUp(self):
        """Przygotowanie - tworzenie tymczasowej bazy danych"""
        # Użyj unikalnego pliku tymczasowego
        fd, self.temp_db_path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        os.unlink(self.temp_db_path)

        # Mockowanie ścieżki bazy danych
        import utils.paths

        self.original_get_db_path = utils.paths.get_db_path
        utils.paths.get_db_path = lambda: self.temp_db_path

        self.settings = Settings()

    def tearDown(self):
        """Czyszczenie - usunięcie tymczasowej bazy"""
        import utils.paths

        utils.paths.get_db_path = self.original_get_db_path

        if hasattr(self.settings, "db") and self.settings.db.conn:
            try:
                self.settings.db.conn.close()
            except:
                pass

        if hasattr(self, "temp_db_path"):
            try:
                if os.path.exists(self.temp_db_path):
                    os.unlink(self.temp_db_path)
            except Exception as e:
                pass

    def test_pressure_limits_default(self):
        """Test domyślnych limitów ciśnienia"""
        sys_min, dia_min, sys_w, dia_w, sys_d, dia_d = (
            self.settings.get_pressure_limits()
        )

        self.assertEqual(sys_min, 90)
        self.assertEqual(dia_min, 60)
        self.assertEqual(sys_w, 140)
        self.assertEqual(dia_w, 90)
        self.assertEqual(sys_d, 180)
        self.assertEqual(dia_d, 120)

    def test_set_pressure_limits(self):
        """Test ustawiania limitów ciśnienia"""
        self.settings.set_pressure_limits(85, 55, 130, 85, 170, 110)
        sys_min, dia_min, sys_w, dia_w, sys_d, dia_d = (
            self.settings.get_pressure_limits()
        )

        self.assertEqual(sys_min, 85)
        self.assertEqual(dia_min, 55)
        self.assertEqual(sys_w, 130)
        self.assertEqual(dia_w, 85)
        self.assertEqual(sys_d, 170)
        self.assertEqual(dia_d, 110)

    def test_heartrate_limits_default(self):
        """Test domyślnych limitów tętna"""
        hr_min, hr_max, hr_d_low, hr_d_high = self.settings.get_heartrate_limits()

        self.assertEqual(hr_min, 60)
        self.assertEqual(hr_max, 100)
        self.assertEqual(hr_d_low, 40)
        self.assertEqual(hr_d_high, 150)

    def test_set_heartrate_limits(self):
        """Test ustawiania limitów tętna"""
        self.settings.set_heartrate_limits(55, 95, 35, 140)
        hr_min, hr_max, hr_d_low, hr_d_high = self.settings.get_heartrate_limits()

        self.assertEqual(hr_min, 55)
        self.assertEqual(hr_max, 95)
        self.assertEqual(hr_d_low, 35)
        self.assertEqual(hr_d_high, 140)

    def test_glucose_limits_default(self):
        """Test domyślnych limitów glukozy"""
        gl_min, gl_max, gl_d_low, gl_d_high = self.settings.get_glucose_limits()

        self.assertEqual(gl_min, 70)
        self.assertEqual(gl_max, 140)
        self.assertEqual(gl_d_low, 50)
        self.assertEqual(gl_d_high, 250)

    def test_set_glucose_limits(self):
        """Test ustawiania limitów glukozy"""
        self.settings.set_glucose_limits(65, 130, 45, 240)
        gl_min, gl_max, gl_d_low, gl_d_high = self.settings.get_glucose_limits()

        self.assertEqual(gl_min, 65)
        self.assertEqual(gl_max, 130)
        self.assertEqual(gl_d_low, 45)
        self.assertEqual(gl_d_high, 240)

    def test_weight_limits(self):
        """Test limitów wagi"""
        self.settings.set_weight_limits(55.0, 120.0)
        w_min, w_max = self.settings.get_weight_limits()

        self.assertEqual(w_min, 55.0)
        self.assertEqual(w_max, 120.0)

    def test_current_user_id(self):
        """Test zarządzania ID aktualnego użytkownika"""
        self.settings.set_current_user_id(5)
        user_id = self.settings.get_current_user_id()

        self.assertEqual(user_id, 5)

    def test_user_management(self):
        """Test zarządzania użytkownikami przez Settings"""
        self.settings.add_user("Test User", "1234")
        users = self.settings.get_all_users()

        self.assertEqual(len(users), 1)
        self.assertEqual(users[0][1], "Test User")

    def test_change_user_pin_success(self):
        """Test zmiany PIN użytkownika - sukces"""
        self.settings.add_user("Test User", "1234")
        users = self.settings.get_all_users()
        user_id = users[0][0]

        result = self.settings.change_user_pin(user_id, "1234", "5678")
        self.assertTrue(result)

        # Sprawdź czy nowy PIN działa
        verified = self.settings.db.verify_user_pin(user_id, "5678")
        self.assertTrue(verified)

    def test_change_user_pin_wrong_old_pin(self):
        """Test zmiany PIN użytkownika - zły stary PIN"""
        self.settings.add_user("Test User", "1234")
        users = self.settings.get_all_users()
        user_id = users[0][0]

        result = self.settings.change_user_pin(user_id, "9999", "5678")
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
