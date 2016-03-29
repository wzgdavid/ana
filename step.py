# encoding: utf-8
import sys
from itertools import combinations
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tushare as ts
from copy import deepcopy
import util

_NO_EARNINGS = 99999
'''
以做多为例，看今天的高点与后n天低点的变动范围
'''
class StepRange():
    def __init__(self, daima):
        df = pd.read_csv('data/%s.xls' % daima)
        util.strip_columns(df)
        self.df = df.loc[:, ['date', 'open', 'high', 'close', 'low', 'ma5', 'ma10', 'ma20', 'ma40', 'KDJ.K', 'KDJ.D', 'KDJ.J']]
        self.daima = daima
    
    @util.display_func_name
    def foo(self, days=5):
        '''没条件 
        '''
        df = deepcopy(self.df)
        daima = self.daima
        #df['rolling low'] = pd.rolling_min(df.low.shift(1), days) #之后n天的最低点（不包括今天）
        df['rolling_low'] = pd.rolling_min(df.low, days) #之后n天的最低点（包括今天）
        df['step'] = (df.rolling_low - df.high) / df.rolling_low

        func_name = sys._getframe().f_code.co_name
        self._to_result(df, days, func_name)
        #df.to_csv('files_tmp/step_%s_%s.csv' % (func_name, daima))


    @util.display_func_name
    def gt_ma(self, days=5, ma='ma5'):
        '''
        '''
        df = deepcopy(self.df)
        daima = self.daima
        df['gt_ma'] = df.low.shift(-1) > df[ma].shift(-1)
        
        df['rolling_low'] = pd.rolling_min(df.low, days) #之后n天的最低点（包括今天）
        df['step'] = np.where(df['gt_ma'], (df.rolling_low - df.high) / df.rolling_low, _NO_EARNINGS)
        
        func_name = sys._getframe().f_code.co_name
        self._to_result(df, days, func_name)

    @util.display_func_name
    def lt_ma(self, days=5, ma='ma5'):
        '''
        '''
        df = deepcopy(self.df)
        daima = self.daima
        df['lt_ma'] = df.high.shift(-1) < df[ma].shift(-1)

        df['rolling_low'] = pd.rolling_min(df.low, days) 
        df['step'] = np.where(df['lt_ma'], (df.rolling_low - df.high) / df.rolling_low, _NO_EARNINGS)
        
        func_name = sys._getframe().f_code.co_name
        self._to_result(df, days, func_name)

    @util.display_func_name
    def ma_up(self, days=5, ma='ma5'):
        '''
        '''
        df = deepcopy(self.df)
        daima = self.daima
        df['ma_up'] = df[ma].shift(-1) > df[ma].shift(-2)
        df['rolling_low'] = pd.rolling_min(df.low, days)
        df['step'] = np.where(df['ma_up'], (df.rolling_low - df.high) / df.rolling_low, _NO_EARNINGS)
        
        func_name = sys._getframe().f_code.co_name
        self._to_result(df, days, func_name)

    @util.display_func_name
    def ma_down(self, days=5, ma='ma5'):
        '''
        '''
        df = deepcopy(self.df)
        daima = self.daima
        df['ma_down'] = df[ma].shift(-1) < df[ma].shift(-2)
        df['rolling_low'] = pd.rolling_min(df.low, days)
        df['step'] = np.where(df['ma_down'], (df.rolling_low - df.high) / df.rolling_low, _NO_EARNINGS)
        
        func_name = sys._getframe().f_code.co_name
        self._to_result(df, days, func_name)

    @util.display_func_name
    def maup_gtma(self, days=5, ma='ma5'):
        '''
        '''
        df = deepcopy(self.df)
        daima = self.daima
        df['ma_up'] = df[ma].shift(-1) > df[ma].shift(-2)
        df['gt_ma'] = df.low.shift(-1) > df[ma].shift(-1)
        df['all'] = df.ma_up & df.gt_ma
        df['rolling_low'] = pd.rolling_min(df.low, days)
        
        df['step'] = np.where(df['all'], (df.rolling_low - df.high) / df.rolling_low, _NO_EARNINGS)
        
        func_name = sys._getframe().f_code.co_name
        self._to_result(df, days, func_name)

    @util.display_func_name
    def maup_gtma_lt_200qian(self, days=5, ma='ma5'):
        '''
        '''
        df = deepcopy(self.df)
        daima = self.daima
        df['ma_up'] = df[ma].shift(-1) > df[ma].shift(-2)
        df['gt_ma'] = df.low.shift(-1) > df[ma].shift(-1)
        df['lt_200qian'] = df.open.shift(-1) < df[ma].shift(-1*days)
        df['all'] = df.ma_up & df.gt_ma & df.lt_200qian
        df['earning'] = np.where(df['all'], df.open.shift(days) - df.open, _NO_EARNINGS)
        
        func_name = sys._getframe().f_code.co_name
        self._to_result(df, days, func_name)

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
        df['rolling_low'] = pd.rolling_min(df.low, days)
        
        df['step'] = np.where(df['all'], (df.rolling_low - df.high) / df.rolling_low, _NO_EARNINGS)
        
        
        func_name = sys._getframe().f_code.co_name
        self._to_result(df, days, func_name)


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
        df['rolling_low'] = pd.rolling_min(df.low, days)
        
        df['step'] = np.where(df['all'], (df.rolling_low - df.high) / df.rolling_low, _NO_EARNINGS)
        
        
        func_name = sys._getframe().f_code.co_name
        self._to_result(df, days, func_name)

    @util.display_func_name
    def madown_ltma(self, days=5, ma='ma5'):
        '''
        '''
        df = deepcopy(self.df)
        daima = self.daima
        df['ma_down'] = df[ma].shift(-1) < df[ma].shift(-2)
        df['lt_ma'] = df.high.shift(-1) < df[ma].shift(-1)
        df['all'] = df.ma_down & df.lt_ma
        df['earning'] = np.where(df['all'], df.open.shift(days) - df.open, _NO_EARNINGS)
        
        func_name = sys._getframe().f_code.co_name
        self._to_result(df, days, func_name)

    def _to_result(self, df, days, func_name):
        daima = self.daima
        df = df.loc[days: , :]  # 因为近期的看不到n天后的数据，所以没收益，因此不计算
        df = df[df.step < _NO_EARNINGS]
        df.to_csv('files_tmp/step_%s_%s.csv' % (func_name, daima))
        
        print df.step.median(), df.step.mean()
        fig,ax1 = plt.subplots(ncols=1, figsize=(8, 13))
        #bins = np.arange(-0.5,0.1,0.05)
        bins = np.arange(-0.5,0.1,0.1)
        plt.ylim(-1.2, 15)
        ax1.hist(df.step, bins, normed=1, histtype='bar', facecolor='b', alpha=0.75)
        ax1.set_title('%s_%s_%s' % (func_name, daima, 'step'))
        

        plt.xlabel('percent')
        plt.tight_layout()
        plt.show()
  

if __name__ == '__main__':

    daima = 'aul9'
    days=5
    ma='ma20'
    le = StepRange(daima)
    #le.foo(days=days)
    #le.maup_gtma_lt_200qian(days=days, ma=ma)
    
    #le.gt_ma(days=days, ma=ma)
    #le.lt_ma(days=days, ma=ma)
    le.ma_up(days=days, ma=ma)
    #le.ma_down(days=days, ma=ma)
    #le.maup_gtma(days=days, ma=ma)
    #le.madown_ltma(days=days, ma=ma)
    #le.allmaup(days=days)
    #le.allmadown(days=days)
    pass