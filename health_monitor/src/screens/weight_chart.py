"""
Ekran wykresu wagi - pełnoekranowy
"""

from kivy.uix.screenmanager import Screen
from db.database import Database
from utils.charts import weight_chart
from utils.dialogs import show_error


class WeightChartScreen(Screen):

    def on_pre_enter(self):
        """Załaduj wykres przed pokazaniem ekranu"""
        self.load_chart()

    def load_chart(self):
        db = Database()
        data = db.get_weights(limit=30)

        if not data:
            show_error("Brak danych do wykresu")
            return

        chart = weight_chart(data[::-1])  # Odwróć dane (najstarsze pierwsze)
        if chart:
            self.ids.chart_container.clear_widgets()
            self.ids.chart_container.add_widget(chart)
        else:
            show_error("Wykresy niedostępne")
