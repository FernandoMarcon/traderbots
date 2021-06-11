import backtrader as bt
import datetime

data = bt.feeds.YahooFinanceData(dataname='ETH',
                                timeframe=bt.TimeFrame.Weeks,
                                fromdate=datetime.datetime(2021,1,1),
                                todate=datetime.datetime(2021,5,30))

class SmaCross(bt.Strategy):
    params = dict(
        pfast = 10,
        pslow = 30
    )

    def __init__(self):
        sma1 = bt.ind.SMA(period = self.p.pfast)
        sma2 = bt.ind.SMA(period = self.p.pslow)
        self.crossover = bt.ind.CrossOver(sma1, sma2)

    def next(self):
        if not self.position:
            if self.crossover > 0:
                self.buy()

        elif self.crossover < 0:
            self.close()

cerebro = bt.Cerebro()

cerebro.broker.set_cash(100)
cerebro.addstrategy(SmaCross)

cerebro.adddata(data)
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.plot()
