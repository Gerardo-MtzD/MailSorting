from dash import Dash, html, dcc, Patch
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from components import ids

df = pd.DataFrame({"name": ["TCS","GM","RD"],"subtotal": [1234,1000,432432], "iva": [2234,221,12222], "total": [12123123,1212,63213]})
print(df)
MEDAL_DATA = px.data.medals_long()

"""def render(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.DONUT_CHART, "children"),
        [Input(ids.NAME_DROPDOWN, "value")]
    )
    def update_chart(names) -> html.Div:
        filtered_data = df.query("name in @names")
        filtered_data = filtered_data.reset_index()
        filtered_data = filtered_data.transpose()
        filtered_data = filtered_data.iloc[1:]
        fig = px.pie(filtered_data, names=filtered_data.index, values=filtered_data[0].values, hole=0.5)
        return html.Div(dcc.Graph(figure=fig),id=ids.DONUT_CHART)
    return html.Div(id=ids.DONUT_CHART)"""

def render(app:Dash):
    @app.callback(
        Output(ids.DONUT_CHART, "children"),
        [Input(ids.NAME_DROPDOWN, "value"),
         ]
    )
    def update_chart(names) -> html.Div:
        filtered_data = df.query("name in @names")
        filtered_data = filtered_data.reset_index()
        filtered_data = filtered_data.transpose()
        filtered_data = filtered_data.iloc[1:]
        print(filtered_data)
        fig = px.pie(filtered_data, names=filtered_data.index, values=filtered_data[0].values, hole=0.5)
        #fig = px.pie(MEDAL_DATA, names="nation", values="count")
        return html.Div(dcc.Graph(figure=fig), id=ids.DONUT_CHART)
    return html.Div(id=ids.DONUT_CHART)