import datetime

from pybit.unified_trading import HTTP

session = HTTP(testnet=False)

def get_data(coin, base_coin, timeframe, limit=2000):

    symbol = coin + base_coin

    result = session.get_kline(
        category="linear",
        symbol=symbol,
        interval=timeframe,
        limit=limit
    )

    data = []
    for kline in result['result']['list']:
        row = {
            "time": datetime.datetime.fromtimestamp(float(kline[0]) / 1000).strftime('%Y-%m-%d %H:%M:%S'),
            "open": float(kline[1]),
            "high": float(kline[2]),
            "low": float(kline[3]),
            "close": float(kline[4]),
            "volume": float(kline[5]),
        }
        data.append(row)

    return data
