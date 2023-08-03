import requests


# Coingecko api 
API_BASE_URL = 'https://api.coingecko.com/api/v3/coins/markets/'
API_BASE_URL_DETAILS = 'https://api.coingecko.com/api/v3/coins/'
# Binance api 
API_BASE_URL_CHARTS = 'https://api.binance.com/api/v3/klines'
API_ORDER_BOOK_URL = 'https://api.binance.com/api/v3/depth'
# CoinMarketCap api
API_KEY = '795fa44a-7532-4eef-ae9a-7de17a0814df'

order_params = {
    'limit': 15,
}

line_params = {
    'interval': '1d',
    'limit': 100,
}

params = {
    'order': 'market_cap_desc',
    'vs_currency': 'usd',
    'per_page': 30,
}

chart_params = {
    'interval': '1d',
    'symbol': '',
    'limit': 10,
} 


def fetch_coins(API_BASE_URL, params):
    response = requests.get(API_BASE_URL, params=params)
    
    if response.status_code == 200:
        top_coins_data = response.json()  
        
        return top_coins_data
    else:
        return None


def fetch_order_book(API_ORDER_BOOK_URL, coin_symbol, params=order_params):
    url = f"{API_ORDER_BOOK_URL}?symbol={coin_symbol}&limit={params['limit']}"
    
    response = requests.get(url)
    
    print(response)
    print(response.url)
    print(coin_symbol)
    
    if response.status_code == 200:
        orderbook_data = response.json()
        return orderbook_data
    else:
        return None

 
    
def fetch_market_charts(API_BASE_URL_CHARTS, coin_symbol, params=chart_params):
    url = f"{API_BASE_URL_CHARTS}?symbol={coin_symbol}&interval={params['interval']}"

    response = requests.get(url)

    if response.status_code == 200:
        candles_data = response.json()
        return candles_data
    else:
        return None
    

def fetch_coin_details(API_BASE_URL_DETAILS, coin_name):
    coin_name = coin_name.lower()
    url = f'{API_BASE_URL_DETAILS}{coin_name}'
    
    response = requests.get(url)
    print(response.url)
    if response.status_code == 200:
        coin_details = response.json()
        return coin_details
    else:
        return None
 
 
def fetch_coin_price(API_BASE_URL_CHARTS, coin_symbol, params=line_params):
    url = f"{API_BASE_URL_CHARTS}/{coin_symbol}?interval={params['interval']}&limit={params['limit']}"
    
    response = requests.get(url)
    print(response)
    print(response.url)
    
    if response.status_code == 200:
        coin_lines = response.json()
        return coin_lines
    else:
        return None



params_test = {
    'interval': '1d',
    'limit': 100,
}   
def test_fetch(API_BASE_URL_CHARTS, coin_symbol, params=line_params):
    url = f"{API_BASE_URL_CHARTS}?symbol={coin_symbol}&interval={params['interval']}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        coin_lines = response.json()
        return coin_lines
    else:
        return None


