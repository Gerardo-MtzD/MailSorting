from dash import Dash, html, dcc, ctx
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from components import ids


def render(app: Dash) -> html.Div:
    all_names = ["GM", "TCS", "RD"]
    return html.Div(
        children=[
            html.H6("Select Name"),
            dcc.Dropdown(
                id=ids.NAME_DROPDOWN,
                options=[{"label": name, "value": name} for name in all_names],
                value=None,
                multi=False,
                clearable=False,
                placeholder="Select an option..."
            ),
        ]
    )
