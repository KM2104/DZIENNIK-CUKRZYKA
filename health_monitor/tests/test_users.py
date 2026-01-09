"""
Testy zarządzania użytkownikami
"""

import sys
import os
import tempfile
import unittest

# Dodaj ścieżkę do modułu src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from db.database import Database


class TestUsers(unittest.TestCase):
    """Testy zarządzania użytkownikami"""

    def setUp(self):
        """Przygotowanie - tworzenie tymczasowej bazy danych"""
        # Użyj unikalnego pliku tymczasowego
        fd, self.temp_db_path = tempfile.mkstemp(suffix=".db")
        os.close(fd)  # Zamknij deskryptor pliku
        os.unlink(self.temp_db_path)  # Usuń plik, żeby Database mógł go stworzyć

        # Mockowanie ścieżki bazy danych
        import utils.paths

        self.original_get_db_path = utils.paths.get_db_path
        utils.paths.get_db_path = lambda: self.temp_db_path

        self.db = Database()

    def tearDown(self):
        """Czyszczenie - usunięcie tymczasowej bazy"""
        import utils.paths

        utils.paths.get_db_path = self.original_get_db_path

        if hasattr(self, "db") and self.db.conn:
            try:
                self.db.conn.close()
            except:
                pass

        if hasattr(self, "temp_db_path"):
            try:
                if os.path.exists(self.temp_db_path):
                    os.unlink(self.temp_db_path)
            except Exception as e:
                pass  # Ignoruj błędy przy czyszczeniu

    def test_add_user(self):
        """Test dodawania użytkownika"""
        self.db.add_user("Jan Kowalski", "1234")
        users = self.db.get_all_users()

        self.assertEqual(len(users), 1)
        self.assertEqual(users[0][1], "Jan Kowalski")

    def test_add_multiple_users(self):
        """Test dodawania wielu użytkowników"""
        self.db.add_user("Jan Kowalski", "1234")
        self.db.add_user("Anna Nowak", "5678")
        users = self.db.get_all_users()

        self.assertEqual(len(users), 2)
        names = [user[1] for user in users]
        self.assertIn("Jan Kowalski", names)
        self.assertIn("Anna Nowak", names)

    def test_verify_user_pin_correct(self):
        """Test weryfikacji poprawnego PIN"""
        self.db.add_user("Jan Kowalski", "1234")
        users = self.db.get_all_users()
        user_id = users[0][0]

        result = self.db.verify_user_pin(user_id, "1234")
        self.assertTrue(result)

    def test_verify_user_pin_incorrect(self):
        """Test weryfikacji niepoprawnego PIN"""
        self.db.add_user("Jan Kowalski", "1234")
        users = self.db.get_all_users()
        user_id = users[0][0]

        result = self.db.verify_user_pin(user_id, "9999")
        self.assertFalse(result)

    def test_update_user_pin(self):
        """Test aktualizacji PIN użytkownika"""
        self.db.add_user("Jan Kowalski", "1234")
        users = self.db.get_all_users()
        user_id = users[0][0]

        self.db.update_user_pin(user_id, "5678")
        result = self.db.verify_user_pin(user_id, "5678")
        self.assertTrue(result)

    def test_delete_user(self):
        """Test usuwania użytkownika"""
        self.db.add_user("Jan Kowalski", "1234")
        self.db.add_user("Anna Nowak", "5678")

        users_before = self.db.get_all_users()
        self.assertEqual(len(users_before), 2)

        user_id = users_before[0][0]
        self.db.delete_user(user_id)

        users_after = self.db.get_all_users()
        self.assertEqual(len(users_after), 1)

    def test_delete_last_user_raises_error(self):
        """Test, że nie można usunąć ostatniego użytkownika"""
        self.db.add_user("Jan Kowalski", "1234")
        users = self.db.get_all_users()
        user_id = users[0][0]

        with self.assertRaises(ValueError):
            self.db.delete_user(user_id)

    def test_get_user_by_id(self):
        """Test pobierania danych użytkownika po ID"""
        self.db.add_user("Jan Kowalski", "1234")
        users = self.db.get_all_users()
        user_id = users[0][0]

        user = self.db.get_user_by_id(user_id)
        self.assertIsNotNone(user)
        self.assertEqual(user[1], "Jan Kowalski")


if __name__ == "__main__":
    unittest.main()
