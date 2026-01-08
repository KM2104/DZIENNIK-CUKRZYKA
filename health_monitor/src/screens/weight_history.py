"""
Ekran historii pomiarów wagi
"""

from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty, BooleanProperty
from db.database import Database
from utils.health_rules import weight_alert, AlertLevel


class WeightHistoryScreen(Screen):
    history = ListProperty([])
    ascending = BooleanProperty(False)  # False = od najnowszych

    def on_pre_enter(self):
        """Załaduj historię przed pokazaniem ekranu"""
        self.load_history()

    def load_history(self):
        db = Database()
        records = db.get_weights(limit=1000)

        # Sortuj według preferencji użytkownika
        if self.ascending:
            records = records[::-1]

        self.history = []
        for value, date in records:
            level = weight_alert(value)
            color = {
                AlertLevel.OK: (0.2, 0.8, 0.2, 1),
                AlertLevel.WARNING: (1, 0.6, 0, 1),
                AlertLevel.DANGER: (1, 0.2, 0.2, 1),
            }[level]

            self.history.append({"text": f"{value} kg | {date[:16]}", "color": color})

    def toggle_sort(self):
        """Zmień kierunek sortowania"""
        self.ascending = not self.ascending
        self.load_history()
