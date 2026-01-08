"""
Ekran główny aplikacji
"""

from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty
from utils.dialogs import show_info


class HomeScreen(Screen):
    weights = ListProperty([])

    def show_chart(self):
        show_info("Funkcja wykresów w przygotowaniu")
