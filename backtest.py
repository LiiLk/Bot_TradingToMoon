import backtrader as bt
import datetime

startcash = 100


class MACDStrategy(bt.Strategy):
    params = (('risk', 0.01),  # risk 1%
              ('macd1', 12),
              ('macd2', 26),
              ('macdsign', 9),)

    def __init__(self):
        # Best period to stochrsi and rsi is 8/14
        self.macd = bt.indicators.MACD(self.data, period_me1=self.p.macd1, period_me2=self.p.macd2,
                                       period_signal=self.p.macdsign)
        self.ema200 = bt.indicators.ExponentialMovingAverage(self.data, period=200)
        self.bollinger = bt.indicators.BollingerBands(self.data)
        self.macdcross = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)
        self.BuySignal = 0
        self.SellSignal = 0

    def next(self):
        cash = self.broker.get_cash()
        if self.ema200 < self.data.close and self.macdcross[0] == 1 and self.macd.macd[0] < -2 and self.macd.signal[0] < -2 and not self.position:
            stop_price = self.bollinger.bot[0]
            # print(self.bollinger.bot)
            qty = (cash * self.p.risk) / (self.data.close - stop_price)
            # print(stop_price)

            self.buy_bracket(exectype=bt.Order.Market, price=self.data.close, size=qty,
                             limitprice=cash * 2 * self.p.risk / qty + self.data.close, stopprice=stop_price)

        elif self.ema200 > self.data.close and self.macdcross[0] == -1 and self.macd.macd[0] > 2 and self.macd.signal[0] > 2 and not self.position:
            stop_price = self.bollinger.top[0]
            # print(self.bollinger.top[0])
            qty = cash * self.p.risk / (self.data.close - stop_price)
            self.sell_bracket(exectype=bt.Order.Market, price=self.data.close, size=qty,
                               limitprice=self.data.close - cash * 2 * self.p.risk / -qty, stopprice=stop_price)
        # if self.position and self.BuySignal > 0 and self.ema8 < self.ema21 < self.ema200:
        #         self.close()
        #         self.BuySignal=0
        # elif self.position and self.SellSignal > 0 and self.ema8 > self.ema21 > self.ema200:
        #         self.close()
        #         self.SellSignal=0

    def notify_trade(self, trade):
        date = self.data.datetime.datetime()
        if trade.isclosed:
            print('-' * 32, ' NOTIFY TRADE ', '-' * 32)
            print('{}, Avg Price: {}, Profit, Gross {}, Net {}'.format(
                date,
                trade.price,
                round(trade.pnl, 2),
                round(trade.pnlcomm, 2)))
            print('-' * 80)



cerebro = bt.Cerebro()

fromdate = datetime.datetime.strptime('2020-06-01', '%Y-%m-%d')
todate = datetime.datetime.strptime('2020-07-01', '%Y-%m-%d')

data = bt.feeds.GenericCSVData(dataname='data/btcusdt-futures-jan2020-nov2020-5mn.csv', dtformat=2, compression=5,
                               timeframe=bt.TimeFrame.Minutes, fromdate=fromdate, todate=todate)

cerebro.adddata(data)

cerebro.broker.setcash(startcash)

cerebro.addstrategy(MACDStrategy)

cerebro.broker.setcommission(leverage=10, mult=10)

cerebro.run()

# Get final portfolio Value
portvalue = cerebro.broker.getvalue()
pnl = portvalue - startcash

# Print out the final result
print('Final Portfolio Value: ${}'.format(portvalue))
print('P/L: ${}'.format(pnl))
print('P/L: {}%'.format(((portvalue - startcash) / startcash) * 100))
# Finally plot the end results

cerebro.plot(style='candlestick')
