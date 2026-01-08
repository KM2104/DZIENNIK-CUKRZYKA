"""
Modele pomiarów zdrowotnych
"""

from datetime import datetime


class Measurement:
    def __init__(self, value, timestamp=None):
        self.value = value
        self.timestamp = timestamp or datetime.now()

    def __repr__(self):
        return f"Measurement(value={self.value}, timestamp={self.timestamp})"
