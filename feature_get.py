import pandas as pd
import numpy as np
import ta
import os

TICKERS = ['AAPL', 'NVDA', 'TSLA', 'SPY']

for ticker in TICKERS:
    df = pd.read_csv(f'./Data/{ticker}.csv')
    df = df.dropna()
    df = df[~df['Date'].str.contains("Date", na=False)]
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df.set_index('Date', inplace=True)
    df.rename(columns=str.lower, inplace=True)


    df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=10).rsi()
    df['sma'] = ta.trend.SMAIndicator(df['close'], window=10).sma_indicator()
    macd = ta.trend.MACD(df['close'], window_fast=8, window_slow=20)
    df['macd'] = macd.macd()
    df['volatility'] = ta.volatility.BollingerBands(df['close']).bollinger_hband() -\
                        ta.volatility.BollingerBands(df['close']).bollinger_lband()

    df['target'] = (df['close'].shift(-1) > df['close']).astype(int)

    df.dropna(inplace=True)
    os.makedirs("./Prepared Data", exist_ok=True)
    df.to_csv(f'./Prepared Data/{ticker}_features.csv')