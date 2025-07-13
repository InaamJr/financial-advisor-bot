import ccxt
import pandas as pd
from datetime import datetime, timedelta

def get_crypto_data(symbol='BTC/USDT', timeframe='1d', limit=100):
    """
    Fetch OHLCV crypto data using ccxt (default: BTC/USDT daily candles).
    """
    exchange = ccxt.binance()
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    except Exception as e:
        print(f"[ERROR] Failed to fetch data for {symbol}: {e}")
        return pd.DataFrame()
