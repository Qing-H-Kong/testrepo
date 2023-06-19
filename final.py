import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()

#Question 1: Use yfinance to Extract Stock Data

ticker = yf.Ticker('TSLA')

tesla_data = ticker.history(period='max')

tesla_data.reset_index(inplace=True)
print(tesla_data.head(5))

#Question 2: Use Webscraping to Extract Tesla Revenue Data

url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm'
data = requests.get(url).text

soup = BeautifulSoup(data, 'html.parser')

soup.find_all("tbody")[1]

tesla_revenue = pd.DataFrame(columns=['Date', 'Revenue'])

rows = []

for row in soup.find('tbody').find_all('tr'):
    col = row.find_all('td')
    Date = col[0].text
    Revenue = col[1].text

    rows.append({'Date': Date, 'Revenue': Revenue})

tesla_revenue = pd.concat([tesla_revenue, pd.DataFrame(rows)], ignore_index=True)
tesla_revenue['Revenue'] = tesla_revenue['Revenue'].str.replace(',', '').str.replace('$', '')

tesla_revenue.dropna(inplace=True)

tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]

print(tesla_revenue.tail(5))

#Question 3: Use yFinance to Extract Stock Data

import yfinance

ticker = yfinance.Ticker('GME')

gme_data = ticker.history(period='max')

gme_data.reset_index(inplace=True)
gme_data.head()
print(gme_data.head())

#Question 4: Use Webscraping to Extraxt GME Revenue Data

url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html'

html_data = requests.get(url).text
soup = BeautifulSoup(html_data, 'html.parser')

soup.find_all("tbody")[1]

gme_revenue = pd.DataFrame(columns=['Date', 'Revenue'])

rows = []

for row in soup.find('tbody').find_all('tr'):
    col = row.find_all('td')
    Date = col[0].text
    Revenue = col[1].text

    rows.append({'Date': Date, 'Revenue': Revenue})

gme_revenue = pd.concat([gme_revenue, pd.DataFrame(rows)], ignore_index=True)

gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(',', '').str.replace('$','')

print(gme_revenue.tail(5))

#Question 5: Plot Telsa Stock Graph

make_graph(tesla_data, tesla_revenue, 'Tesla')

#Question 6: Plot GameStop Stock Graph

make_graph(gme_data, gme_revenue, 'GameStop')