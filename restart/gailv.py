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
        '''以多为例，突破前n天高点，以前n天高点为开仓价，
        开仓止损为前zs天的最低价，看后m天（包含当天）低点与开仓止损的比值
        空反之'''
        print 'tupohl------%s------%s-----------'% (n, m)
        df = self._init_data(n, m, zs)
        df['higher'] = df.h > df.nhh
        df['lower'] = df.l < df.nll
        # duo tou
        df['hbz'] = np.where(df['higher'], df.mll/df.zsll , None)
        # kong tou  
        df['lbz'] = np.where(df['lower'], df.mhh/df.zshh , None)
        self._to_result(df)

    def tupohlp(self, n, m, zs=0.02):
        '''以多为例，突破前n天高点，以前n天高点为开仓价，
        开仓止损为开仓价下的百分比zs，看后m天（包含当天）低点与开仓止损的比值
        空反之'''
        print 'tupohlp------%s------%s-----------'% (n, m)
        df = self._init_data(n, m)
        df['higher'] = df.h > df.nhh
        df['lower'] = df.l < df.nll
        # duo tou
        df['hbz'] = np.where(df['higher'], df.mll/(df.nhh*(1-zs)) , None)
        # kong tou  
        df['lbz'] = np.where(df['lower'], df.mhh/(df.nll*(1+zs)) , None)
        self._to_result(df)

    def tupohl_low(self, n, m, zs=2):
        '''tupohl变式，加条件,函数名以多为例'''
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
        ''''''
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


    def tupohl_hlc(self, n, m, zs=2):
        print 'tupohl_hlc------%s------%s-----------'% (n, m)
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


    def tupohl_yang(self, n, m, zs=2):
        ''''''
        print 'tupohl_yang------%s------%s-----------'% (n, m)
        df = self._init_data(n, m, zs)

        # duo tou
        df['higher'] = df.h > df.nhh
        df['hh1'] = df.c.shift(1) > df.o.shift(1)
        #df['hh1'] = df.c.shift(1) < df.o.shift(1) # 即使把条件改成，前一天是阴线，今天突破开多，m天不止损概率也差不多（低几个百分点），只是数量少很多,说明某一天阴线阳线，对趋势影响不大
        df['hbz'] = np.where(df['higher'] & df.hh1, df.mll/df.zsll , None)
        #df['hbz_biggerthan1'] = np.where(df.hbz>1, True, None)
        # kong tou  
        df['lower'] = df.l < df.nll
        df['ll1'] = df.c.shift(1) < df.o.shift(1)
        #df['ll1'] = df.c.shift(1) > df.o.shift(1)
        df['lbz'] = np.where(df['lower'] & df.ll1, df.mhh/df.zshh , None)
        #df['lbz_smallerthan1'] = np.where(df.lbz<1, True, None)

        self._to_result(df)

    def tupohl_hlc_yang(self, n, m, zs=2):
        '''在tupohl_hcl 加个yang的条件，没效果'''
        print 'tupohl_hlc_yang------%s------%s-----------'% (n, m)
        df = self._init_data(n, m, zs)

        # duo tou
        df['higher'] = df.h > df.nhh
        df['hh1'] = df.l.shift(1) > df.l.shift(2)
        df['hh2'] = df.h.shift(1) > df.h.shift(2)
        df['hh3'] = df.c.shift(1) > df.c.shift(2)
        df['hh4'] = df.c.shift(1) > df.o.shift(1)
        df['hbz'] = np.where(df['higher'] & df.hh1 & df.hh2 & df.hh3 & df.hh4, df.mll/df.zsll , None)
        #df['hbz_biggerthan1'] = np.where(df.hbz>1, True, None)
        # kong tou  
        df['lower'] = df.l < df.nll
        df['ll1'] = df.h.shift(1) < df.h.shift(2)
        df['ll2'] = df.l.shift(1) < df.l.shift(2)
        df['ll3'] = df.c.shift(1) < df.c.shift(2)
        df['ll4'] = df.c.shift(1) < df.o.shift(1)
        df['lbz'] = np.where(df['lower'] & df.ll1 & df.ll2 & df.ll3 & df.ll4, df.mhh/df.zshh , None)
        #df['lbz_smallerthan1'] = np.where(df.lbz<1, True, None)

        self._to_result(df)


    '''
    ############################################################################################
    ############################################################################################
    ########################分割线要明显########################################################
    ############################################################################################
    ############################################################################################
    '''

    def yyy(self, n):
        '''前n天高(低)点作为移动止损

        '''
        print 'yyy---------------'
        df = self._init_data(n)
        df['hbz'] = np.where(1, df.l/df.nll , None) # df.l当天低点， df.nll前n天低点，df.l>df.nll则没止损
        df['lbz'] = np.where(1, df.h/df.nhh , None)
        self._to_result(df)

    def yyy_high(self, n):
        '''前n天高(低)点作为移动止损
    
        '''
        print 'yyy_high---------------'
        df = self._init_data(n)
        df['hh'] = df.h.shift(1) > df.h.shift(2)
        df['hbz'] = np.where( df.hh, df.l/df.nll , None) # df.l当天低点， df.nll前n天低点，df.l>df.nll则没止损
        
        df['ll'] = df.l.shift(1) < df.l.shift(2)
        df['lbz'] = np.where( df.ll , df.h/df.nhh , None)
        self._to_result(df)    

    def yyy_low(self, n):
        '''
        '''
        print 'yyy_low---------------'
        df = self._init_data(n)
        df['hh'] = df.l.shift(1) > df.l.shift(2)
        df['hbz'] = np.where(df.hh, df.l/df.nll , None) # df.l当天低点， df.nll前n天低点，df.l>df.nll则没止损
        
        df['ll'] = df.h.shift(1) < df.h.shift(2)
        df['lbz'] = np.where(df.ll, df.h/df.nhh , None)
        self._to_result(df)    

    def yyy_close(self, n):
        '''
        '''
        print 'yyy_close---------------'
        df = self._init_data(n)
        df['hh1'] = df.c.shift(1) > df.c.shift(2)
        df['hbz'] = np.where(df.hh1, df.l/df.nll , None) # df.l当天低点， df.nll前n天低点，df.l>df.nll则没止损
        
        df['ll1'] = df.c.shift(1) < df.c.shift(2)
        df['lbz'] = np.where(df.ll1, df.h/df.nhh , None)
        self._to_result(df)        

    def yyy_hlc(self, n):
        '''
        '''
        print 'yyy_hlc---------------'
        df = self._init_data(n)
        df['hh1'] = df.h.shift(1) > df.h.shift(2)
        df['hh2'] = df.l.shift(1) > df.l.shift(2)
        df['hh3'] = df.c.shift(1) > df.c.shift(2)
        df['hbz'] = np.where(df.hh1 & df.hh2 & df.hh3 ,df.l/df.nll,  None) # df.l当天低点， df.nll前n天低点，df.l>df.nll则没止损
        
        df['ll1'] = df.h.shift(1) < df.h.shift(2)
        df['ll2'] = df.l.shift(1) < df.l.shift(2)
        df['ll3'] = df.c.shift(1) < df.c.shift(2)
        df['lbz'] = np.where(df.ll1 & df.ll2 & df.ll3, df.h/df.nhh , None)
        self._to_result(df)  

    def yyy_ma(self, n, ma):
        '''前n天高低点作为移动止损
    
        '''
        print 'yyy_ma---------------'
        self.get_ma(ma)
        df = self._init_data(n)
        ma1 = 'ma%s' % ma
        df['hh1'] = df.l.shift(1) > df[ma1]
        df['hbz'] = np.where(df.hh1, df.l/df.nll , None) # df.l当天低点， df.nll前n天低点，df.l>df.nll则没止损
        
        df['ll1'] = df.h.shift(1) < df[ma1]
        
        df['lbz'] = np.where(df.ll1, df.h/df.nhh , None)
        self._to_result(df)    

    
    def hhh(self, n, m):
        '''后m天高点与开仓点比值范围'''
        print 'hhh---------------'
        df = self._init_data(n, m)
        df['hbz'] = np.where(1, df.mhh/df.nhh , None) # df.l当天低点， df.nll前n天低点，df.l>df.nll则没止损
        df['lbz'] = np.where(1, df.mll/df.nll , None)
        hlist = [x for x in sorted(df.hbz) if x>0]
        print df.hbz.mean(), #hlist
        print df.lbz.mean()

    def hhh_high(self, n, m):
        '''后m天高点与开仓点比值范围'''
        print 'hhh---------------'
        df = self._init_data(n, m)
        df['higher'] = df.h > df.nhh
        df['lower'] = df.l < df.nll
        df['hbz'] = np.where(df.higher, df.mhh/df.nhh , None) # df.l当天低点， df.nll前n天低点，df.l>df.nll则没止损
        df['lbz'] = np.where(df.lower, df.mll/df.nll , None)
        hlist = [x for x in sorted(df.hbz) if x>0]
        len1 = len(hlist)
        print df.hbz.mean(),# hlist
        print df.lbz.mean()

    def hhh_highlow(self, n, m):
        '''后m天高点与开仓点比值范围'''
        print 'hhh---------------'
        df = self._init_data(n, m)
        df['higher'] = df.h > df.nhh
        df['hh1'] = df.l.shift(1) > df.l.shift(2)
        df['hh2'] = df.h.shift(1) > df.h.shift(2)
        df['lower'] = df.l < df.nll
        df['ll1'] = df.l.shift(1) < df.l.shift(2)
        df['ll2'] = df.h.shift(1) < df.h.shift(2)
        df['hbz'] = np.where(df.higher & df.hh1 & df.hh2, df.mhh/df.nhh , None) # df.l当天低点， df.nll前n天低点，df.l>df.nll则没止损
        df['lbz'] = np.where(df.lower & df.ll1 & df.ll2, df.mll/df.nll , None)
        hlist = [x for x in sorted(df.hbz) if x>0]
        len1 = len(hlist)
        print df.hbz.mean(),# hlist
        print df.lbz.mean()


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
        print str(hgl)[:4], len1, '肯定打开仓止损的单数', len1*(1-hgl)#, hgl*len1

        #print df.lbz.mean() # 应该小于1
        llist = [x for x in sorted(df.lbz) if x>0]
        len2 = len(llist)
        llistsmallerthan1 = [x for x in llist if x<1]
        lgl = len(llistsmallerthan1)/float(len2) # 小于1 的概率(在m天里没止损de概率)
        print str(lgl)[:4], len2, '肯定打开仓止损的单数', len2*(1-lgl)#, hgl*len1

        df.to_csv('tmp.csv')


