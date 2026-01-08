"""
Docstring for health_monitor.src.screens.settings
Warstwa ekranu ustawień aplikacji - zarządzanie preferencjami użytkownika
"""

from kivy.uix.screenmanager import Screen
from utils.settings import Settings
from utils.dialogs import show_info
from utils.backup import backup_database, restore_database
from utils.dialogs import show_error, show_info


class SettingsScreen(Screen):

    def on_pre_enter(self):
        s = Settings()
        w_min, w_max = s.get_weight_limits()
        self.ids.w_min.text = str(w_min)
        self.ids.w_max.text = str(w_max)

    def save(self):
        s = Settings()
        s.set_weight_limits(float(self.ids.w_min.text), float(self.ids.w_max.text))
        show_info("Ustawienia zapisane")

    def backup(self):
        try:
            path = backup_database()
            show_info(f"Backup zapisany:\n{path}")
        except Exception as e:
            show_error(str(e))

    def restore(self):
        # na start zakładamy stałą nazwę
        path = "/sdcard/HealthMonitor/health_backup_last.db"
        try:
            restore_database(path)
            show_info("Backup przywrócony")
        except Exception as e:
            show_error(str(e))
