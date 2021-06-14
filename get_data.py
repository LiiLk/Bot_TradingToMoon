import csvfile as csvfile

import config, csv
from binance.client import Client
client = Client(config.API_KEY, config.SECRET_KEY)

candles = client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_5MINUTE)

csvfile = open('2017-2020-5minutes.csv', 'w', newline='')
candlestick_writer = csv.writer(csvfile, delimiter=',')


# for candlestick in candles:
#     print(candlestick)
#
#     candlestick_writer.writerow(candlestick)
# print(len(candles))

candlesticks = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_5MINUTE, "1 Sept, 2017", "1 Jan, 2020")

for candlestick in candlesticks:

    candlestick_writer.writerow(candlestick)
csvfile.close()
