import backtrader as bt
from strat import MultiSignalStrategy
import pandas as pd
import matplotlib.pyplot as plt

class PandasSignalData(bt.feeds.PandasData):
    lines = ('signal',)
    params = (('signal', -1),)

class FixedCommission(bt.CommInfoBase):
    params = (
        ('commission', 2.0),  
    )

    def _getcommission(self, size, price, pseudoexec):
      
        return self.p.commission  

df = pd.read_csv('./Input/multi_signal.csv')
print(df[['Date', 'ticker', 'signal']].head(10))
print(df['signal'].unique())

df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)
tickers = df['ticker'].unique()

cerebro = bt.Cerebro()
cerebro.broker.setcash(100000)
fixed_comm = FixedCommission(commission=2.0)
cerebro.broker.addcommissioninfo(fixed_comm)
cerebro.addstrategy(MultiSignalStrategy)
cerebro.addsizer(bt.sizers.PercentSizer, percents=30)
# cerebro.addsizer(bt.sizers.FixedSize, stake=3)

for t in tickers:
    sub_df = df[df['ticker'] == t].copy()
    data = PandasSignalData(dataname=sub_df)
    cerebro.adddata(data, name=t)

cerebro.addanalyzer(bt.analyzers.SharpeRatio_A, _name='sharpe')
cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')

results = cerebro.run()
analyzers = results[0].analyzers

init_value = 100000
final_value = cerebro.broker.getvalue()
profit = final_value - init_value
profit_pct = (profit / init_value) * 100

sharpe = analyzers.sharpe.get_analysis()
dd = analyzers.drawdown.get_analysis()

strat = results[0]
winrate = (strat.winning_trades / strat.total_trades * 100) if strat.total_trades > 0 else 0

print("\nBacktest Summary")
print(f"Initial Portfolio Value: {init_value:,.2f} USD")
print(f"Final Portfolio Value:   {final_value:,.2f} USD")
print(f"Total Profit:            {profit:,.2f} USD ({profit_pct:.2f}%)")
if sharpe.get('sharperatio') is not None:
    print(f"Sharpe Ratio: {sharpe['sharperatio']:.3f}")
else:
    print("Sharpe Ratio unavailable.")
print(f"Max Drawdown: {dd['max']['drawdown']:.2f}%")
print(f"Win Rate: {winrate:.2f}% ({strat.winning_trades}/{strat.total_trades})")

cerebro.plot(style='candlestick')


plt.figure(figsize=(10, 5))
plt.plot(strat.dates, strat.portfolio_values, color='dodgerblue', linewidth=2)
plt.title('Portfolio Value Over Time', fontsize=14, weight='bold')
plt.xlabel('Date')
plt.ylabel('Portfolio Value (USD)')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()