"""
Ekran wykresu tętna - pełnoekranowy
"""

from kivy.uix.screenmanager import Screen
from db.database import Database
from utils.charts import heartrate_chart
from utils.dialogs import show_error


class HeartRateChartScreen(Screen):

    def on_pre_enter(self):
        """Załaduj wykres przed pokazaniem ekranu"""
        self.load_chart()

    def load_chart(self):
        db = Database()
        data = db.get_heartrates(limit=30)

        if not data:
            show_error("Brak danych do wykresu")
            return

        chart = heartrate_chart(data[::-1])  # Odwróć dane (najstarsze pierwsze)
        if chart:
            self.ids.chart_container.clear_widgets()
            self.ids.chart_container.add_widget(chart)
        else:
            show_error("Wykresy niedostępne")
