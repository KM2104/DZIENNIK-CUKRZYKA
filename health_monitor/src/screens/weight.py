"""
Ekran pomiaru wagi
"""

from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty
from db.database import Database
from utils.validators import validate_weight, ValidationError
from utils.dialogs import show_error, show_info
from utils.health_rules import weight_alert, AlertLevel
from utils.alerts import show_health_alert
from utils.export_csv import export_weights_csv
from utils.export_pdf import export_weights_pdf
from utils.paths import get_export_path


class WeightScreen(Screen):
    weights = ListProperty([])

    def on_pre_enter(self):
        self.load_weights()

    def load_weights(self):
        db = Database()
        records = db.get_weights()
        self.weights = []

        for value, date in records:
            level = weight_alert(value)
            color = {
                AlertLevel.OK: (1, 1, 1, 1),
                AlertLevel.WARNING: (1, 0.6, 0, 1),
                AlertLevel.DANGER: (1, 0, 0, 1),
            }[level]

            self.weights.append({"text": f"{value} kg  |  {date[:16]}", "color": color})

    def save_weight(self, value):
        try:
            weight = validate_weight(value)
            db = Database()
            db.add_weight(weight)
            self.load_weights()
            show_info("Waga zapisana")
        except ValidationError as e:
            show_error(str(e))

    def show_chart(self):
        """Przekieruj na ekran wykresu"""
        from kivy.app import App

        App.get_running_app().root.current = "weight_chart"

    def export_csv(self):
        db = Database()
        data = db.get_weights(limit=1000)
        path = get_export_path("waga.csv")
        export_weights_csv(data, path)
        show_info(f"Zapisano CSV:\n{path}")

    def export_pdf(self):
        db = Database()
        data = db.get_weights(limit=1000)
        path = get_export_path("waga.pdf")
        export_weights_pdf(data, path)
        show_info(f"Zapisano PDF:\n{path}")
