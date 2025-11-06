import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import joblib
from sklearn.model_selection import GridSearchCV
import xgboost as xgb
import seaborn as sns

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
    scoring='roc_auc',  
    verbose=2,
    n_jobs=-1
)

grid_search.fit(X_train, y_train)

print("Best Parameter Combination:", grid_search.best_params_)
print("Best accuracy:", grid_search.best_score_)

best_model = grid_search.best_estimator_

importance = best_model.get_booster().get_score(importance_type='gain')
importance_df = pd.DataFrame({
    'Feature': list(importance.keys()),
    'Importance': list(importance.values())
}).sort_values(by='Importance', ascending=False)

plt.figure(figsize=(8, 5))
sns.barplot(
    data=importance_df,
    x='Importance',
    y='Feature',
    palette='viridis'
)
plt.title('Feature Importance (Gain)', fontsize=14, weight='bold')
plt.xlabel('Importance Score', fontsize=12)
plt.ylabel('Features', fontsize=12)
plt.grid(axis='x', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

joblib.dump(best_model, 'models/xgb_model.pkl')
print('Model and feature name saved')
