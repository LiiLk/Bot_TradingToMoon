from flask import Flask, render_template, request, flash, redirect, jsonify
import config,csv
from binance.client import Client
from binance.enums import *
from flask import Flask
from flask_cors import CORS, cross_origin
app = Flask(__name__)
app.secret_key=',:41"?h?RsB#V4fj\Pr6'
cors = CORS(app)
app.config['CORS-HEADERS'] = 'Content-Type'
client = Client(config.API_KEY, config.SECRET_KEY)

@app.route('/')

def index():
    title = 'Binance Futures'

    account = client.get_account()

    balances = account['balances']

    exchange_info = client.get_exchange_info()
    symbols = exchange_info['symbols']

    return render_template('index.html', title=title, my_balances=balances, symbols=symbols)
@app.route("/buy", methods=['POST'])
def buy():
    print(request.form)
    try:
        order = client.create_order(symbol=request.form['symbol'],
                                    side=SIDE_BUY,
                                    type=ORDER_TYPE_MARKET,
                                    quantity=request.form['quantity'])
    except Exception as e:
        flash(e.message, "error")
    return redirect('/')

@app.route("/sell")
def sell():
    return 'sell'
@app.route("/settings")
def settings():
    return 'settings'
@app.route("/history")
def history():
    candlesticks = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_5MINUTE, "1 may, 2021")

    processed_candlesticks = []

    for data_candlestick in candlesticks:
        candlestick = { "time": data_candlestick[0] / 1000,
                        "open": data_candlestick[1],
                        "high": data_candlestick[2],
                        "low": data_candlestick[3],
                        "close": data_candlestick[4]
                        }

        processed_candlesticks.append(candlestick)
    return jsonify(processed_candlesticks)
