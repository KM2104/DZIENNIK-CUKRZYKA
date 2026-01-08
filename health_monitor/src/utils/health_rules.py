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


def weight_alert(weight: float) -> AlertLevel:
    s = Settings()
    min_w, max_w = s.get_weight_limits()

    if weight < min_w * 0.8 or weight > max_w * 1.2:
        return AlertLevel.DANGER
    if weight < min_w or weight > max_w:
        return AlertLevel.WARNING
    return AlertLevel.OK


def pressure_alert(sys: int, dia: int) -> AlertLevel:
    s = Settings()
    sys_w, dia_w, sys_d, dia_d = s.get_pressure_limits()

    if sys >= sys_d or dia >= dia_d:
        return AlertLevel.DANGER
    if sys >= sys_w or dia >= dia_w:
        return AlertLevel.WARNING
    return AlertLevel.OK

