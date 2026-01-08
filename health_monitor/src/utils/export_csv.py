"""
Docstring for health_monitor.src.utils.export_csv
Warstwa eksportu danych do CSV
"""

import csv


def export_weights_csv(data, filepath):
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Waga (kg)", "Data"])
        for value, date in data:
            writer.writerow([value, date])


def export_pressure_csv(data, filepath):
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Skurczowe", "Rozkurczowe", "Data"])
        for sys, dia, date in data:
            writer.writerow([sys, dia, date])


def export_heartrate_csv(data, filepath):
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Tętno (bpm)", "Data"])
        for value, date in data:
            writer.writerow([value, date])


def export_glucose_csv(data, filepath):
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["Glukoza (mg/dL)", "Data utworzenia", "Czas pomiaru", "Czas od posiłku"]
        )
        for row in data:
            # Obsługa starych (2 kolumny) i nowych (4 kolumny) rekordów
            if len(row) == 2:
                value, date = row
                writer.writerow([value, date, "", ""])
            else:
                value, date, measurement_time, meal_timing = row
                writer.writerow(
                    [value, date, measurement_time or "", meal_timing or ""]
                )
