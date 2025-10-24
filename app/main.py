import os, sys
import streamlit as st
import pandas as pd

from lightweight_charts.widgets import StreamlitChart
from st_screen_stats import ScreenData

# Add the project root to the Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(script_dir, "..")
sys.path.append(os.path.abspath(project_root))

from src.api.bybit.history_data import get_data

screenD = ScreenData(setTimeout=1000)
screen_stats = screenD.st_screen_data()

width = screen_stats['innerWidth'] * 0.88 - screen_stats['innerWidth'] * 0.2
height = screen_stats['innerHeight'] * 0.8

# Dashboard styling
with open("./.streamlit/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(layout="wide")

st.title("Crypto Trading Analysis Dashboard")
st.write("")

interval = "5"

# Data Preparation
def map_timeframe_to_interval(timeframe: str) -> str:
    mapping = {
        '1m': '1',
        '5m': '5',
        '1h': '60',
        '4h': '240',
        '1d': 'D'
    }
    return mapping.get(timeframe, '5')


with st.container(horizontal_alignment="left"):

    option_map = {
        0: "1m",
        1: "5m",
        2: "1h",
        3: "4h",
        4: "1d"
    }

    timeframe_switch = st.segmented_control(
        default=1,
        label="Timeframe",
        label_visibility="collapsed",
        options=option_map.keys(),
        format_func=lambda option: option_map[option],
        selection_mode="single",
    )

# Update interval based on selection
if timeframe_switch is not None:
    interval = map_timeframe_to_interval(option_map[timeframe_switch])

def data_loader():
    # load base data
    base_data = pd.DataFrame(get_data("SOL", "USDT", interval)).sort_values(by='time')

    # extend time series into the future
    max_time = pd.to_datetime(base_data['time'].max())
    start_time = max_time + pd.Timedelta(minutes=int(interval) if interval not in ['D'] else 1440)
    future_time_series = pd.date_range(
        start=start_time,
        periods=100,
        freq=f"{interval}min" if interval not in ['D'] else 'D')
    extend_time = pd.DataFrame({'time': future_time_series})

    # combine base data with extended time series
    return pd.concat([base_data, extend_time], ignore_index=True)

with st.container(horizontal_alignment="center"):
    chart = StreamlitChart(
        height=screen_stats['innerHeight'] * 0.7,
        width=screen_stats['innerWidth'] * 0.95
    )

    chart.layout(background_color="#0a0a0a", text_color="#ffffff")
    chart.grid(vert_enabled=False, horz_enabled=False)

    chart.set(data_loader())
    chart.load()
