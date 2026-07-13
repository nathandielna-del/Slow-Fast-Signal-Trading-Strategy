# Quantitative Trading Strategies Portfolio

This repository contains Python scripts developed during a Coursera course to explore financial data analysis and algorithmic trading concepts. It serves as a practical progression from basic time series manipulation to building statistical predictive models.

---

## 🚀 Strategy 1: Moving Average Crossover

This project is a Python script that tests a stock buying and selling strategy based on moving averages. It is an intentionally basic approach that serves primarily as a practical case study for learning how to manipulate time series, rather than a trading tool to be used with real capital.

### How it works
The code downloads the historical closing prices of a stock and calculates two indicators:
* A 10-day moving average (MA10), which reacts quickly to price changes.
* A 50-day moving average (MA50), which outlines the underlying trend.

The decision rule is simple:
* If the MA10 crosses above the MA50, the script generates a buy signal (1). The short-term trend is upward.
* If the MA10 crosses back below the MA50, the script generates a signal to close the position (0).

### Tools used
* **Python**
* **Pandas:** for data cleaning, calculating averages (`.rolling`), and dataframe manipulation.
* **yfinance:** to fetch stock prices directly from Yahoo Finance without having to manually download CSV files.
* **Matplotlib:** to plot the price chart and visualize the signals.

---

## 🚀 Strategy 2: Vectorized Multiple Regression Backtesting Engine

### Overview
An advanced, end-to-end quantitative backtesting pipeline built to predict the SPDR S&P 500 ETF Trust (SPY) movements using global market indices. This model transitions from simple moving averages to statistical machine learning (OLS Regression).

### Technical Architecture
* **Data Engineering:** Automated extraction of 14 years of historical data across 8 global indices (NASDAQ, DJI, CAC40, DAX, etc.) via the `yfinance` API.
* **Algorithmic Logic:** Fully vectorized data manipulation using `Pandas` and `NumPy` to eliminate iterative loops ($O(1)$ time complexity for signal generation).
* **Predictive Modeling:** Built a Multiple Linear Regression model (`statsmodels`) on a rolling training set to generate daily Buy/Short signals.
* **Performance Evaluation:** Implemented practical quantitative standards to evaluate the strategy's robustness, specifically calculating the **Yearly Sharpe Ratio** and **Maximum Drawdown**.

### Key Results
The backtester successfully simulates trading execution and compares the signal-based wealth generation against a standard Buy-and-Hold benchmark, proving the alpha-generation capability of the statistical model.

---

## ⚙️ How to test the code

If you want to run the scripts on your local machine:
1. Make sure you have installed the required libraries. You can do this with: `pip install pandas numpy yfinance matplotlib statsmodels`
2. Run the desired script. By default, Strategy 1 is configured to analyze Apple stock (AAPL), but you can modify the "ticker" directly in the code. Strategy 2 targets the S&P 500 (SPY).
