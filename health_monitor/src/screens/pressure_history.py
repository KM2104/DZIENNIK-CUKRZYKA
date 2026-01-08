"""
Ekran historii pomiarów ciśnienia
"""

from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty, BooleanProperty
from db.database import Database
from utils.health_rules import pressure_alert, AlertLevel


class PressureHistoryScreen(Screen):
    history = ListProperty([])
    ascending = BooleanProperty(False)  # False = od najnowszych

    def on_pre_enter(self):
        """Załaduj historię przed pokazaniem ekranu"""
        self.load_history()

    def load_history(self):
        db = Database()
        records = db.get_pressures(limit=1000)

        total = len(records)

        # Sortuj według preferencji użytkownika
        if self.ascending:
            records = records[::-1]

        self.history = []
        for idx, (sys, dia, date) in enumerate(records):
            level = pressure_alert(sys, dia)
            color = {
                AlertLevel.OK: (0.2, 0.8, 0.2, 1),
                AlertLevel.WARNING: (1, 0.6, 0, 1),
                AlertLevel.DANGER: (1, 0.2, 0.2, 1),
            }[level]

            # Numer pomiaru (0 = najstarszy, jak na wykresie)
            if self.ascending:
                # Jeśli od najstarszych, idx odpowiada numerowi na wykresie
                chart_num = idx
            else:
                # Jeśli od najnowszych, odwróć numerację
                chart_num = total - idx - 1

            self.history.append(
                {
                    "text": f"#{chart_num}: {sys}/{dia} mmHg | {date[:16]}",
                    "color": color,
                }
            )

    def toggle_sort(self):
        """Zmień kierunek sortowania"""
        self.ascending = not self.ascending
        self.load_history()
