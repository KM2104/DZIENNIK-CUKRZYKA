"""
Zarządzanie bazą danych
"""

import sqlite3
from datetime import datetime
from utils.paths import get_db_path


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(get_db_path())
        self.create_tables()

    def create_tables(self):
        cur = self.conn.cursor()

        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS weight (
            id INTEGER PRIMARY KEY,
            value REAL,
            date TEXT
        )
        """
        )

        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS pressure (
            id INTEGER PRIMARY KEY,
            systolic INTEGER,
            diastolic INTEGER,
            date TEXT
        )
        """
        )

        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS heartrate (
            id INTEGER PRIMARY KEY,
            value INTEGER,
            date TEXT
        )
        """
        )

        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS glucose (
            id INTEGER PRIMARY KEY,
            value INTEGER,
            date TEXT,
            measurement_time TEXT,
            meal_timing TEXT
        )
        """
        )

        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """
        )

        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            pin TEXT NOT NULL,
            created_date TEXT,
            is_admin INTEGER DEFAULT 0
        )
        """
        )

        self.conn.commit()

        # Migracja: Dodaj brakujące kolumny do istniejącej tabeli glucose
        self._migrate_glucose_table()
        self._migrate_user_columns()
        self._create_admin_user()

    def _create_admin_user(self):
        """Tworzy domyślnego użytkownika admin jeśli nie istnieje"""
        cur = self.conn.cursor()

        # Sprawdź czy istnieje użytkownik admin
        cur.execute("SELECT id FROM users WHERE is_admin = 1")
        admin_exists = cur.fetchone()

        if not admin_exists:
            # Dodaj użytkownika admin z hasłem 1111
            cur.execute(
                "INSERT INTO users (name, pin, created_date, is_admin) VALUES (?, ?, ?, ?)",
                ("admin", "1111", datetime.now().isoformat(), 1),
            )
            self.conn.commit()

    def _migrate_glucose_table(self):
        """Dodaje nowe kolumny do tabeli glucose jeśli ich nie ma"""
        cur = self.conn.cursor()

        # Sprawdź czy kolumny measurement_time i meal_timing istnieją
        cur.execute("PRAGMA table_info(glucose)")
        columns = [row[1] for row in cur.fetchall()]

        if "measurement_time" not in columns:
            cur.execute("ALTER TABLE glucose ADD COLUMN measurement_time TEXT")
            self.conn.commit()

        if "meal_timing" not in columns:
            cur.execute("ALTER TABLE glucose ADD COLUMN meal_timing TEXT")
            self.conn.commit()

    def _migrate_user_columns(self):
        """Dodaje kolumnę user_id do tabel pomiarów jeśli jej nie ma"""
        cur = self.conn.cursor()

        tables = ["weight", "pressure", "heartrate", "glucose"]
        for table in tables:
            cur.execute(f"PRAGMA table_info({table})")
            columns = [row[1] for row in cur.fetchall()]

            if "user_id" not in columns:
                cur.execute(f"ALTER TABLE {table} ADD COLUMN user_id INTEGER DEFAULT 1")
                self.conn.commit()

        # Migracja: Dodaj kolumnę is_admin do tabeli users jeśli jej nie ma
        cur.execute("PRAGMA table_info(users)")
        columns = [row[1] for row in cur.fetchall()]

        if "is_admin" not in columns:
            cur.execute("ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0")
            self.conn.commit()

    def add_weight(self, value):
        self.conn.execute(
            "INSERT INTO weight (value, date) VALUES (?, ?)",
            (value, datetime.now().isoformat()),
        )
        self.conn.commit()

    def add_pressure(self, sys, dia):
        self.conn.execute(
            "INSERT INTO pressure (systolic, diastolic, date) VALUES (?, ?, ?)",
            (sys, dia, datetime.now().isoformat()),
        )
        self.conn.commit()

    def add_heartrate(self, value):
        self.conn.execute(
            "INSERT INTO heartrate (value, date) VALUES (?, ?)",
            (value, datetime.now().isoformat()),
        )
        self.conn.commit()

    def add_glucose(self, value, measurement_time=None, meal_timing=""):
        if measurement_time is None:
            measurement_time = datetime.now().isoformat()
        self.conn.execute(
            "INSERT INTO glucose (value, date, measurement_time, meal_timing) VALUES (?, ?, ?, ?)",
            (value, datetime.now().isoformat(), measurement_time, meal_timing),
        )
        self.conn.commit()

    def get_weights(self, limit=100):
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT value, date
            FROM weight
            ORDER BY date DESC
            LIMIT ?
        """,
            (limit,),
        )
        return cur.fetchall()

    def get_pressures(self, limit=100):
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT systolic, diastolic, date
            FROM pressure
            ORDER BY date DESC
            LIMIT ?
        """,
            (limit,),
        )
        return cur.fetchall()

    def get_heartrates(self, limit=100):
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT value, date
            FROM heartrate
            ORDER BY date DESC
            LIMIT ?
        """,
            (limit,),
        )
        return cur.fetchall()

    def get_glucose(self, limit=100):
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT value, date, measurement_time, meal_timing
            FROM glucose
            ORDER BY date DESC
            LIMIT ?
        """,
            (limit,),
        )
        return cur.fetchall()

    def set_setting(self, key: str, value: str):
        self.conn.execute(
            "REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value)
        )
        self.conn.commit()

    def get_setting(self, key: str, default=None):
        cur = self.conn.cursor()
        cur.execute("SELECT value FROM settings WHERE key = ?", (key,))
        row = cur.fetchone()
        return row[0] if row else default

    # === Zarządzanie użytkownikami ===

    def add_user(self, name: str, pin: str):
        """Dodaje nowego użytkownika"""
        self.conn.execute(
            "INSERT INTO users (name, pin, created_date) VALUES (?, ?, ?)",
            (name, pin, datetime.now().isoformat()),
        )
        self.conn.commit()

    def get_all_users(self):
        """Pobiera listę wszystkich użytkowników"""
        cur = self.conn.cursor()
        cur.execute("SELECT id, name, created_date, is_admin FROM users ORDER BY name")
        return cur.fetchall()

    def verify_user_pin(self, user_id: int, pin: str):
        """Sprawdza czy PIN użytkownika jest poprawny"""
        cur = self.conn.cursor()
        cur.execute("SELECT pin FROM users WHERE id = ?", (user_id,))
        row = cur.fetchone()
        return row and row[0] == pin

    def is_admin(self, user_id: int):
        """Sprawdza czy użytkownik jest administratorem"""
        cur = self.conn.cursor()
        cur.execute("SELECT is_admin FROM users WHERE id = ?", (user_id,))
        row = cur.fetchone()
        return row and row[0] == 1

    def update_user_name(self, user_id: int, new_name: str):
        """Aktualizuje nazwę użytkownika"""
        self.conn.execute("UPDATE users SET name = ? WHERE id = ?", (new_name, user_id))
        self.conn.commit()

    def update_user_pin(self, user_id: int, new_pin: str):
        """Aktualizuje PIN użytkownika"""
        self.conn.execute("UPDATE users SET pin = ? WHERE id = ?", (new_pin, user_id))
        self.conn.commit()

    def delete_user(self, user_id: int):
        """Usuwa użytkownika (tylko jeśli nie jest jedynym i nie jest adminem)"""
        cur = self.conn.cursor()

        # Sprawdź czy użytkownik jest adminem
        cur.execute("SELECT is_admin FROM users WHERE id = ?", (user_id,))
        row = cur.fetchone()
        if row and row[0] == 1:
            raise ValueError("Nie można usunąć użytkownika admin")

        cur.execute("SELECT COUNT(*) FROM users")
        count = cur.fetchone()[0]

        if count <= 1:
            raise ValueError("Nie można usunąć ostatniego użytkownika")

        self.conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.conn.commit()

    def get_user_by_id(self, user_id: int):
        """Pobiera dane użytkownika po ID"""
        cur = self.conn.cursor()
        cur.execute("SELECT id, name, created_date FROM users WHERE id = ?", (user_id,))
        return cur.fetchone()
