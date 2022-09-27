import yfinance
from datetime import date, timedelta
from plotly import graph_objects, express


today = date.today()
end_date = today.strftime("%Y-%m-%d")
start_date = (date.today() - timedelta(days=365)).strftime("%Y-%m-%d")

stock_symbol = input("Stock symbol: ")
data = yfinance.download(
    f"{stock_symbol}",
    start=start_date,
    end=end_date,
    progress=False
)
data["Date"] = data.index
data = data[["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]]
data.reset_index(drop=True, inplace=True)
print(data.head())

# candlestick chart
figure = graph_objects.Figure(
    data=[graph_objects.Candlestick(
        x=data["Date"],
        open=data["Open"],
        high=data["High"],
        low=data["Low"],
        close=data["Close"]
        )
    ]
)
figure.update_layout(
    title=f"{stock_symbol} Stock Price Analysis",
    xaxis_rangeslider_visible=False
)
figure.show()

# bar
figure = express.bar(data, x="Date", y="Close")
figure.show()

# line
figure = express.line(
    data,
    x="Date",
    y="Close",
    title=f'Stock Market Analysis for {stock_symbol} with Rangeslider'
)
figure.update_xaxes(rangeslider_visible=True)
figure.show()


# time period selectors
figure = express.line(
    data,
    x="Date",
    y="Close",
    title=f"Stock Market Analysis for {stock_symbol} with Time Period Selectors",
)
figure.update_xaxes(
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=3, label="3m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)
figure.show()


# hiding weekend
figure = express.scatter(
    data,
    x="Date",
    y="Close",
    range_x=["2021-09-07", "2022-09-07"],
    title=f"Stock Market Analysis for {stock_symbol} without weekends"
)
figure.update_xaxes(
    rangebreaks=[
        dict(bounds=["sat", "sun"])
    ]
)
figure.show()
