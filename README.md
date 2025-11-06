# XGBoost Back Test

## 1. Introduction

After learning quantative finance for 2 weeks, this is my first from 0 back test workflow. This report presents the results of a **XGBoost** model predicitng stocks trend, conducted using **Backtrader**. 

The goal was to find out the optimzed parameter for indicators and the model, and get the optimized result in the back test.

---

## 2. Experiment Setup

| Item | Description |
|------|--------------|
| **Framework** | Backtrader |
| **Data Source** | Yahoo Finance | 
| **Stock Code** | AAPL, NVDA, TSLA, SPY| 
| **Time Period** | *2015-01-01 to 2024-12-31* |
| **Initial Cash** | 100,000 |
| **Commission** | 0.001% per trade |
| **Position Size** | 30% of the portfolio per trade   |
| **Parameters Tested** | Fast MACD: [8, 12], Slow MACD: [20, 26], RSI: [10, 14, 20], SMA: [10, 20, 30]|
| **Metrics Used** | Portfolio Value, Sharpe Ratio, Max Drawdown |

---

## 3. Strategy Logic

**XGBoost Predict Signal Strategy**

### Feature Extract
We extract features from the downloaded data, by getting everyday's values corresponding to the output of the indicator that we chose to use above, and save it into a csv.
Then, we combine all 4 features csv into one csv. Optimized parameter for the indicators has chosen base on the combination with highest average sharpe ratio. Also, everyday signal is also added to the csv (If next day > today -> 1, otherwise 0)

### Training
- Data were splitted into training (2015-01-01 to 2020-12-31) and testing (2021-01-01 to 2024-12-31).
- Optimized parameter for the XGBoost model has found by using grid search
- Features importance has printed out

### Signal Prediction
After trained, the model is used to generate probability of rising on next day and signal that for the testing set, and save in a csv.

### Back Test
The results are then put in the Back Trader framework for back test

## 4. Results Summary

### 4.1 Back Test Plot
![Back Test Plot](Results/BackTest.png)

### 4.2 Best Parameter Combination

| Fast | Slow | Total Return | Sharpe | Sortino | Volatility | Winrate |
|------|------|---------------|--------|----------|-------------|----------|
| 10   | 10   | 2.1 %         | 0.961  | 1.007    | 0.011       | 41.7%    |

**Best Strategy:** Fast = `15`, Slow = `20`, Sharpe = `0.961`

---

### 4.3 Performance Metrics Across All Combinations
 
![Heatmap of Sharpe Ratios](Results/Sharpe_Heatmap.png)

---

## 5. Portfolio Performance

### 5.1 Portfolio Value Over Time 
![Portfolio Value Curve](Results/Portfolio_Change.png)

**Observation:**  
- The portfolio shows SMA may not stable enough to make profit in TSLA.  
- Temporary drawdowns occur during sideways or volatile markets.  
- Final capital: **$102,081** (+2.1% total return)

---

##  6. Analysis and Visualizations

### 6.1 Return-Sharpe Relationship
![Return Volatility Sharpe ](Results/Return_Sharpe.png)

**Interpretation:**  
- Sharpe ratio is highly correlated with return.
- The highest win rate setup comes with median sharpe ratio

---

## 7. Statistical Summary

| Metric | Value | Description |
|--------|--------|-------------|
| **Average Daily Return** | 0.12% | Mean of daily portfolio returns |
| **Annualized Volatility** | 18.2% | Standard deviation × √252 |
| **Sharpe Ratio** | 1.72 | Risk-adjusted performance |
| **Sortino Ratio** | 2.56 | Penalizes only downside risk |
| **Max Drawdown** | 9.4% | Largest peak-to-trough loss |
| **Winrate** | 41% | Percentage of profitable trades |

---

##  8. Discussion & Insights

- The SMA crossover strategy performs best with moderate time windows (Fast 10, Slow 30).  
- Overly short windows increase noise and transaction costs.  
- Sharpe ratio correlates negatively with volatility at extremes.  
- Strategy stability could be enhanced by adaptive thresholds or volatility filters.

---

## 9. Future Improvements

- Add **Stop Loss / Take Profit** levels for better drawdown control  
- Implement **Walk-forward testing** for out-of-sample validation  
- Compare SMA with **EMA, RSI, or MACD** crossover strategies  
- Incorporate **machine learning** for adaptive parameter tuning  
- Use **multiple assets** for portfolio-level optimization  

---

## 10. Conclusion

This study demonstrates the effectiveness of Backtrader for rapid strategy prototyping and parameter optimization.  
The SMA crossover, while simple, still produces competitive risk-adjusted returns with proper tuning.  
Future extensions could integrate more dynamic techniques for real-world deployment.
