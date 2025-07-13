import pandas as pd
from engine.explainer import natural_language_explanation  # ✅ Using Option A (non-LLM) explanation

def generate_advice(df: pd.DataFrame, symbol: str = "AAPL") -> str:
    """
    Generates a trading recommendation (BUY, SELL, HOLD) based on the latest signal.

    Parameters:
    - df: DataFrame with 'signal', 'sma_short', 'sma_long'
    - symbol: stock symbol string

    Returns:
    - Formatted natural language advice
    """

    # ✅ Validate input DataFrame
    if df.empty or 'signal' not in df.columns:
        return f"[ERROR] No valid data to generate advice for {symbol}."

    # ✅ Extract latest signal row
    latest = df.iloc[-1]
    signal = int(latest['signal'])

    # ✅ Determine action type
    if signal == 1:
        action = "BUY"
    elif signal == -1:
        action = "SELL"
    else:
        action = "HOLD"

    # ✅ Use our own natural explanation generator
    explanation = natural_language_explanation(
        signal=action,
        short_ma=latest['sma_short'],
        long_ma=latest['sma_long'],
        symbol=symbol
    )

    # ✅ Return combined message
    return f"📢 Recommendation: {action} {symbol.upper()}\n\n🧠 {explanation}"
