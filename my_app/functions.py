import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


# Global variables
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}


def get_investor_data():
    """
    Connect to dataroma.com and get the investor data
    Returns:
        - investor_df: dataframe with investor data
    """
    url = "https://www.dataroma.com/m/home.php"
    r = requests.get(url=url, headers=headers)
    
    soup = BeautifulSoup(r.content, "html.parser")
    n = soup.find("span", id="port_body")
    names_res = n.find_all("li")
    url_res = n.find_all("a")

    names = []
    for i in names_res:
        names.append(i.text)

    urls = []
    for i in url_res:
        urls.append("https://dataroma.com" + i.get("href"))

    investors = pd.DataFrame(names)[0].str.split(pat="Updated", expand=True)
    investors.columns = ["investor", "update_date"]

    investors["update_date"] = pd.to_datetime(investors["update_date"])

    investor_df = investors.assign(url=urls)
    return investor_df


def list_investors():
    """
    List all investors in the database
    Returns:
        - list_investors_df: dataframe with all investors
    """
    list_investors_df = investor_df.drop(columns=["update_date", "url"])
    return list_investors_df


def search_investor(search_term, investor_df):
    """
    Search for investor across investor_df
    Returns:
        - search_result_url: URL of search result
        - search_result_investor: name of search result
    """
    
    search_result = investor_df[investor_df["investor"].str.contains(search_term, case=False, na=False)]
    search_result_url = search_result['url'].values[0] # search_result.iloc[0]['url']
    search_result_investor = search_result['investor'].values[0]
    return search_result_url, search_result_investor


def get_portfolio_data(search_result_url, search_result_investor):
    """
    Get portfolio data for searched investor
    Returns:
        - portfolio_df: dataframe with portfolio data for
    """
    r2 = requests.get(url=search_result_url, headers=headers)

    soup = BeautifulSoup(r2.content, "html.parser")
    n = soup.find("table", id="grid")

    portfolio_df = pd.read_html(str(n))[0]
    portfolio_df['investorName'] = search_result_investor
    return portfolio_df



