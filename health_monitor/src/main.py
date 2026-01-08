"""
Health Monitor - Główny plik aplikacji punkt startowy
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

from screens.home import HomeScreen
from screens.weight import WeightScreen
from screens.pressure import PressureScreen
from screens.settings import SettingsScreen
from screens.login import LoginScreen


class HealthApp(App):

    def build(self):
        Builder.load_file("health.kv")

        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.current = "login"  # aplikacja startuje od PIN
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(WeightScreen(name="weight"))
        sm.add_widget(PressureScreen(name="pressure"))
        sm.add_widget(SettingsScreen(name="settings"))


        return sm


if __name__ == "__main__":
    HealthApp().run()

