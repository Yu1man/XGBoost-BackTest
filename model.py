import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import joblib
from sklearn.model_selection import GridSearchCV
import xgboost as xgb

df = pd.read_csv('./Prepared Data/multi_stock_features.csv')

df['Date'] = pd.to_datetime(df['Date'])

train_df = df[df['Date'] < '2021-01-01']

X_train = train_df.drop(columns=['target', 'ticker', 'Date'], errors='ignore') 
y_train = train_df['target']

param_grid = {
    'max_depth': [3, 5, 7],
    'learning_rate': [0.01, 0.05, 0.1],
    'n_estimators': [100, 200, 300],
    'subsample': [0.8, 1.0],
    'colsample_bytree': [0.8, 1.0]
}

model = xgb.XGBClassifier(
    objective='binary:logistic',
    eval_metric='logloss',
    use_label_encoder=False
)

grid_search = GridSearchCV(
    estimator=model,
    param_grid=param_grid,
    cv=3,                   
    scoring='accuracy',  
    verbose=2,
    n_jobs=-1
)

grid_search.fit(X_train, y_train)

print("Best Parameter Combination:", grid_search.best_params_)
print("Best accuracy:", grid_search.best_score_)

best_model = grid_search.best_estimator_

xgb.plot_importance(best_model, importance_type='gain', title='Feature Importance')
plt.show()

joblib.dump(best_model, 'models/xgb_model.pkl')
print('Model and feature name saved')
