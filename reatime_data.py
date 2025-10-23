import websocket, datetime, threading, json

import pandas as pd

class WebSocketManager:
    def __init__(self, message_callback=None, symbol=None, timeframe=None):
        websocket.enableTrace(False)
        self.message_callback = message_callback
        self.symbol = symbol
        self.timeframe = timeframe

        def on_message(ws, message):
            data = json.loads(message)
            
            # Handle subscription confirmation
            if data.get("op") == "subscribe":
                print(f"Subscription confirmed: {data}")
                return
            
            # Handle kline data
            if "data" in data and len(data["data"]) > 0:
                row = {
                    "time": datetime.datetime.fromtimestamp(float(data["data"][0]["start"]) / 1000).strftime('%Y-%m-%d %H:%M:%S'),
                    "open": float(data["data"][0]["open"]),
                    "high": float(data["data"][0]["high"]),
                    "low": float(data["data"][0]["low"]),
                    "close": float(data["data"][0]["close"]),
                    "volume": float(data["data"][0]["volume"]),
                }

                if self.message_callback:
                    self.message_callback(pd.Series(row))
        
        def on_open(ws):
            # Subscribe to the topic when connection opens
            subscribe_message = {
                "op": "subscribe",
                "args": [f"kline.{self.timeframe}.{self.symbol}"]
            }
            ws.send(json.dumps(subscribe_message))
            print(f"Subscribed to kline.{self.timeframe}.{self.symbol}")
        
        def on_error(ws, error):
            print(f"WebSocket error: {error}")
        
        def on_close(ws, close_status_code, close_msg):
            print(f"WebSocket closed: {close_status_code} - {close_msg}")

        self.ws = websocket.WebSocketApp(
            url=f"wss://stream.bybit.com/v5/public/linear",
            on_message=on_message,
            on_open=on_open,
            on_error=on_error,
            on_close=on_close
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
