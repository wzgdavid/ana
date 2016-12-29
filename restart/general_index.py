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

    def run(self, df):
        '''没有资金管理，没有止损，每出现一次开仓信号，就开一手，一旦出现相反信号全平仓'''
        cnt = 0 # 每出一次开仓信号，就开一手，共几手的计数。一旦相反信号出来全平仓
        kprice = 0 # 所有持仓的开仓价格之和，不是多仓就是空仓
        total = 0
        icnt = 0 # 交易次数
        # 做多
        for i, bksk in enumerate(df.bksk):
            
            idx = df.index[i]
            
            if bksk == 'bk':
                
                bkprice = df.loc[idx, 'sdjj'] # 买开仓的价位
                #print bkprice
                kprice += bkprice
                cnt += 1
                
            elif bksk == 'sk' and cnt != 0:
                skprice = df.loc[idx, 'sdjj']
                gain = skprice*cnt - kprice # 平仓盈亏
                #print skprice, kprice, gain
                total += gain
                icnt += cnt
                print icnt, cnt, total
                cnt = 0
                kprice = 0
                
        

        cnt = 0 # 每出一次开仓信号，就开一手，共几手的计数。一旦相反信号出来全平仓
        kprice = 0 # 所有持仓的开仓价格之和，不是多仓就是空仓
        total2 = 0

        print '------------------------------------'
        # 做空 分开计算容易写
        for i, bksk in enumerate(df.bksk):

            idx = df.index[i]
            
            if bksk == 'sk':
                
                skprice = df.loc[idx, 'sdjj'] # 开仓的价位
                #print skprice
                kprice += skprice
                cnt += 1
            elif bksk == 'bk' and cnt != 0:
                bkprice = df.loc[idx, 'sdjj'] # 平仓价格
                gain = kprice - bkprice*cnt # 平仓盈亏
                #print skprice, kprice, gain
                total2 += gain
                icnt += cnt
                print icnt, cnt, total2
                cnt = 0
                kprice = 0
        print total + total2 



class GeneralIndex(General):
    def __init__(self, daima):
        super(GeneralIndex, self).__init__(daima)

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