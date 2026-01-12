"""
Docstring for health_monitor.src.utils.health_rules
Warstwa reguł zdrowotnych
"""

from utils.settings import Settings
from enum import Enum


class AlertLevel(Enum):
    OK = "OK"
    WARNING = "OSTRZEŻENIE"
    DANGER = "NIEBEZPIECZNE"
    WARNING_LOW = "OSTRZEŻENIE_NISKIE"
    WARNING_HIGH = "OSTRZEŻENIE_WYSOKIE"
    DANGER_LOW = "NIEBEZPIECZNE_NISKIE"
    DANGER_HIGH = "NIEBEZPIECZNE_WYSOKIE"


def weight_alert(weight: float) -> AlertLevel:
    s = Settings()
    min_w, max_w = s.get_weight_limits()

    if weight < min_w * 0.8:
        return AlertLevel.DANGER_LOW
    if weight > max_w * 1.2:
        return AlertLevel.DANGER_HIGH
    if weight < min_w:
        return AlertLevel.WARNING_LOW
    if weight > max_w:
        return AlertLevel.WARNING_HIGH
    return AlertLevel.OK


def pressure_alert(sys: int, dia: int) -> AlertLevel:
    s = Settings()
    sys_min, dia_min, sys_w, dia_w, sys_d, dia_d = s.get_pressure_limits()

    # Sprawdzenie wartości niebezpiecznych
    if sys < sys_min or dia < dia_min:
        return AlertLevel.DANGER_LOW
    if sys >= sys_d or dia >= dia_d:
        return AlertLevel.DANGER_HIGH
    # Sprawdzenie ostrzeżenia
    if sys >= sys_w or dia >= dia_w:
        return AlertLevel.WARNING_HIGH
    return AlertLevel.OK


def heartrate_alert(heartrate: int) -> AlertLevel:
    """
    Ocena tętna:
    - OK: 60-100 bpm (normalne tętno spoczynkowe)
    - WARNING: 50-59 lub 101-120 bpm
    - DANGER: <50 lub >120 bpm
    """
    if heartrate < 50:
        return AlertLevel.DANGER_LOW
    if heartrate > 120:
        return AlertLevel.DANGER_HIGH
    if heartrate < 60:
        return AlertLevel.WARNING_LOW
    if heartrate > 100:
        return AlertLevel.WARNING_HIGH
    return AlertLevel.OK


def glucose_alert(glucose: int) -> AlertLevel:
    """
    Ocena poziomu glukozy (mg/dL):
    - OK: 70-140 mg/dL (poziom normalny/po posiłku)
    - WARNING: 50-69 lub 141-200 mg/dL
    - DANGER: <50 lub >200 mg/dL
    """
    if glucose < 50:
        return AlertLevel.DANGER_LOW
    if glucose > 200:
        return AlertLevel.DANGER_HIGH
    if glucose < 70:
        return AlertLevel.WARNING_LOW
    if glucose > 140:
        return AlertLevel.WARNING_HIGH
    return AlertLevel.OK
