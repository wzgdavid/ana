# encoding: utf-8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from general_index import General, GeneralIndex, rangerun, rangerun3
from copy import deepcopy

class Tongji(GeneralIndex):
    def __init__(self, daima):
        super(Tongji, self).__init__(daima)
        
        self.get_sdjj()

    def ratio(self, x):
        '''
        后x天平均价格与当天平均价格的比值
        '''
        print 'ratio------%s-----'% (x)
        df = deepcopy(self.df)
        df['shiftx'] = df.sdjj.shift(-1*x)
        df['ratio'] = df.shiftx / df.sdjj
        self._to_result(df)
        
    def close_ratio_tupoh(self, x, n):
        print 'close_ratio_tupoh------%s-----%s---'% (x, n)
        self.get_nhh(n)
        df = deepcopy(self.df)
        df['shiftx'] = df.sdjj.shift(-1*x)
        df['higher'] = df.h > df.nhh
        df['ratio'] = np.where(df['higher'], df.shiftx / df.sdjj, None)
        self._to_result(df)

    def close_ratio_tupol(self, x, n):
        print 'close_ratio_tupol------%s-----%s---'% (x, n)
        self.get_nll(n)
        df = deepcopy(self.df)
        df['shiftx'] = df.sdjj.shift(-1*x)
        df['lower'] = df.l < df.nll
        df['ratio'] = np.where(df['lower'], df.sdjj / df.shiftx, None)
        self._to_result(df)
    
    def _to_result(self, df):
        mean = df.ratio.mean()
        median =  df.ratio.median()
        print '均值：%s，中位数：%s' % (round(mean, 5), round(median, 5))
        df.to_csv('tmp.csv')


if __name__ == '__main__':
    t = Tongji('999999')
    t.ratio(20)
    t.close_ratio_tupol(20, 7)
    t.close_ratio_tupol(20, 10)
    t.close_ratio_tupol(20, 20)
