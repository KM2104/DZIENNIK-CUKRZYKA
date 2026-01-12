"""
Skrypt do usunięcia nadmiarowych użytkowników z bazy danych
Zachowuje tylko admin (ID: 28) i Użytkownik 1 (ID: 1)
"""

import sys
import os

# Dodaj ścieżkę do modułów
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from db.database import Database


def cleanup_users():
    db = Database()
    users = db.get_all_users()

    print("Obecni użytkownicy w bazie:")
    for user in users:
        if len(user) == 4:
            user_id, name, created, is_admin = user
            admin_label = "[ADMIN]" if is_admin else ""
            print(f"  ID: {user_id}, Nazwa: {name} {admin_label}")
        else:
            user_id, name, created = user
            print(f"  ID: {user_id}, Nazwa: {name}")

    print("\nUsuwanie użytkowników (zachowuję ID: 1 i ID: 28)...")

    keep_ids = [1, 28]
    deleted_count = 0

    for user in users:
        user_id = user[0]
        user_name = user[1]

        if user_id not in keep_ids:
            try:
                # Usuń bezpośrednio z bazy - omiń walidację
                db.conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
                db.conn.commit()
                print(f"  ✓ Usunięto: {user_name} (ID: {user_id})")
                deleted_count += 1
            except Exception as e:
                print(f"  ✗ Błąd usuwania {user_name} (ID: {user_id}): {e}")

    print(f"\nUsunięto {deleted_count} użytkowników")

    # Pokaż końcową listę
    users = db.get_all_users()
    print("\nPozostali użytkownicy:")
    for user in users:
        if len(user) == 4:
            user_id, name, created, is_admin = user
            admin_label = "[ADMIN]" if is_admin else ""
            print(f"  ID: {user_id}, Nazwa: {name} {admin_label}")
        else:
            user_id, name, created = user
            print(f"  ID: {user_id}, Nazwa: {name}")


if __name__ == "__main__":
    print("=" * 50)
    print("CZYSZCZENIE BAZY UŻYTKOWNIKÓW")
    print("=" * 50)
    cleanup_users()
    print("\nGotowe!")
