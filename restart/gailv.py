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


    def foo(self, n, m, zs=2):
        '''没条件， 对比用'''
        print 'foo------%s------%s-----------'% (n, m)
        df = self._init_data(n, m, zs)
        df['hbz'] = np.where(1, df.mll/df.zsll , None)
        df['lbz'] = np.where(1, df.mhh/df.zshh , None)
        self._to_result(df)

    def tupohl(self, n, m, zs=2):
        print 'tupohl------%s------%s-----------'% (n, m)

        df = self._init_data(n, m, zs)

        # duo tou
        df['higher'] = df.h > df.nhh
        df['lower'] = df.l < df.nll
        df['hbz'] = np.where(df['higher'], df.mll/df.zsll , None)
        #df['hbz_biggerthan1'] = np.where(df.hbz>1, True, None)
        # kong tou  
        
        df['lbz'] = np.where(df['lower'], df.mhh/df.zshh , None)
        #df['lbz_smallerthan1'] = np.where(df.lbz<1, True, None)
        #print df.hbz.mean() # 应该大于1

        self._to_result(df)


    def tupohl_low(self, n, m, zs=2):
        print 'tupohl_low------%s------%s-----------'% (n, m)
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


    def tupohl_close(self, n, m, zs=2):
        print 'tupohl_close------%s------%s-----------'% (n, m)
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

    def tupohl_high(self, n, m, zs=2):
        print 'tupohl_high------%s------%s-----------'% (n, m)
        df = self._init_data(n, m, zs)

        # duo tou
        df['higher'] = df.h > df.nhh
        df['hh'] = df.h.shift(1) > df.h.shift(2)
        df['hbz'] = np.where(df['higher'] & df.hh, df.mll/df.zsll , None)
        #df['hbz_biggerthan1'] = np.where(df.hbz>1, True, None)
        #print df.hbz.mean() # 应该大于1
        # kong tou  
        df['lower'] = df.l < df.nll
        df['ll'] = df.l.shift(1) < df.l.shift(2)
        df['lbz'] = np.where(df['lower'] & df.ll, df.mhh/df.zshh , None)
        #df['lbz_smallerthan1'] = np.where(df.lbz<1, True, None)
        self._to_result(df)


    def tupohl_lowclose(self, n, m, zs=2):
        print 'tupohl_lowclose------%s------%s-----------'% (n, m)
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


    def tupohl_highclose(self, n, m, zs=2):
        print 'tupohl_highclose------%s------%s-----------'% (n, m)
        df = self._init_data(n, m, zs)

        # duo tou
        df['higher'] = df.h > df.nhh
        df['hh1'] = df.h.shift(1) > df.h.shift(2)
        df['hh2'] = df.c.shift(1) > df.c.shift(2)
        df['hbz'] = np.where(df['higher'] & df.hh1 & df.hh2, df.mll/df.zsll , None)
        #df['hbz_biggerthan1'] = np.where(df.hbz>1, True, None)
        # kong tou  
        df['lower'] = df.l < df.nll
        df['ll1'] = df.l.shift(1) < df.l.shift(2)
        df['ll2'] = df.c.shift(1) < df.c.shift(2)
        df['lbz'] = np.where(df['lower'] & df.ll1 & df.ll2, df.mhh/df.zshh , None)
        #df['lbz_smallerthan1'] = np.where(df.lbz<1, True, None)

        self._to_result(df)


    def tupohl_lowhigh(self, n, m, zs=2):
        '''函数名起名以多为例'''
        print 'tupohl_lowhigh------%s------%s-----------'% (n, m)
        df = self._init_data(n, m, zs)

        # duo tou
        df['higher'] = df.h > df.nhh
        df['hh1'] = df.l.shift(1) > df.l.shift(2)
        df['hh2'] = df.h.shift(1) > df.h.shift(2)
        df['hbz'] = np.where(df['higher'] & df.hh1 & df.hh2, df.mll/df.zsll , None)
        #df['hbz_biggerthan1'] = np.where(df.hbz>1, True, None)
        # kong tou  
        df['lower'] = df.l < df.nll
        df['ll1'] = df.h.shift(1) < df.h.shift(2)
        df['ll2'] = df.l.shift(1) < df.l.shift(2)
        df['lbz'] = np.where(df['lower'] & df.ll1 & df.ll2, df.mhh/df.zshh , None)
        #df['lbz_smallerthan1'] = np.where(df.lbz<1, True, None)

        self._to_result(df)


    def tupohl_all(self, n, m, zs=2):
        print 'tupohl_all------%s------%s-----------'% (n, m)
        df = self._init_data(n, m, zs)

        # duo tou
        df['higher'] = df.h > df.nhh
        df['hh1'] = df.l.shift(1) > df.l.shift(2)
        df['hh2'] = df.h.shift(1) > df.h.shift(2)
        df['hh3'] = df.c.shift(1) > df.c.shift(2)
        df['hbz'] = np.where(df['higher'] & df.hh1 & df.hh2 & df.hh3, df.mll/df.zsll , None)
        #df['hbz_biggerthan1'] = np.where(df.hbz>1, True, None)
        # kong tou  
        df['lower'] = df.l < df.nll
        df['ll1'] = df.h.shift(1) < df.h.shift(2)
        df['ll2'] = df.l.shift(1) < df.l.shift(2)
        df['ll3'] = df.c.shift(1) < df.c.shift(2)
        df['lbz'] = np.where(df['lower'] & df.ll1 & df.ll2 & df.ll3, df.mhh/df.zshh , None)
        #df['lbz_smallerthan1'] = np.where(df.lbz<1, True, None)

        self._to_result(df)


    def yyy(self, n):
        '''前n天高低点作为移动止损
        其实yyy(n) 等于 foo(n,1,n)

        '''
        df = self._init_data(n)
        df['hbz'] = np.where(1, df.l/df.nll , None) # df.l当天低点， df.nll前n天低点，df.l>df.nll则没止损
        df['lbz'] = np.where(1, df.h/df.nhh , None)
        self._to_result(df)
        

    def _init_data(self, n=2, m=2, zs=2):
        self.get_nhh(n)
        self.get_nll(n)
        self.get_mhh(m)
        self.get_mll(m)
        self.get_zshh(zs)
        self.get_zsll(zs)
        return deepcopy(self.df) 

    def _to_result(self, df):
        hlist = [x for x in sorted(df.hbz) if x>0]
        len1 = len(hlist)
        hlistbiggerthan1 = [x for x in hlist if x>1]
        hgl = len(hlistbiggerthan1)/float(len1) # 大于1 的概率(在m天里没止损de概率)
        print str(hgl)[:4], len1#, hgl*len1

        #print df.lbz.mean() # 应该小于1
        llist = [x for x in sorted(df.lbz) if x>0]
        len2 = len(llist)
        llistsmallerthan1 = [x for x in llist if x<1]
        lgl = len(llistsmallerthan1)/float(len2) # 小于1 的概率(在m天里没止损de概率)
        print str(lgl)[:4], len2#, lgl*len2

        df.to_csv('tmp.csv')


if __name__ == '__main__':
    g = GL('c') # ta rb c m a ma jd dy 999999
    #g.foo(2,2,2)
    g.tupohl(2,1,2)
    #g.tupohl(2,3)
    #g.tupohl(2,4)
    #g.tupohl(2,5)
    #g.tupohl(2,6)
    #g.tupohl(2,7)
    #g.tupohl_low(2,3)
    #g.tupohl_close(2,3)
    #g.tupohl_high(2,3)
    #g.tupohl_lowclose(2,3)
    g.tupohl_highclose(2,1,4)
    #g.tupohl_lowhigh(2,3)
    #g.tupohl_all(2,3)

    g.yyy(4)
    g.foo(4,1,4)


    
    