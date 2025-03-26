import pandas as pd
import numpy as np
import yfinance as yf
from alpaca_trade_api.rest import REST
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.vector_ar.vecm import coint_johansen
from itertools import combinations
import warnings
import multiprocessing as mp
from functools import partial
from tqdm import tqdm
import os
import datetime as dt
from statsmodels.stats.multitest import multipletests

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# ALPACA_API_KEY = os.getenv("PAIRS_ALPACA_API_KEY","")
# ALPACA_API_SECRET = os.getenv("PAIRS_ALPACA_API_SECRET","")
# ALPACA_BASE_URL = os.getenv("ALPACA_BASE_URL","")  # Change to live URL if needed

PAIRS_ALPACA_API_KEY = "PKAG2XN1QE6FKGQU2A1N"
PAIRS_ALPACA_API_SECRET = "feAY92yOdWTnocqm1VN5GyGBqUkwDw4wYDtI3p5L"
ALPACA_BASE_URL = "https://paper-api.alpaca.markets/"

api = REST(PAIRS_ALPACA_API_KEY, PAIRS_ALPACA_API_SECRET, ALPACA_BASE_URL)

# Step 1: Get the list of S&P 500 tickers
def get_sp500_tickers():
    """
    Scrapes the list of S&P 500 tickers from Wikipedia.
    """
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    table = pd.read_html(url)
    df = table[0]
    tickers = df['Symbol'].tolist()
    # Replace dots with hyphens for Yahoo Finance compatibility
    tickers = [ticker.replace('.', '-') for ticker in tickers]
    return tickers

# Step 2: Fetch historical price data
def fetch_price_data(tickers, start_date, end_date):
    """
    Downloads adjusted closing prices for the given tickers and date range.
    Handles both single and multiple tickers.
    """
    data = yf.download(tickers, start=start_date, end=end_date, group_by='ticker', threads=True, auto_adjust=False)
    
    # If only one ticker is downloaded, yfinance returns a DataFrame with single-level columns
    if len(tickers) == 1:
        adj_close = data[['Adj Close']].rename(columns={'Adj Close': tickers[0]})
    else:
        # For multiple tickers, extract the 'Adj Close' from each ticker's group
        # This results in a DataFrame where each column is a ticker's 'Adj Close'
        adj_close = pd.concat([data[ticker]['Adj Close'] for ticker in tickers if (ticker in data.columns.get_level_values(0)) and ('Adj Close' in data[ticker].columns)], axis=1)
        adj_close.columns = [ticker for ticker in tickers if (ticker in data.columns.get_level_values(0)) and ('Adj Close' in data[ticker].columns)]
    
    return adj_close

# Step 3: Engle-Granger Cointegration Test for a Pair
def cointegration_test(pair, data, significance_level=0.05):
    """
    Performs the Engle-Granger two-step cointegration test on a pair of stocks.
    Returns the test results and necessary statistics.
    """
    stock1, stock2 = pair
    S1 = data[stock1].dropna()
    S2 = data[stock2].dropna()
    min_length = min(len(S1), len(S2))
    
    if min_length < 100:
        return None  # Insufficient data
    
    # Align the data
    S1 = S1[-min_length:]
    S2 = S2[-min_length:]
    
    try:
        # Step 1: Regression of S1 on S2
        S2_constant = sm.add_constant(S2)
        model = sm.OLS(S1, S2_constant)
        results = model.fit()
        residuals = results.resid
        r_squared = results.rsquared
        
        # Step 2: ADF test on residuals
        adf_result = adfuller(residuals)
        pvalue_adf = adf_result[1]
        
        # Step 3: Estimate Error Correction Model if ADF test is significant
        if pvalue_adf < significance_level:
            delta_S1 = S1.diff().dropna()
            delta_S2 = S2.diff().dropna()
            lagged_residuals = residuals.shift(1).dropna()
            min_length_ecm = min(len(delta_S1), len(delta_S2), len(lagged_residuals))
            delta_S1 = delta_S1[-min_length_ecm:]
            delta_S2 = delta_S2[-min_length_ecm:]
            lagged_residuals = lagged_residuals[-min_length_ecm:]
            
            # ECM: ΔS2_t = γ₀ + γ₁ΔS1_t + γ₂û_{t-1} + v_t
            X = pd.DataFrame({
                'delta_S1': delta_S1.values,
                'lagged_residuals': lagged_residuals.values
            })
            X_constant = sm.add_constant(X)
            ecm_model = sm.OLS(delta_S2.values, X_constant)
            ecm_results = ecm_model.fit()
            gamma2 = ecm_results.params['lagged_residuals']
            gamma2_pvalue = ecm_results.pvalues['lagged_residuals']
            
            # Check if γ₂ is negative and significant
            if gamma2 < 0 and gamma2_pvalue < significance_level:
                return {
                    'Stock1': stock1,
                    'Stock2': stock2,
                    'ADF p-value': pvalue_adf,
                    'γ₂': gamma2,
                    'γ₂ p-value': gamma2_pvalue,
                    'R-squared': r_squared,
                    'residuals': residuals,
                    'S1': S1,
                    'S2': S2,
                    'ECM_results': ecm_results
                }
    except Exception as e:
        # Handle exceptions (e.g., numerical issues)
        return None
    return None

