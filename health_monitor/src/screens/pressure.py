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




class PressureScreen(Screen):
    pressures = ListProperty([])

    def on_pre_enter(self):
        self.load_pressures()

    def load_pressures(self):
        db = Database()
        records = db.get_pressures()
        self.pressures = [
            {"text": f"{s}/{d} mmHg  |  {date[:16]}"}
            for s, d, date in records
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
        db = Database()
        data = db.get_pressures(limit=30)

        if not data:
            show_error("Brak danych do wykresu")
            return

        chart = pressure_chart(data[::-1])
        self.ids.chart_box.clear_widgets()
        self.ids.chart_box.add_widget(chart)


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

