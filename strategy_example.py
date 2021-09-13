# Import the backtrader platform
import backtrader as bt
import backtrader.indicators as btind
import datetime as dt
import pandas as pd
import yf as yf
from pandas_datareader import data as pdr
import math

#importing data
yf.pdr_override()
startyear = 2020
startmonth = 1
startday = 1
start = dt.datetime(startyear, startmonth, startday)
#endyear = 2020
#endmonth = 4
#endday = 16
#end = dt.datetime(endyear, endmonth, endday)
end = dt.datetime.now()
asset = "EURUSD=X"
df = pdr.get_data_yahoo(asset, start, end)

#set up commission scheme
startcash = 1000.0

class forexSpreadCommisionScheme(bt.CommInfoBase):
    params = (
        ('commtype', bt.CommInfoBase.COMM_PERC),
        ('stocklike', False)
    )

    def _getcommission(self, size, price, pseudoexec):
        return size * price * self.p.commission

comminfo = forexSpreadCommisionScheme(
    commission=0.0035,
    leverage=30
)


#Defining strategy

class BaseStrategy(bt.Strategy):

    params = (('risk', 0.01),  # risk 1%
              ('stop_dist', 0.01))  # stoploss distance 1%

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))


    def __init__(self):
        self.bbands = bt.indicators.BollingerBands()
        self.sto = btind.Stochastic()
        percD = self.sto.lines.percD
        percK = self.sto.lines.percK
        self.buysell_sig = btind.CrossOver(percD, percK)

    def next(self):
        cash = self.broker.get_cash()
        self.dt = self.data.datetime.date()

        if not self.position:

            if self.buysell_sig < 0:
                stop_price = (self.data.close[0] * (1 - self.p.stop_dist))
                qty = math.floor(cash * self.p.risk / (self.data.close[0] - stop_price))
                self.buy_bracket(exectype=bt.Order.Market, price=self.data.close[0], size=qty, limitprice= cash*3*self.p.risk / qty + self.data.close[0], stopprice=stop_price)


            elif self.buysell_sig > 0:
                stop_price = (self.data.close[0] * (1 + self.p.stop_dist))
                qty = math.floor(cash * self.p.risk / (self.data.close[0] - stop_price))
                self.sell_bracket(exectype=bt.Order.Market, price=self.data.close[0], size=qty, limitprice= self.data.close[0] - cash*3*self.p.risk / -qty, stopprice=stop_price)

        '''else:
            if self.position.size < 0:
                if self.buysell_sig < 0:
                    self.order_target_size(price=self.data.close[0])
            if self.position.size > 0:
                if self.buysell_sig > 0:
                    self.order_target_size(price=self.data.close[0])'''

    def notify_order(self, order):
        date = self.data.datetime.datetime().date()

        if order.status == order.Accepted:
            print('-' * 32, ' NOTIFY ORDER ', '-' * 32)
            print('{} Order Accepted'.format(order.info['name']))
            print('{}, Status {}: Ref: {}, Size: {}, Cash {}, Price: {}'.format(
                date,
                order.status,
                order.ref,
                order.size,
                self.broker.get_cash(),
                'NA' if not order.price else round(order.price, 5)
            ))

        if order.status == order.Completed:
            print('-' * 32, ' NOTIFY ORDER ', '-' * 32)
            print('{} Order Completed'.format(order.info['name']))
            print('{}, Status {}: Ref: {}, Size: {}, Price: {}'.format(
                date,
                order.status,
                order.ref,
                order.size,
                'NA' if not order.executed.price else round(order.executed.price, 5)
            ))
            print('Created: {} Price: {} Size: {}'.format(bt.num2date(order.created.dt), order.created.price,
                                                          order.created.size))
            print('-' * 80)

        if order.status == order.Canceled:
            print('-' * 32, ' NOTIFY ORDER ', '-' * 32)
            print('{} Order Canceled'.format(order.info['name']))
            print('{}, Status {}: Ref: {}, Size: {}, Price: {}'.format(
                date,
                order.status,
                order.ref,
                order.size,
                'NA' if not order.price else round(order.price, 5)
            ))

        if order.status == order.Rejected:
            print('-' * 32, ' NOTIFY ORDER ', '-' * 32)
            print('WARNING! {} Order Rejected'.format(order.info['name']))
            print('{}, Status {}: Ref: {}, Size: {}, Price: {}'.format(
                date,
                order.status,
                order.ref,
                order.size,
                'NA' if not order.price else round(order.price, 5)
            ))
            print('-' * 80)

    def notify_trade(self, trade):
        date = self.data.datetime.datetime()
        if trade.isclosed:
            print('-' * 32, ' NOTIFY TRADE ', '-' * 32)
            print('{}, Close Price: {}, Profit, Gross {}, Net {}, Commission {}'.format(
                date,
                trade.price,
                round(trade.pnl, 2),
                round(trade.pnlcomm, 2),
                round(trade.commission), 4))
            print('-' * 80)

if __name__ == '__main__':

    # Create a cerebro entity
    cerebro = bt.Cerebro()

    cerebro.addstrategy(BaseStrategy)

    data = bt.feeds.PandasData(dataname=df)

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(startcash)

    # Set the commission
    cerebro.broker.addcommissioninfo(comminfo)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    portvalue = cerebro.broker.getvalue()
    pnl = portvalue - startcash

    # Print out the final result
    print('----SUMMARY----')
    print('Final Portfolio Value: ${}'.format(portvalue))
    print('P/L: ${}'.format(pnl))

    cerebro.plot()