from dash import Dash, html
from dash.dependencies import Input, Output, State
from components import ids

def check_for_file(app:Dash) -> html.Div:
    fetch_file = ["","",""]
    @app.callback(
        State(ids.NAME_DROPDOWN, 'value'),
        State(ids.YEAR_DROPDOWN, 'value'),
        State(ids.MONTH_DROPDOWN,'value')
    )
    def fetch(dn,dy,dm) -> list[str]:
        fetch_file = [dn,dy,dm]
        return fetch_file

    return html.Div(
            children=[fetch_file]
        )
