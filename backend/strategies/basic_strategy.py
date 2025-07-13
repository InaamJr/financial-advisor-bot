import pandas as pd

def apply_moving_average_strategy(df: pd.DataFrame, short_window=10, long_window=50) -> pd.DataFrame:
    """
    Adds moving average crossover strategy signals and signal strength to the DataFrame.

    Parameters:
    - short_window: short period MA (e.g. 10 days)
    - long_window: long period MA (e.g. 50 days)

    Returns:
    - DataFrame with 'signal' and 'signal_strength' columns:
        'signal': 1 = Buy, -1 = Sell, 0 = Hold
        'signal_strength': absolute difference between short and long MA
    """
    if df.empty or 'close' not in df.columns:
        print("[ERROR] DataFrame empty or missing 'close' column.")
        return df

    df = df.copy()

    # ✅ Format the date if present
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')

    # ✅ Calculate short and long MAs
    df['sma_short'] = df['close'].rolling(window=short_window, min_periods=1).mean().round(2)
    df['sma_long'] = df['close'].rolling(window=long_window, min_periods=1).mean().round(2)

    # ✅ Generate trading signal
    df['signal'] = df.apply(
        lambda row: 1 if row['sma_short'] > row['sma_long'] else (-1 if row['sma_short'] < row['sma_long'] else 0),
        axis=1
    )

    # ✅ Add signal strength (difference between SMAs)
    df['signal_strength'] = (df['sma_short'] - df['sma_long']).abs().round(2)

    return df
