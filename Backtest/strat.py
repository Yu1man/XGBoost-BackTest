import backtrader as bt

class MultiSignalStrategy(bt.Strategy):
    def __init__(self):
        self.signals = {data._name: data.signal for data in self.datas}

    def next(self):
        for data in self.datas:
            name = data._name
            signal = self.signals[name][0]
            pos = self.getposition(data).size
            print(f"{self.datetime.date(0)} | {name} | signal={signal} | pos={pos}")

            if pos == 0 and signal == 1:
                self.buy(data=data)
                print(f"BUY {name} at {data.close[0]:.2f}")
            elif pos != 0 and signal == 0:
                self.close(data=data)
                print(f"SELL {name} at {data.close[0]:.2f}")

            if len(self.data) == self.data.buflen() - 1 and self.position:
                self.close()
            print(f"Auto-closed position on last bar: {self.data.datetime.date(0)}")