# encoding: utf-8
import sys
sys.path.append("..")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from general_index import General, GeneralIndex, rangerun, rangerun3
from copy import deepcopy
import util

class GL(GeneralIndex):
    def __init__(self, daima):
        super(GL, self).__init__(daima)

    def tupohl(self, n, m, zs=2):
        print 'tupohl------%s------%s-----------'% (n, m)

        df = self._init_data(n, m, zs)

        # duo tou
        df['higher'] = df.h > df.nhh
        df['hbz'] = np.where(df['higher'], df.mll/df.zsll , None)
        #df['hbz_biggerthan1'] = np.where(df.hbz>1, True, None)
        # kong tou  
        df['lower'] = df.l < df.nll
        df['lbz'] = np.where(df['lower'], df.mhh/df.zshh , None)
        #df['lbz_smallerthan1'] = np.where(df.lbz<1, True, None)
        #print df.hbz.mean() # 应该大于1

        self._to_result(df)


    def tupohl2(self, n, m, zs=2):
        print 'tupohl2------%s------%s-----------'% (n, m)
        df = self._init_data(n, m, zs)

        # duo tou
        df['higher'] = df.h > df.nhh
        df['hh'] = df.l.shift(1) > df.l.shift(2)
        df['hbz'] = np.where(df['higher'] & df.hh, df.mll/df.zsll , None)
        #df['hbz_biggerthan1'] = np.where(df.hbz>1, True, None)
        # kong tou  
        df['lower'] = df.l < df.nll
        df['ll'] = df.h.shift(1) < df.h.shift(2)
        df['lbz'] = np.where(df['lower'] & df.ll, df.mhh/df.zshh , None)
        #df['lbz_smallerthan1'] = np.where(df.lbz<1, True, None)

        self._to_result(df)


    def chhll(self, n, m, zs=2):
        print 'chhll------%s------%s-----------'% (n, m)
        df = self._init_data(n, m, zs)

        # duo tou
        df['higher'] = df.h > df.nhh
        df['hh'] = df.c.shift(1) > df.c.shift(2)
        df['hbz'] = np.where(df['higher'] & df.hh, df.mll/df.zsll , None)
        #df['hbz_biggerthan1'] = np.where(df.hbz>1, True, None)
        #print df.hbz.mean() # 应该大于1
        # kong tou  
        df['lower'] = df.l < df.nll
        df['ll'] = df.c.shift(1) < df.c.shift(2)
        df['lbz'] = np.where(df['lower'] & df.ll, df.mhh/df.zshh , None)
        #df['lbz_smallerthan1'] = np.where(df.lbz<1, True, None)
        self._to_result(df)


    def all(self, n, m, zs=2):
        print 'all------%s------%s-----------'% (n, m)
        df = self._init_data(n, m, zs)

        # duo tou
        df['higher'] = df.h > df.nhh
        df['hh1'] = df.l.shift(1) > df.l.shift(2)
        df['hh2'] = df.c.shift(1) > df.c.shift(2)
        df['hbz'] = np.where(df['higher'] & df.hh1 & df.hh2, df.mll/df.zsll , None)
        #df['hbz_biggerthan1'] = np.where(df.hbz>1, True, None)
        # kong tou  
        df['lower'] = df.l < df.nll
        df['ll1'] = df.h.shift(1) < df.h.shift(2)
        df['ll2'] = df.c.shift(1) < df.c.shift(2)
        df['lbz'] = np.where(df['lower'] & df.ll1 & df.ll2, df.mhh/df.zshh , None)
        #df['lbz_smallerthan1'] = np.where(df.lbz<1, True, None)

        self._to_result(df)


    def _init_data(self, n, m, zs):
        self.get_nhh(n)
        self.get_nll(n)
        self.get_mhh(m)
        self.get_mll(m)
        self.get_zshh(zs)
        self.get_zsll(zs)
        return deepcopy(self.df) 

    def _to_result(self, df):
        hlist = [x for x in sorted(df.hbz) if x>0]
        hlistbiggerthan1 = [x for x in hlist if x>1]
        hgl = len(hlistbiggerthan1)/float(len(hlist)) # 大于1 的概率(在m天里没止损)
        print hgl, 'hgl', len(hlist)

        #print df.lbz.mean() # 应该小于1
        llist = [x for x in sorted(df.lbz) if x>0]
        llistsmallerthan1 = [x for x in llist if x<1]
        lgl = len(llistsmallerthan1)/float(len(llist)) # 小于1 的概率(在m天里没止损)
        print lgl, 'lgl', len(llist)

        df.to_csv('tmp.csv')


if __name__ == '__main__':
    g = GL('999999') # ta rb c m a ma jd dy 999999
    #g.tupohl(2,2)
    #g.tupohl(2,3)
    #g.tupohl(2,4)
    #g.tupohl(2,5)
    #g.tupohl(2,6)
    #g.tupohl(2,7)
    g.tupohl(2,3, 1)
    #g.chhll(2,3)
    #g.tupohl2(2,3)
    g.all(2,3,1)
    g.all(2,3,2)
    #g.chhll(2,3)
    #g.tupohl(4,3)
    
    