
"""
@author: nathandielna
"""

import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt 

# Import your asset (here it is 'AAPL' for the example)
# you can choose the day you begin the backtesting
asset = yf.Ticker('AAPL').history(start='2021-01-01')

#creation of the moving average
asset['MA10'] = asset['Close'].rolling(10).mean() #fast
asset['MA50'] = asset['Close'].rolling(50).mean() #slow
asset = asset.dropna()

# Shares is at 1 when we are long
asset['Shares'] = (asset['MA10'] > asset['MA50']).astype(int)

#Profit calcul
asset['Close1'] = asset['Close'].shift(-1)
asset['Profit'] = [asset.loc[ei, 'Close1'] - asset.loc[ei, 'Close'] if asset.loc[ei, 'Shares']==1 else 0 for ei in asset.index]

# PnL
asset['wealth'] = asset['Profit'].cumsum()

asset['wealth'].plot()
plt.title('Total money you win is {}'.format(asset.loc[asset.index[-2], 'wealth']))