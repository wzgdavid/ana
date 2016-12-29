# encoding: utf-8
import sys
sys.path.append("..")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from general_index import General, GeneralIndex
from copy import deepcopy
import util

class Kxian(GeneralIndex):
    def __init__(self, daima):
        super(Kxian, self).__init__(daima)
        #self.get_ma(5,10,20,30,40)
        self.get_sdjj()

    @util.display_func_name
    def tupo_hl(self, n=10):
        '''最高价突破前n天最高开多，最低突破前n天最低开空，
        
        暂时还想不出移动止损怎么写，先写不带移动止损的，用信号平仓的策略

        '''
        self.get_nhh(n)
        self.get_nll(n)
        df = deepcopy(self.df) 
        #df['tupo_sdh'] = df.sdjj.shift(1) < df.nsdh.shift(1) & df.sdjj > df.nsdh 
        df['tmp1'] = df.h.shift(1) < df.nhh.shift(1)
        df['tmp2'] = df.h > df.nhh
        df['tupo_h'] = df.tmp1 & df.tmp2  #今天的四点均价突破前n天的四点均价高点
        df['bksk'] = np.where(df['tupo_h'], 'bk' , None)
        #df.loc[: ,'bkcnt'] = 0
        #df['bkcnt'] = np.where(df['tupo_sdh'], df.bkcnt.shift(1)+1 , df.bkcnt.shift(2))

        df['tmp1'] = df.l.shift(1) > df.nll.shift(1)
        df['tmp2'] = df.l < df.nll
        df['tupo_l'] = df.tmp1 & df.tmp2
        # bk表示买开仓或买平仓，sk相反
        df['bksk'] = np.where(df['tupo_l'], 'sk' , df['bksk'])
        #df.to_csv('tmp.csv')
        self.run(df)

    @util.display_func_name
    def hl(self, n=10):
        '''最高价比前n天最高还高开多， 最低价比前n天最低还低开空  
        和tupo_hl的区别， tupo_hl只是突破的那一天为信号， 此函数不管
        目的是为了看满足这个条件下的概率，真实不可能开那么多仓位
        基本上tupo_hl 和 hl 的平均值差不多
        '''
        self.get_nhh(n)
        self.get_nll(n)
        df = deepcopy(self.df) 


        df['higher'] = df.h > df.nhh 
        df['bksk'] = np.where(df['higher'], 'bk' , None)
        df['lower'] = df.l < df.nll
        # bk表示买开仓或买平仓，sk相反
        df['bksk'] = np.where(df['lower'], 'sk' , df['bksk'])
        df.to_csv('tmp.csv')
        self.run(df)

    @util.display_func_name
    def ma_cross(self, a=5, b=25):
        '''ma金叉死叉 a比b小
        '''
        self.get_ma(a, b)
        df = deepcopy(self.df) 
        maa = 'ma%s' % a
        mab = 'ma%s' % b
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
    def cross_ma(self, n=20):
        '''k线穿越ma, 定义，前一天开盘价在ma下，今天开盘在ma上为一次向上穿越，反之
        跑下来这个策略收益低
        '''
        self.get_ma(n)
        df = deepcopy(self.df) 
        ma = 'ma%s' % n

        df['tmp1'] = df.o.shift(1) < df[ma].shift(1)
        df['tmp2'] = df.o > df[ma]
        df['crossup'] = df.tmp1 & df.tmp2

        df['tmp1'] = df.o.shift(1) > df[ma].shift(1)
        df['tmp2'] = df.o < df[ma]
        df['crossdown'] = df.tmp1 & df.tmp2
        df['bksk'] = np.where(df['crossup'], 'bk' , None)
        df['bksk'] = np.where(df['crossdown'], 'sk' , df['bksk'])
        df.to_csv('tmp.csv')
        self.run(df)

    @util.display_func_name
    def ma_updown(self, n=20):
        '''ma向上开多， ma向下开空
        单跑这个策略收益低
        '''
        self.get_ma(n)
        df = deepcopy(self.df) 
        ma = 'ma%s' % n


        df['maup'] = df[ma] > df[ma].shift(1)


        df['madown'] = df[ma] < df[ma].shift(1)
        df['bksk'] = np.where(df['maup'], 'bk' , None)
        df['bksk'] = np.where(df['madown'], 'sk' , df['bksk'])
        df.to_csv('tmp.csv')
        self.run(df)

if __name__ == '__main__':
    k = Kxian('rb')
    #k.ma_updown(50)
    #k.cross_ma()
    #k.tupo_hl(20)
    k.hl(20)
    #k.ma_cross(10,50)
    '''r1 = range(11, 30)
    r2 = range(80, 222, 5)
    for a in r1:
        for b in r2:
            print a, b
            k.ma_cross(a,b)'''