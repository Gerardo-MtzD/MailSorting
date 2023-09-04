from dash import Dash
import dash_bootstrap_components as dbc

from components.layout import create_layout


def run_dashboard() -> None:
    app = Dash(external_stylesheets=[dbc.themes.LITERA])
    app.title = "Financial Dashboard"
    app.layout = create_layout(app)
    app.run()


if __name__ == "__main__":
    run_dashboard()