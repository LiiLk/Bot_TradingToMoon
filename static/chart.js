var chart = LightweightCharts.createChart(document.getElementById('chart'), {
    width: 900,
    height: 500,
    layout: {
        backgroundColor: '#000000',
        textColor: 'rgba(255, 255, 255, 0.9)',
    },
    grid: {
        vertLines: {
            color: 'rgba(197, 203, 206, 0.5)',
        },
        horzLines: {
            color: 'rgba(197, 203, 206, 0.5)',
        },
    },
    crosshair: {
        mode: LightweightCharts.CrosshairMode.Normal,
    },
    priceScale: {
        borderColor: 'rgba(197, 203, 206, 0.8)',
    },
    timeScale: {
        borderColor: 'rgba(197, 203, 206, 0.8)',
        timeVisible: true,
        
    },
});

var candleSeries = chart.addCandlestickSeries({
    upColor: 'rgba(0, 255, 0, 1)',
    downColor: '#FF0000',
    borderDownColor: 'rgba(255, 0, 0, 1)',
    borderUpColor: 'rgba(0, 255, 0, 1)',
    wickDownColor: 'rgba(255, 0, 0, 1)',
    wickUpColor: 'rgba(0, 255, 0, 1)',
});

fetch('http://localhost:5000/history')
    .then((r) => r.json())
    .then((response) => {
        console.log(response)

        candleSeries.setData(response);
    })

var binanceSocket = new WebSocket("wss://fstream.binance.com/ws/btcusdt@kline_5m");

binanceSocket.onmessage = function (event) {
    var message = JSON.parse(event.data);

    var candlestick = message.k;

    console.log(candlestick)

    candleSeries.update({
        time: candlestick.t / 1000,
        open: candlestick.o,
        high: candlestick.h,
        low: candlestick.l,
        close: candlestick.c
    })
}
