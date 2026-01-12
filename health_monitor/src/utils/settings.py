"""
Docstring for health_monitor.src.utils.settings
Warstwa ustawień aplikacji - zarządzanie preferencjami użytkownika
"""

from db.database import Database


class Settings:
    def __init__(self):
        self.db = Database()

    # === Limity Wagi ===
    def get_weight_limits(self):
        return (
            float(self.db.get_setting("weight_min", 50)),
            float(self.db.get_setting("weight_max", 150)),
        )

    def set_weight_limits(self, min_v, max_v):
        self.db.set_setting("weight_min", str(min_v))
        self.db.set_setting("weight_max", str(max_v))

    # === Limity Ciśnienia ===
    def get_pressure_limits(self):
        return (
            int(self.db.get_setting("sys_min", 90)),
            int(self.db.get_setting("dia_min", 60)),
            int(self.db.get_setting("sys_warn", 140)),
            int(self.db.get_setting("dia_warn", 90)),
            int(self.db.get_setting("sys_danger", 180)),
            int(self.db.get_setting("dia_danger", 120)),
        )

    def set_pressure_limits(self, sys_min, dia_min, sys_w, dia_w, sys_d, dia_d):
        self.db.set_setting("sys_min", str(sys_min))
        self.db.set_setting("dia_min", str(dia_min))
        self.db.set_setting("sys_warn", str(sys_w))
        self.db.set_setting("dia_warn", str(dia_w))
        self.db.set_setting("sys_danger", str(sys_d))
        self.db.set_setting("dia_danger", str(dia_d))

    # === Limity Tętna ===
    def get_heartrate_limits(self):
        return (
            int(self.db.get_setting("hr_min", 60)),
            int(self.db.get_setting("hr_max", 100)),
            int(self.db.get_setting("hr_danger_low", 40)),
            int(self.db.get_setting("hr_danger_high", 150)),
        )

    def set_heartrate_limits(self, min_v, max_v, danger_low, danger_high):
        self.db.set_setting("hr_min", str(min_v))
        self.db.set_setting("hr_max", str(max_v))
        self.db.set_setting("hr_danger_low", str(danger_low))
        self.db.set_setting("hr_danger_high", str(danger_high))

    # === Limity Glukozy ===
    def get_glucose_limits(self):
        return (
            int(self.db.get_setting("glucose_min", 70)),
            int(self.db.get_setting("glucose_max", 140)),
            int(self.db.get_setting("glucose_danger_low", 50)),
            int(self.db.get_setting("glucose_danger_high", 250)),
        )

    def set_glucose_limits(self, min_v, max_v, danger_low, danger_high):
        self.db.set_setting("glucose_min", str(min_v))
        self.db.set_setting("glucose_max", str(max_v))
        self.db.set_setting("glucose_danger_low", str(danger_low))
        self.db.set_setting("glucose_danger_high", str(danger_high))

    # === Zarządzanie użytkownikami ===
    def get_all_users(self):
        """Pobiera listę wszystkich użytkowników"""
        return self.db.get_all_users()

    def add_user(self, name: str, pin: str):
        """Dodaje nowego użytkownika"""
        self.db.add_user(name, pin)

    def delete_user(self, user_id: int):
        """Usuwa użytkownika"""
        self.db.delete_user(user_id)

    def is_admin(self, user_id: int):
        """Sprawdza czy użytkownik jest administratorem"""
        return self.db.is_admin(user_id)

    def update_user_name(self, user_id: int, new_name: str):
        """Aktualizuje nazwę użytkownika"""
        self.db.update_user_name(user_id, new_name)

    def change_user_pin(self, user_id: int, old_pin: str, new_pin: str):
        """Zmienia PIN użytkownika po weryfikacji starego PIN"""
        if self.db.verify_user_pin(user_id, old_pin):
            self.db.update_user_pin(user_id, new_pin)
            return True
        return False

    def get_current_user_id(self):
        """Pobiera ID aktualnie zalogowanego użytkownika"""
        user_id = self.db.get_setting("current_user_id")
        return int(user_id) if user_id else 1

    def set_current_user_id(self, user_id: int):
        """Ustawia aktualnie zalogowanego użytkownika"""
        self.db.set_setting("current_user_id", str(user_id))
