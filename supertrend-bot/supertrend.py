import ccxt
import pandas as pd

exchange = ccxt.binance()

bars = exchange.fetch_ohlcv('ETH/USDT', limit = 30, timeframe='15m')
df = pd.DataFrame(bars[:-1], columns=['timestamp','open','high','low','close','volume'])
# df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

def tr(df):
    df['previous_close'] = df['close'].shift(1)
    df['high-low'] = df['high'] - df['low']
    df['high-pc'] = abs(df['high'] - df['previous_close'])
    df['low-pc'] = abs(df['low'] - df['previous_close'])
    tr = df[["high-low","high-pc",'low-pc']].max(axis=1)
    return tr

def atr(df, period = 14):
    df['tr'] = tr(df)
    df['atr'] = df['tr'].rolling(period).mean()

    return df

def supertrend(df, period = 14, multiplier=3.0):
    df['atr'] = atr(df,period=period)
    df['basic_upperband'] = ((df['high'] + df['low']) / 2) + (multiplier*df['atr'])
    df['basic_lowerband'] = ((df['high'] + df['low']) / 2) - (multiplier*df['atr'])
    return df

supertrend(df)
