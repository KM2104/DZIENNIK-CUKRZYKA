"""
Docstring for health_monitor.src.utils.backup
Warstwa zarządzania kopiami zapasowymi danych aplikacji
"""

import shutil
from utils.paths import get_db_path, get_app_data_dir
from datetime import datetime
from kivy.utils import platform
import os


def get_sdcard_backup_dir():
    """Zwraca ścieżkę do katalogu backupów na karcie SD"""
    if platform == "android":
        backup_dir = "/sdcard/HealthMonitor/backups"
        # Utwórz katalog jeśli nie istnieje
        if not os.path.exists(backup_dir):
            try:
                os.makedirs(backup_dir)
            except:
                pass
        return backup_dir
    else:
        # Na PC używamy podkatalogu w folderze aplikacji
        backup_dir = os.path.join(os.getcwd(), "backups")
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        return backup_dir


def backup_database(location="app"):
    """
    Tworzy kopię zapasową bazy danych

    Args:
        location (str): 'app' - folder aplikacji, 'sdcard' - karta SD/zewnętrzny folder backupów

    Returns:
        str: Ścieżka do utworzonego backupu
    """
    src = get_db_path()
    if not os.path.exists(src):
        raise FileNotFoundError("Brak bazy danych")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"health_backup_{ts}.db"

    if location == "sdcard":
        dst_dir = get_sdcard_backup_dir()
    else:
        dst_dir = get_app_data_dir()

    dst = os.path.join(dst_dir, filename)
    shutil.copy2(src, dst)
    return dst


def list_backups(location="app"):
    """
    Zwraca listę dostępnych backupów z określonej lokalizacji

    Args:
        location (str): 'app' - folder aplikacji, 'sdcard' - karta SD

    Returns:
        list: Lista krotek (ścieżka_do_pliku, data_modyfikacji)
    """
    if location == "sdcard":
        backup_dir = get_sdcard_backup_dir()
    else:
        backup_dir = get_app_data_dir()

    if not os.path.exists(backup_dir):
        return []

    backups = []
    for filename in os.listdir(backup_dir):
        if filename.startswith("health_backup_") and filename.endswith(".db"):
            filepath = os.path.join(backup_dir, filename)
            mtime = os.path.getmtime(filepath)
            backups.append((filepath, mtime, filename))

    # Sortuj od najnowszego do najstarszego
    backups.sort(key=lambda x: x[1], reverse=True)
    return backups


def restore_database(backup_path):
    """Przywraca bazę danych z wybranego backupu"""
    if not os.path.exists(backup_path):
        raise FileNotFoundError(f"Plik backupu nie istnieje: {backup_path}")

    dst = get_db_path()
    shutil.copy2(backup_path, dst)
