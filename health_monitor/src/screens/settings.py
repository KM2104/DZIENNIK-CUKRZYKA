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
from utils.export_csv import (
    export_weights_csv,
    export_pressure_csv,
    export_heartrate_csv,
    export_glucose_csv,
)
from utils.paths import get_export_dir
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from db.database import Database
from datetime import datetime
import os


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

    def change_username(self):
        """Otwiera dialog zmiany nazwy użytkownika"""
        content = BoxLayout(orientation="vertical", spacing=10, padding=10)

        new_name_input = TextInput(
            hint_text="Nowa nazwa użytkownika",
            multiline=False,
            size_hint_y=None,
            height=40,
        )

        content.add_widget(
            Label(
                text="Zmiana nazwy użytkownika", size_hint_y=None, height=30, bold=True
            )
        )
        content.add_widget(new_name_input)

        btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)

        popup = Popup(title="Zmiana nazwy", content=content, size_hint=(0.8, 0.4))

        def confirm_change(instance):
            if not new_name_input.text.strip():
                show_error("Wprowadź nową nazwę użytkownika")
                return

            s = Settings()
            user_id = s.get_current_user_id()

            try:
                s.update_user_name(user_id, new_name_input.text.strip())
                show_info("Nazwa użytkownika zmieniona pomyślnie")
                self.refresh_user_list()
                popup.dismiss()
            except Exception as e:
                show_error(f"Błąd: {str(e)}")

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
            # Teraz users zawiera: user_id, name, created_date, is_admin
            if len(user) == 4:
                user_id, name, created, is_admin = user
                admin_badge = " [ADMIN]" if is_admin else ""
                user_list_text += f"• {name}{admin_badge} (ID: {user_id})\n"
            else:
                # Stara wersja danych bez is_admin
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

    def delete_user_dialog(self):
        """Otwiera dialog wyboru użytkownika do usunięcia z opcją zapisu danych"""
        s = Settings()
        db = Database()
        users = s.get_all_users()
        current_user_id = s.get_current_user_id()

        if not users or len(users) <= 1:
            show_error("Nie można usunąć jedynego użytkownika w systemie")
            return

        content = BoxLayout(orientation="vertical", spacing=10, padding=10)
        content.add_widget(
            Label(
                text="Wybierz użytkownika do usunięcia:",
                size_hint_y=None,
                height=40,
                bold=True,
            )
        )

        popup = Popup(
            title="Usuwanie użytkownika", content=content, size_hint=(0.9, 0.7)
        )

        for user in users:
            if len(user) == 4:
                user_id, name, created, is_admin = user
                admin_badge = " [ADMIN]" if is_admin else ""
            else:
                user_id, name, created = user
                admin_badge = ""
                is_admin = 0

            # Nie pozwalaj usuwać admina
            if is_admin:
                continue

            def make_handler(uid, uname):
                def handler(instance):
                    popup.dismiss()
                    self.confirm_delete_user(uid, uname)

                return handler

            btn = Button(
                text=f"{name}{admin_badge} (ID: {user_id})",
                size_hint_y=None,
                height=50,
                background_color=(0.9, 0.5, 0.5, 1),
            )
            btn.bind(on_press=make_handler(user_id, name))
            content.add_widget(btn)

        btn_cancel = Button(
            text="Anuluj",
            size_hint_y=None,
            height=50,
            background_color=(0.7, 0.7, 0.7, 1),
            on_press=popup.dismiss,
        )
        content.add_widget(btn_cancel)

        popup.open()

    def confirm_delete_user(self, user_id, user_name):
        """Potwierdza usunięcie użytkownika i oferuje eksport danych"""
        content = BoxLayout(orientation="vertical", spacing=10, padding=10)

        content.add_widget(
            Label(
                text=f"Czy na pewno chcesz usunąć użytkownika:\n{user_name}?",
                size_hint_y=None,
                height=60,
                bold=True,
            )
        )

        content.add_widget(
            Label(
                text="Przed usunięciem możesz zapisać jego wyniki do pliku CSV.",
                size_hint_y=None,
                height=40,
                color=(0.7, 0.4, 0, 1),
            )
        )

        btn_layout = BoxLayout(
            orientation="vertical", spacing=5, size_hint_y=None, height=160
        )

        popup = Popup(
            title=f"Usuwanie: {user_name}", content=content, size_hint=(0.9, 0.6)
        )

        def export_and_delete(instance):
            """Eksportuje dane użytkownika i usuwa go"""
            try:
                self.export_user_data(user_id, user_name)
                self.delete_user_confirmed(user_id, user_name)
                popup.dismiss()
            except Exception as e:
                show_error(f"Błąd podczas eksportu: {str(e)}")

        def delete_without_export(instance):
            """Usuwa użytkownika bez eksportu"""
            self.delete_user_confirmed(user_id, user_name)
            popup.dismiss()

        btn_export = Button(
            text="💾 Zapisz dane i usuń użytkownika",
            background_color=(0.4, 0.7, 0.9, 1),
            size_hint_y=None,
            height=50,
            on_press=export_and_delete,
        )

        btn_delete = Button(
            text="🗑️ Usuń bez zapisu",
            background_color=(0.9, 0.4, 0.4, 1),
            size_hint_y=None,
            height=50,
            on_press=delete_without_export,
        )

        btn_cancel = Button(
            text="Anuluj",
            background_color=(0.7, 0.7, 0.7, 1),
            size_hint_y=None,
            height=50,
            on_press=popup.dismiss,
        )

        btn_layout.add_widget(btn_export)
        btn_layout.add_widget(btn_delete)
        btn_layout.add_widget(btn_cancel)
        content.add_widget(btn_layout)

        popup.open()

    def export_user_data(self, user_id, user_name):
        """Eksportuje wszystkie dane użytkownika do plików CSV"""
        db = Database()
        export_dir = get_export_dir()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Pobierz wszystkie pomiary użytkownika
        weights = db.get_weights(limit=10000)
        pressures = db.get_pressures(limit=10000)
        heartrates = db.get_heartrates(limit=10000)
        glucoses = db.get_glucose(limit=10000)

        # Eksportuj do CSV
        base_filename = f"{user_name}_{timestamp}"

        if weights:
            filepath = os.path.join(export_dir, f"{base_filename}_waga.csv")
            export_weights_csv(weights, filepath)

        if pressures:
            filepath = os.path.join(export_dir, f"{base_filename}_cisnienie.csv")
            export_pressure_csv(pressures, filepath)

        if heartrates:
            filepath = os.path.join(export_dir, f"{base_filename}_tetno.csv")
            export_heartrate_csv(heartrates, filepath)

        if glucoses:
            filepath = os.path.join(export_dir, f"{base_filename}_glukoza.csv")
            export_glucose_csv(glucoses, filepath)

        show_info(f"Dane użytkownika {user_name} zapisane w:\n{export_dir}")

    def delete_user_confirmed(self, user_id, user_name):
        """Usuwa użytkownika po potwierdzeniu"""
        try:
            s = Settings()
            s.delete_user(user_id)
            show_info(f"Użytkownik {user_name} został usunięty")
            self.refresh_user_list()
        except Exception as e:
            show_error(f"Błąd usuwania: {str(e)}")
