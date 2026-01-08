"""
Ekran wykresu glukozy - pełnoekranowy
"""

from kivy.uix.screenmanager import Screen
from db.database import Database
from utils.charts import glucose_chart
from utils.dialogs import show_error


class GlucoseChartScreen(Screen):

    def on_pre_enter(self):
        """Załaduj wykres przed pokazaniem ekranu"""
        self.load_chart()

    def load_chart(self):
        db = Database()
        raw_data = db.get_glucose(limit=30)

        if not raw_data:
            show_error("Brak danych do wykresu")
            return

        # Konwertuj dane do formatu (value, date) dla wykresu
        # Obsługa starych (2 kolumny) i nowych (4 kolumny) rekordów
        data = []
        for row in raw_data:
            if len(row) == 2:
                data.append((row[0], row[1]))
            else:
                data.append((row[0], row[1]))  # value, date

        chart = glucose_chart(data[::-1])  # Odwróć dane (najstarsze pierwsze)
        if chart:
            self.ids.chart_container.clear_widgets()
            self.ids.chart_container.add_widget(chart)
        else:
            show_error("Wykresy niedostępne")
