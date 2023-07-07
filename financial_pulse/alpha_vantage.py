import requests
import json


API_BASE_URL = 'https://www.alphavantage.co/query?'
API_KEY = 'HA2INLZE28RQ2TH9'
FUNCTION = 'INCOME_STATEMENT'
SYMBOL = 'AAPL'
# INTERVAL = '5min'


params = {
    'function': FUNCTION,
    'symbol': SYMBOL,
    # 'interval': INTERVAL,
    'apikey': API_KEY,
}


def fetch_financial_data(api_base_url, params):
    response = requests.get(api_base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None