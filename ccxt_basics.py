# CryptoCurrency eXchange Trading
sys.path.insert(1, '../../Documents/exchange/')
import ccxt, sys, config

print(ccxt.exchanges)

exchange = ccxt.binance({
    'apiKey' : config.API_KEY,
    'secret' : config.API_SECRET
})

# Get all coin pairs
markets = exchange.load_markets()
for market in markets:
    print(market)

ticker = 'ETH/USDT'
exchange.fetch_ticker(ticker)

ohlc = exchange.fetch_ohlcv(ticker)
for candle in ohlc:
    print(candle)

# order book?
order_book = exchange.fetch_order_book(ticker)
order_book

balances = exchange.fetch_balance()

for ticker in balances['total']:
    coin = balances['total'][ticker]
    if coin > 0.0:
        print(ticker+'\t'+str(coin))

# Orders
exchange.create_market_sell_order('ADA/USDT', amount = 30)
exchange.create_market_buy_order('ETH/USDT', amount = 100)

# Fees
# https://github.com/ccxt/ccxt/wiki/Manual#fees
