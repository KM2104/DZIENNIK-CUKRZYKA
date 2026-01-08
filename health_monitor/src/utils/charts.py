"""
Moduł wykresów do monitorowania zdrowia
"""

try:
    from kivy_garden.graph import Graph, MeshLinePlot
    from kivy.graphics import Color

    CHARTS_AVAILABLE = True
except ImportError:
    CHARTS_AVAILABLE = False
    print("Uwaga: Wykresy niedostępne (brak kivy_garden.graph)")


def weight_chart(data):
    if not CHARTS_AVAILABLE or not data:
        return None

    values = [v for v, _ in data]
    min_val = min(values)
    max_val = max(values)

    # Wykres wagi - optymalizowany dla Androida
    graph = Graph(
        xlabel="Pomiary",
        ylabel="Waga (kg)",
        x_ticks_minor=0,
        x_ticks_major=max(1, len(data) // 5),
        y_ticks_major=5,
        y_grid_label=True,
        x_grid_label=True,
        padding=10,
        x_grid=True,
        y_grid=True,
        xmin=0,
        xmax=len(data),
        ymin=min_val - 5,
        ymax=max_val + 5,
        label_options={"color": [0, 0, 0, 1], "bold": True},
        background_color=[1, 1, 1, 1],
        border_color=[0.2, 0.2, 0.2, 1],
    )

    # Dane do wykresu - grubsza linia
    plot = MeshLinePlot(color=[0.2, 0.7, 0.3, 1])
    plot.points = [(i, v) for i, v in enumerate(values)]
    graph.add_plot(plot)

    return graph


def pressure_chart(data):
    if not CHARTS_AVAILABLE or not data:
        return None

    # Wykres ciśnienia - optymalizowany dla Androida
    sys_values = [s for s, _, _ in data]
    dia_values = [d for _, d, _ in data]

    all_values = sys_values + dia_values
    min_val = min(all_values)
    max_val = max(all_values)

    graph = Graph(
        xlabel="Pomiary",
        ylabel="Ciśnienie (mmHg)",
        x_ticks_minor=0,
        x_ticks_major=max(1, len(data) // 5),
        y_ticks_major=20,
        y_grid_label=True,
        x_grid_label=True,
        padding=10,
        x_grid=True,
        y_grid=True,
        xmin=0,
        xmax=len(data),
        ymin=min_val - 10,
        ymax=max_val + 10,
        label_options={"color": [0, 0, 0, 1], "bold": True},
        background_color=[1, 1, 1, 1],
        border_color=[0.2, 0.2, 0.2, 1],
    )

    # Skurczowe (czerwone) - grubsza linia
    plot_sys = MeshLinePlot(color=[1, 0.2, 0.2, 1])
    plot_sys.points = [(i, s) for i, s in enumerate(sys_values)]
    graph.add_plot(plot_sys)

    # Rozkurczowe (niebieskie) - grubsza linia
    plot_dia = MeshLinePlot(color=[0.2, 0.4, 1, 1])
    plot_dia.points = [(i, d) for i, d in enumerate(dia_values)]
    graph.add_plot(plot_dia)

    return graph

    return graph
