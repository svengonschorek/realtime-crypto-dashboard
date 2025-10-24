import os, sys
import streamlit as st

from st_screen_stats import ScreenData

# Add the project root to the Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(script_dir, "..")
sys.path.append(os.path.abspath(project_root))

from src.api.bybit.history_data import get_data
from src.components.charts.candlestick_chart import candlestick_chart

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

candlestick_chart(
    height=screen_stats['innerHeight'] * 0.65,
    width=screen_stats['innerWidth'] * 0.95
)
