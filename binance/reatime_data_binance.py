import websocket, datetime, json, threading

import pandas as pd

class WebSocketManager:
    def __init__(self, message_callback=None, symbol=None, timeframe=None):
        websocket.enableTrace(False)
        self.message_callback = message_callback
        self.symbol = symbol
        self.timeframe = timeframe

        def on_message(ws, message):

            message = json.loads(message)

            row = {
                "time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "price": float(message['k']['c']),
                "volume": float(message['k']['v'])
            }

            if self.message_callback:
                self.message_callback(pd.Series(row))

        self.ws = websocket.WebSocketApp(
            url=f"wss://fstream.binance.com/ws/{self.symbol}@kline_{self.timeframe}",
            on_message=on_message
        )

        self._running = True
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()

    def run(self):
        while self._running:
            self.ws.run_forever(reconnect=5)

    def close(self):
        self._running = False
        if self.ws:
            self.ws.close()
