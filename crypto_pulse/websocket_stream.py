import websocket

# websocket url binance
WEBSOCKET_BASE_URL = 'wss://stream.binance.com:9443/ws/'


socket_params = {
    'interval': '1m',
}


def on_message(ws, message):
    print(message)
    
    
def on_error(ws, error):
    print(error)
    
    
def on_close(ws, close_status_code, close_msg):
    print(close_msg)   
      
    
def websocket_stream(coin_symbol, params=socket_params):
    socket = f'{WEBSOCKET_BASE_URL}{coin_symbol}@kline_{params["interval"]}'
    
    ws = websocket.WebSocketApp(socket,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    
    ws.run_forever()


# Example usage:
if __name__ == "__main__":
    coin_symbol = 'btcusdt'
    websocket_stream(coin_symbol)