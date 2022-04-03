# %%
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# %%
print("hello")

# %%
# Make request
url = "https://www.dataroma.com/m/home.php"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
}
r = requests.get(url=url, headers=headers)

# Parse the HTML
soup = BeautifulSoup(r.content, "html.parser")

# get names from tag and id
n = soup.find("span", id="port_body")
names_res = n.find_all("li")
url_res = n.find_all("a")

# iterate to extract names
names = []
for i in names_res:
    names.append(i.text)

# get URL's
urls = []
for i in url_res:
    urls.append("https://dataroma.com" + i.get("href"))

# split name from update date
investors = pd.DataFrame(names)[0].str.split(pat="Updated", expand=True)
investors.columns = ["investor", "update_date"]

# parse as date object
investors["update_date"] = pd.to_datetime(investors["update_date"])

# merge with urls
investor_df = investors.assign(url=urls)
investor_df.head(5)


# %% Search for investor

investor_df[investor_df["investor"].str.contains("Ackman")]
ackman = investor_df[
    investor_df["investor"].str.contains("Ackman", case=False, na=False)
]
ackman_url = ackman["url"][0]
ackman_url = "https://dataroma.com/m/holdings.php?m=psc"

# %%
r2 = requests.get(url=ackman_url, headers=headers)

# Parse the HTML
soup = BeautifulSoup(r2.content, "html.parser")

# get names from tag and id
n = soup.find("table", id="grid")
ackman_df = n.find_all("td")

tbl_list = []
for i in ackman_df:
    tbl_list.append(i.text)

col_names = [
    "history",
    "stock",
    "%OfPortfolio",
    "rencentActivity",
    "shares",
    "reportedPrice",
    "value",
    "",
    "currentPrice",
    "+/-ReportedPrice",
    "52WeekLow",
    "52WeekHigh",
]

ackman_df = pd.DataFrame(
    [tbl_list[n : n + 12] for n in range(0, len(tbl_list), 12)], columns=col_names
)

# drop first row
ackman_df = ackman_df.drop([0])
