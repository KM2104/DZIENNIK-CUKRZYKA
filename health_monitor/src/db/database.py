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

        self.conn.commit()

        # Migracja: Dodaj brakujące kolumny do istniejącej tabeli glucose
        self._migrate_glucose_table()

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
