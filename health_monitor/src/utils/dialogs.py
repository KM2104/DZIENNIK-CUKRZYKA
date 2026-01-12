from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.clock import Clock


def show_error(message: str):
    Popup(title="Błąd", content=Label(text=message), size_hint=(0.8, 0.3)).open()


def show_info(message: str):
    """Wyświetla okno informacyjne, które automatycznie zamyka się po 1 sekundzie"""
    popup = Popup(title="Informacja", content=Label(text=message), size_hint=(0.8, 0.3))
    popup.open()

    # Automatyczne zamknięcie po 1 sekundzie
    Clock.schedule_once(lambda dt: popup.dismiss(), 1)
