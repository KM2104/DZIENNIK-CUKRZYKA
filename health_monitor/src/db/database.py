"""
Zarządzanie bazą danych
"""

from datetime import datetime
from utils.paths import get_db_path

# Próba użycia pysqlcipher3 (szyfrowanie), fallback do sqlite3
try:
    from pysqlcipher3 import dbapi2 as sqlite3

    USE_ENCRYPTION = True
except ImportError:
    import sqlite3

    USE_ENCRYPTION = False
    print("Uwaga: Używam sqlite3 bez szyfrowania (pysqlcipher3 niedostępny)")


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(get_db_path())
        if USE_ENCRYPTION:
            self.conn.execute("PRAGMA key='twoj_super_tajny_klucz'")
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
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """
        )

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
