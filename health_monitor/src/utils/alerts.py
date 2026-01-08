"""
Docstring for health_monitor.src.utils.alerts
Warstwa alertów zdrowotnych - kolorowanie i komunikaty  
"""

from kivy.uix.popup import Popup
from kivy.uix.label import Label
from utils.health_rules import AlertLevel


def show_health_alert(level: AlertLevel):
    if level == AlertLevel.OK:
        return

    title = "Alert zdrowotny"
    message = {
        AlertLevel.WARNING: "Wynik poza normą",
        AlertLevel.DANGER: "Wynik niebezpieczny – skonsultuj się z lekarzem"
    }[level]

    Popup(
        title=title,
        content=Label(text=message),
        size_hint=(0.8, 0.3)
    ).open()
