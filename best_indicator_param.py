import pandas as pd
import numpy as np
import ta
import itertools
import os
import seaborn as sns
import matplotlib.pyplot as plt

# === 設定 ===
TICKERS = ['AAPL', 'NVDA', 'TSLA', 'SPY']
rsi_periods = [10, 14, 20]
sma_periods = [10, 20, 30]
macd_fast = [8, 12]
macd_slow = [20, 26]

results = []

for rsi_p, sma_p, macd_f, macd_s in itertools.product(rsi_periods, sma_periods, macd_fast, macd_slow):

    sharpes = []  # Save sharpe ratio

    for ticker in TICKERS:
        df = pd.read_csv(f'./Data/{ticker}.csv')
        df = df.dropna()
        df = df[~df['Date'].str.contains("Date", na=False)]
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df.set_index('Date', inplace=True)
        df.rename(columns=str.lower, inplace=True)

        # Indicator
        df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=rsi_p).rsi()
        df['sma'] = ta.trend.SMAIndicator(df['close'], window=sma_p).sma_indicator()
        macd = ta.trend.MACD(df['close'], window_fast=macd_f, window_slow=macd_s)
        df['macd'] = macd.macd()

        # Create signal
        df['signal'] = (df['rsi'] > 50).astype(int)

        # Calculate Returns
        df['return'] = df['close'].pct_change()
        df['strategy'] = df['signal'].shift(1) * df['return']
        df.dropna(inplace=True)

        # Sharpe Ratio
        if df['strategy'].std() > 0:
            sharpe = (df['strategy'].mean() / df['strategy'].std()) * np.sqrt(252)
            sharpes.append(sharpe)

    # Average Sharpe 
    if sharpes:
        avg_sharpe = np.mean(sharpes)
        results.append({
            'rsi': rsi_p,
            'sma': sma_p,
            'macd_fast': macd_f,
            'macd_slow': macd_s,
            'avg_sharpe': avg_sharpe
        })
        print(f"RSI={rsi_p}, SMA={sma_p}, MACD({macd_f},{macd_s}) → Sharpe={avg_sharpe:.3f}")

# Result
results_df = pd.DataFrame(results)
results_df = results_df.sort_values(by='avg_sharpe', ascending=False)
os.makedirs('./Optimization Results', exist_ok=True)
results_df.to_csv('./Optimization Results/best_indicators.csv', index=False)

print("\nTop 5 Best Indicator Sets:")
print(results_df.head(5))