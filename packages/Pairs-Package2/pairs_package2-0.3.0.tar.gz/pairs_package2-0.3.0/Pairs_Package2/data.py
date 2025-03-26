import pandas as pd
import os
import statsmodels.api as sm
from alpaca_trade_api.rest import REST, TimeFrame, Order, Account
from dotenv import load_dotenv

load_dotenv()


# # Replace with your Alpaca API credentials
# ALPACA_API_KEY = os.getenv("PAIRS_ALPACA_API_KEY","")
# ALPACA_API_SECRET = os.getenv("PAIRS_ALPACA_API_SECRET","")
# ALPACA_BASE_URL = os.getenv("ALPACA_BASE_URL","")

PAIRS_ALPACA_API_KEY = "PKAG2XN1QE6FKGQU2A1N"
PAIRS_ALPACA_API_SECRET = "feAY92yOdWTnocqm1VN5GyGBqUkwDw4wYDtI3p5L"
ALPACA_BASE_URL = "https://paper-api.alpaca.markets/"
# Initialize Alpaca API client
api = REST(PAIRS_ALPACA_API_KEY, PAIRS_ALPACA_API_SECRET, ALPACA_BASE_URL)

HEADERS = {
    "APCA-API-KEY-ID": PAIRS_ALPACA_API_KEY,
    "APCA-API-SECRET-KEY": PAIRS_ALPACA_API_SECRET
}

def fetch_data(symbol, start_date, end_date):
    """Fetch historical market data from Alpaca."""
    try:
        bars = api.get_bars(symbol, TimeFrame.Day, start=start_date, end=end_date).df
        bars.index = pd.to_datetime(bars.index)  # Ensure datetime format
        return bars
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return pd.DataFrame()

def calculate_residuals(stock1_prices, stock2_prices):
    stock2_with_const = sm.add_constant(stock2_prices)
    model = sm.OLS(stock1_prices, stock2_with_const)
    results = model.fit()
    residuals = results.resid
    return residuals

def calculate_macd(residuals, short_window=12, long_window=26, signal_window=9):
    short_ema = residuals.ewm(span=short_window, adjust=False).mean()
    long_ema = residuals.ewm(span=long_window, adjust=False).mean()
    macd_line = short_ema - long_ema
    signal_line = macd_line.ewm(span=signal_window, adjust=False).mean()
    macd_histogram = macd_line - signal_line
    return macd_line, signal_line, macd_histogram
