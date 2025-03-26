from Pairs_Package2.signals import generate_trading_signals_macd, rolling_betas, beta_neutral_weights, normalize_weights
from Pairs_Package2.data import fetch_data
from Pairs_Package2.broker_info import get_pairs_net_liquidation
from Pairs_Package2.cointegration import get_cointegrated_pairs
import statsmodels.api as sm
import os
from datetime import datetime, timedelta
import sys
import pandas as pd
import requests
from alpaca_trade_api.rest import REST, TimeFrame, Order, Account
from dotenv import load_dotenv

load_dotenv()

# # Replace with your Alpaca API credentials
# ALPACA_API_KEY = os.getenv("PAIRS_ALPACA_API_KEY","")
# ALPACA_API_SECRET = os.getenv("PAIRS_ALPACA_API_SECRET","")
# ALPACA_BASE_URL = os.getenv("ALPACA_BASE_URL","")

# Initialize Alpaca API client
PAIRS_ALPACA_API_KEY = "PKAG2XN1QE6FKGQU2A1N"
PAIRS_ALPACA_API_SECRET = "feAY92yOdWTnocqm1VN5GyGBqUkwDw4wYDtI3p5L"
ALPACA_BASE_URL = "https://paper-api.alpaca.markets/"
# Initialize Alpaca API client
api = REST(PAIRS_ALPACA_API_KEY, PAIRS_ALPACA_API_SECRET, ALPACA_BASE_URL)

HEADERS = {
    "APCA-API-KEY-ID": PAIRS_ALPACA_API_KEY,
    "APCA-API-SECRET-KEY": PAIRS_ALPACA_API_SECRET
}


# Here we want to generate our signals table. 
#--------------------------------------------------------------------------------------------
def generate_signals_table(stock1_prices, stock2_prices, residuals, market_returns):
    """
    Generate a signals table that follows the backtest_pair logic:
      - Uses MACD-based signals derived from residuals.
      - Uses rolling beta estimates to compute beta-neutral weights.
      - Assigns positions as:
            * For a long residual signal: long stock1 and short stock2.
            * For a short residual signal: short stock1 and long stock2.
      - Forces positions to zero when exit signals are active.
      - Shifts the signals to avoid lookahead bias.
    
    Parameters:
      stock1_prices, stock2_prices: pd.Series with .name attributes set to the respective symbols.
      residuals: pd.Series from the OLS regression residuals.
      market_returns: DataFrame (or Series) of benchmark returns (with a 'SPY' column for rolling beta).
      zscore_threshold: Parameter passed to generate_trading_signals_macd (used here as the MACD threshold).
    
    Returns:
      signals_table: pd.DataFrame containing beta-weighted positions for each stock.
    """
    # Generate MACD-based signals
    long_signals, short_signals, exit_signals = generate_trading_signals_macd(residuals, threshold = 0.02)

    # Create boolean DataFrames for trade entries
    long_entries = pd.DataFrame(False, index=stock1_prices.index, columns=[stock1_prices.name, stock2_prices.name])
    short_entries = pd.DataFrame(False, index=stock1_prices.index, columns=[stock1_prices.name, stock2_prices.name])
    exit_positions = pd.DataFrame(False, index=stock1_prices.index, columns=[stock1_prices.name, stock2_prices.name])
 
    # Combine signals into a single DataFrame for clarity
    long_short_exit_pair = pd.concat([long_signals, short_signals, exit_signals], axis=1)
    long_short_exit_pair.columns = ["Long", "Short", "Exit"]
    

    # Signal assignment:
    # - When the residual is “short” (i.e. short_signals True): 
    #       • Long the second stock and short the first.
    # - When the residual is “long” (i.e. long_signals True):
    #       • Long the first stock and short the second.
    long_entries.loc[long_short_exit_pair['Short'], stock2_prices.name] = True
    short_entries.loc[long_short_exit_pair['Short'], stock1_prices.name] = True
    long_entries.loc[long_short_exit_pair['Long'], stock1_prices.name] = True
    short_entries.loc[long_short_exit_pair['Long'], stock2_prices.name] = True
    exit_positions.loc[long_short_exit_pair['Exit'], stock1_prices.name] = True
    exit_positions.loc[long_short_exit_pair['Exit'], stock2_prices.name] = True

    # Compute rolling betas from percentage returns
    stock1_returns = stock1_prices.pct_change().dropna()
    stock2_returns = stock2_prices.pct_change().dropna()
   
    rolling_beta_1, rolling_beta_2 = rolling_betas(stock1_returns, stock2_returns, market_returns)
    market_returns = market_returns
    
    # Compute beta-neutral weights (assumes rolling_beta_* have a column 'SPY')
    common_index = rolling_beta_1.dropna().index
    weights = []
    for ts in common_index:
        beta1 = rolling_beta_1.loc[ts, 'SPY']
        beta2 = rolling_beta_2.loc[ts, 'SPY']
        w1_n, w2_n = beta_neutral_weights(beta1, beta2)
        w1, w2 = normalize_weights(w1_n, w2_n)
        weights.append((w1, w2))
    weights_df = pd.DataFrame(weights, index=common_index, columns=[stock1_prices.name, stock2_prices.name])

    signals_table = pd.concat(
    [weights_df.abs(), long_entries, short_entries, exit_positions],
    axis=1,
    join='outer', 
    keys=['Weights', 'Long Entries', 'Short Entries', 'Exit Positions'])

    # # # Reindex to match the full price series and drop any missing values; then shift to avoid lookahead bias.
    # signals_table = weights_df.reindex(stock1_prices.index, method='nearest').dropna().shift(1)

    return signals_table

