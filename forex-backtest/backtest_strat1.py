import backtrader as bt
import pandas as pd

# Define Strategy
class SMACross(bt.Strategy):
    params = (("short_period", 10), ("long_period", 50),)

    def __init__(self):
        self.sma_short = bt.indicators.SimpleMovingAverage(period=self.params.short_period)
        self.sma_long = bt.indicators.SimpleMovingAverage(period=self.params.long_period)

    def next(self):
        if self.sma_short[0] > self.sma_long[0] and not self.position:
            self.buy()
        elif self.sma_short[0] < self.sma_long[0] and self.position:
            self.sell()

# Load Data
# Load Forex Data (Modify for your source)
data = pd.read_csv("data/EURUSD_2016.csv", parse_dates=["Gmt time"], index_col="Gmt time", 
                   date_parser=lambda x: pd.to_datetime(x, format="%d.%m.%Y %H:%M:%S.%f"))

# Select data from January to March 2016
data_q1 = data.loc["2015-01":"2015-03"]

data_feed = bt.feeds.PandasData(dataname=data_q1)

# Backtest Setup
cerebro = bt.Cerebro()
cerebro.addstrategy(SMACross)
cerebro.adddata(data_feed)
cerebro.broker.set_cash(10000)
cerebro.broker.setcommission(commission=0.0002, leverage=30)

# Run Backtest
cerebro.run()
cerebro.plot()
