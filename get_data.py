import csvfile as csvfile
from binance.enums import HistoricalKlinesType

import config, csv
from binance.client import Client
client = Client(config.API_KEY, config.SECRET_KEY)

csvfile = open('data/btcusdt-futures-jan2020-nov2020-1h.csv', 'w', newline='')
candlestick_writer = csv.writer(csvfile, delimiter=',')

candlesticks = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1HOUR, "1 Jan, 2020", "1 Nov, 2020", klines_type=HistoricalKlinesType.FUTURES)

for candlestick in candlesticks:
      candlestick[0] = candlestick[0] / 1000
      candlestick_writer.writerow(candlestick)

csvfile.close()
