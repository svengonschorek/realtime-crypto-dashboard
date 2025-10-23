import pandas as pd
import asyncio, threading

from lightweight_charts import Chart

from reatime_data import WebSocketManager
from history_data import get_data


ws_thread = None
ws_manager = None

def map_timeframe_to_interval(timeframe: str) -> str:
    mapping = {
        '1m': '1',
        '5m': '5',
        '1h': '60',
        '4h': '240',
        '1d': 'D'
    }
    return mapping.get(timeframe, '5')

def calculate_sma(df, period: int = 50):
    return pd.DataFrame({
        'time': df['time'],
        f'SMA {period}': df['close'].rolling(window=period).mean()
    }).dropna()

def start_ws(chart):
    global ws_manager

    def handle_realtime_data(row):
        chart.update(row)
    symbol = chart.topbar['Coin'].value + 'USDT'
    timeframe = chart.topbar['Timeframe'].value.lower()

    ws_manager = WebSocketManager(
        message_callback=handle_realtime_data, 
        symbol=symbol,
        timeframe=map_timeframe_to_interval(timeframe)
    )

def on_search(chart):
    new_data = pd.DataFrame(
        get_data(
            chart.topbar['Coin'].value,
            "USDT",
            map_timeframe_to_interval(chart.topbar['Timeframe'].value)
        )
    ).sort_values(by='time')

    chart.topbar['Coin'].set(chart.topbar['Coin'].value)
    chart.set(new_data)

    # Update SMA line
    sma_data = calculate_sma(new_data, period=50)
    if sma_line:
        sma_line.set(sma_data)

    # Stop previous WebSocketManager
    if ws_manager:
        ws_manager.close()

    # Start new WebSocketManager
    ws_thread = threading.Thread(target=start_ws, args=(chart,), daemon=True)
    ws_thread.start()

def on_timeframe_selection(chart):
    new_data = pd.DataFrame(
        get_data(
            chart.topbar['Coin'].value,
            "USDT",
            map_timeframe_to_interval(chart.topbar['Timeframe'].value))
        ).sort_values(by='time')
    chart.set(new_data)

    # Update SMA line
    sma_data = calculate_sma(new_data, period=50)
    if sma_line:
        sma_line.set(sma_data)

    # Stop previous WebSocketManager
    if ws_manager:
        ws_manager.close()

    # Start new WebSocketManager
    ws_thread = threading.Thread(target=start_ws, args=(chart,), daemon=True)
    ws_thread.start()

async def main():
    global ws_thread, sma_line

    chart = Chart()
    chart.legend(True)
    chart.events.search += on_search

    chart.topbar.textbox('Coin', 'SOL', func=on_search)
    chart.topbar.switcher('Timeframe', ('1m', '5m', '1h', '4h', '1d'), default='5m',
        func=on_timeframe_selection
    )

    # initial data load
    df = pd.DataFrame(
        get_data(
            chart.topbar['Coin'].value,
            "USDT",
            map_timeframe_to_interval(chart.topbar['Timeframe'].value)
        )
    ).sort_values(by='time')

    chart.set(df)

    # Show SMA 50 line
    sma_line = chart.create_line('SMA 50')
    sma_data = calculate_sma(df, period=50)
    sma_line.set(sma_data)

    # Start initial WebSocketManager
    ws_thread = threading.Thread(target=start_ws, args=(chart,), daemon=True)
    ws_thread.start()
    await chart.show_async()

if __name__ == "__main__":
    asyncio.run(main())
