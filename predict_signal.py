import joblib
import pandas as pd
import os

model = joblib.load('./models/xgb_model.pkl')
df = pd.read_csv('./Prepared Data/multi_stock_features.csv')

test_df  = df[df['Date'] >= '2021-01-01']

X_test = test_df.drop(columns=['target', 'ticker', 'Date'], errors='ignore') 
y_test = test_df['target']

test_df['prob_up'] = model.predict_proba(X_test)[:, 1]
test_df['signal'] = (test_df['prob_up'] > 0.55).astype(int)

os.makedirs("./Input", exist_ok=True)
test_df.to_csv('./Input/multi_signal.csv', index=False)