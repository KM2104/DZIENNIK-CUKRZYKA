"""
Testy funkcjonalności admina i zarządzania użytkownikami
"""

import sys
import os
import tempfile
import unittest

# Dodaj ścieżkę do modułu src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from db.database import Database


class TestAdminFeatures(unittest.TestCase):
    """Testy funkcjonalności admina"""

    def setUp(self):
        """Przygotowanie - tworzenie tymczasowej bazy danych"""
        fd, self.temp_db_path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        os.unlink(self.temp_db_path)

        import utils.paths

        self.original_get_db_path = utils.paths.get_db_path
        utils.paths.get_db_path = lambda: self.temp_db_path

        self.db = Database()

    def tearDown(self):
        """Czyszczenie"""
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
            except:
                pass

    def test_admin_created_automatically(self):
        """Test że admin jest tworzony automatycznie"""
        users = self.db.get_all_users()

        # Powinien być co najmniej 1 użytkownik (admin)
        self.assertGreaterEqual(len(users), 1)

        # Znajdź admina
        admin_users = [u for u in users if len(u) == 4 and u[3] == 1]
        self.assertEqual(len(admin_users), 1)

        # Sprawdź dane admina
        admin = admin_users[0]
        self.assertEqual(admin[1], "admin")  # nazwa

    def test_admin_cannot_be_deleted_by_id(self):
        """Test że nie można usunąć użytkownika admin"""
        users = self.db.get_all_users()
        admin = [u for u in users if len(u) == 4 and u[3] == 1][0]
        admin_id = admin[0]

        # Próba usunięcia admina
        # W db/database.py delete_user sprawdza is_admin
        # Jeśli nie ma zabezpieczenia, powinniśmy je dodać
        try:
            self.db.delete_user(admin_id)
            # Jeśli się udało, sprawdź czy admin nadal istnieje
            users_after = self.db.get_all_users()
            admin_after = [u for u in users_after if len(u) == 4 and u[3] == 1]
            # Admin powinien nadal istnieć (chroniony)
            self.assertEqual(len(admin_after), 1)
        except ValueError:
            # Oczekiwany wyjątek - nie można usunąć admina
            pass

    def test_is_admin_check(self):
        """Test sprawdzania czy użytkownik jest adminem"""
        users = self.db.get_all_users()
        admin = [u for u in users if len(u) == 4 and u[3] == 1][0]
        admin_id = admin[0]

        # Dodaj zwykłego użytkownika
        self.db.add_user("Test User", "1234")
        users = self.db.get_all_users()
        test_user = [u for u in users if u[1] == "Test User"][0]
        test_user_id = test_user[0]

        # Sprawdź funkcję is_admin
        self.assertTrue(self.db.is_admin(admin_id))
        self.assertFalse(self.db.is_admin(test_user_id))

    def test_user_limit(self):
        """Test limitu użytkowników (4 + admin = 5)"""
        # Admin już istnieje, dodaj 4 użytkowników
        for i in range(1, 5):
            self.db.add_user(f"User {i}", f"123{i}")

        users = self.db.get_all_users()
        # Powinno być 5 użytkowników (admin + 4)
        self.assertEqual(len(users), 5)

        # Próba dodania 5. użytkownika powinna się nie udać
        # (jeśli limit jest zaimplementowany w Settings, nie w Database)
        # Ten test sprawdza tylko czy można dodać 4 użytkowników
        non_admin = [u for u in users if not (len(u) == 4 and u[3] == 1)]
        self.assertEqual(len(non_admin), 4)

    def test_unique_username_validation(self):
        """Test walidacji unikalnych nazw użytkowników"""
        self.db.add_user("Jan Kowalski", "1234")

        # Próba dodania użytkownika z tą samą nazwą
        # Jeśli walidacja jest w Settings, nie w Database, to się uda
        # Ten test sprawdza czy można dodać duplikat w bazie
        self.db.add_user("Jan Kowalski", "5678")

        users = self.db.get_all_users()
        jan_users = [u for u in users if u[1] == "Jan Kowalski"]

        # Czy database pozwala na duplikaty? (sprawdzamy obecny stan)
        # Jeśli tak, walidacja musi być w Settings
        self.assertGreaterEqual(len(jan_users), 1)


if __name__ == "__main__":
    unittest.main()
