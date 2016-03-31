# encoding: utf-8
import sys
from itertools import combinations
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy
import util

_NO_EARNINGS = 9999999

class LookEarnings():
    def __init__(self, daima):
        df = pd.read_csv('data/%s.xls' % daima)
        util.strip_columns(df)
        self.df = df.loc[:, ['date', 'open', 'high', 'close', 'low', 'ma5', 'ma10', 'ma20', 'ma40', 'KDJ.K', 'KDJ.D', 'KDJ.J']]
        self.daima = daima
    
    @util.display_func_name
    def foo(self, days=5):
        '''没条件  做多 看n天后收益
          作为参考基准,结果比这个差的就不用看了
        '''
        df = deepcopy(self.df)
        daima = self.daima

        df['earning'] = df.open.shift(days) - df.open

        func_name = sys._getframe().f_code.co_name
        self._to_result(df, days, func_name)

    @util.display_func_name
    def foosell(self, days=5):
        '''没条件  做空 看n天后收益
          作为参考基准,结果比这个差的就不用看了
        '''
        df = deepcopy(self.df)
        daima = self.daima

        df['earning'] = df.open - df.open.shift(days)

        func_name = sys._getframe().f_code.co_name
        self._to_result(df, days, func_name)

    @util.display_func_name
    def gt_ma(self, days=5, ma='ma5'):
        '''
        做多
        '''
        df = deepcopy(self.df)
        daima = self.daima
        df['gt_ma'] = df.low.shift(-1) > df[ma].shift(-1)
        df['earning'] = np.where(df['gt_ma'], df.open.shift(days) - df.open, _NO_EARNINGS)
        
        func_name = sys._getframe().f_code.co_name
        self._to_result(df, days, func_name)

    @util.display_func_name
    def lt_ma(self, days=5, ma='ma5'):
        '''
        做空
        '''
        df = deepcopy(self.df)
        daima = self.daima
        df['lt_ma'] = df.high.shift(-1) < df[ma].shift(-1)
        df['earning'] = np.where(df['lt_ma'], df.open - df.open.shift(days), _NO_EARNINGS)
        
        func_name = sys._getframe().f_code.co_name
        df.to_csv('files_tmp/looke_%s_%s_before.csv' % (func_name, daima))  # 以函数名作为文件名保存
        self._to_result(df, days, func_name)

    @util.display_func_name
    def ma_up(self, days=5, ma='ma5'):
        '''
        做多
        '''
        df = deepcopy(self.df)
        daima = self.daima
        df['ma_up'] = df[ma].shift(-1) > df[ma].shift(-2)
        df['earning'] = np.where(df['ma_up'], df.open.shift(days) - df.open, _NO_EARNINGS)
        
        func_name = sys._getframe().f_code.co_name
        self._to_result(df, days, func_name)

    @util.display_func_name
    def ma_down(self, days=5, ma='ma5'):
        '''
        做空
        '''
        df = deepcopy(self.df)
        daima = self.daima
        df['ma_down'] = df[ma].shift(-1) < df[ma].shift(-2)
        df['earning'] = np.where(df['ma_down'], df.open - df.open.shift(days), _NO_EARNINGS)
        
        func_name = sys._getframe().f_code.co_name
        self._to_result(df, days, func_name)

    @util.display_func_name
    def maup_gtma(self, days=5, ma='ma5'):
        '''
        做多
        '''
        df = deepcopy(self.df)
        daima = self.daima
        df['ma_up'] = df[ma].shift(-1) > df[ma].shift(-2)
        df['gt_ma'] = df.low.shift(-1) > df[ma].shift(-1)
        df['all'] = df.ma_up & df.gt_ma
        df['earning'] = np.where(df['all'], df.open.shift(days) - df.open, _NO_EARNINGS)
        
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
        做多
        '''
        df = deepcopy(self.df)
        daima = self.daima
        df['up1'] = df['ma5'].shift(-1) > df['ma5'].shift(-2)
        df['up2'] = df['ma10'].shift(-1) > df['ma10'].shift(-2)
        df['up3'] = df['ma20'].shift(-1) > df['ma20'].shift(-2)
        df['up4'] = df['ma40'].shift(-1) > df['ma40'].shift(-2)
        
        df['all'] = df.up1 & df.up2 & df.up3 & df.up4
        df['earning'] = np.where(df['all'], df.open.shift(days) - df.open, _NO_EARNINGS)
        
        func_name = sys._getframe().f_code.co_name
        self._to_result(df, days, func_name)


    @util.display_func_name
    def allmadown(self, days=5):
        '''
        做空
        '''
        df = deepcopy(self.df)
        daima = self.daima
        df['down1'] = df['ma5'].shift(-1) < df['ma5'].shift(-2)
        df['down2'] = df['ma10'].shift(-1)< df['ma10'].shift(-2)
        df['down3'] = df['ma20'].shift(-1) < df['ma20'].shift(-2)
        df['down4'] = df['ma40'].shift(-1) < df['ma40'].shift(-2)
        
        df['all'] = df.down1 & df.down2 & df.down3 & df.down4
        df['earning'] = np.where(df['all'], df.open - df.open.shift(days), _NO_EARNINGS)
        
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
        df.to_csv('files_tmp/looke_%s_%s.csv' % (func_name, daima))  # 以函数名作为文件名保存

        df = df.where(df.earning != _NO_EARNINGS) 
        #df2 = df.where(df.earning > 0) 
        summ = df.earning.sum()

        count = df.earning.count() #
        #count2 = df2.earning.count()
        mean = df.earning.mean()
        median = df.earning.median()
        print "earnings of  ---- mean:%s, median:%s, count:%s" %(mean, median, count)
        
    
        #sorted_earnings = sorted(df.earning)
  

if __name__ == '__main__':

    daima = 'ml9'
    days=200
    ma='ma20'
    le = LookEarnings(daima)
    le.foo(days=days)
    le.foosell(days=days)
    #le.maup_gtma_lt_200qian(days=days, ma=ma)
    
    le.gt_ma(days=days, ma=ma)
    le.lt_ma(days=days, ma=ma)
    le.ma_up(days=days, ma=ma)
    le.ma_down(days=days, ma=ma)
    #le.maup_gtma(days=days, ma=ma)
    #le.madown_ltma(days=days, ma=ma)
    le.allmaup(days=days)
    le.allmadown(days=days)
    pass