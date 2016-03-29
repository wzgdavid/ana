# encoding: utf-8
import sys
from itertools import combinations
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tushare as ts
from copy import deepcopy
import util
'''
看n天里最低，最高点,变动范围
'''

_NO_PCT = 99999

class Normal():
    def __init__(self, daima):
        df = pd.read_csv('data/%s.xls' % daima)
        util.strip_columns(df)
        self.df = df.loc[:, ['date', 'open', 'high', 'close', 'low', 'ma5', 'ma10', 'ma20', 'ma40', 'KDJ.K', 'KDJ.D', 'KDJ.J']]
        self.daima = daima
    
    @util.display_func_name
    def foo(self, days=5):
        '''没条件  买进 看n天后收益
          作为参考基准,结果比这个差的就不用看了
        '''
        df = deepcopy(self.df)
        daima = self.daima

        df['pct'] = (df.open.shift(days) - df.open) / df.open
        df['low_pct'] = (pd.rolling_min(df.low, days) - df.open) / df.open
        df['high_pct'] = (pd.rolling_max(df.high, days) - df.open) / df.open
        #df['pct']= df.pct.apply(lambda x: float('%.2f' % x))
        func_name = sys._getframe().f_code.co_name
        #self._to_result(df, days, func_name)
        self._to_normal_distribution(df, days, func_name)

    @util.display_func_name
    def gt_ma(self, days=5, ma='ma5'):
        '''
        '''
        df = deepcopy(self.df)
        daima = self.daima
        df['gt_ma'] = df.low.shift(-1) > df[ma].shift(-1)
        df['pct'] = np.where(df['gt_ma'], (df.open.shift(days) - df.open) / df.open, _NO_PCT)
        df['low_pct'] = np.where(df['gt_ma'], (pd.rolling_min(df.low, days) - df.open) / df.open, _NO_PCT)
        df['high_pct'] = np.where(df['gt_ma'],(pd.rolling_max(df.high, days) - df.open) / df.open, _NO_PCT)
        func_name = sys._getframe().f_code.co_name
        self._to_normal_distribution(df, days, func_name)

    @util.display_func_name
    def lt_ma(self, days=5, ma='ma5'):
        '''
        '''
        df = deepcopy(self.df)
        daima = self.daima
        df['lt_ma'] = df.high.shift(-1) < df[ma].shift(-1)
        df['pct'] = np.where(df['lt_ma'], (df.open.shift(days) - df.open) / df.open, _NO_PCT)
        df['low_pct'] = np.where(df['lt_ma'], (pd.rolling_min(df.low, days) - df.open) / df.open, _NO_PCT)
        df['high_pct'] = np.where(df['lt_ma'],(pd.rolling_max(df.high, days) - df.open) / df.open, _NO_PCT)
        func_name = sys._getframe().f_code.co_name
        self._to_normal_distribution(df, days, func_name)


    @util.display_func_name
    def ma_up(self, days=5, ma='ma5'):
        '''
        '''
        df = deepcopy(self.df)
        daima = self.daima
        df['ma_up'] = df[ma].shift(-1) > df[ma].shift(-2)
        df['pct'] = np.where(df['ma_up'], (df.open.shift(days) - df.open) / df.open, _NO_PCT)
        df['low_pct'] = np.where(df['ma_up'], (pd.rolling_min(df.low, days) - df.open) / df.open, _NO_PCT)
        df['high_pct'] = np.where(df['ma_up'],(pd.rolling_max(df.high, days) - df.open) / df.open, _NO_PCT)
        
        func_name = sys._getframe().f_code.co_name
        self._to_normal_distribution(df, days, func_name)

    @util.display_func_name
    def ma_down(self, days=5, ma='ma5'):
        '''
        '''
        df = deepcopy(self.df)
        daima = self.daima
        df['ma_down'] = df[ma].shift(-1) < df[ma].shift(-2)
        df['pct'] = np.where(df['ma_down'], (df.open.shift(days) - df.open) / df.open, _NO_PCT)
        func_name = sys._getframe().f_code.co_name
        self._to_normal_distribution(df, days, func_name)

    @util.display_func_name
    def maup_gtma(self, days=5, ma='ma5'):
        '''
        '''
        df = deepcopy(self.df)
        daima = self.daima
        df['ma_up'] = df[ma].shift(-1) > df[ma].shift(-2)
        df['gt_ma'] = df.low.shift(-1) > df[ma].shift(-1)
        df['all'] = df.ma_up & df.gt_ma
        df['pct'] = np.where(df['all'], (df.open.shift(days) - df.open) / df.open, _NO_PCT)
        df['low_pct'] = np.where(df['all'], (pd.rolling_min(df.low, days) - df.open) / df.open, _NO_PCT)
        df['high_pct'] = np.where(df['all'],(pd.rolling_max(df.high, days) - df.open) / df.open, _NO_PCT)
        func_name = sys._getframe().f_code.co_name
        self._to_normal_distribution(df, days, func_name)

    @util.display_func_name
    def allmaup(self, days=5):
        '''
        '''
        df = deepcopy(self.df)
        daima = self.daima
        df['up1'] = df['ma5'].shift(-1) > df['ma5'].shift(-2)
        df['up2'] = df['ma10'].shift(-1) > df['ma10'].shift(-2)
        df['up3'] = df['ma20'].shift(-1) > df['ma20'].shift(-2)
        df['up4'] = df['ma40'].shift(-1) > df['ma40'].shift(-2)
        
        df['all'] = df.up1 & df.up2 & df.up3 & df.up4
        df['pct'] = np.where(df['all'], (df.open.shift(days) - df.open) / df.open, _NO_PCT)
        df['low_pct'] = np.where(df['all'], (pd.rolling_min(df.low, days) - df.open) / df.open, _NO_PCT)
        df['high_pct'] = np.where(df['all'],(pd.rolling_max(df.high, days) - df.open) / df.open, _NO_PCT)
        func_name = sys._getframe().f_code.co_name
        self._to_normal_distribution(df, days, func_name)


    @util.display_func_name
    def allmadown(self, days=5):
        '''
        '''
        df = deepcopy(self.df)
        daima = self.daima
        df['down1'] = df['ma5'].shift(-1) < df['ma5'].shift(-2)
        df['down2'] = df['ma10'].shift(-1)< df['ma10'].shift(-2)
        df['down3'] = df['ma20'].shift(-1) < df['ma20'].shift(-2)
        df['down4'] = df['ma40'].shift(-1) < df['ma40'].shift(-2)
        
        df['all'] = df.down1 & df.down2 & df.down3 & df.down4
        df['pct'] = np.where(df['all'], (df.open.shift(days) - df.open) / df.open, _NO_PCT)
        df['low_pct'] = np.where(df['all'], (pd.rolling_min(df.low, days) - df.open) / df.open, _NO_PCT)
        df['high_pct'] = np.where(df['all'],(pd.rolling_max(df.high, days) - df.open) / df.open, _NO_PCT)
        func_name = sys._getframe().f_code.co_name
        self._to_normal_distribution(df, days, func_name)

    @util.display_func_name
    def madown_ltma(self, days=5, ma='ma5'):
        '''
        '''
        df = deepcopy(self.df)
        daima = self.daima
        df['ma_down'] = df[ma].shift(-1) < df[ma].shift(-2)
        df['lt_ma'] = df.high.shift(-1) < df[ma].shift(-1)
        df['all'] = df.ma_down & df.lt_ma
        df['earning'] = np.where(df['all'], df.open.shift(days) - df.open, _NO_PCT)
        
        func_name = sys._getframe().f_code.co_name
        self._to_result(df, days, func_name)

    def _to_result(self, df, days, func_name):
        daima = self.daima
        df = df.loc[days: , :]  # 因为近期的看不到n天后的数据，所以没收益，因此不计算
        df.to_csv('files_tmp/looke_%s_%s.csv' % (func_name, daima))  # 以函数名作为文件名保存

        df = df.where(df.earning != _NO_PCT) 
        summ = df.earning.sum()

        count = df.earning.count() # 
        mean = df.earning.mean()
        median = df.earning.median()
        print "earnings of  ---- mean:%s, median:%s, count:%s" %(mean, median, count)
    
        sorted_earnings = sorted(df.earning)
  
    def _to_normal_distribution(self, df, days, func_name):
        daima = self.daima
        df = df.loc[days: , :]  # 因为近期的看不到n天后的数据，所以没收益，因此不计算
        
        #mu = 2000
        #sigma = 25
        #x = mu + sigma*np.random.randn(9999)
        #df = df.where(df.pct != _NO_PCT) 
        df = df[df['pct'] < _NO_PCT]
        #bins = [-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.5,0.6]
        bins = np.arange(-3,5,0.5)
        df.to_csv('files_tmp/normal_%s_%s.csv' % (func_name, daima))  # 以函数名作为文件名保存
        fig,(ax1, ax2, ax3) = plt.subplots(ncols=3, figsize=(20, 8))
        
        #ax1.hist(df.pct, bins, normed=1, histtype='bar', facecolor='b', alpha=0.75)
        #ax1.set_title('%s_%s_%s' % (func_name, daima, 'pct'))
        '''
        ax2.hist(df.low_pct, 50, normed=1, histtype='stepfilled', facecolor='g', alpha=0.75)
        ax2.set_title('%s_%s_%s' % (func_name, daima, 'low_pct'))

        ax3.hist(df.high_pct, 50, normed=1, histtype='stepfilled', facecolor='r', alpha=0.75)
        ax3.set_title('%s_%s_%s' % (func_name, daima, 'high_pct'))
        '''
        bins = np.arange(-0.4,0.1,0.01)
        ax2.hist(df.low_pct, bins, normed=1, histtype='bar', rwidth=1,facecolor='g', alpha=0.75)
        ax2.set_title('%s_%s_%s' % (func_name, daima, 'low_pct'))
        
        bins = np.arange(-0.1,0.3,0.01)
        ax3.hist(df.high_pct, bins, normed=1, histtype='bar', rwidth=1,facecolor='r', alpha=0.75)
        ax3.set_title('%s_%s_%s' % (func_name, daima, 'high_pct'))

        plt.xlabel('percent')
        plt.tight_layout()
        plt.show()


        


if __name__ == '__main__':

    daima = 't001'
    days=5
    ma='ma20'
    le = Normal(daima)
    #le.foo(days=days)
    #le.gt_ma(days=days, ma=ma)
    #le.lt_ma(days=days, ma=ma)
    #le.ma_up(days=days, ma=ma)
    #le.ma_down(days=days, ma=ma)
    le.maup_gtma(days=days, ma=ma)
    #le.madown_ltma(days=days, ma=ma)
    #le.allmaup(days=days)
    #le.allmadown(days=days)
    pass