## Now we want to actually interact with the API to place our orders etc.

def is_shortable(symbol):
    """
    Checks if a stock is shortable (easy to borrow) through Alpaca API.
    
    Parameters:
        symbol (str): The stock symbol to check
        
    Returns:
        bool: True if the stock is shortable, False otherwise
    """
    try:
        # Get asset information from Alpaca
        asset = api.get_asset(symbol)
        
        # Check if the asset is shortable (easy to borrow)
        return asset.easy_to_borrow
    except Exception as e:
        print(f"Error checking if {symbol} is shortable: {e}")
        return False


#First we want to get the actual value of the portfolio of the two pairs.
def get_account_info():
    account = api.get_account()
    return float(account.equity)  # Returns current account equity

#Next, we create a function to ajust position of the current stock pairs that we have that we have 
def adjust_position(symbol, target_allocation):
    """
    Adjusts the position in a symbol to match the target dollar allocation.
    Uses recent bar data (previous close) to compute how many shares to trade.
    
    Parameters:
        symbol (str): The stock symbol to adjust
        target_allocation (float): Target dollar amount allocation (negative for short)
    """
    try:
        bars = api.get_bars(symbol, TimeFrame.Day, limit=5, start=datetime.today().date()-timedelta(days=6), end=datetime.today().date()-timedelta(days=1)).df
        if bars.empty:
            print(f"Skipping {symbol}: no price data available.")
            return

        previous_close = bars.iloc[-1].close
        target_shares = int(target_allocation // previous_close)
        
        try:
            position = api.get_position(symbol)
            current_shares = int(float(position.qty))
        except Exception:
            current_shares = 0

        share_diff = target_shares - current_shares
        if share_diff > 0:
            api.submit_order(
                symbol=symbol,
                qty=share_diff,
                side="buy",
                type="market",
                time_in_force="gtc"
            )
            print(f"BUY {share_diff} shares of {symbol} (target: {target_shares}).")
        elif share_diff < 0:
            api.submit_order(
                symbol=symbol,
                qty=abs(share_diff),
                side="sell",  # This creates a short position if selling more than owned
                type="market",
                time_in_force="gtc"
            )
            print(f"SELL {abs(share_diff)} shares of {symbol} (target: {target_shares}).")
        else:
            print(f"{symbol} is already at the target allocation ({target_shares} shares).")
    except Exception as e:
        print(f"Error adjusting position for {symbol}: {e}")


## Next we need an actual way to place orders to Alpaca:
def place_orders(df_orders):
    """
    Expects a DataFrame with columns "Symbol" and "Dollar Allocation".
    Iterates over each row to adjust the position.
    """
    for _, row in df_orders.iterrows():
        adjust_position(row["Symbol"], row["Dollar Allocation"])

## As well as a way to close positions
def close_positions(new_portfolio_df):
    """
    Closes any open positions for symbols that are not in the new portfolio.
    """
    try:
        positions = api.list_positions()
        new_symbols = set(new_portfolio_df["Symbol"])
        for position in positions:
            if position.symbol not in new_symbols:
                qty = abs(int(float(position.qty)))
                side = "sell" if position.side == "long" else "buy"
                api.submit_order(
                    symbol=position.symbol,
                    qty=qty,
                    side=side,
                    type="market",
                    time_in_force="gtc"
                )
                print(f"Closing position for {position.symbol}: {side.upper()} {qty} shares.")
        print("Closed positions not in the new portfolio.")
    except Exception as e:
        print(f"Error closing positions: {e}")

def send_daily_pair_trade(stock1_ticker, stock2_ticker, equity, allocation_multiplier=1.0):
    """
    Generates beta‑weighted pair trade signals using our custom generate_signals_table function,
    then sends orders via Alpaca based on the most recent signal.
    
    Parameters:
      stock1_ticker: Ticker symbol for the first stock
      stock2_ticker: Ticker symbol for the second stock
      allocation_multiplier: Fraction of total equity to allocate
    """

    # Define date range
    end_date = (datetime.today() - timedelta(1)).strftime("%Y-%m-%d")
    start_date = (datetime.today() - timedelta(100)).strftime("%Y-%m-%d")
    benchmark_ticker = "SPY"  # Using S&P 500 as the benchmark
    
    # Check if stocks are shortable first, before doing any other processing
    stock1_shortable = is_shortable(stock1_ticker)
    stock2_shortable = is_shortable(stock2_ticker)
    
    # print(f"{stock1_ticker} shortable: {stock1_shortable}")
    # print(f"{stock2_ticker} shortable: {stock2_shortable}")
    
    # If either stock is not shortable, exit immediately
    if not stock1_shortable or not stock2_shortable:
        print(f"ERROR: One or both stocks in the pair are not shortable.")
        print(f"{stock1_ticker} shortable: {stock1_shortable}")
        print(f"{stock2_ticker} shortable: {stock2_shortable}")
        print("Exiting program as pairs trading requires ability to short both stocks.")
        return
    
    # Fetch price data from Alpaca
    stock1_bars = fetch_data(stock1_ticker, start_date, end_date)
    stock2_bars = fetch_data(stock2_ticker, start_date, end_date)
    benchmark_bars = fetch_data(benchmark_ticker, start_date, end_date)
    
    if stock1_bars.empty or stock2_bars.empty or benchmark_bars.empty:
        print("Error: Could not fetch sufficient price data for one or more symbols.")
        return
    
    # Extract closing prices and set the .name attribute
    stock1_prices = stock1_bars["close"].copy()
    stock2_prices = stock2_bars["close"].copy()
    stock1_prices.name = stock1_ticker
    stock2_prices.name = stock2_ticker
    
    # Compute regression residuals (OLS of stock1 on stock2)
    stock2_const = sm.add_constant(stock2_prices)
    model = sm.OLS(stock1_prices, stock2_const)
    results = model.fit()
    residuals = results.resid
    
    # Compute benchmark returns from the closing prices of the benchmark
    benchmark_prices = benchmark_bars["close"]
    benchmark_returns = benchmark_prices.pct_change().dropna().to_frame(name="SPY")

    # Generate the signals table (with multi-index columns)
    signals_table = generate_signals_table(stock1_prices, stock2_prices, residuals, benchmark_returns)
    
    # Print the signals table for reference
    print("Generated signals table:")
    print(signals_table.tail())

    # Get the latest signals row (which contains multi-index columns)
    latest_signal = signals_table.iloc[-1]
    
    # Extract the signals from the multi-index
    latest_weights = latest_signal["Weights"]
    latest_long_entries = latest_signal["Long Entries"]
    latest_short_entries = latest_signal["Short Entries"]
    latest_exit_positions = latest_signal["Exit Positions"]
    
    # # Get current account equity
    # equity = get_account_info()
    
    # Determine target allocations for each symbol based on the signal
    def get_target_allocation(ticker):
        if latest_exit_positions.get(ticker, False):
            return 0.0
        elif latest_long_entries.get(ticker, False):
            return allocation_multiplier * equity * latest_weights.get(ticker, 0)
        elif latest_short_entries.get(ticker, False):
            return -allocation_multiplier * equity * latest_weights.get(ticker, 0)
        else:
            return 0.0

    target_allocation_stock1 = get_target_allocation(stock1_ticker)
    target_allocation_stock2 = get_target_allocation(stock2_ticker)
  
    # Create a DataFrame of orders with the proper target dollar allocations
    df_orders = pd.DataFrame({
        "Symbol": [stock1_ticker, stock2_ticker],
        "Dollar Allocation": [target_allocation_stock1, target_allocation_stock2]
    })
    
    print("Placing orders based on latest signals:")
    print(df_orders)
    
    # Place orders and then close positions that are not in the new portfolio
    place_orders(df_orders)
    # close_positions(df_orders)

def close_old_positions(pairs):
    try:
        positions = api.list_positions()
        new_portfolio_symbols = set([x for x in pairs['Stock1']]+[x for x in pairs['Stock2']])
        for position in positions:
            symbol = position.symbol

            if symbol not in new_portfolio_symbols:
                qty = abs(int(float(position.qty)))
                side = 'sell' if position.side == 'long' else 'buy'

                api.submit_order(
                    symbol=symbol, 
                    qty=qty,
                    side=side,
                    type='market',
                    time_in_force='gtc'
                )
                print(f"Closing {side.upper()} order for {qty} shares of {symbol} (not in new portfolio).")
        print("Unwanted positions have been closed.")
    except Exception as e:
        print(f"Error closing positions: {e}")

def daily_pairs_run():
    today = datetime.today().date()

    if today.day == 1:
        try:
            end_date = today - timedelta(days=1)
            end_date = end_date.strftime("%Y-%m-%d")
            start_date = today - timedelta(days=731)
            start_date = start_date.strftime("%Y-%m-%d")
            get_cointegrated_pairs(start_date=start_date, end_date=end_date)

            csv_path = os.path.join(os.path.expanduser('~'), ".pairs_package2", 'strong_cointegrated_pairs.csv')

            if not os.path.exists(csv_path):
                raise FileNotFoundError(f"CSV file not found at {csv_path}")
            
            pairs = pd.read_csv(csv_path)
            

            balance = get_pairs_net_liquidation()

            pairs['Notional'] = balance/len(pairs)
            pairs = pairs[['Stock1', 'Stock2', 'Notional']]
            pairs['Stock1'] = [x.replace('-','.') for x in pairs['Stock1']]
            pairs['Stock2'] = [x.replace('-','.') for x in pairs['Stock2']]
            close_old_positions(pairs)
            for index, row in pairs.iterrows():
                send_daily_pair_trade(row['Stock1'], row['Stock2'], row['Notional'], allocation_multiplier=1.0)
        except Exception as e:
            print(e)
    else:
            
        csv_path = os.path.join(os.path.expanduser('~'), ".pairs_package2", 'strong_cointegrated_pairs.csv')

        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found at {csv_path}")
        
        pairs = pd.read_csv(csv_path)


        balance = get_pairs_net_liquidation()

        pairs['Notional'] = balance/len(pairs)
        pairs = pairs[['Stock1', 'Stock2', 'Notional']]
        pairs['Stock1'] = [x.replace('-','.') for x in pairs['Stock1']]
        pairs['Stock2'] = [x.replace('-','.') for x in pairs['Stock2']]

        for index, row in pairs.iterrows():
            send_daily_pair_trade(row['Stock1'], row['Stock2'], row['Notional'], allocation_multiplier=1.0)