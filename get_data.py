import yfinance as yf
import pandas as pd
import os

# Setting
TICKERS = ['AAPL', 'NVDA', 'TSLA', 'SPY']                    
START_DATE = "2015-01-01"         
END_DATE = "2024-12-31"    

for ticker in TICKERS:
    SAVE_PATH = f"./Data/{ticker}.csv"

    os.makedirs("./Data", exist_ok=True)

    # Download data
    print(f"Downloading {ticker} from {START_DATE} to {END_DATE} ...")
    data = yf.download(ticker, start=START_DATE, end=END_DATE, progress=False)

    # Clear format
    data.reset_index(inplace=True)
    data = data[['Date','Open','High','Low','Close','Volume']]

    # Save as csv
    data.to_csv(SAVE_PATH, index=False)
    print(f"Saved to {SAVE_PATH}")
    print(f"Total rows: {len(data)}")
    print(data.head())