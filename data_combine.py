import pandas as pd
import glob
import os

files = glob.glob("./Prepared Data/*_features.csv")

all_data = []

for file in files:
    df = pd.read_csv(file)
    
    ticker = os.path.basename(file).split('_')[0]
    df['ticker'] = ticker
    
    all_data.append(df)

combined_df = pd.concat(all_data, ignore_index=True)

print(" Combined dataset shape:", combined_df.shape)
print(combined_df.head())
print(combined_df['ticker'].value_counts())

os.makedirs("./Prepared Data", exist_ok=True)
combined_df.to_csv("./Prepared Data/multi_stock_features.csv", index=False)
print("Saved combined dataset to ./Prepared Data/multi_stock_features.csv")