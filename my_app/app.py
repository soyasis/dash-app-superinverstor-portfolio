import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from shiny import App, reactive, render, ui
from functions import *


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
    ui.output_plot("plot"),
    ui.output_text("name")
)


def server(input, output, session):

    # initiliaze 
    
    
    # Pie Chart
    """ fig = px.pie(values=portfolio_df['% ofPortfolio'], names=portfolio_df['Stock'])
    fig = fig.show()
    register_widget("fig", fig)

    @reactive.Effect
    def _():
        fig.name = input.name() """
    @output
    @render.plot    
    def plot():
        search_result_url, search_result_investor = search_investor(input.name(), investor_df)
        portfolio_df = get_portfolio_data(search_result_url, search_result_investor)
        y = portfolio_df['% ofPortfolio']
        labels = portfolio_df['Stock']
        fig = plt.pie(y, labels = labels, startangle = 90)

        return fig
    
    @output
    @render.text
    def name():
        return f"The current investor is {input.name()}" 
      
        


app = App(app_ui, server)

 
 
