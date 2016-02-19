#encoding: utf-8
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
        self.price = 5000

    def get_price(self):
        '''
        the price is randomly created
        '''
        pprice = self.previous_bar.price
        low = pprice * 0.999
        high = pprice * 1.001
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
        prices_list = self.get_sliced_barprice(bar_num)
        for prices in prices_list:
            avg = sum(prices) / bar_num
            rtn.append(format(avg, '.1f'))
        return rtn

    def art(self, bar_num):
        pass

    def new_high(self):

        pass

    def get_sliced_barprice(self, bar_num):
        '''

        '''
        slice_num = len(self.bars) - bar_num + 1
        get_price = attrgetter('price')
        for n in range(slice_num):
            prices = [ get_price(bar) for bar in self.bars[n: n + bar_num] ]
            yield prices

    def movestoploss_buy(self, atr, n):
        '''
        return a earnings or loss
        '''
        rtn = 0
        start = self.bars[0].price
        temp_high = self.bars[0].price
        for i, bar in enumerate(self.bars):
            
            if bar.price > temp_high:
                temp_high = bar.price
            stoploss = temp_high - n * atr
            
            #self.__movestoploss_print(i, temp_high, stoploss, bar.price)
            if bar.price <= stoploss:
                rtn = stoploss - start
                return rtn
        return self.bars[-1].price - start
   
    def __movestoploss_print(self, i, temp_high, stoploss, barprice):
        '''for test use'''
        print str(i)+',', format(temp_high, '.1f'), format(stoploss, '.1f'), format(barprice, '.1f')


    def movestoploss_sell(self, atr):
        pass


def movesotploss_avg_earnings():
    earnings = 0
    runtimes = 9999
    for n in range(runtimes):
        bs = BarSequence(50)
        a = Analysis(bs)
        earnings += a.movestoploss_buy(5, 1)
    avg_earning = earnings / runtimes
    print avg_earning

if __name__ == '__main__':
    
    bs = BarSequence(500)
    #bs.print_bar_prices()

    a = Analysis(bs)
    #print a.get_sliced_barprice(3)
    #print a.movestoploss_buy(10,1)
    movesotploss_avg_earnings()
