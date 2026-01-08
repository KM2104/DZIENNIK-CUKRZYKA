from kivy.uix.popup import Popup
from kivy.uix.label import Label


def show_error(message: str):
    Popup(
        title="Błąd",
        content=Label(text=message),
        size_hint=(0.8, 0.3)
    ).open()


def show_info(message: str):
    Popup(
        title="Informacja",
        content=Label(text=message),
        size_hint=(0.8, 0.3)
    ).open()
