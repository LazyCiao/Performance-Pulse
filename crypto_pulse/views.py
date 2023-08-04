from django.core.paginator import Paginator
import plotly.graph_objects as go
from django.shortcuts import render
from django.contrib import messages
from .api_calls import (
    fetch_coins,
    fetch_market_charts,
    fetch_coin_details,
    fetch_order_book,
    API_BASE_URL,
    API_BASE_URL_CHARTS,
    API_BASE_URL_DETAILS,
    API_ORDER_BOOK_URL,
    params,
    chart_params,
    order_params
)
import re
import json
import datetime
from .websocket import BinanceWebSocket


def crypto(request):
    coin_data = fetch_coins(API_BASE_URL, params)

    if coin_data is None:
        messages.error(request, 'The limit for fetch requests has been reached. Please try again later.')
        return render(request, 'crypto_pulse/crypto.html')

    if 'error' in coin_data and coin_data['error']['code'] == 429:
        messages.error(request, 'The limit for fetch requests has been reached. Please try again later.')
        return render(request, 'crypto_pulse/crypto.html')
    
    # Split data into 10 coins per page
    paginator = Paginator(coin_data, 10)  

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Store coin data in the session
    request.session['coin_data'] = coin_data
    
    # List to store coin data as dictionaries
    coins = []  
    for coin in page_obj:
        coin_info = {
            'name': coin.get('name'),
            'symbol': coin.get('symbol'),
            'image': coin.get('image'),
            'market_cap': coin.get('market_cap'),
            'daily_price_change': coin.get('price_change_percentage_24h'),
            'daily_volume': coin.get('total_volume'),
            'current_price': coin.get('current_price'),
        }
        coins.append(coin_info)

    return render(request, 'crypto_pulse/crypto.html', {'page_obj': page_obj, 'coins': coins})


def coin_chart(request, coin_symbol):
    # Format symbol
    coin_symbol = coin_symbol.upper() + 'USDT'
    if coin_symbol == 'USDTUSDT':
        coin_symbol = 'BUSDUSDT'
    title_coin_symbol = coin_symbol.replace('USDT', '/USDT')
    
    # Fetch data      
    candles_data = fetch_market_charts(API_BASE_URL_CHARTS, coin_symbol=coin_symbol, params=chart_params)
    orderbook_data = fetch_order_book(API_ORDER_BOOK_URL, coin_symbol=coin_symbol, params=order_params)
    
    # Check if data was successfully fetched
    if candles_data is None and orderbook_data is None:
        messages.error(request, 'Failed to fetch candlestick data. Please try again.')
        return render(request, 'crypto_pulse/coin_chart.html')
    
    # Parse the orderbook data from Binance API
    bids_data = orderbook_data['bids']
    bids_total = [float(bid[0]) * float(bid[1]) for bid in bids_data]
    asks_data = orderbook_data['asks']
    asks_total = [float(ask[0]) * float(ask[1]) for ask in asks_data]
    
    # Parse the data from the Binance API to create the candlestick chart
    timestamps = [candle[0] for candle in candles_data]
    open_prices = [float(candle[1]) for candle in candles_data]
    high_prices = [float(candle[2]) for candle in candles_data]
    low_prices = [float(candle[3]) for candle in candles_data]
    close_prices = [float(candle[4]) for candle in candles_data]
    
    # Calculate the date range for the last 3 months
    today = datetime.date.today()
    three_months_ago = today - datetime.timedelta(days=90)
    
    # Filter the data to show only the last 3 months
    filtered_data = [(timestamp, open_price, high_price, low_price, close_price)
                     for timestamp, open_price, high_price, low_price, close_price in zip(timestamps, open_prices, high_prices, low_prices, close_prices)
                     if datetime.datetime.fromtimestamp(timestamp / 1000).date() >= three_months_ago]
    
    # Create the candlestick chart
    fig = go.Figure(data=[go.Candlestick(x=[candle[0] for candle in filtered_data],
                                        open=[candle[1] for candle in filtered_data],
                                        high=[candle[2] for candle in filtered_data],
                                        low=[candle[3] for candle in filtered_data],
                                        close=[candle[4] for candle in filtered_data])])
    
    # Customize the chart layout
    fig.update_layout(
        xaxis=dict(
            type='date',  # Set the x-axis type to 'date'
            range=[three_months_ago, today + datetime.timedelta(days=1)],  # Set the x-axis range to include an extra day
            gridcolor='rgba(255, 255, 255, 0.2)',  # Set the grid color with transparency
            showgrid=True,  # Show the grid lines
        ),
        yaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.2)',  # Set the grid color with transparency for the y-axis
            showgrid=True,  # Show the grid lines for the y-axis
        ),
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Set the plot area background to transparent
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Set the entire chart background to transparent
        font=dict(color='white'),  # Set the font color for the labels and legend to white
        title=dict(text=f'{title_coin_symbol}',  # Set the title of the chart
                   x=0.5,  # Set the title position to the center of the chart
                   y=0.95,  # Set the title position relative to the y-axis
                   font=dict(size=24)  # Set the font size of the title
                   ),
        xaxis_rangeslider_visible=False
    )
    
    # Convert the chart to JSON to pass it to the template
    chart_json = fig.to_json()
    
    # Get coin data from the session
    coin_data = request.session.get('coin_data', [])
    coin_info = {}
    for coin in coin_data:
        real_coin_symbol = coin_symbol.replace('USDT', '').lower()
        if coin['symbol'] == real_coin_symbol:
            coin_info = {
                'name': coin.get('name'),
                'current_price': coin.get('current_price'),
                'daily_price_change': coin.get('price_change_percentage_24h'),
                'daily_volume': coin.get('total_volume'),
                'market_cap': coin.get('market_cap'),
            }
            break
        
    # Pass the selected coin's data and chart JSON to the template
    return render(request, 'crypto_pulse/coin_chart.html', {'chart_json': chart_json, 'coin_info': coin_info, 'bids': bids_data, 'asks': asks_data, 'bids_total': bids_total, 'asks_total': asks_total})


def coin_details(request, coin_name):
    # Fetch data for description
    print(coin_name)
    if coin_name.lower() == 'xrp':
        coin_name = 'ripple'
    if coin_name.lower() == 'binance usd':
        coin_name = 'tether'
    if coin_name.lower() == 'bnb':
        coin_name = 'busd'
    coin_details = fetch_coin_details(API_BASE_URL_DETAILS, coin_name=coin_name)
    print(coin_name)
    
    # Check if data was successfully fetched
    if coin_details is None:
        messages.error(request, 'Failed to fetch data. Please try again.')
        return render(request, 'crypto_pulse/coin_chart.html')
    
    # Create a dictionary to store descriptions
    description = coin_details['description']['en']
    name = coin_details['name']
    symbol = coin_details['symbol'].upper()
    
    # Clean the description by removing URLs and links
    cleaned_description = description.replace('<a href="', '')
    url_pattern = re.compile(r'http[s]?://\S+|www\.\S+')
    cleaned_description = re.sub(url_pattern, '', cleaned_description)

    context = {
        'description': cleaned_description,
        'name': name,
        'symbol': symbol,
        # 'chart_data': chart_data,  # Pass the chart data to the template
    }
    
    # print(formatted_coin_details)
    return render(request, 'crypto_pulse/coin_details.html', context)


def test(request):
    binance_ws = BinanceWebSocket(template_name='crypto_pulse/test.html', coin_symbol='btcusdt', interval='1m')

    context = {
        'websocket_url': binance_ws.websocket_url,
    }
    return render(request, 'crypto_pulse/test.html', context)