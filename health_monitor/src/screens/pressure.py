"""
Ekran pomiaru ciśnienia
"""

from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty
from db.database import Database
from utils.validators import validate_pressure, ValidationError
from utils.dialogs import show_error, show_info
from utils.charts import pressure_chart
from utils.health_rules import pressure_alert
from utils.alerts import show_health_alert
from utils.export_csv import export_pressure_csv
from utils.export_pdf import export_pressure_pdf
from utils.paths import get_export_path


class PressureScreen(Screen):
    pressures = ListProperty([])

    def on_pre_enter(self):
        self.load_pressures()

    def load_pressures(self):
        db = Database()
        records = db.get_pressures()
        self.pressures = [
            {"text": f"{s}/{d} mmHg  |  {date[:16]}"} for s, d, date in records
        ]

    def save_pressure(self, sys, dia):
        try:
            systolic, diastolic = validate_pressure(sys, dia)
            db = Database()
            db.add_pressure(systolic, diastolic)
            self.load_pressures()
            show_info("Ciśnienie zapisane")
        except ValidationError as e:
            show_error(str(e))

    def show_chart(self):
        """Przekieruj na ekran wykresu"""
        from kivy.app import App

        App.get_running_app().root.current = "pressure_chart"

    def save_pressure(self, sys, dia):
        try:
            systolic, diastolic = validate_pressure(sys, dia)
            db = Database()
            db.add_pressure(systolic, diastolic)

            level = pressure_alert(systolic, diastolic)
            show_health_alert(level)

            self.load_pressures()
            show_info("Ciśnienie zapisane")

        except ValidationError as e:
            show_error(str(e))

    def export_csv(self):
        db = Database()
        data = db.get_pressures(limit=1000)
        path = get_export_path("cisnienie.csv")
        export_pressure_csv(data, path)
        show_info(f"Zapisano CSV:\n{path}")

    def export_pdf(self):
        db = Database()
        data = db.get_pressures(limit=1000)
        path = get_export_path("cisnienie.pdf")
        export_pressure_pdf(data, path)
        show_info(f"Zapisano PDF:\n{path}")