if __name__ == '__main__':
    g = GL('m') # ta rb c m a ma jd dy 999999
    #g.foo(2,3,2)
    #g.tupohl(3, 3)
    #g.tupohl(4, 3)
    g.tupohl(4, 3)
    #g.tupohlp(3, 2, zs=0.03)
    #g.tupohl(2,3)
    
    #g.tupohl(2,3)
    #g.tupohl(2,4)
    #g.tupohl(2,5)
    #g.tupohl(2,6)
    #g.tupohl(2,7)
    #g.tupohl_low(2,3)
    #g.tupohl_close(2,3)

    #g.tupohl_yang(2,3)
    #g.tupohl_high(2,3)
    #g.tupohl_lowclose(2,3)
    #g.tupohl_highclose(2,3)
    g.tupohl_lowhigh(2,3)
    g.tupohl_lowhigh(3,3)
    g.tupohl_lowhigh(10,3)
    g.tupohl_lowhigh(100,3)
    #g.tupohl_hlc(2,3)
    #g.tupohl_hlc_yang(2,3)
    #g.tupohl_lowhigh(4,1,2)
    ##g.tupohl_all(2,3)
    #g.tupohl(4,1,4)
    #g.yyy(3)
    #g.yyy_low(3)
    #g.yyy_high(3)
    #g.yyy_close(3)
    #g.yyy_ma(4, 10)
    #g.foo(2,1,4)
    #g.hhh(2,10)
    #g.hhh_hl(2,10)
    #g.hhh_hl_hl(2,10)


    
    