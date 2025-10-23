import datetime, json

from time import sleep

from pybit.unified_trading import WebSocket
import pandas as pd

ws = WebSocket(
    testnet=False,
    channel_type="linear"
)

def map_timeframe_to_interval(timeframe: str) -> str:
    mapping = {
        '1m': '1',
        '5m': '5',
        '1h': '60',
        '4h': '240',
        '1d': 'D'
    }
    return mapping.get(timeframe, '5')

def handle_realtime_data(message):
    print("Received message:", message)

    row = {
        "time": datetime.datetime.fromtimestamp(float(message["data"][0]["start"]) / 1000).strftime('%Y-%m-%d %H:%M:%S'),
        "open": float(message["data"][0]["open"]),
        "high": float(message["data"][0]["high"]),
        "low": float(message["data"][0]["low"]),
        "close": float(message["data"][0]["close"]),
        "volume": float(message["data"][0]["volume"]),
    }
    kline = pd.Series(row)
    print("Received kline:", kline)


ws.kline_stream(
    symbol="SOLUSDT",
    interval=map_timeframe_to_interval(5),
    callback=handle_realtime_data
)

while True:
    sleep(1)