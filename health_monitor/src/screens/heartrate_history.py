"""
Ekran historii pomiarów tętna
"""

from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty, BooleanProperty
from db.database import Database
from utils.health_rules import heartrate_alert, AlertLevel


class HeartRateHistoryScreen(Screen):
    history = ListProperty([])
    ascending = BooleanProperty(False)  # False = od najnowszych

    def on_pre_enter(self):
        """Załaduj historię przed pokazaniem ekranu"""
        self.load_history()

    def load_history(self):
        db = Database()
        records = db.get_heartrates(limit=1000)

        total = len(records)

        # Sortuj według preferencji użytkownika
        if self.ascending:
            records = records[::-1]

        self.history = []
        for idx, (value, date) in enumerate(records):
            level = heartrate_alert(value)
            color = {
                AlertLevel.OK: (0, 0, 0, 1),  # Czarny - norma
                AlertLevel.WARNING_LOW: (0, 0, 1, 1),  # Niebieski - poniżej normy
                AlertLevel.WARNING_HIGH: (1, 0, 0, 1),  # Czerwony - ponad normę
                AlertLevel.DANGER_LOW: (
                    0,
                    0,
                    0.8,
                    1,
                ),  # Ciemnoniebieski - niebezpiecznie niskie
                AlertLevel.DANGER_HIGH: (
                    0.8,
                    0,
                    0,
                    1,
                ),  # Ciemnoczerwony - niebezpiecznie wysokie
            }.get(
                level, (0, 0, 0, 1)
            )  # Domyślnie czarny

            # Numer pomiaru (0 = najstarszy, jak na wykresie)
            if self.ascending:
                # Jeśli od najstarszych, idx odpowiada numerowi na wykresie
                chart_num = idx
            else:
                # Jeśli od najnowszych, odwróć numerację
                chart_num = total - idx - 1

            self.history.append(
                {"text": f"#{chart_num}: {value} bpm | {date[:16]}", "color": color}
            )

    def toggle_sort(self):
        """Zmień kierunek sortowania"""
        self.ascending = not self.ascending
        self.load_history()
