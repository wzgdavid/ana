# encoding: utf-8
import sys
sys.path.append("..")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from general_index import General, GeneralIndex
from copy import deepcopy
import util

class Sdjj(GeneralIndex):
    '''看四点均价'''
    def __init__(self, daima):
        super(Sdjj, self).__init__(daima)
        #self.get_ma(5,10,20)
        self.get_sdjj()

    def foo(self):
        print self.df['o']
        pass
    
    @util.display_func_name
    def tupo_sdhsdl(self, n=10):
        '''四点均线突破前n天最高开多，突破前n天最低开空，
        
        暂时还想不出移动止损怎么写，先写不带移动止损的，用信号平仓的策略
        # 暂时结果 rb 11(28008), 12(28080.25) 天最好
        '''
        self.get_nsdl(n)
        self.get_nsdh(n)
        df = deepcopy(self.df) 
        #df['tupo_sdh'] = df.sdjj.shift(1) < df.nsdh.shift(1) & df.sdjj > df.nsdh 
        df['tmp1'] = df.sdjj.shift(1) < df.nsdh.shift(1)
        df['tmp2'] = df.sdjj > df.nsdh
        df['tupo_sdh'] = df.tmp1 & df.tmp2  #今天的四点均价突破前n天的四点均价高点
        df['bksk'] = np.where(df['tupo_sdh'], 'bk' , None)
        #df.loc[: ,'bkcnt'] = 0
        #df['bkcnt'] = np.where(df['tupo_sdh'], df.bkcnt.shift(1)+1 , df.bkcnt.shift(2))

        df['tmp1'] = df.sdjj.shift(1) > df.nsdl.shift(1)
        df['tmp2'] = df.sdjj < df.nsdl
        df['tupo_sdl'] = df.tmp1 & df.tmp2
        # bk表示买开仓或买平仓，sk相反
        df['bksk'] = np.where(df['tupo_sdl'], 'sk' , df['bksk'])

        self.run(df)
    
    @util.display_func_name
    def sdhsdl(self, n=10):
        '''四点均价比前n天最高还高开多， 反之开空  
        和tupo_sdhsdl的区别， tupo_sdhsdl只是突破的那一天为信号， 此函数不管
        目的是为了看满足这个条件下的概率，真实不可能开那么多仓位
        '''
        self.get_nsdl(n)
        self.get_nsdh(n)
        df = deepcopy(self.df) 


        df['tupo_sdh'] = df.sdjj > df.nsdh  #今天的四点均价突破前n天的四点均价高点
        df['bksk'] = np.where(df['tupo_sdh'], 'bk' , None)
        df['tupo_sdl'] = df.sdjj < df.nsdl
        # bk表示买开仓或买平仓，sk相反
        df['bksk'] = np.where(df['tupo_sdl'], 'sk' , df['bksk'])

        self.run(df)

    @util.display_func_name
    def sdhsdl_run2(self, n=12, m=12):
        '''四点均价比前n天最高还高开多， 反之开空  
        开平仓参数不同， n 开仓参数， m平仓参数
        和 xian 的 hl() 对应
        '''
        self.get_nsdl(n)
        self.get_nsdh(n)
        self.get_nsdhp(m)
        self.get_nsdlp(m)
        df = deepcopy(self.df) 

        df['tupo_sdh'] = df.sdjj > df.nsdh  #今天的四点均价突破前n天的四点均价高点
        df['bksk'] = np.where(df['tupo_sdh'], 'bk' , None)
        df['tupo_sdl'] = df.sdjj < df.nsdl
        df['bksk'] = np.where(df['tupo_sdl'], 'sk' , df['bksk'])

        # 平仓
        

        df['tupo_sdhp'] = df.sdjj > df.nsdhp  
        df['bpsp'] = np.where(df['tupo_sdhp'], 'sp' , None)
        df['tupo_sdlp'] = df.sdjj < df.nsdlp
        df['bpsp'] = np.where(df['tupo_sdlp'], 'bp' , df['bpsp'])
        df.to_csv('tmp.csv')
        #print df.columns
        self.run2(df)

    @util.display_func_name
    def sdhsdl_ma(self, n=10, man=20, p=0.07):
        '''四点均价比前n天最高还高开多， 反之开空  
        和tupo_sdhsdl的区别， tupo_sdhsdl只是突破的那一天为信号， 此函数不管
        目的是为了看满足这个条件下的概率，真实不可能开那么多仓位

        再加个条件，离ma 一定 的距离，在1+-p范围外（避免震荡）
        man为ma的参数
        '''
        self.get_nsdl(n)
        self.get_nsdh(n)
        self.get_ma_sdjj(man)
        df = deepcopy(self.df)
        ma = 'sdjjma%s' % man
        df.to_csv('tmp.csv')

        df['tupo_sdh'] = df.sdjj > df.nsdh  #今天的四点均价突破前n天的四点均价高点
        df['bigger_than_ma'] = df.sdjj > df[ma] * (1+p)
        df['canbk'] = df.tupo_sdh & df.bigger_than_ma
        df['bksk'] = np.where(df['canbk'], 'bk' , None)
        df['tupo_sdl'] = df.sdjj < df.nsdl
        df['smaller_than_ma'] = df.sdjj < df[ma] * (1-p)
        df['cansk'] = df.tupo_sdl & df.smaller_than_ma
        # bk表示买开仓或买平仓，sk相反
        df['bksk'] = np.where(df['cansk'], 'sk' , df['bksk'])

        self.run(df)

    @util.display_func_name
    def qian_n_ri(self, n=10):
        '''比第前n日高，买开仓，反之 (连着几天取这几天的第一天)
        
        '''
        df = deepcopy(self.df) 
        df['tmp1'] = df.sdjj > df.sdjj.shift(n)
        df['tmp2'] = df.sdjj.shift(1) < df.sdjj.shift(n+1)
        df['higher'] = df.tmp1 & df.tmp2 # 第一次比前第n天高
        df['tmp1'] = df.sdjj < df.sdjj.shift(n)
        df['tmp2'] = df.sdjj.shift(1) > df.sdjj.shift(n+1)
        df['lower'] = df.tmp1 & df.tmp2 # 第一次比前第n天低
          
        df['bksk'] = np.where(df['higher'], 'bk' , None)
        # bk表示买开仓或买平仓，sk相反
        df['bksk'] = np.where(df['lower'], 'sk' , df['bksk'])
        #df.to_csv('tmp.csv')
        #print df.loc[:, ['date','sdjj', 'higher']]
        self.run(df)

    @util.display_func_name
    def qian_n_ri2(self, n=10):
        '''比前n日高，买开仓，反之'''
        df = deepcopy(self.df) 
        df['higher'] = df.sdjj > df.sdjj.shift(n)
        df['lower'] = df.sdjj < df.sdjj.shift(n)
          
        df['bksk'] = np.where(df['higher'], 'bk' , None)
        # bk表示买开仓或买平仓，sk相反
        df['bksk'] = np.where(df['lower'], 'sk' , df['bksk'])
        #df.to_csv('tmp.csv')
        #print df.loc[:, ['date','sdjj', 'higher']]
        self.run(df)
  
    @util.display_func_name
    def tupo_ma(self, n=10):
        '''向上穿过ma，买开，向下，卖; 相反信号平仓
        
        '''
        self.get_ma_sdjj(n)
        df = deepcopy(self.df)
        ma = 'sdjjma%s' % n
        
        df['tmp1'] = df.sdjj > df[ma]
        df['tmp2'] = df.sdjj.shift(1) < df[ma].shift(1)
        df['htupo'] = df.tmp1 & df.tmp2 # 向上突破
        df['tmp1'] = df.sdjj < df[ma]
        df['tmp2'] = df.sdjj.shift(1) > df[ma].shift(1)
        df['ltupo'] = df.tmp1 & df.tmp2 # 向下突破
        df['bksk'] = np.where(df['htupo'], 'bk' , None)
        # bk表示买开仓或买平仓，sk相反
        df['bksk'] = np.where(df['ltupo'], 'sk' , df['bksk'])
        df.to_csv('tmp.csv')
        self.run(df)


    @util.display_func_name
    def ma_cross(self, a=5, b=25):
        '''ma金叉死叉 a比b小
        '''
        self.get_ma_sdjj(a, b)
        df = deepcopy(self.df) 
        maa = 'sdjjma%s' % a
        mab = 'sdjjma%s' % b
        df['tmp1'] = df[maa].shift(1) < df[mab].shift(1)
        df['tmp2'] = df[maa] > df[mab]
        df['jincha'] = df.tmp1 & df.tmp2

        df['tmp1'] = df[maa].shift(1) > df[mab].shift(1)
        df['tmp2'] = df[maa] < df[mab]
        df['sicha'] = df.tmp1 & df.tmp2
        df['bksk'] = np.where(df['jincha'], 'bk' , None)
        df['bksk'] = np.where(df['sicha'], 'sk' , df['bksk'])
        #df.to_csv('tmp.csv')
        self.run(df)

    @util.display_func_name
    def ma_cross_run2(self, a=5, b=25, c=10, d=30):
        '''a  b 开仓的均线，  c  d  平仓用的均线
        a比b小  c比d小
        '''
        self.get_ma_sdjj(a, b, c, d)
        df = deepcopy(self.df) 
        maa = 'sdjjma%s' % a
        mab = 'sdjjma%s' % b
        mac = 'sdjjma%s' % c
        mad = 'sdjjma%s' % d
        # 开仓
        df['tmp1'] = df[maa].shift(1) < df[mab].shift(1)
        df['tmp2'] = df[maa] > df[mab]
        df['jincha'] = df.tmp1 & df.tmp2

        df['tmp1'] = df[maa].shift(1) > df[mab].shift(1)
        df['tmp2'] = df[maa] < df[mab]
        df['sicha'] = df.tmp1 & df.tmp2
        df['bksk'] = np.where(df['jincha'], 'bk' , None)
        df['bksk'] = np.where(df['sicha'], 'sk' , df['bksk'])

        # 平仓
        df['tmp1'] = df[mac].shift(1) < df[mad].shift(1)
        df['tmp2'] = df[mac] > df[mad]
        df['jinchap'] = df.tmp1 & df.tmp2

        df['tmp1'] = df[mac].shift(1) > df[mad].shift(1)
        df['tmp2'] = df[mac] < df[mad]
        df['sichap'] = df.tmp1 & df.tmp2
        df['bpsp'] = np.where(df['jinchap'], 'sp' , None)
        df['bpsp'] = np.where(df['sichap'], 'bp' , df['bpsp'])



        df.to_csv('tmp.csv')
        self.run2(df)

def rangerun(foo):
    r1 = range(5, 15)
    r2 = range(5, 50, 2)
    for a in r1:
        for b in r2:
            print a, b
            foo(a,b)


if __name__ == '__main__':
    s = Sdjj('rb')
    #s.foo()
    
    #s.tupo_sdhsdl(12) # rb 11(28008), 12(28080.25) 天最好

    s.ma_cross(5,10)
    s.ma_cross_run2(5,10,5,10)
    #s.sdhsdl_run2(12,12)
    #s.sdhsdl(12)
    #s.tupo_ma(11)
    #s.qian_n_ri(11)
    #print s.df.index
    #print s.df.loc[:, ['date','sdjj', 'tupo_sdl', 'tupo_sdh']]
    #s.df.to_csv('tmp.csv')  
    #df = pd.read_csv('../data/%s.xls' % 'RBL9')
    #print df
    #rangerun(s.sdhsdl_ma)