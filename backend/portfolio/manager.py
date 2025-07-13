import pandas as pd

class PortfolioManager:
    def __init__(self, initial_cash=10000):
        self.cash = initial_cash
        self.position = 0  # number of shares
        self.trade_log = []

    def execute_trades(self, df: pd.DataFrame) -> pd.DataFrame:
        equity_curve = []
        for idx, row in df.iterrows():
            price = row["close"]
            signal = row["signal"]
            date = row["date"]

            # BUY signal
            if signal == 1 and self.cash >= price:
                qty = self.cash // price
                cost = qty * price
                self.cash -= cost
                self.position += qty
                self.trade_log.append((date, "BUY", qty, price))

            # SELL signal
            elif signal == -1 and self.position > 0:
                revenue = self.position * price
                self.cash += revenue
                self.trade_log.append((date, "SELL", self.position, price))
                self.position = 0

            # Log equity
            total_value = self.cash + self.position * price
            equity_curve.append({"date": date, "equity": total_value})

        return pd.DataFrame(equity_curve)

    def get_trade_log(self) -> pd.DataFrame:
        return pd.DataFrame(self.trade_log, columns=["date", "action", "quantity", "price"])
