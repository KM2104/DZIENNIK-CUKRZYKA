"""
Docstring for health_monitor.src.screens.login
Warstwa ekranu logowania użytkownika
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from db.database import Database
from utils.dialogs import show_error, show_info
from utils.settings import Settings


class LoginScreen(Screen):

    def on_pre_enter(self):
        """Sprawdza czy są użytkownicy w systemie"""
        db = Database()
        users = db.get_all_users()

        # Jeśli brak użytkowników, utwórz pierwszego
        if not users:
            self.ids.user_selector.text = "Tworzenie pierwszego użytkownika"
        else:
            # Pokaż listę użytkowników
            self.refresh_user_selector()

    def refresh_user_selector(self):
        """Odświeża listę użytkowników do wyboru"""
        db = Database()
        users = db.get_all_users()

        if users:
            # Ustaw tekst z nazwą pierwszego użytkownika
            first_user = users[0]
            user_text = f"Użytkownik: {first_user[1]}"

            if len(users) > 1:
                user_text += f" (i {len(users)-1} więcej)"

            self.ids.user_selector.text = user_text

            # Zapisz listę użytkowników jako atrybut
            self.available_users = users
        else:
            self.ids.user_selector.text = "Brak użytkowników"
            self.available_users = []

    def select_user(self):
        """Otwiera dialog wyboru użytkownika"""
        db = Database()
        users = db.get_all_users()

        if not users:
            show_error("Brak użytkowników w systemie")
            return

        content = BoxLayout(orientation="vertical", spacing=10, padding=10)
        content.add_widget(
            Label(text="Wybierz użytkownika:", size_hint_y=None, height=30, bold=True)
        )

        popup = Popup(title="Wybór użytkownika", content=content, size_hint=(0.8, 0.6))

        for user in users:
            # Teraz users zawiera: user_id, name, created_date, is_admin
            if len(user) == 4:
                user_id, name, created, is_admin = user
                admin_badge = " [ADMIN]" if is_admin else ""
            else:
                # Stara wersja danych bez is_admin
                user_id, name, created = user
                admin_badge = ""

            def make_handler(uid, uname):
                def handler(instance):
                    s = Settings()
                    s.set_current_user_id(uid)
                    self.ids.user_selector.text = f"Użytkownik: {uname}"
                    popup.dismiss()
                    show_info(f"Wybrano: {uname}")

                return handler

            btn = Button(
                text=f"{name}{admin_badge}",
                size_hint_y=None,
                height=50,
                background_color=(0.5, 0.7, 0.9, 1),
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

    def check_pin(self, pin_input):
        """Sprawdza PIN użytkownika"""
        db = Database()
        users = db.get_all_users()

        # Jeśli brak użytkowników, utwórz pierwszego
        if not users:
            if len(pin_input) < 4:
                show_error("PIN musi mieć minimum 4 znaki")
                return

            db.add_user("Użytkownik 1", pin_input)
            s = Settings()
            s.set_current_user_id(1)
            show_info("Pierwszy użytkownik utworzony. Zaloguj się ponownie.")
            self.ids.pin.text = ""
            self.refresh_user_selector()
            return

        # Pobierz aktualnie wybranego użytkownika
        s = Settings()
        current_user_id = s.get_current_user_id()

        # Sprawdź PIN
        if db.verify_user_pin(current_user_id, pin_input):
            self.manager.current = "home"
        else:
            show_error("Niepoprawny PIN")
            self.ids.pin.text = ""
