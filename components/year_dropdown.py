from dash import Dash, html, dcc, ctx
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from components import ids
import datetime as dt


def render(app:Dash) -> html.Div:
    all_years = [str(year) for year in range(2019,dt.datetime.now().year+1)]
    app.callback(
        Output(ids.YEAR_DROPDOWN, "value"),
    )

    return html.Div(
        children=[
            html.H6('Select year'),
            dcc.Dropdown(
            id=ids.YEAR_DROPDOWN,
            options=[{"label": year, "value": year} for year in all_years],
            multi=False,
            value=all_years[0],
            placeholder='Select a year...'
        ),
        ]
    )