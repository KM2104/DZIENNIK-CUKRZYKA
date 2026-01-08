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
