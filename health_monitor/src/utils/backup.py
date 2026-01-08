"""
Docstring for health_monitor.src.utils.backup
Warstwa zarządzania kopiami zapasowymi danych aplikacji
"""
import shutil
from utils.paths import get_db_path, get_app_data_dir
from datetime import datetime
import os


def backup_database():
    src = get_db_path()
    if not os.path.exists(src):
        raise FileNotFoundError("Brak bazy danych")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    dst = os.path.join(
        get_app_data_dir(),
        f"health_backup_{ts}.db"
    )

    shutil.copy2(src, dst)
    return dst

def restore_database(backup_path):
    dst = get_db_path()
    shutil.copy2(backup_path, dst)

