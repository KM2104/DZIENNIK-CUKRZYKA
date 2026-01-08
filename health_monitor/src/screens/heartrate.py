"""
Ekran pomiaru tętna
"""

from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty
from db.database import Database
from utils.validators import validate_heartrate, ValidationError
from utils.dialogs import show_error, show_info
from utils.health_rules import heartrate_alert, AlertLevel
from utils.export_csv import export_heartrate_csv
from utils.export_pdf import export_heartrate_pdf
from utils.paths import get_export_path


class HeartRateScreen(Screen):
    heartrates = ListProperty([])

    def on_pre_enter(self):
        self.load_heartrates()

    def load_heartrates(self):
        db = Database()
        records = db.get_heartrates()
        self.heartrates = []

        for value, date in records:
            level = heartrate_alert(value)
            color = {
                AlertLevel.OK: (1, 1, 1, 1),
                AlertLevel.WARNING: (1, 0.6, 0, 1),
                AlertLevel.DANGER: (1, 0, 0, 1),
            }[level]

            self.heartrates.append(
                {"text": f"{value} bpm  |  {date[:16]}", "color": color}
            )

    def save_heartrate(self, value):
        try:
            heartrate = validate_heartrate(value)
            db = Database()
            db.add_heartrate(heartrate)
            self.load_heartrates()
            show_info("Tętno zapisane")
        except ValidationError as e:
            show_error(str(e))

    def show_chart(self):
        self.manager.current = "heartrate_chart"

    def export_csv(self):
        try:
            db = Database()
            records = db.get_heartrates()
            path = get_export_path("heartrate.csv")
            export_heartrate_csv(records, path)
            show_info(f"Wyeksportowano do:\n{path}")
        except Exception as e:
            show_error(f"Błąd eksportu: {str(e)}")

    def export_pdf(self):
        try:
            db = Database()
            records = db.get_heartrates()
            path = get_export_path("heartrate.pdf")
            export_heartrate_pdf(records, path)
            show_info(f"Wyeksportowano do:\n{path}")
        except Exception as e:
            show_error(f"Błąd eksportu: {str(e)}")
