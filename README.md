# Trading Strategy: Moving Average Crossover

This project is a Python script that tests a stock buying and selling strategy based on moving averages. I developed it while taking a Coursera course to familiarize myself with financial data analysis.

It is an intentionally basic approach that serves primarily as a practical case study for learning how to manipulate time series, rather than a trading tool to be used with real capital.

## How it works

The code downloads the historical closing prices of a stock and calculates two indicators:
- A 10-day moving average (MA10), which reacts quickly to price changes.
- A 50-day moving average (MA50), which outlines the underlying trend.

The decision rule is simple:
- If the MA10 crosses above the MA50, the script generates a buy signal (1). The short-term trend is upward.
- If the MA10 crosses back below the MA50, the script generates a signal to close the position (0).

## Tools used

- Python
- Pandas: for data cleaning, calculating averages (.rolling), and dataframe manipulation.
- yfinance: to fetch stock prices directly from Yahoo Finance without having to manually download CSV files.
- Matplotlib: to plot the price chart and visualize the signals.

## How to test the code

If you want to run the script on your local machine:

1. Make sure you have installed the required libraries. You can do this with:
   pip install pandas yfinance matplotlib

2. Run the script. By default, it is configured to analyze Apple stock (AAPL), but you can modify the "ticker" directly in the code to test other stocks (e.g., MSFT, TSLA, etc.).
