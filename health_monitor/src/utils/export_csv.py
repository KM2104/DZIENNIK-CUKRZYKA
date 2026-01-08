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
