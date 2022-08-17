import numpy as np
import pandas as pd
from shiny import *
from shinywidgets import output_widget, register_widget, reactive_read
from functions import *
import plotly.express as px


# get investor df
investor_df = get_investor_data()

# generate list of investors
investors_array = investor_df.sort_values('investor')["investor"].values
investors_list = investors_array.tolist()
#investor_dict = dict(enumerate(investors_array.flatten(), 1))
#investor_dict = {'a': 1, 'b': 2}

app_ui = ui.page_fluid(
    ui.h2("Superinvestors Portfolio"),
    ui.input_select("name", "Investor", investors_list),
    output_widget("fig"),
    ui.output_text("name")
)


def server(input, output, session):

    # initiliaze 
    search_result_url, search_result_investor = search_investor('AKO Capital', investor_df)
    portfolio_df = get_portfolio_data(search_result_url, search_result_investor)
    
    
    # Pie Chart
    """ fig = px.pie(values=portfolio_df['% ofPortfolio'], names=portfolio_df['Stock'])
    fig = fig.show()
    register_widget("fig", fig)

    @reactive.Effect
    def _():
        fig.name = input.name() """
        

    @output
    @render.text
    def name():
        return f"The current investor is {input.name()}" 
      
        


app = App(app_ui, server)

 
 
