import websocket
import threading
import logging

class BinanceWebSocket:
    def __init__(self, template_name, coin_symbol, interval):
        self.template_name = template_name
        self.coin_symbol = coin_symbol
        self.interval = interval
        self.websocket_url = f'wss://stream.binance.com:9443/ws/{coin_symbol}@kline_{interval}'
        self.ws = websocket.WebSocketApp(self.websocket_url, on_message=self.on_message)

        # Set up logging to display WebSocket messages in the CLI
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
        self.logger = logging.getLogger(__name__)

        # Start the WebSocket connection in a separate thread
        self.websocket_thread = threading.Thread(target=self.run_forever)
        self.websocket_thread.daemon = True  # This allows the thread to be terminated when the main thread (Django view) exits
        self.websocket_thread.start()

    def run_forever(self):
        self.ws.run_forever()

    def on_message(self, ws, message):
        # Process the received data and pass it to the template for rendering
        # Your data processing code goes here
        # You can use Django's template rendering to update the 'test.html' file
        # Example: render_template(self.template_name, processed_data)

        # Log the message in the CLI
        self.logger.info(message)
