
import random
from operator import itemgetter, attrgetter

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


class BarSequence():

    def __init__(self, num):
        self.bars = []
        self.create_bars(num)

    def create_bars(self, num):
        self.bars = []
        for i, n in enumerate(range(num)):
            if i == 0:
                bar = Bar()
            else:
                bar = Bar(previous_bar)
            previous_bar = bar
            self.bars.append(bar)

    def print_bar_prices(self):
        for bar in self.bars:
            print bar.price


class Analysis():
    def __init__(self, bar_sequence):
        self.bars = bar_sequence.bars
        self._gethighlow()

    def _gethighlow(self):
        temp_high = self.bars[0].price
        temp_low = self.bars[0].price
        for bar in self.bars:
            if bar.price > temp_high:
                temp_high = bar.price
            if bar.price < temp_low:
                temp_low = bar.price
        self.high = temp_high
        self.low = temp_low

    def ma(self, bar_num):
        '''
        
        '''
        rtn = []
        prices_list = self.get_sliced_price(bar_num)
        for prices in prices_list:
            rtn.append(sum(prices) / bar_num)
        return rtn

    def get_sliced_price(self, bar_num):
        rtn = []
        slice_num = len(self.bars) - bar_num + 1
        get_price = attrgetter('price')
        for n in range(slice_num):
            prices = [ get_price(bar) for bar in self.bars[n: n + bar_num] ]
            rtn.append(prices)
        return rtn
        

    def stoploss_buy(self):
        pass

    def stoploss_sell(self):
        pass


if __name__ == '__main__':
    
    bs = BarSequence(9)
    bs.print_bar_prices()

    a = Analysis(bs)
    print a.get_sliced_price(3)
    print a.ma(3)
