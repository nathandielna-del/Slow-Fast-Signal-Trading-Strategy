#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 13:41:28 2026

@author: nathandielna
"""

import yfinance as yf
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import warnings


warnings.filterwarnings("ignore")

print("ÉTAPE 1: Extraction des données via Yahoo Finance API ")


tickers_mapping = {
    'spy': 'SPY',         
    'sp500': '^GSPC',     
    'nasdaq': '^IXIC',    
    'dji': '^DJI',
    'cac40': '^FCHI',     
    'daxi': '^GDAXI',     
    'aord': '^AORD',      
    'hsi': '^HSI',       
    'nikkei': '^N225'     
}


data = {}
for name, ticker in tickers_mapping.items():
    data[name] = yf.download(ticker, start='2010-01-01', end='2024-01-01')

print("Extraction terminée.\n")

print("--- ÉTAPE 2: Data Munging (Nettoyage et structuration) ---")

indicepanel = pd.DataFrame(index=data['spy'].index)

# Calcul des variations 
indicepanel['spy'] = data['spy']['Open'].shift(-1) - data['spy']['Open']
indicepanel['spy_lag1'] = indicepanel['spy'].shift(1)

for col in ['sp500', 'nasdaq', 'dji', 'cac40', 'daxi', 'aord', 'hsi', 'nikkei']:
    indicepanel[col] = data[col]['Open'] - data[col]['Open'].shift(1)

# Ajout du prix d'ouverture pour le calcul de la richesse future
indicepanel['Price'] = data['spy']['Open']

# Forward fill pour combler les trous (jours fériés), puis suppression des NA restants
indicepanel = indicepanel.fillna(method='ffill').dropna()


print("--- ÉTAPE 3: Entraînement du Modèle de Régression ---")
# Split des données (Train / Test)
Train = indicepanel.iloc[-2000:-1000, :].copy()
Test = indicepanel.iloc[-1000:, :].copy()

# OLS Regression
formula = 'spy ~ spy_lag1 + sp500 + nasdaq + dji + cac40 + aord + daxi + nikkei + hsi'
lm = smf.ols(formula=formula, data=Train).fit()


print("--- ÉTAPE 4: Génération des Signaux et Calcul des Profits ---")

Train['PredictedY'] = lm.predict(Train)
Test['PredictedY'] = lm.predict(Test)

# Stratégie : Si la prédiction est positive (>0), on achète (1), sinon on vend à découvert (-1)
Train['Order'] = [1 if sig > 0 else -1 for sig in Train['PredictedY']]
Train['Profit'] = Train['spy'] * Train['Order']
Train['Wealth'] = Train['Profit'].cumsum()

Test['Order'] = [1 if sig > 0 else -1 for sig in Test['PredictedY']]
Test['Profit'] = Test['spy'] * Test['Order']
Test['Wealth'] = Test['Profit'].cumsum()

# Ajustement de la richesse avec le prix initial de l'action
Train['Wealth'] = Train['Wealth'] + Train.loc[Train.index[0], 'Price']
Test['Wealth'] = Test['Wealth'] + Test.loc[Test.index[0], 'Price']


print("--- ÉTAPE 5: Évaluation des Standards Pratiques (Sharpe & Drawdown) ---")
def calculate_metrics(df, dataset_name):
   
    # Sharpe Ratio
    df['Return'] = np.log(df['Wealth']) - np.log(df['Wealth'].shift(1))
    dailyr = df['Return'].dropna()
    daily_sharpe = dailyr.mean() / dailyr.std(ddof=1)
    yearly_sharpe = (252**0.5) * daily_sharpe
    
    # Maximum Drawdown
    df['Peak'] = df['Wealth'].cummax()
    df['Drawdown'] = (df['Peak'] - df['Wealth']) / df['Peak']
    max_drawdown = df['Drawdown'].max()
    
    print(f"\nPerformances sur le set de {dataset_name} :")
    print(f"Profit Total : {df['Profit'].sum():.2f}")
    print(f"Yearly Sharpe Ratio : {yearly_sharpe:.4f}")
    print(f"Maximum Drawdown : {max_drawdown:.4f}")

calculate_metrics(Train, "TRAIN")
calculate_metrics(Test, "TEST")


print("\n--- ÉTAPE 6: Visualisation de la Stratégie ---")
plt.figure(figsize=(10, 6))
plt.title('Performance de la Stratégie (Test Set)')
plt.plot(Test.index, Test['Wealth'].values, color='green', label='Signal based strategy')

# Comparaison avec la stratégie basique 
buy_and_hold = Test['spy'].cumsum().values + Test.loc[Test.index[0], 'Price']
plt.plot(Test.index, buy_and_hold, color='red', label='Buy and Hold strategy')

plt.legend()
plt.grid(True, alpha=0.3)
plt.ylabel('Wealth ($)')
plt.show()