import yfinance as yf
import pandas as pd

def get_stock_data(ticker: str, period="6mo", interval="1d") -> pd.DataFrame:
    """
    Fetch stock data using yf.Ticker().history() to avoid MultiIndex issues.
    Returns a clean, flat DataFrame with expected columns.
    """
    try:
        ticker_obj = yf.Ticker(ticker)
        data = ticker_obj.history(period=period, interval=interval, auto_adjust=False)

        if data.empty:
            raise ValueError("No data returned from Yahoo Finance.")

        data.reset_index(inplace=True)

        # Rename columns to lowercase
        data.columns = [col.lower() for col in data.columns]

        # Print for debug
        print(f"[DEBUG] Final stock DataFrame columns: {data.columns.tolist()}")

        # Required columns
        required_cols = ['date', 'open', 'high', 'low', 'close', 'volume']
        missing = [col for col in required_cols if col not in data.columns]
        if missing:
            raise KeyError(f"Missing columns: {missing}")

        return data[required_cols]

    except Exception as e:
        print(f"[ERROR] Failed to fetch data for {ticker}: {e}")
        return pd.DataFrame()
