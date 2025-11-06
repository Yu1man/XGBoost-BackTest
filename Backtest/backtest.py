import backtrader as bt
from strat import MultiSignalStrategy
import pandas as pd

class PandasSignalData(bt.feeds.PandasData):
    lines = ('signal',)
    params = (('signal', -1),)

df = pd.read_csv('./Input/multi_signal.csv')
print(df[['Date', 'ticker', 'signal']].head(10))
print(df['signal'].unique())

df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)
tickers = df['ticker'].unique()

cerebro = bt.Cerebro()
cerebro.broker.setcash(100000)
cerebro.broker.setcommission(commission=0.001)
cerebro.addstrategy(MultiSignalStrategy)
cerebro.addsizer(bt.sizers.PercentSizer, percents=40)
# cerebro.addsizer(bt.sizers.FixedSize, stake=3)

for t in tickers:
    sub_df = df[df['ticker'] == t].copy()
    data = PandasSignalData(dataname=sub_df)
    cerebro.adddata(data, name=t)

cerebro.addanalyzer(bt.analyzers.SharpeRatio_A, _name='sharpe')
cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')

results = cerebro.run()
analyzers = results[0].analyzers

sharpe = analyzers.sharpe.get_analysis()
dd = analyzers.drawdown.get_analysis()

print("\n Backtest Result")
print(f"Final Portfolio Value: {cerebro.broker.getvalue():,.2f}")
if sharpe.get('sharperatio') is not None:
    print(f"Sharpe Ratio: {sharpe['sharperatio']:.3f}")
else:
    print(" Sharpe Ratio unavailable.")
print(f"Max Drawdown: {dd['max']['drawdown']:.2f}%")

cerebro.plot(style='candlestick')