# Step 4: Find Cointegrated Pairs with Parallel Processing and Multiple Testing Correction
def find_cointegrated_pairs_parallel(data, significance_level=0.05, n_jobs=None, correction_method='bonferroni'):
    """
    Finds all cointegrated pairs using parallel processing.
    Applies Bonferroni or FDR correction for multiple testing.
    """
    tickers = data.columns.tolist()
    pairs = list(combinations(tickers, 2))
    total_tests = len(pairs)
    
    print(f"Total pairs to test: {total_tests}")
    
    # Prepare multiprocessing pool
    if n_jobs is None:
        n_jobs = max(mp.cpu_count() - 7, 1)  # Leave one CPU free
    pool = mp.Pool(processes=n_jobs)
    
    # Partial function with fixed data and initial significance_level
    func = partial(cointegration_test, data=data, significance_level=significance_level)
    
    # Use tqdm for progress bar
    results = []
    for result in tqdm(pool.imap_unordered(func, pairs), total=total_tests):
        if result is not None:
            results.append(result)
    
    pool.close()
    pool.join()
    
    # Extract p-values for multiple testing correction
    p_values = [pair['ADF p-value'] for pair in results]
    
    if correction_method.lower() == 'fdr':
        # Apply Benjamini-Hochberg FDR correction
        reject, pvals_corrected, _, _ = multipletests(p_values, alpha=significance_level, method='fdr_bh')
        # Filter pairs based on FDR rejection
        corrected_results = []
        for i, pair in enumerate(results):
            if reject[i]:
                pair['Adjusted ADF p-value'] = pvals_corrected[i]
                corrected_results.append(pair)
        results = corrected_results
        print(f"Number of cointegrated pairs after FDR correction: {len(results)}")
    elif correction_method.lower() == 'bonferroni':
        # Bonferroni is already applied during testing by adjusting the significance_level
        print(f"Number of cointegrated pairs after Bonferroni correction: {len(results)}")
    else:
        print("Invalid correction method specified. No correction applied.")
    
    return results

def get_unique_stocks_from_pairs(pairs):
    """
    Extracts the unique stock symbols from a list of pairs.
    """
    unique_stocks = set()
    for pair in pairs:
        unique_stocks.add(pair['Stock1'])
        unique_stocks.add(pair['Stock2'])
    return list(unique_stocks)

# Step 6: Johansen Cointegration Test
def johansen_cointegration_test(data, det_order=0, k_ar_diff=1):
    """
    Performs the Johansen cointegration test on a multivariate time series.
    Returns the test results.
    """
    result = coint_johansen(data, det_order=det_order, k_ar_diff=k_ar_diff)
    return result

# Step 7: Main Execution Function
def get_cointegrated_pairs(start_date,end_date):
    # Step 1: Get tickers
    tickers = get_sp500_tickers()
    print(f"Total tickers retrieved: {len(tickers)}")

    # Use few tickers for testing
    tickers = tickers

    # Step 2: Fetch price data
    print(f"Fetching price data from {start_date} to {end_date}...")
    data = fetch_price_data(tickers, start_date, end_date)

    # Check if data is empty
    if data.empty:
        print("No data fetched. Please check the tickers and date range.")
        return
    
    # Clean data by dropping tickers with missing data
    initial_tickers = data.shape[1]
    data = data.dropna(axis=1)
    cleaned_tickers = data.shape[1]
    print(f"Tickers after dropping those with missing data: {cleaned_tickers} (Dropped {initial_tickers - cleaned_tickers})")
    
    if cleaned_tickers < 2:
        print("Not enough tickers with complete data to form pairs.")
        return
    
    # Step 3: Find cointegrated pairs with parallel processing and multiple testing corrections
    print("Performing Engle-Granger cointegration tests on all pairs with parallel processing...")
    
    # Choose correction method: 'bonferroni' or 'fdr'
    correction_method = 'bonferroni'  # Change to 'fdr' if desired
    cointegrated_pairs = find_cointegrated_pairs_parallel(data, significance_level=0.05, correction_method=correction_method)
    print(f"Number of cointegrated pairs found: {len(cointegrated_pairs)}")
    
    if not cointegrated_pairs:
        print("No cointegrated pairs found with the specified significance level and correction method.")
        return
    
    # Step 4: Save results to CSV
    results_df = pd.DataFrame(cointegrated_pairs)
    
    # Reorder columns for better readability
    cols_order = ['Stock1', 'Stock2', 'ADF p-value', 'γ₂', 'γ₂ p-value', 'R-squared']
    results_df = results_df[cols_order]
    
    # Save both original and corrected p-values if FDR is applied
    if correction_method.lower() == 'fdr':
        results_df['Adjusted ADF p-value'] = [pair['Adjusted ADF p-value'] for pair in cointegrated_pairs]
    
    weak_pairs_df = results_df[results_df['R-squared'] < 0.8]
    
    # Generate correlation matrix for final selected pairs
    print("Generating correlation matrix for selected cointegrated pairs...")
    
    # Step 6: Evaluate Cointegration Strength
    # For example, filter pairs with R-squared above a certain threshold
    strong_pairs_df = results_df[results_df['R-squared'] > 0.8] #0.85 if wanna find fewer and stronger pairs found
    save_dir = os.path.join(os.path.expanduser('~'), ".pairs_package2")
    os.makedirs(save_dir, exist_ok=True)
    csv_path = os.path.join(save_dir, "strong_cointegrated_pairs.csv")
    strong_pairs_df.to_csv(csv_path, index=False)
    print("Strong cointegrated pairs saved to 'strong_cointegrated_pairs.csv'")