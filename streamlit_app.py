import streamlit as st
import pandas as pd

from lightweight_charts.widgets import StreamlitChart
from st_screen_stats import ScreenData

from history_data import get_data

screenD = ScreenData(setTimeout=1000)
screen_stats = screenD.st_screen_data()

width = screen_stats['innerWidth'] * 0.88 - screen_stats['innerWidth'] * 0.2
height = screen_stats['innerHeight'] * 0.8

# Dashboard styling
with open(".streamlit/styles.css") as f:
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

with st.container(horizontal_alignment="center"):
    chart = StreamlitChart(
        height=screen_stats['innerHeight'] * 0.7,
        width=screen_stats['innerWidth'] * 0.95,
    )

    chart.layout(background_color="#0a0a0a", text_color="#ffffff")
    chart.grid(vert_enabled=False, horz_enabled=False)

    chart.set(pd.DataFrame(get_data("SOL", "USDT", interval)).sort_values(by='time'))
    chart.load()
