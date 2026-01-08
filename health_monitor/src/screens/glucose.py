"""
Ekran pomiaru glukozy
"""

from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty, StringProperty
from db.database import Database
from utils.validators import validate_glucose, ValidationError
from utils.dialogs import show_error, show_info
from utils.health_rules import glucose_alert, AlertLevel
from utils.export_csv import export_glucose_csv
from utils.export_pdf import export_glucose_pdf
from utils.paths import get_export_path
from datetime import datetime


class GlucoseScreen(Screen):
    glucose_levels = ListProperty([])
    meal_timing = StringProperty("na czczo")

    def on_pre_enter(self):
        self.load_glucose()
        # Ustaw domyślną datę/czas
        now = datetime.now()
        self.ids.measurement_date.text = now.strftime("%Y-%m-%d")
        self.ids.measurement_time.text = now.strftime("%H:%M")

    def load_glucose(self):
        db = Database()
        records = db.get_glucose()
        self.glucose_levels = []

        for row in records:
            # Obsługa starych i nowych rekordów
            if len(row) == 2:
                value, date = row
                meal_timing = ""
            else:
                value, date, measurement_time, meal_timing = row

            level = glucose_alert(value)
            color = {
                AlertLevel.OK: (1, 1, 1, 1),
                AlertLevel.WARNING: (1, 0.6, 0, 1),
                AlertLevel.DANGER: (1, 0, 0, 1),
            }[level]

            # Wyświetl wartość, czas od posiłku i datę
            timing_text = f" [{meal_timing}]" if meal_timing else ""
            self.glucose_levels.append(
                {"text": f"{value} mg/dL{timing_text}  |  {date[:16]}", "color": color}
            )

    def save_glucose(self, value, date_str, time_str, custom_timing):
        try:
            glucose = validate_glucose(value)

            # Złóż datę i czas w jeden timestamp
            try:
                measurement_datetime = f"{date_str} {time_str}"
                datetime.strptime(measurement_datetime, "%Y-%m-%d %H:%M")  # Walidacja
            except ValueError:
                raise ValidationError("Nieprawidłowy format daty lub czasu")

            # Określ timing od posiłku
            if self.meal_timing == "własny":
                timing = custom_timing if custom_timing else "nie podano"
            else:
                timing = self.meal_timing

            db = Database()
            db.add_glucose(glucose, measurement_datetime, timing)
            self.load_glucose()
            show_info("Glukoza zapisana")
        except ValidationError as e:
            show_error(str(e))

    def set_meal_timing(self, value):
        """Ustawia czas względem posiłku"""
        self.meal_timing = value

    def show_chart(self):
        self.manager.current = "glucose_chart"

    def export_csv(self):
        try:
            db = Database()
            records = db.get_glucose()
            path = get_export_path("glucose.csv")
            export_glucose_csv(records, path)
            show_info(f"Wyeksportowano do:\n{path}")
        except Exception as e:
            show_error(f"Błąd eksportu: {str(e)}")

    def export_pdf(self):
        try:
            db = Database()
            records = db.get_glucose()
            path = get_export_path("glucose.pdf")
            export_glucose_pdf(records, path)
            show_info(f"Wyeksportowano do:\n{path}")
        except Exception as e:
            show_error(f"Błąd eksportu: {str(e)}")
