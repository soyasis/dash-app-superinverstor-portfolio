# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
from functions import *


app = Dash(__name__)


# get investor df
investor_df = get_investor_data()

# generate list of investors
investors_array = investor_df.sort_values('investor')["investor"].values
#investors_list = investors_array.tolist()

        
    
app.layout = html.Div(children=[
    
    html.H1(children="Superinvestor's Portfolios"),

    html.Div(children='''
        A simple Dash Application on top of the DataRoma.com
    '''),
    
    html.Br(),
    html.Br(),
    html.Label('Select investor'),
        dcc.Dropdown(
            investors_array, 
            value=investors_array[0],
            id='investor-select'),
        
    dcc.Graph(id='pie-chart')
])

@app.callback(
    Output('pie-chart', 'figure'),
    Input('investor-select', 'value'))
def update_figure(investor_name):
    search_result_url, search_result_investor = search_investor(investor_name, investor_df)
    portfolio_df = get_portfolio_data(search_result_url, search_result_investor)

    y = portfolio_df['% ofPortfolio']
    labels = portfolio_df['Stock']
    fig = px.pie(values=y, names=labels)

    fig.update_layout(transition_duration=500)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)


