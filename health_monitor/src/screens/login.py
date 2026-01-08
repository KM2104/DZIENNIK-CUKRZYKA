"""
Docstring for health_monitor.src.screens.login
Warstwa ekranu logowania użytkownika
"""

from kivy.uix.screenmanager import Screen
from db.database import Database
from utils.dialogs import show_error, show_info

class LoginScreen(Screen):

    def check_pin(self, pin_input):
        db = Database()
        saved_pin = db.get_setting("user_pin", "")
        if not saved_pin:
            # jeśli PIN nie ustawiony – ustawiamy pierwszy raz
            db.set_setting("user_pin", pin_input)
            show_info("PIN zapisany. Zaloguj się ponownie.")
            self.ids.pin.text = ""
            return
        if pin_input == saved_pin:
            self.manager.current = "home"
        else:
            show_error("Niepoprawny PIN")
