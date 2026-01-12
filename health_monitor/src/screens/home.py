"""
Ekran główny aplikacji
"""

from kivy.uix.screenmanager import Screen
from utils.settings import Settings
from utils.dialogs import show_error


class HomeScreen(Screen):

    def go_to_settings(self):
        """Przejdź do ustawień tylko jeśli użytkownik jest adminem"""
        s = Settings()
        user_id = s.get_current_user_id()

        if s.is_admin(user_id):
            self.manager.current = "settings"
        else:
            show_error("Tylko administrator ma dostęp do ustawień")
