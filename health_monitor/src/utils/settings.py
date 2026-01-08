"""
Docstring for health_monitor.src.utils.settings
Warstwa ustawień aplikacji - zarządzanie preferencjami użytkownika
"""

from db.database import Database


class Settings:
    def __init__(self):
        self.db = Database()

    def get_weight_limits(self):
        return (
            float(self.db.get_setting("weight_min", 50)),
            float(self.db.get_setting("weight_max", 150))
        )

    def set_weight_limits(self, min_v, max_v):
        self.db.set_setting("weight_min", str(min_v))
        self.db.set_setting("weight_max", str(max_v))

    def get_pressure_limits(self):
        return (
            int(self.db.get_setting("sys_warn", 140)),
            int(self.db.get_setting("dia_warn", 90)),
            int(self.db.get_setting("sys_danger", 180)),
            int(self.db.get_setting("dia_danger", 120))
        )

    def set_pressure_limits(self, sys_w, dia_w, sys_d, dia_d):
        self.db.set_setting("sys_warn", str(sys_w))
        self.db.set_setting("dia_warn", str(dia_w))
        self.db.set_setting("sys_danger", str(sys_d))
        self.db.set_setting("dia_danger", str(dia_d))
