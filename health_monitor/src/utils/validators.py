"""
Walidatory danych wejściowych
"""


class ValidationError(Exception):
    pass


def validate_weight(value: str) -> float:
    try:
        weight = float(value)
    except ValueError:
        raise ValidationError("Waga musi być liczbą")

    if weight <= 0 or weight > 500:
        raise ValidationError("Nieprawidłowa wartość wagi")

    return weight


def validate_pressure(sys: str, dia: str) -> tuple[int, int]:
    try:
        systolic = int(sys)
        diastolic = int(dia)
    except ValueError:
        raise ValidationError("Ciśnienie musi być liczbą")

    if not (50 <= systolic <= 300):
        raise ValidationError("Nieprawidłowe ciśnienie skurczowe")

    if not (30 <= diastolic <= 200):
        raise ValidationError("Nieprawidłowe ciśnienie rozkurczowe")

    if systolic <= diastolic:
        raise ValidationError("Skurczowe musi być większe od rozkurczowego")

    return systolic, diastolic

