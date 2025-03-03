import backtrader as bt
import pandas as pd

# Define Strategy
class MomentumStrategy(bt.Strategy):
    params = dict(stop_loss=0.005, take_profit=0.01)  # 50 pips SL, 100 pips TP

    def __init__(self):
        self.entry_price = None

    def next(self):
        if len(self.data) < 3:  # Need at least 3 candles to analyze trend
            return

        # Detect bullish momentum (higher closes, even if some candles are red)
        bullish_momentum = (self.data.close[-3] > self.data.close[-4] and
                            self.data.close[-2] > self.data.close[-3] and
                            self.data.close[-1] > self.data.close[-2] and
                            self.data.close[0] > self.data.close[-1])

        # Detect bearish momentum (lower closes)
        bearish_momentum = (self.data.close[-3] < self.data.close[-4] and
                            self.data.close[-2] < self.data.close[-3] and
                             self.data.close[-1] < self.data.close[-2] and
                             self.data.close[0] < self.data.close[-1])

        if not self.position:  # No active trade
            if bullish_momentum:  # Buy Signal
                self.buy()
                self.entry_price = self.data.close[0]
            elif bearish_momentum:  # Sell Signal
                self.sell()
                self.entry_price = self.data.close[0]
        else:  # Manage Open Trade
            if self.position.size > 0 and (self.data.close[0] >= self.entry_price * (1 + self.params.take_profit) or
                                           self.data.close[0] <= self.entry_price * (1 - self.params.stop_loss)):
                self.sell()  # Exit Long
            elif self.position.size < 0 and (self.data.close[0] <= self.entry_price * (1 - self.params.take_profit) or
                                             self.data.close[0] >= self.entry_price * (1 + self.params.stop_loss)):
                self.buy()  # Exit Short

# Load Forex Data (Modify for your source)
data = pd.read_csv("data/EURUSD_2016.csv", parse_dates=["Gmt time"], index_col="Gmt time", 
                   date_format="%d.%m.%Y %H:%M:%S.%f")  # Use 'date_format' instead

# Select data from January to March 2016
data_q1 = data.loc["2015-01":"2015-03"]


data_feed = bt.feeds.PandasData(dataname=data_q1)

# Backtesting Engine
cerebro = bt.Cerebro()
cerebro.addstrategy(MomentumStrategy, stop_loss=0.005, take_profit=0.01)
cerebro.adddata(data_feed)
cerebro.broker.set_cash(10000)
cerebro.broker.setcommission(commission=0.0002, leverage=30)

# Run Backtest
cerebro.run()
cerebro.plot()
