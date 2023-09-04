from dash import Dash, html, dcc, ctx
from pathlib import Path
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from components import ids
import datetime as dt
import plotly.express as px
import pandas as pd
from utils.sort_month import sort_month
import subprocess


all_months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                  'August', 'September', 'October', 'November', 'December']

all_years = [str(year) for year in range(2019,dt.datetime.now().year+1)]

def create_layout(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.DONUT_CHART, 'figure'),
        [Input(ids.NAME_DROPDOWN, 'value'),
         Input(ids.MONTH_DROPDOWN, 'value'),
         Input(ids.YEAR_DROPDOWN, 'value')]
    )
    def display_graph(names, month, year):
        fig = blank_figure()
        df = []
        if ctx.triggered:
            input_id = ctx.triggered[0]["prop_id"].split(".")[0]
            df = fetch_file(month, year)
            names = adapt_name(names)
            if df is not None:
                filtered_data = df.query("NAME in @names")
                filtered_data = filtered_data.sum()
                print(filtered_data)
                fig = px.pie(filtered_data, names=filtered_data.index, values=filtered_data.values,
                         hole=0.5, color_discrete_sequence=px.colors.sequential.Blues_r)
                fig.update_traces(textinfo='value')
        return fig

    @app.callback(
        Output(ids.MONTH_DROPDOWN, 'options'),
        Input(ids.YEAR_DROPDOWN, 'value')
    )
    def update_month(year):
        print(f"selected year: {year}, real year: {dt.datetime.now().year}")
        if int(year) == dt.datetime.now().year:
            return [{"label": month, "value": month} for month in all_months[:int(dt.datetime.now().month)]]
        else:
            return [{"label": month, "value": month} for month in all_months]

    return html.Div([
        html.Label('Name'),
        dcc.Dropdown(
            id=ids.NAME_DROPDOWN,
            options=[
                {'label': 'GM', 'value': 'GM'},
                {'label': 'TCS', 'value': 'TCS'},
                {'label': 'RD', 'value': 'RD'}
            ],
            value = 'GM',
            multi=False
        ),
        html.Label('Month'),
        dcc.Dropdown(
            id=ids.MONTH_DROPDOWN,
            options=[{"label": month, "value": month} for month in all_months[:int(dt.datetime.now().month)]],
            value='January',
            multi=False
        ),
        html.Label('Year'),
        dcc.Dropdown(
            id= ids.YEAR_DROPDOWN,
            options=[{"label": year, "value": year} for year in all_years],
            value=all_years[-1],
            multi=False
        ),
        dcc.Graph(id=ids.DONUT_CHART, responsive=True),
        dcc.Store(id=ids.STORAGE)
    ])

def fetch_file(month: str, year: int) -> pd.DataFrame:
    month = str(dt.datetime.strptime(month, '%B').month)
    ROOT_DIRECTION = Path(Path.home() / 'Documents')
    wanted_path = Path(ROOT_DIRECTION / str(year) / sort_month(month) / 'FRAME.csv')
    print(wanted_path)
    if wanted_path.is_file():
        print('retrieving doc')
        df = pd.read_csv(str(wanted_path))
        print(df.head())
        df = df.drop(['Unnamed: 0', 'FOLIO', 'CONCEPT'], axis=1)
        df = df.set_index('NAME')
        return df
    else:
        print('call for main')
        subprocess.run(['python', 'main.py', f"{month}", f'{year}'])
        if wanted_path.is_file():
            df = pd.read_csv(str(wanted_path))
            print(df.head())
            df = df.drop(['Unnamed: 0', 'FOLIO', 'CONCEPT'], axis=1)
            df = df.set_index('NAME')
            return df


def adapt_name(name: str) -> str:
    if name == 'GM':
        return 'MAMG650207659'
    elif name == 'TCS':
        return 'TSE090522B18'
    elif name == 'RD':
        return 'DEMR650805NP2'
    else:
        raise Exception


def blank_figure():
    fig = go.Figure(go.Scatter(x=[], y=[]))
    fig.update_layout(template=None)
    fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
    fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)

    return fig
