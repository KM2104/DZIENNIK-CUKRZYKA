"""
Docstring for health_monitor.src.utils.export_pdf
Warstwa eksportu danych do PDF dla lekarza
"""

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("Uwaga: Eksport PDF niedostępny (brak reportlab)")

from datetime import datetime


def export_weights_pdf(data, filepath):
    if not PDF_AVAILABLE:
        raise ImportError("Eksport PDF wymaga instalacji pakietu reportlab")

    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4

    y = height - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Raport – Waga ciała")

    y -= 30
    c.setFont("Helvetica", 10)
    c.drawString(
        50, y, f"Data wygenerowania: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )

    y -= 40
    for value, date in data:
        c.drawString(50, y, f"{date[:16]}  –  {value} kg")
        y -= 18
        if y < 50:
            c.showPage()
            y = height - 50

    c.save()


def export_pressure_pdf(data, filepath):
    if not PDF_AVAILABLE:
        raise ImportError("Eksport PDF wymaga instalacji pakietu reportlab")

    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4

    y = height - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Raport – Ciśnienie tętnicze")

    y -= 30
    c.setFont("Helvetica", 10)

    for sys, dia, date in data:
        c.drawString(50, y, f"{date[:16]}  –  {sys}/{dia} mmHg")
        y -= 18
        if y < 50:
            c.showPage()
            y = height - 50

    c.save()
