# Realtime Kline Dashboard

A Python application that visualizes cryptocurrency price data in real-time using Binance's WebSocket API and historical data endpoints.

## Features

- **Real-time price updates** - Live cryptocurrency price data via Binance WebSocket
- **Historical data** - Fetches historical kline/candlestick data from Binance
- **Interactive dashboard** - Built with lightweight-charts for smooth visualization  
- **Multiple timeframes** - Support for 1m, 5m, 1h, 4h, and 1d intervals
- **Technical indicators** - Simple Moving Average (SMA) overlay
- **Coin switching** - Search and switch between different cryptocurrencies

## Installation

1. Clone the repository:
```bash
git clone https://github.com/svengonschorek/realtime-crypto-dashboard.git

cd realtime-kline-dashboard
```

2. Install dependencies using uv:
```bash
uv sync
```

## Usage

Run the dashboard:
```bash
uv run dashboard.py
```

The application will open a web-based chart interface where you can:
- Search for different cryptocurrencies in the search box
- Switch between timeframes using the dropdown menu
- View live price updates and historical data with SMA indicator

## Dependencies

- `lightweight-charts` - Interactive financial charts
- `requests` - HTTP requests for historical data
- `websocket-client` - WebSocket client for real-time data
- `pandas` - Data manipulation and analysis

## Project Structure

- `dashboard.py` - Main application with chart setup and event handlers
- `crypto_history_data.py` - Fetches historical kline data from Binance API
- `crypto_reatime_data.py` - WebSocket manager for live price updates
- `pyproject.toml` - Project configuration and dependencies

## Data Sources

- Historical data: Binance Vision API (`https://data-api.binance.vision`)
- Real-time data: Binance WebSocket streams (`wss://fstream.binance.com`)
