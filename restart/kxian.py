# encoding: utf-8
import sys
sys.path.append("..")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from general_index import General, GeneralIndex, rangerun, rangerun3
from copy import deepcopy
import util

class Kxian(GeneralIndex):
    def __init__(self, daima):
        super(Kxian, self).__init__(daima)
        #self.get_ma(5,10,20,30,40)
        self.get_sdjj()
        self.get_atr(100)

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
    def hl_run3(self, n=10, m=10):
        '''其实不带run3的函数就像是带run3的一种情况n=m'''
        self.get_nhh(n)
        self.get_nll(n)
        self.get_nhh(m)
        self.get_nll(m)
        df = deepcopy(self.df) 

        df['higher'] = df.h > df.nhh 
        df['bksk'] = np.where(df['higher'], 'bk' , None)
        df['lower'] = df.l < df.nll
        df['bksk'] = np.where(df['lower'], 'sk' , df['bksk'])

        df['phigher'] = df.h > df.nhh 
        df['bpsp'] = np.where(df['phigher'], 'sp' , None)
        df['plower'] = df.l < df.nll
        df['bpsp'] = np.where(df['plower'], 'bp' , df['bpsp'])
        df.to_csv('tmp.csv')
        return self.run3b(df, zj=60000, f=0.06, zs=0.02)

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


    @util.display_func_name
    def ma_updown_run3(self, n=10, m=10, x=1):
        '''ma比前x天高开多，反之开空'''
        self.get_ma(n)
        self.get_ma(m)
        df = deepcopy(self.df) 
        ma1 = 'ma%s' % n
        ma2 = 'ma%s' % m

        df['maup'] = df[ma1] > df[ma1].shift(x)
        df['madown'] = df[ma1] < df[ma1].shift(x)
        df['bksk'] = np.where(df['maup'], 'bk' , None)
        df['bksk'] = np.where(df['madown'], 'sk' , df['bksk'])

        df['pmaup'] = df[ma2] > df[ma2].shift(x)
        df['pmadown'] = df[ma2] < df[ma2].shift(x)
        df['bpsp'] = np.where(df['pmaup'], 'sp' , None)
        df['bpsp'] = np.where(df['pmadown'], 'bp' , df['bpsp'])
        #df.to_csv('tmp.csv')
        return self.run3b(df, zj=60000, f=0.06, zs=0.02) # 相同的策略不同的品种结果不一样，但同一种品种，f 和 zs还是有相对优势的参数
   
    @util.display_func_name
    def suijikaicang(self, n=5):
        '''
        随机平均n天开一仓，方向随机

        跑下来随机开，结果也比较随机，基本也就在初始本金上下几倍里
        '''
        df = deepcopy(self.df)
        print np.random.randint(n*2, size=len(df)) # 得到随机0 到2n-1的整数
        df['krandint'] = np.random.randint(n*2, size=len(df))
        df['prandint'] = np.random.randint(n*2, size=len(df))

        df['bksk'] = np.where(df['krandint']== 0, 'bk' , None)
        df['bksk'] = np.where(df['krandint']==2*n-1, 'sk' , df['bksk'])
        df['bpsp'] = np.where(df['krandint']== 0, 'sp' , None)
        df['bpsp'] = np.where(df['krandint']==2*n-1, 'bp' , df['bpsp'])
        df.to_csv('tmp.csv')
        return self.run3b(df, zj=60000, f=0.06, zs=0.02)

    def gudingkaicang(self, mode=3, n=10):
        '''
        固定一个间隔n开仓平仓，做好开仓止损
        mode 1   开多
        mode 2   开空
        mode 3   一次开多  一次开空
        '''

        pass

    @util.display_func_name
    def bigger_smaller_than_ma_run3(self, n=10, m=10):
        '''前一天k线在ma上开多，反之开空；n开仓用，m平仓用
       这个跑下来不好
        '''
        self.get_ma(n)
        self.get_ma(m)
        df = deepcopy(self.df) 
        ma1 = 'ma%s' % n
        ma2 = 'ma%s' % m

        df['bigger'] = df.l.shift(1) > df[ma1].shift(1)
        df['smaller'] = df.h.shift(1) < df[ma1].shift(1)
        df['bksk'] = np.where(df['bigger'], 'bk' , None)
        df['bksk'] = np.where(df['smaller'], 'sk' , df['bksk'])

        df['pbigger'] = df.l.shift(1) > df[ma1].shift(1)
        df['psmaller'] = df.h.shift(1) < df[ma1].shift(1)
        df['bpsp'] = np.where(df['pbigger'], 'sp' , None)
        df['bpsp'] = np.where(df['psmaller'], 'bp' , df['bpsp'])
        df.to_csv('tmp.csv')
        return self.run3b(df, zj=60000, f=0.02, zs=0.02)


    @util.display_func_name
    def qian_n_ri2_run3(self, n=10, m=10):
        '''比前n日高，买开仓，反之'''
        df = deepcopy(self.df) 
        df['higher'] = df.sdjj > df.sdjj.shift(n)
        df['lower'] = df.sdjj < df.sdjj.shift(n)
          
        df['bksk'] = np.where(df['higher'], 'bk' , None)
        # bk表示买开仓或买平仓，sk相反
        df['bksk'] = np.where(df['lower'], 'sk' , df['bksk'])

        df['higherp'] = df.sdjj > df.sdjj.shift(m)
        df['lowerp'] = df.sdjj < df.sdjj.shift(m)
          
        df['bpsp'] = np.where(df['higherp'], 'sp' , None)
        df['bpsp'] = np.where(df['lowerp'], 'bp' , df['bpsp'])
        df.to_csv('tmp.csv')
        return self.run3b(df, zj=60000, f=0.06, zs=0.02)

if __name__ == '__main__':
    k = Kxian('m')
    #k.ma_updown(50)
    #k.cross_ma()
    #k.tupo_hl(20)
    #k.hl(20)
    #k.ma_cross(10,50)
    #print k.hl_run3()
    print k.ma_updown_run3(10,10)
    #print k.bigger_smaller_than_ma_run3(10)
    #rangerun3(k.ma_updown_run3, range(2,20), range(8,9))

    #print k.suijikaicang()
    #print k.qian_n_ri2_run3()