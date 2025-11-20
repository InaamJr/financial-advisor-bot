import pandas as pd
import math

def backtest_strategy(df: pd.DataFrame, initial_cash: float = 10000.0):
    """
    Backtest a moving average crossover strategy based on generated signals.

    Args:
        df (pd.DataFrame): Stock price data with 'signal' column.
        initial_cash (float): Starting portfolio cash.

    Returns:
        tuple: (performance summary, trade log dataframe, equity curve dataframe)
    """
    df = df.copy()
    cash = initial_cash
    position = 0  # Number of shares held
    trade_log = []
    equity_curve = []
    buy_price = None  # To track the price at which we bought

    for i in range(1, len(df)):
        row = df.iloc[i]
        price = float(row['close'])
        signal = row['signal']
        date = str(row['date'])[:10]  # Convert to string for JSON

        # === BUY Signal ===
        if signal == 1 and position == 0:
            position = int(cash // price)  # Number of shares to buy
            buy_price = price
            cash -= position * price
            trade_log.append({
                "date": date,
                "action": "BUY",
                "price": round(price, 2),
                "shares": position,
                "cash": round(cash, 2)
            })

        # === SELL Signal ===
        elif signal == -1 and position > 0:
            pnl = 0.0
            if buy_price is not None:
                pnl = (price - buy_price) * position
                pnl = 0.0 if pd.isna(pnl) or math.isnan(pnl) else round(pnl, 2)

            cash += position * price
            trade_log.append({
                "date": date,
                "action": "SELL",
                "price": round(price, 2),
                "shares": position,
                "cash": round(cash, 2),
                "pnl": pnl
            })
            position = 0
            buy_price = None  # Reset buy_price after selling

        # === Track Equity Over Time ===
        equity = cash + (position * price)
        equity_curve.append({
            "date": date,
            "equity": round(equity, 2),
            "close": round(price, 2)
        })

    # === Final Portfolio Value (if position still open) ===
    if position > 0:
        final_price = float(df.iloc[-1]['close'])
        cash += position * final_price

    final_value = cash
    returns = ((final_value - initial_cash) / initial_cash) * 100

    # === Summary Report ===
    summary = {
        "Initial Cash": round(initial_cash, 2),
        "Final Value": round(final_value, 2),
        "Return (%)": round(returns, 2),
        "Total Trades": len(trade_log),
        "Profitable Trades": sum(1 for t in trade_log if t.get('pnl', 0) > 0),
        "Losing Trades": sum(1 for t in trade_log if t.get('pnl', 0) < 0),
    }

    # Convert logs to DataFrames and replace NaN values with 0
    trade_df = pd.DataFrame(trade_log).fillna(0)
    equity_df = pd.DataFrame(equity_curve).fillna(0)

    num_buys = sum(1 for t in trade_log if t["action"] == "BUY")
    num_sells = sum(1 for t in trade_log if t["action"] == "SELL")
    print(f"[DEBUG] Number of BUYs: {num_buys}, SELLs: {num_sells}")

    return summary, trade_df, equity_df
