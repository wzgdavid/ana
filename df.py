# encoding: utf-8
import sys
from itertools import combinations
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import util
'''
看n天里最低，最高点,变动范围
'''


class LookLow():
    def __init__(self, daima):
        df = pd.read_csv('data/%s.xls' % daima)
        util.strip_columns(df)
        self.df = df.loc[:, ['date', 'open', 'high', 'close', 'low', 'ma5', 'ma10', 'ma20', 'ma40', 'KDJ.K', 'KDJ.D', 'KDJ.J']]
        self.daima = daima

    @util.display_func_name
    def bar(self, days=5):
        df = self.df
        daima = self.daima
        df['low_pct'] = (pd.rolling_min(df.low, days) - df.open) / df.open
        df['high_pct'] = (pd.rolling_max(df.high, days) - df.open) / df.open

        func_name = sys._getframe().f_code.co_name
        self._to_result(df, days, func_name)

    @util.display_func_name
    def gt_ma(self, ma='ma5', days=5):
        df = self.df
        daima = self.daima

        df['gt_ma'] = df.low.shift(-1) > df[ma].shift(-1)
        low_value = (pd.rolling_min(df.low, days) - df.open) / df.open
        high_value = (pd.rolling_max(df.high, days) - df.open) / df.open

        df['low_pct'] = np.where(df['gt_ma'], low_value , 9)
        df['high_pct'] = np.where(df['gt_ma'], high_value , 9)
        
        func_name = sys._getframe().f_code.co_name
        self._to_result(df, days, func_name)


    @util.display_func_name
    def lt_ma(self, ma='ma5', days=5):
        df = self.df
        daima = self.daima

        df['lt_ma'] = df.high.shift(-1) < df[ma].shift(-1)
        low_value = (pd.rolling_min(df.low, days) - df.open) / df.open
        high_value = (pd.rolling_max(df.high, days) - df.open) / df.open

        df['low_pct'] = np.where(df['lt_ma'], low_value , 9)
        df['high_pct'] = np.where(df['lt_ma'], high_value , 9)

        func_name = sys._getframe().f_code.co_name
        self._to_result(df, days, func_name)

    @util.display_func_name
    def ma_up(self, ma='ma5', days=5):
        df = self.df
        daima = self.daima

        df['ma_up'] = df[ma].shift(-1) > df[ma].shift(-2)
        low_value = (pd.rolling_min(df.low, days) - df.open) / df.open
        high_value = (pd.rolling_max(df.high, days) - df.open) / df.open

        df['low_pct'] = np.where(df['ma_up'], low_value , 9)
        df['high_pct'] = np.where(df['ma_up'], high_value , 9)

        func_name = sys._getframe().f_code.co_name
        self._to_result(df, days, func_name)

    @util.display_func_name
    def ma_down(self, ma='ma5', days=5):
        df = self.df
        daima = self.daima

        df['ma_down'] = df[ma].shift(-1) < df[ma].shift(-2)
        low_value = (pd.rolling_min(df.low, days) - df.open) / df.open
        high_value = (pd.rolling_max(df.high, days) - df.open) / df.open

        df['low_pct'] = np.where(df['ma_down'], low_value , 9)
        df['high_pct'] = np.where(df['ma_down'], high_value , 9)

        func_name = sys._getframe().f_code.co_name
        self._to_result(df, days, func_name)


    @util.display_func_name
    def maup_gtma(self, ma='ma5', days=5):
        df = self.df
        daima = self.daima

        df['ma_up'] = df[ma].shift(-1) > df[ma].shift(-2)
        df['gt_ma'] = df.low.shift(-1) > df[ma].shift(-1)
        df['all'] = df.ma_up & df.gt_ma
        low_value = (pd.rolling_min(df.low, days) - df.open) / df.open
        high_value = (pd.rolling_max(df.high, days) - df.open) / df.open

        df['low_pct'] = np.where(df['all'], low_value , 9)
        df['high_pct'] = np.where(df['all'], high_value , 9)

        func_name = sys._getframe().f_code.co_name
        self._to_result(df, days, func_name)

    @util.display_func_name
    def maup_ltma(self, ma='ma5', days=5):
        df = self.df
        daima = self.daima

        df['ma_up'] = df[ma].shift(-1) > df[ma].shift(-2)
        df['lt_ma'] = df.high.shift(-1) < df[ma].shift(-1)
        df['all'] = df.ma_up & df.lt_ma
        low_value = (pd.rolling_min(df.low, days) - df.open) / df.open
        high_value = (pd.rolling_max(df.high, days) - df.open) / df.open

        df['low_pct'] = np.where(df['all'], low_value , 9)
        df['high_pct'] = np.where(df['all'], high_value , 9)

        func_name = sys._getframe().f_code.co_name
        self._to_result(df, days, func_name)

    @util.display_func_name
    def madown_ltma(self, ma='ma5', days=5):
        df = self.df
        daima = self.daima

        df['ma_down'] = df[ma].shift(-1) < df[ma].shift(-2)
        df['lt_ma'] = df.high.shift(-1) < df[ma].shift(-1)
        df['all'] = df.ma_down & df.lt_ma
        low_value = (pd.rolling_min(df.low, days) - df.open) / df.open
        high_value = (pd.rolling_max(df.high, days) - df.open) / df.open

        df['low_pct'] = np.where(df['all'], low_value , 9)
        df['high_pct'] = np.where(df['all'], high_value , 9)

        func_name = sys._getframe().f_code.co_name
        self._to_result(df, days, func_name)

    @util.display_func_name
    def madown_gtma(self, ma='ma5', days=5):
        df = self.df
        daima = self.daima

        df['ma_down'] = df[ma].shift(-1) < df[ma].shift(-2)
        df['gt_ma'] = df.low.shift(-1) > df[ma].shift(-1)
        df['all'] = df.ma_down & df.gt_ma
        low_value = (pd.rolling_min(df.low, days) - df.open) / df.open
        high_value = (pd.rolling_max(df.high, days) - df.open) / df.open

        df['low_pct'] = np.where(df['all'], low_value , 9)
        df['high_pct'] = np.where(df['all'], high_value , 9)

        func_name = sys._getframe().f_code.co_name
        self._to_result(df, days, func_name)

    @util.display_func_name
    def ma51020_up(self, days=5):
        df = self.df
        daima = self.daima

        df['up1'] = df['ma5'].shift(-1) > df['ma5'].shift(-2)
        df['up2'] = df['ma10'].shift(-1) > df['ma10'].shift(-2)
        df['up3'] = df['ma20'].shift(-1) > df['ma20'].shift(-2)
        
        df['all'] = df.up1 & df.up2 & df.up3
        low_value = (pd.rolling_min(df.low, days) - df.open) / df.open
        high_value = (pd.rolling_max(df.high, days) - df.open) / df.open

        df['low_pct'] = np.where(df['all'], low_value , 9)
        df['high_pct'] = np.where(df['all'], high_value , 9)

        func_name = sys._getframe().f_code.co_name
        self._to_result(df, days, func_name)

    @util.display_func_name
    def ma5102040_up(self, days=5):
        df = self.df
        daima = self.daima

        df['up1'] = df['ma5'].shift(-1) > df['ma5'].shift(-2)
        df['up2'] = df['ma10'].shift(-1) > df['ma10'].shift(-2)
        df['up3'] = df['ma20'].shift(-1) > df['ma20'].shift(-2)
        df['up4'] = df['ma40'].shift(-1) > df['ma40'].shift(-2)
        
        df['all'] = df.up1 & df.up2 & df.up3 & df.up4
        low_value = (pd.rolling_min(df.low, days) - df.open) / df.open
        high_value = (pd.rolling_max(df.high, days) - df.open) / df.open

        df['low_pct'] = np.where(df['all'], low_value , 9)
        df['high_pct'] = np.where(df['all'], high_value , 9)

        
        func_name = sys._getframe().f_code.co_name
        self._to_result(df, days, func_name)

    @util.display_func_name
    def ma102040_up(self, days=5):
        df = self.df
        daima = self.daima

        
        df['up2'] = df['ma10'].shift(-1) > df['ma10'].shift(-2)
        df['up3'] = df['ma20'].shift(-1) > df['ma20'].shift(-2)
        df['up4'] = df['ma40'].shift(-1) > df['ma40'].shift(-2)
        
        df['all'] = df.up2 & df.up3 & df.up4
        low_value = (pd.rolling_min(df.low, days) - df.open) / df.open
        high_value = (pd.rolling_max(df.high, days) - df.open) / df.open

        df['low_pct'] = np.where(df['all'], low_value , 9)
        df['high_pct'] = np.where(df['all'], high_value , 9)

        
        func_name = sys._getframe().f_code.co_name
        self._to_result(df, days, func_name)


    @util.display_func_name
    def which_ma_up_and_gtma(self, which_ma=[], ma='', days=5):
        df = self.df
        daima = self.daima

        # first all true
        df['up1'] = df.high>df.low
        df['up2'] = df.high>df.low
        df['up3'] = df.high>df.low
        df['up4'] = df.high>df.low
        
        if 'ma5' in which_ma:
            df['up1'] = df['ma5'].shift(-1) > df['ma5'].shift(-2)
        if 'ma10' in which_ma:
            df['up2'] = df['ma10'].shift(-1) > df['ma10'].shift(-2)
        if 'ma20' in which_ma:
            df['up3'] = df['ma20'].shift(-1) > df['ma20'].shift(-2)
        if 'ma40' in which_ma:
            df['up4'] = df['ma40'].shift(-1) > df['ma40'].shift(-2)
        
        df['gt_ma'] = df.low.shift(-1) > df[ma].shift(-1)

        df['all'] = df.up1 & df.up2 & df.up3 & df.up4 & df.gt_ma
        low_value = (pd.rolling_min(df.low, days) - df.open) / df.open
        high_value = (pd.rolling_max(df.high, days) - df.open) / df.open

        df['low_pct'] = np.where(df['all'], low_value , 9)
        df['high_pct'] = np.where(df['all'], high_value , 9)

        
        func_name = sys._getframe().f_code.co_name
        self._to_result(df, days, func_name)

    def _to_result(self, df, days, func_name):
        daima = self.daima
        df = df.loc[days: , :]  # 因为近期的看不到n天后的数据，所以没收益，因此不计算
        df = df[df.low_pct < 9]
        df.to_csv('files_tmp/looklow_%s_%s.csv' % (func_name, daima))  # 以函数名作为文件名保存

        median_low =  df.low_pct.median()
        median_high =  df.high_pct.median()
    
        mean_low = df.low_pct.mean()
        mean_high = df.high_pct.mean()

        lowsorted = sorted(df.low_pct, reverse=True)
        highsorted = sorted(df.high_pct)
        print 'count', len(lowsorted)
        #print lowsorted
        #print highsorted
        #print median_low, median_high, median_high +median_low
        #print lowsorted[len(lowsorted)*2/3],  highsorted[len(highsorted)*2/3], highsorted[len(highsorted)*2/3] + lowsorted[len(lowsorted)*2/3]
        print lowsorted[len(lowsorted)*3/4],  highsorted[len(highsorted)*3/4], highsorted[len(highsorted)*3/4]+ lowsorted[len(lowsorted)*3/4]
        #print lowsorted[len(lowsorted)*4/5],  highsorted[len(highsorted)*4/5], highsorted[len(highsorted)*4/5]+ lowsorted[len(lowsorted)*4/5]
        #print lowsorted[len(lowsorted)*9/10],  highsorted[len(highsorted)*9/10]
        #print lowsorted[len(lowsorted)*29/30],  highsorted[len(highsorted)*29/30]
        #print daima, days
        print median_low, median_high, median_high + median_low
        #print mean_low, mean_high, mean_high + mean_low


if __name__ == '__main__':
    #run_gtma()
    days=5
    ma='ma20'
    ll = LookLow('000004')
    ll.bar(days=days)
    #ll.ma_up(ma=ma,days=days)
    ll.maup_gtma(ma=ma,days=days)
    ll.ma102040_up(days=days)
    ll.ma5102040_up(days=days)
    #ll.which_ma_up_and_gtma(which_ma=['ma5', 'ma10', 'ma20', 'ma40'], ma=ma, days=days)

    #ll.ma_up(ma='ma20',days=days)
    #ll.ma_up(ma='ma40',days=days)
    #ll.gt_ma(ma='ma20',days=days)
    #ll.gt_ma(ma='ma40',days=days)
