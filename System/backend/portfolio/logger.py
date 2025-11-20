import pandas as pd

def save_trade_log(trades: pd.DataFrame, filename="trade_log.csv"):
    trades.to_csv(filename, index=False)
    print(f"[LOG] Trade log saved to {filename}")

def save_equity_curve(equity: pd.DataFrame, filename="equity_curve.csv"):
    equity.to_csv(filename, index=False)
    print(f"[LOG] Equity curve saved to {filename}")
