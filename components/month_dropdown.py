from dash import Dash, html, dcc, ctx
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from components import ids
import datetime as dt


def render(app: Dash) -> html.Div:
    all_months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                  'August', 'September', 'October', 'November', 'December']
    app.callback(
        Output(ids.MONTH_DROPDOWN, "value"),
    )
    return html.Div(
        children=[
            html.H6('Select date'),
            dcc.Dropdown(
                id=ids.MONTH_DROPDOWN,
                options=[{"label": month, "value": month} for month in all_months[:int(dt.datetime.now().month)]],
                multi=False,
                value=all_months[0],
                placeholder='Select a month...'
            ),

        ]
    )
