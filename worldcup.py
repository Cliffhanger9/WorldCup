from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import numpy as np

df = pd.read_csv('FifaWorldCup.csv')
wins = df['Winners'].value_counts().reset_index()
wins.columns = ['Country', 'Wins']

winners_l = df['Winners'].unique()

choropleth_map = px.choropleth(
    wins,
    locations='Country',
    locationmode='country names',
    color= 'Wins',
    hover_name='Country',
    color_continuous_scale=px.colors.sequential.Plasma,
    title = 'Fifa World Cup Wins by Country (uncoloured = 0 wins)'
)


app = Dash(__name__)
server = app.server
world_cup_years = [
    1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966,
    1970, 1974, 1978, 1982, 1986, 1990, 1994, 1998,
    2002, 2006, 2010, 2014, 2018, 2022
]
app.layout = [
    html.H1("Fifa World Cup Dashboard", style ={'TextAlign' : 'center', 'fontFamily':'Poppins', 'color': '#BF9345'}),
    html.Div("All Fifa World Cup Winners:", style={'textAlign':'left', 'fontSize': 18, 'margin-bottom':'20px', 'color': '#2E8B57'}),
    html.Ul([html.Li(country) for country in winners_l],
            style={'textAlign':'left', 'fontSize': 18, 'margin-bottom':'30px', 'color': '#2E8B57'}),
    html.Div([
        dcc.Slider(
            id = 'slider',
            min = 0,
            max = len(world_cup_years)-1,
            value = 0,
            marks = {i: str(year) for i, year in enumerate(world_cup_years)},
            step = None,

        )

    ], style = {'textAlign': 'center', 'margin-bottom': '30px'}),
    html.Div(
        id = 'year-output',
        style = {'textAlign': 'center', 'fontSize':30, 'margin-bottom': '30px', 'color': '#2E8B57'}
    ),
    dcc.Graph(figure=choropleth_map)
]

@callback(
    Output("year-output", "children"),
    [Input("slider", "value")]
)
def winner_runnerup_year(index):
    year = world_cup_years[index]
    result = df[df['Year']==year]

    winner = result.iloc[0]["Winners"]
    runner = result.iloc[0]["Runners-up"]
    return f"The winner in the {year} Fifa World Cup was {winner} and the runner up was {runner}"




if __name__ == '__main__':
    app.run(debug=True)
