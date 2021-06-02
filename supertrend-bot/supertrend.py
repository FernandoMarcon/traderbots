import ccxt, schedule, time, warnings
import numpy as np
from datetime import datetime
import pandas as pd

import sys
sys.path.insert(1, '../../Documents/exchange/')
import config


# Settings
pd.set_option('display.max_rows',None)
warnings.filterwarnings('ignore')

# Connection
exchange = ccxt.binance({
    "apiKey": config.API_KEY,
    "secret": config.API_SECRET
})

# print(exchange.fetch_balance())

# Functions
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
    df['upperband'] = ((df['high'] + df['low']) / 2) + (multiplier*df['atr'])
    df['lowerband'] = ((df['high'] + df['low']) / 2) - (multiplier*df['atr'])

    for current in range(1, len(df.index)):
        previous = current - 1
        df['in_uptrend'] = True

        if df['close'][current] > df['upperband'][previous]:
            df['in_uptrend'][current] = True
        elif df['close'][current] < df['lowerband'][previous]:
            df['in_uptrend'][current] = False
        else:
            df['in_uptrend'][current] = df['in_uptrend'][previous]

            if df['in_uptrend'][current] and df['lowerband'][current] < df['lowerband'][previous]:
                df['lowerband'][current] = df['lowerband'][previous]

            if not df['in_uptrend'][current] and df['upperband'][current] > df['upperband'][previous]:
                df['upperband'][current] = df['upperband'][previous]

    return df

# Bot
in_position = False
def  check_buy_sell_signals(df):
    global in_position

    print('checking for buys and sells')

    last_row_index = len(df.index) - 1
    previous_row_index = last_row_index - 1

    if not df['in_uptrend'][previous_row_index] and df['in_uptrend'][last_row_index]:
        if not in_position:
            print('changed to uptrend, buy')
            order = exchange.create_market_buy_order('ETH/USDT', 0.0000001)
            print(order)
            in_position = True
        else:
            print("Already in position, nothing to do")

    if df['in_uptrend'][previous_row_index] and not df['in_uptrend'][last_row_index]:
        if in_position:
            print('changed to downtrend, sell')
            order = exchange.create_market_sell_order('ETH/USDT', 1)
            print(order)
            in_position = False

def run_bot():
    print(f"Fetching new bars for {datetime.now().isoformat()}")
    bars = exchange.fetch_ohlcv('ETH/USDT', limit = 100, timeframe='1m')
    df = pd.DataFrame(bars[:-1], columns=['timestamp','open','high','low','close','volume'])

    supertrend_data = supertrend(df)
    check_buy_sell_signals(supertrend_data)

schedule.every(10).seconds.do(run_bot)

while True:
    schedule.run_pending()
    time.sleep(1)
