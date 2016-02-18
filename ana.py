
import random


class Bar():
    bar_count = 0
    def __init__(self, previous_bar=None):
        if not previous_bar:
            self.__init_bar()
        else:
            self.previous_bar = previous_bar
            self.get_price()

    def __new__():
        bar_count += 1

    def __init_bar(self):
        self.price = 50000

    def get_price(self):
        '''
        the price is randomly created
        '''
        pprice = self.previous_bar.price
        low = pprice * 0.99
        high = pprice * 1.01
        self.price = random.uniform(low, high)

def get_bars(num):
    bars = []
    for i, n in enumerate(range(num)):
        if i == 0:
            bar = Bar()
        else:
            bar = Bar(pbar)
        pbar = bar
        bars.append(bar)
    return bars

def print_prices(bars):
    for bar in bars:
        print bar.price


print_prices(get_bars(20))
