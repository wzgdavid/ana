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
        
        #self.df.dropna(how='any')
        #print self.df

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
    def tupo_hl_run3(self, n=10):
        '''最高价突破前n天最高开多，最低突破前n天最低开空，
        
        暂时还想不出移动止损怎么写，先写不带移动止损的，用信号平仓的策略

        '''
        self.get_nhh(n)
        self.get_nll(n)

        df = deepcopy(self.df) 
        #df['tupo_sdh'] = df.sdjj.shift(1) < df.nsdh.shift(1) & df.sdjj > df.nsdh 
        df['tmp1'] = df.h.shift(2) < df.nhh.shift(2)
        df['tmp2'] = df.h.shift(1) > df.nhh.shift(1)
        df['tupo_h'] = df.tmp1 & df.tmp2  #今天的四点均价突破前n天的四点均价高点
        df['bksk'] = np.where(df['tupo_h'], 'bk' , None)
        df['bpsp'] = np.where(df['tupo_h'], 'sp' , None)

        df['tmp1'] = df.l.shift(2) > df.nll.shift(2)
        df['tmp2'] = df.l.shift(1) < df.nll.shift(1)
        df['tupo_l'] = df.tmp1 & df.tmp2

        df['bksk'] = np.where(df['tupo_l'], 'sk' , df['bksk'])
        df['bpsp'] = np.where(df['tupo_l'], 'bp' , df['bpsp'])
        df.to_csv('tmp.csv')
        return self.run3b(df, zj=100000, f=0.06, zs=0.02)

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
        return self.run3b(df, zj=200000, f=0.06, zs=0.02)

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
    def ma_cross_run3(self, a=5, b=25):
        '''
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

        df['tmp1'] = df[maa].shift(1) < df[mab].shift(1)
        df['tmp2'] = df[maa] > df[mab]
        df['pjincha'] = df.tmp1 & df.tmp2

        df['tmp1'] = df[maa].shift(1) > df[mab].shift(1)
        df['tmp2'] = df[maa] < df[mab]
        df['psicha'] = df.tmp1 & df.tmp2
        df['bpsp'] = np.where(df['pjincha'], 'sp' , None)
        df['bpsp'] = np.where(df['psicha'], 'bp' , df['bpsp'])

        df.to_csv('tmp.csv')
        return self.run3b(df, zj=100000, f=0.06, zs=0.02)

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
        '''ma比前x天高开多，反之开空
        不管哪个品种，策略间比较，跑下来这个最好
        '''
        self.get_ma(n)
        self.get_ma(m)
        #self.get_atr(100)

        #self.df.loc[1:100, 'bksk'] = None
        #print df
        #print self.df
        df = deepcopy(self.df) 
        #df.loc[df.index[0]:df.index[100], 'bksk'] = 50
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
        df.to_csv('tmp.csv')
        return self.run3b(df, zj=200000, f=0.06, zs=0.02) # 相同的策略不同的品种结果不一样，但同一种品种，f 和 zs还是有相对优势的参数
                            # zs 一般最优是0.02， f是越大收益越高，风险也越大，和资金管理书上说的如出一辙
    
    @util.display_func_name
    def ma_start_updown_run3(self, n=10, m=10):
        '''大前天和昨天ma比前天高，开多，反之开空
        '''
        self.get_ma(n)
        self.get_ma(m)

        df = deepcopy(self.df) 
        ma = 'ma%s' % n
        ma2 = 'ma%s' % m

        df['tmp1'] = df[ma].shift(2) < df[ma].shift(3)
        df['tmp2'] = df[ma].shift(2) < df[ma].shift(1)
        df['ma_startup'] = df.tmp1 & df.tmp2
        df['tmp1'] = df[ma].shift(2) > df[ma].shift(3)
        df['tmp2'] = df[ma].shift(2) > df[ma].shift(1)
        df['ma_startdown'] = df.tmp1 & df.tmp2
        df['bksk'] = np.where(df['ma_startup'], 'bk' , None)
        df['bksk'] = np.where(df['ma_startdown'], 'sk' , df['bksk'])

        df['tmp1'] = df[ma2].shift(2) < df[ma2].shift(3)
        df['tmp2'] = df[ma2].shift(2) < df[ma2].shift(1)
        df['pma_startup'] = df.tmp1 & df.tmp2
        df['tmp1'] = df[ma2].shift(2) > df[ma2].shift(3)
        df['tmp2'] = df[ma2].shift(2) > df[ma2].shift(1)
        df['pma_startdown'] = df.tmp1 & df.tmp2
        df['bpsp'] = np.where(df['pma_startup'], 'sp' , None)
        df['bpsp'] = np.where(df['pma_startdown'], 'bp' , df['bpsp'])
        df.to_csv('tmp.csv')
        return self.run3b(df, zj=100000, f=0.06, zs=0.02)

    @util.display_func_name
    def ma_updown_2day_run3(self, n=10, m=10):
        '''ma连着两天比前一天ma高，开多，反之开空
        '''
        self.get_ma(n)
        self.get_ma(m)

        df = deepcopy(self.df) 
        ma = 'ma%s' % n
        ma2 = 'ma%s' % m

        df['tmp1'] = df[ma].shift(2) > df[ma].shift(3)
        df['tmp2'] = df[ma].shift(1) > df[ma].shift(2)
        df['ma_startup'] = df.tmp1 & df.tmp2
        df['tmp1'] = df[ma].shift(2) < df[ma].shift(3)
        df['tmp2'] = df[ma].shift(1) < df[ma].shift(2)
        df['ma_startdown'] = df.tmp1 & df.tmp2
        df['bksk'] = np.where(df['ma_startup'], 'bk' , None)
        df['bksk'] = np.where(df['ma_startdown'], 'sk' , df['bksk'])

        df['tmp1'] = df[ma2].shift(2) > df[ma2].shift(3)
        df['tmp2'] = df[ma2].shift(1) > df[ma2].shift(2)
        df['pma_startup'] = df.tmp1 & df.tmp2
        df['tmp1'] = df[ma2].shift(2) < df[ma2].shift(3)
        df['tmp2'] = df[ma2].shift(1) < df[ma2].shift(2)
        df['pma_startdown'] = df.tmp1 & df.tmp2
        df['bpsp'] = np.where(df['pma_startup'], 'sp' , None)
        df['bpsp'] = np.where(df['pma_startdown'], 'bp' , df['bpsp'])
        df.to_csv('tmp.csv')
        return self.run3b(df, zj=100000, f=0.06, zs=0.02)

    @util.display_func_name
    def ma_updown_3day_run3(self, n=10, m=10):
        '''ma连着三天比前一天ma高，开多，反之开空
        '''
        self.get_ma(n)
        self.get_ma(m)

        df = deepcopy(self.df) 
        ma = 'ma%s' % n
        ma2 = 'ma%s' % m
        df['tmp0'] = df[ma].shift(3) > df[ma].shift(4)
        df['tmp1'] = df[ma].shift(2) > df[ma].shift(3)
        df['tmp2'] = df[ma].shift(1) > df[ma].shift(2)
        df['ma_up'] = df.tmp1 & df.tmp2 & df.tmp0
        df['tmp0'] = df[ma].shift(3) < df[ma].shift(4)
        df['tmp1'] = df[ma].shift(2) < df[ma].shift(3)
        df['tmp2'] = df[ma].shift(1) < df[ma].shift(2)
        df['ma_down'] = df.tmp1 & df.tmp2 & df.tmp0
        df['bksk'] = np.where(df['ma_up'], 'bk' , None)
        df['bksk'] = np.where(df['ma_down'], 'sk' , df['bksk'])
        
        df['tmp0'] = df[ma2].shift(3) > df[ma2].shift(4)
        df['tmp1'] = df[ma2].shift(2) > df[ma2].shift(3)
        df['tmp2'] = df[ma2].shift(1) > df[ma2].shift(2)
        df['pma_up'] = df.tmp1 & df.tmp2 & df.tmp0
        df['tmp0'] = df[ma2].shift(3) < df[ma2].shift(4)
        df['tmp1'] = df[ma2].shift(2) < df[ma2].shift(3)
        df['tmp2'] = df[ma2].shift(1) < df[ma2].shift(2)
        df['pma_down'] = df.tmp1 & df.tmp2 & df.tmp0
        df['bpsp'] = np.where(df['pma_up'], 'sp' , None)
        df['bpsp'] = np.where(df['pma_down'], 'bp' , df['bpsp'])
        df.to_csv('tmp.csv')
        return self.run3b(df, zj=100000, f=0.06, zs=0.02)

    @util.display_func_name
    def ma_updown_run3_shift(self, n=10, m=10):
        '''
        昨天ma比前天ma高，开多，反之开空
        '''
        self.get_ma(n)
        self.get_ma(m)
        #self.get_atr(100)

        #self.df.loc[1:100, 'bksk'] = None
        #print df
        #print self.df
        df = deepcopy(self.df) 
        #df.loc[df.index[0]:df.index[100], 'bksk'] = 50
        ma1 = 'ma%s' % n
        ma2 = 'ma%s' % m

        df['maup'] = df[ma1].shift(1) > df[ma1].shift(2)
        df['madown'] = df[ma1].shift(1) < df[ma1].shift(2)
        df['bksk'] = np.where(df['maup'], 'bk' , None)
        df['bksk'] = np.where(df['madown'], 'sk' , df['bksk'])

        df['pmaup'] = df[ma2].shift(1) > df[ma2].shift(2)
        df['pmadown'] = df[ma2].shift(1) < df[ma2].shift(2)
        df['bpsp'] = np.where(df['pmaup'], 'sp' , None)
        df['bpsp'] = np.where(df['pmadown'], 'bp' , df['bpsp'])
        df.to_csv('tmp.csv')
        return self.run3b(df, zj=100000, f=0.06, zs=0.02) 

    @util.display_func_name
    def suijikaicang(self, n=10):
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
        df['bpsp'] = np.where(df['krandint'].shift(2)== 0, 'sp' , None)
        df['bpsp'] = np.where(df['krandint'].shift(2)==2*n-1, 'bp' , df['bpsp'])
        df.to_csv('tmp.csv')
        return self.run3b(df, zj=100000, f=0.06, zs=0.02)

    def gudingkaicang(self, mode=3, n=10):
        '''
        固定一个间隔n开仓平仓，做好开仓止损, 平仓第二天，再开仓
        mode 1   开多
        mode 2   开空
        mode 3   一次开多  一次开空
        '''
        df = deepcopy(self.df)
        t = [1]
        t.extend([0] * (n-1))

        print t
        #for x in range(n-1):
        #    t.append()
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
        return self.run3b(df, zj=100000, f=0.06, zs=0.02)


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
        return self.run3b(df, zj=100000, f=0.06, zs=0.02)

    @util.display_func_name
    def qian_n_ri2_maupdown_run3(self, n=10, m=10):
        '''n天ma向上，sdjj比前n日高，买开仓，反之
        sdjj比前m日低，平仓
        '''
        self.get_ma(n)
        df = deepcopy(self.df) 
        ma = 'ma%s' % n
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
        return self.run3b(df, zj=100000, f=0.06, zs=0.02)

    @util.display_func_name
    def maupdown_qiannri(self, n=10, m=10):
        '''n天maupdown开仓， m天qiannri高低平仓'''
        self.get_ma(n)
        df = deepcopy(self.df) 
        ma1 = 'ma%s' % n

        df['maup'] = df[ma1].shift(1) > df[ma1].shift(2)
        df['madown'] = df[ma1].shift(1) < df[ma1].shift(2)
        df['bksk'] = np.where(df['maup'], 'bk' , None)
        df['bksk'] = np.where(df['madown'], 'sk' , df['bksk'])
        
        df['higherp'] = df.sdjj.shift(1) > df.sdjj.shift(m+1)
        df['lowerp'] = df.sdjj.shift(1) < df.sdjj.shift(m+1)
        df['bpsp'] = np.where(df['higherp'], 'sp' , None)
        df['bpsp'] = np.where(df['lowerp'], 'bp' , df['bpsp'])
        df.to_csv('tmp.csv')
        return self.run3b(df, zj=100000, f=0.06, zs=0.02)


if __name__ == '__main__':
    k = Kxian('ta')
    #k.gudingkaicang()
    #k.ma_updown(50)
    #k.cross_ma()
    #k.tupo_hl(20)
    #k.hl(20)
    #k.ma_cross(5,10)
    print k.hl_run3(10,10)
    #print k.tupo_hl_run3()
    #print k.ma_updown_run3(10)
    #print k.ma_updown_run3_shift()
    #print k.bigger_smaller_than_ma_run3(10)
    #rangerun3(k.ma_updown_run3, range(2,20), range(8,9))

    #print k.suijikaicang()
    #print k.qian_n_ri2_run3(10)
    #print k.maupdown_qiannri()

    #print k.ma_start_updown_run3(5)
    #print k.ma_updown_2day_run3(10)
    #print k.ma_updown_3day_run3()
    #print k.ma_cross_run3(5,10)