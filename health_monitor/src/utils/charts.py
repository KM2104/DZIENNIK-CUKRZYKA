"""
Moduł wykresów do monitorowania zdrowia
"""

try:
    from matplotlib import pyplot as plt
    from kivy.garden.matplotlib import FigureCanvasKivyAgg

    CHARTS_AVAILABLE = True
except ImportError:
    CHARTS_AVAILABLE = False
    print("Uwaga: Wykresy niedostępne (brak matplotlib lub garden.matplotlib)")


def weight_chart(data):
    if not CHARTS_AVAILABLE:
        return None

    values = [v for v, _ in data]
    dates = [d[:10] for _, d in data]

    fig, ax = plt.subplots()
    ax.plot(dates, values, marker="o")
    ax.set_title("Trend wagi")
    ax.set_ylabel("kg")
    ax.set_xlabel("Data")
    ax.grid(True)

    fig.autofmt_xdate()

    return FigureCanvasKivyAgg(fig)


def pressure_chart(data):
    if not CHARTS_AVAILABLE:
        return None

    sys = [s for s, _, _ in data]
    dia = [d for _, d, _ in data]
    dates = [dt[:10] for _, _, dt in data]

    fig, ax = plt.subplots()
    ax.plot(dates, sys, label="Skurczowe")
    ax.plot(dates, dia, label="Rozkurczowe")
    ax.set_title("Trend ciśnienia")
    ax.set_ylabel("mmHg")
    ax.legend()
    ax.grid(True)

    fig.autofmt_xdate()

    return FigureCanvasKivyAgg(fig)
