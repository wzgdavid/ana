#encoding: utf-8
import random
from operator import itemgetter, attrgetter

__RUNTIMES = 9000
__BAR_NUM = 1000
class Bar():
    __init_price = 5000
    def __init__(self, previous_bar=None):
        if not previous_bar:
            self.__init_bar()
        else:
            self.previous_bar = previous_bar
            self.get_price()


    def __init_bar(self):
        self.price = self.__init_price

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

    def earnings_movestoploss(self, loss_scope):
        '''
        when new high price renew the stoploss
        '''
        rtn = 0
        start = self.bars[0].price
        temp_high = self.bars[0].price
        for i, bar in enumerate(self.bars):
            
            if bar.price > temp_high:
                temp_high = bar.price
            stoploss = temp_high - loss_scope
            
            #self.__movestoploss_print(i, temp_high, stoploss, bar.price)
            if bar.price <= stoploss:
                rtn = stoploss - start
                return rtn
        return self.bars[-1].price - start

    def earnings_movestoploss_2(self, loss_scope):
        '''
        when the price moved one loss_scope, the stoploss add on loss_scope
        '''
        rtn = 0
        start = self.bars[0].price
        stoploss = self.bars[0].price - loss_scope
        for i, bar in enumerate(self.bars):
            
            if bar.price > stoploss + loss_scope:
                stoploss += loss_scope
            
            #self.__movestoploss_print(i, temp_high, stoploss, bar.price)
            if bar.price <= stoploss:
                rtn = stoploss - start
                return rtn
        return self.bars[-1].price - start
   
    def earnings_fixedterm(self):
        
        return self.bars[-1].price - self.bars[0].price
       

    def earnings_stoploss(self, loss_scope):
        if self.low <= self.bars[0].price - loss_scope:
            return -loss_scope
        return self.bars[-1].price - self.bars[0].price

    def earnings_target_profit(self, target_profit):
        if self.high >= self.bars[0].price + target_profit:
            return target_profit
        return self.bars[-1].price - self.bars[0].price

    def __movestoploss_print(self, i, temp_high, stoploss, barprice):
        '''for test use'''
        print str(i)+',', format(temp_high, '.1f'), format(stoploss, '.1f'), format(barprice, '.1f')


    def movestoploss_sell(self, atr):
        pass

'''
strategy
'''
def movesotploss_avg_earnings(loss_scope, runtimes=__RUNTIMES):
    '''

    '''
    earnings = 0
    for n in range(runtimes):
        a = Analysis(BarSequence(__BAR_NUM))
        one_earning = a.earnings_movestoploss(loss_scope)
        #print one_earning
        earnings += one_earning
    avg_earning = earnings / runtimes
    return avg_earning

def movesotploss_avg_earnings_2(loss_scope, runtimes=__RUNTIMES):
    earnings = 0
    for n in range(runtimes):
        a = Analysis(BarSequence(__BAR_NUM))
        one_earning = a.earnings_movestoploss_2(loss_scope)
        #print one_earning
        earnings += one_earning
    avg_earning = earnings / runtimes
    return avg_earning


def fixedterm_avg_earnings(runtimes=__RUNTIMES):
    earnings = 0
    for n in range(runtimes):
        bs = BarSequence(__BAR_NUM)
        a = Analysis(bs)
        one_earning = a.earnings_fixedterm()
        #print one_earning
        earnings += one_earning
    avg_earning = earnings / runtimes
    return avg_earning


def stoploss_avg_earnings(loss_scope, runtimes=__RUNTIMES):
    earnings = 0
    for n in range(runtimes):
        bs = BarSequence(__BAR_NUM)
        a = Analysis(bs)
        one_earning = a.earnings_stoploss(loss_scope)
        #print one_earning
        earnings += one_earning
    avg_earning = earnings / runtimes
    return avg_earning


def target_profit_avg_earnings(target_profit, runtimes=__RUNTIMES):
    earnings = 0
    for n in range(runtimes):
        bs = BarSequence(__BAR_NUM)
        a = Analysis(bs)
        one_earning = a.earnings_target_profit(target_profit)
        #print one_earning
        earnings += one_earning
    avg_earning = earnings / runtimes
    return avg_earning


if __name__ == '__main__':
    
    bs = BarSequence(200)
    #bs.print_bar_prices()

    a = Analysis(bs)
    #print a.get_sliced_barprice(3)
    #print a.earnings_movestoploss_2(100)
    #print a.earnings_stoploss(50)
    #print a.earnings_target_profit(50)


    #print movesotploss_avg_earnings(100) # 15.9 14
    print movesotploss_avg_earnings_2(100) # 16
    #print fixedterm_avg_earnings() # -6.7 -6
    #print stoploss_avg_earnings(100) # 20 6
    #print target_profit_avg_earnings(100) # -13 -13 NO
