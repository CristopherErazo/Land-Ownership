import plotly.graph_objects as go
from pathlib import Path

def example_plot():
    # Example datasets
    datasets = {
        "Dataset A": [1, 3, 2, 4],
        "Dataset B": [2, 2, 3, 5],
        "Dataset C": [4, 1, 3, 2],
    }

    fig = go.Figure()

    # Add all datasets as traces (initially only first visible)
    for i, (name, y) in enumerate(datasets.items()):
        fig.add_trace(
            go.Scatter(
                y=y,
                mode="lines+markers",
                name=name,
                visible=(i == 0)
            )
        )

    # Create dropdown buttons
    buttons = []
    for i, name in enumerate(datasets.keys()):
        visibility = [False] * len(datasets)
        visibility[i] = True
        buttons.append(
            dict(
                label=name,
                method="update",
                args=[{"visible": visibility},
                    {"title": f"Showing {name}"}]
            )
        )

    fig.update_layout(
        updatemenus=[dict(
            active=0,
            buttons=buttons,
            x=1.15,
            y=1
        )]
    )

    dir_path = "./docs/_static/plots/"
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    file_path = Path(dir_path) / "interactive_plot.html"

    fig.write_html(file_path, include_plotlyjs="cdn")

if __name__ == "__main__":
    example_plot()