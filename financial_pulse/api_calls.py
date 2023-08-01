import requests


API_BASE_URL = 'https://www.alphavantage.co/query?'
API_KEY = 'HA2INLZE28RQ2TH9'


params = {
    'apikey': API_KEY,
} 
      
news_sentiment_params = {
    'apikey': API_KEY,
    'sort' : 'LATEST',
    'limit' : 3,
}


def fetch_income_statement(api_base_url, params, symbol=None):
    params['function'] = 'INCOME_STATEMENT'
    if symbol:
        params['symbol'] = symbol
    response = requests.get(api_base_url, params=params)
    print(response)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None


def fetch_balance_sheet(api_base_url, params, symbol=None):
    params['function'] = 'BALANCE_SHEET'
    if symbol:
        params['symbol'] = symbol
    response = requests.get(api_base_url, params=params)
    print(response)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None
    

def fetch_news_sentiment(api_base_url, news_sentiment_params, symbol=None):
    news_sentiment_params['function'] = 'NEWS_SENTIMENT'
    if symbol:
        news_sentiment_params['tickers'] = symbol  
    response = requests.get(api_base_url, params=news_sentiment_params)
    print(response)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None
    

def fetch_overview(api_base_url, params, symbol=None):
    params['function'] = 'OVERVIEW'
    if symbol:
        params['symbol'] = symbol
    response = requests.get(api_base_url, params=params)
    print(response)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None