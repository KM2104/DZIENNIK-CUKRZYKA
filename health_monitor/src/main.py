"""
Health Monitor - Główny plik aplikacji punkt startowy
"""

# Wyłącz multitouch emulation (czerwone kółka przy Ctrl+klik)
from kivy.config import Config

Config.set("input", "mouse", "mouse,multitouch_on_demand")

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from screens.home import HomeScreen
from screens.weight import WeightScreen
from screens.pressure import PressureScreen
from screens.heartrate import HeartRateScreen
from screens.glucose import GlucoseScreen
from screens.settings import SettingsScreen
from screens.login import LoginScreen
from screens.weight_chart import WeightChartScreen
from screens.pressure_chart import PressureChartScreen
from screens.heartrate_chart import HeartRateChartScreen
from screens.glucose_chart import GlucoseChartScreen
from screens.weight_history import WeightHistoryScreen
from screens.pressure_history import PressureHistoryScreen
from screens.heartrate_history import HeartRateHistoryScreen
from screens.glucose_history import GlucoseHistoryScreen


class HealthApp(App):

    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.current = "login"  # aplikacja startuje od PIN
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(WeightScreen(name="weight"))
        sm.add_widget(PressureScreen(name="pressure"))
        sm.add_widget(HeartRateScreen(name="heartrate"))
        sm.add_widget(GlucoseScreen(name="glucose"))
        sm.add_widget(SettingsScreen(name="settings"))
        sm.add_widget(WeightChartScreen(name="weight_chart"))
        sm.add_widget(PressureChartScreen(name="pressure_chart"))
        sm.add_widget(HeartRateChartScreen(name="heartrate_chart"))
        sm.add_widget(GlucoseChartScreen(name="glucose_chart"))
        sm.add_widget(WeightHistoryScreen(name="weight_history"))
        sm.add_widget(PressureHistoryScreen(name="pressure_history"))
        sm.add_widget(HeartRateHistoryScreen(name="heartrate_history"))
        sm.add_widget(GlucoseHistoryScreen(name="glucose_history"))

        return sm


if __name__ == "__main__":
    HealthApp().run()
