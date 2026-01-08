"""
Docstring for health_monitor.src.utils.paths
Warstwa zarządzania ścieżkami zapisu plików danych :
w aplikacji PC - wkatalogu aplikacji,
w aplikacji mobilnej Anroid: /sdcard/Download
"""

import os
from kivy.utils import platform


def get_export_path(filename):
    if platform == "android":
        return f"/sdcard/Download/{filename}"
    return os.path.join(os.getcwd(), filename)

def get_app_data_dir():
    if platform == "android":
        return "/sdcard/HealthMonitor"
    return os.getcwd()


def get_db_path():
    return os.path.join(get_app_data_dir(), "health.db")
