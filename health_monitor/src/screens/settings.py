"""
Docstring for health_monitor.src.screens.settings
Warstwa ekranu ustawień aplikacji - zarządzanie preferencjami użytkownika
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from utils.settings import Settings
from utils.dialogs import show_info, show_error
from utils.backup import backup_database, restore_database
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class SettingsScreen(Screen):

    def on_pre_enter(self):
        """Ładuje wszystkie ustawienia przy wejściu na ekran"""
        s = Settings()

        # Limity wagi
        w_min, w_max = s.get_weight_limits()
        self.ids.w_min.text = str(w_min)
        self.ids.w_max.text = str(w_max)

        # Limity ciśnienia
        sys_min, dia_min, sys_w, dia_w, sys_d, dia_d = s.get_pressure_limits()
        self.ids.sys_min.text = str(sys_min)
        self.ids.dia_min.text = str(dia_min)
        self.ids.sys_warn.text = str(sys_w)
        self.ids.dia_warn.text = str(dia_w)
        self.ids.sys_danger.text = str(sys_d)
        self.ids.dia_danger.text = str(dia_d)

        # Limity tętna
        hr_min, hr_max, hr_d_low, hr_d_high = s.get_heartrate_limits()
        self.ids.hr_min.text = str(hr_min)
        self.ids.hr_max.text = str(hr_max)
        self.ids.hr_danger_low.text = str(hr_d_low)
        self.ids.hr_danger_high.text = str(hr_d_high)

        # Limity glukozy
        gl_min, gl_max, gl_d_low, gl_d_high = s.get_glucose_limits()
        self.ids.glucose_min.text = str(gl_min)
        self.ids.glucose_max.text = str(gl_max)
        self.ids.glucose_danger_low.text = str(gl_d_low)
        self.ids.glucose_danger_high.text = str(gl_d_high)

        # Załaduj listę użytkowników
        self.refresh_user_list()

    def save_limits(self):
        """Zapisuje wszystkie limity parametrów zdrowotnych"""
        try:
            s = Settings()

            # Zapisz limity wagi
            s.set_weight_limits(float(self.ids.w_min.text), float(self.ids.w_max.text))

            # Zapisz limity ciśnienia
            s.set_pressure_limits(
                int(self.ids.sys_min.text),
                int(self.ids.dia_min.text),
                int(self.ids.sys_warn.text),
                int(self.ids.dia_warn.text),
                int(self.ids.sys_danger.text),
                int(self.ids.dia_danger.text),
            )

            # Zapisz limity tętna
            s.set_heartrate_limits(
                int(self.ids.hr_min.text),
                int(self.ids.hr_max.text),
                int(self.ids.hr_danger_low.text),
                int(self.ids.hr_danger_high.text),
            )

            # Zapisz limity glukozy
            s.set_glucose_limits(
                int(self.ids.glucose_min.text),
                int(self.ids.glucose_max.text),
                int(self.ids.glucose_danger_low.text),
                int(self.ids.glucose_danger_high.text),
            )

            show_info("Wszystkie ustawienia zapisane")
        except ValueError as e:
            show_error(f"Błąd: Wprowadź poprawne wartości liczbowe")
        except Exception as e:
            show_error(f"Błąd zapisu: {str(e)}")

    def change_pin(self):
        """Otwiera dialog zmiany PIN"""
        content = BoxLayout(orientation="vertical", spacing=10, padding=10)

        old_pin_input = TextInput(
            hint_text="Stary PIN",
            password=True,
            multiline=False,
            size_hint_y=None,
            height=40,
        )
        new_pin_input = TextInput(
            hint_text="Nowy PIN",
            password=True,
            multiline=False,
            size_hint_y=None,
            height=40,
        )
        confirm_pin_input = TextInput(
            hint_text="Potwierdź nowy PIN",
            password=True,
            multiline=False,
            size_hint_y=None,
            height=40,
        )

        content.add_widget(
            Label(text="Zmiana PIN", size_hint_y=None, height=30, bold=True)
        )
        content.add_widget(old_pin_input)
        content.add_widget(new_pin_input)
        content.add_widget(confirm_pin_input)

        btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)

        popup = Popup(title="Zmiana PIN", content=content, size_hint=(0.8, 0.5))

        def confirm_change(instance):
            if new_pin_input.text != confirm_pin_input.text:
                show_error("Nowe PIN się nie zgadzają")
                return

            if len(new_pin_input.text) < 4:
                show_error("PIN musi mieć minimum 4 znaki")
                return

            s = Settings()
            user_id = s.get_current_user_id()

            if s.change_user_pin(user_id, old_pin_input.text, new_pin_input.text):
                show_info("PIN zmieniony pomyślnie")
                popup.dismiss()
            else:
                show_error("Niepoprawny stary PIN")

        btn_ok = Button(
            text="Zmień", on_press=confirm_change, background_color=(0.4, 0.8, 0.6, 1)
        )
        btn_cancel = Button(
            text="Anuluj", on_press=popup.dismiss, background_color=(0.8, 0.4, 0.4, 1)
        )

        btn_layout.add_widget(btn_ok)
        btn_layout.add_widget(btn_cancel)
        content.add_widget(btn_layout)

        popup.open()

    def add_new_user(self):
        """Otwiera dialog dodawania nowego użytkownika"""
        content = BoxLayout(orientation="vertical", spacing=10, padding=10)

        name_input = TextInput(
            hint_text="Imię użytkownika", multiline=False, size_hint_y=None, height=40
        )
        pin_input = TextInput(
            hint_text="PIN (min. 4 znaki)",
            password=True,
            multiline=False,
            size_hint_y=None,
            height=40,
        )
        confirm_pin_input = TextInput(
            hint_text="Potwierdź PIN",
            password=True,
            multiline=False,
            size_hint_y=None,
            height=40,
        )

        content.add_widget(
            Label(
                text="Dodaj nowego użytkownika", size_hint_y=None, height=30, bold=True
            )
        )
        content.add_widget(name_input)
        content.add_widget(pin_input)
        content.add_widget(confirm_pin_input)

        btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)

        popup = Popup(title="Nowy użytkownik", content=content, size_hint=(0.8, 0.5))

        def confirm_add(instance):
            if not name_input.text.strip():
                show_error("Wprowadź imię użytkownika")
                return

            if pin_input.text != confirm_pin_input.text:
                show_error("PIN się nie zgadzają")
                return

            if len(pin_input.text) < 4:
                show_error("PIN musi mieć minimum 4 znaki")
                return

            try:
                s = Settings()
                s.add_user(name_input.text.strip(), pin_input.text)
                show_info(f"Użytkownik {name_input.text} dodany")
                self.refresh_user_list()
                popup.dismiss()
            except Exception as e:
                show_error(f"Błąd: {str(e)}")

        btn_ok = Button(
            text="Dodaj", on_press=confirm_add, background_color=(0.4, 0.8, 0.6, 1)
        )
        btn_cancel = Button(
            text="Anuluj", on_press=popup.dismiss, background_color=(0.8, 0.4, 0.4, 1)
        )

        btn_layout.add_widget(btn_ok)
        btn_layout.add_widget(btn_cancel)
        content.add_widget(btn_layout)

        popup.open()

    def refresh_user_list(self):
        """Odświeża listę użytkowników"""
        s = Settings()
        users = s.get_all_users()

        user_list_text = "Użytkownicy:\n\n"
        for user in users:
            user_id, name, created = user
            user_list_text += f"• {name} (ID: {user_id})\n"

        if hasattr(self.ids, "user_list"):
            self.ids.user_list.text = user_list_text

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
