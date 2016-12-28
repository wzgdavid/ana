# encoding: utf-8
#import sys
#sys.path.append("..")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class General(object):
    def __init__(self, daima):
        #df = pd.read_csv('../data/%s.xls' % daima) # windows excel 制表符\t 影响读取
        df = pd.read_csv('../data/%s.csv' % daima)
        self.df = df
        self.daima = daima

    def foo(self):
        print self.df['o']


class GeneralIndex(General):
    def __init__(self, daima):
        super(GeneralIndex, self).__init__(daima)
        self.get_sdjj()
    #def __new__(self, daima):
    #    super(General, self).__init__(daima)

    #def ma5(self, n):
    #    self.ma5 = 

    def get_sdjj(self):
        '''
        四点均价  开收盘价，最高价，最低价
        '''
        self.df['sdjj'] = (self.df['o'] + self.df['c'] + self.df['h'] + self.df['l']) / 4

    #def get_ma5(self):
        #df['ma5'] = pd.rolling(self.df.c.shift(-1*5), 5).mean()
        
    #    self.df['ma5'] = self.df.c.rolling(window=5,center=False).mean()

    def get_ma(self, *malist):
        '''get_ma(5,10,20)  得到5,10,20周期的ma
        '''
        for n in malist:
            self.df['ma%s' % n]  = self.df.c.rolling(window=n, center=False).mean()

    def get_high_percent(self, n):
        '''最高点向下百分比
        '''
        self.df['hp'] = self.df.h * (1 - float(n)/100)

    def get_low_percent(self, n):
        '''最低点向上百分比
        '''
        self.df['lp'] = self.df.l * (1 + float(n)/100)

    def get_nhh(self, n):
        '''前n天最高价最高点（不包含当天）'''
        self.df['nhh'] = self.df.h.shift(1).rolling(window=n, center=False).max()

    def get_nll(self, n):
        '''前n天最低价最低点（不包含当天）'''
        self.df['nll'] = self.df.l.shift(1).rolling(window=n, center=False).min()

    def get_nsdh(self, n):
        '''前n天四点均价最高点（不包含当天）'''
        self.df['nsdh'] = self.df.sdjj.shift(1).rolling(window=n, center=False).max()

    def get_nsdl(self, n):
        '''前n天四点均价最低点（不包含当天）'''
        self.df['nsdl'] = self.df.sdjj.shift(1).rolling(window=n, center=False).min()


if __name__ == '__main__':

    #g = General('rb')
    #g.foo()
    gi = GeneralIndex('rb')
    #print gi.df['sdjj']
    #gi.get_ma5()
    #print gi.df.loc[:, ['c','ma5']]
    #print gi.df.describe()
    #gi.sdjj
    #gi.get_ma(5,10,20)
    
    #print gi.df.loc[:,['c','ma5', 'ma10', 'ma20']]
    gi.get_nsdl(10)
    print gi.df.loc[:, ['date','sdjj','nsdl']]
    #print gi.df.describe()