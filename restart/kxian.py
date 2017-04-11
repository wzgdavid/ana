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
        #self.df.dropna(how='any')
        #print self.df


    @util.display_func_name
    def hl(self, n=10):
        '''突破前n天最高价开多， 突破前n天最低价开空 '''
        self.get_nhh(n)
        self.get_nll(n)
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
        return self.run3b(df, zj=100000, f=0.02, zs=0.02, usehl=True)
        #self.run4(df, zj=100000, f=0.05, zs=0.02, ydzs=0.07, usehl=True)
        #self.run6(df, zj=100000, kclimit=3, f=0.02, zs=0.02, usehl=True)


    @util.display_func_name
    def hl_ma(self, n=10, m=3):
        '''突破前n天最高价, 且nnh_ma向上开多， 反之 '''
        self.get_nhh(n)
        self.get_nll(n)
        self.get_nhh_ma(m)
        self.get_nll_ma(m)
        df = deepcopy(self.df) 

        df['higher'] = df.h > df.nhh
        df['nhh_maup'] = df.nhh_ma > df.nhh_ma.shift(2)
        df['bksk'] = np.where(df['higher'] & df.nhh_maup, 'bk' , None)
        df['lower'] = df.l < df.nll
        df['nll_madown'] = df.nll_ma < df.nll_ma.shift(2)
        df['bksk'] = np.where(df['lower'] & df.nll_madown, 'sk' , df['bksk'])

        df['phigher'] = df.h > df.nhh 
        df['bpsp'] = np.where(df['phigher'], 'sp' , None)
        df['plower'] = df.l < df.nll
        df['bpsp'] = np.where(df['plower'], 'bp' , df['bpsp'])
        df.to_csv('tmp.csv')
        return self.run3b(df, zj=100000, f=0.02, zs=0.02, usehl=True)
        #self.run4(df, zj=100000, f=0.05, zs=0.02, ydzs=0.07, usehl=True)
        #self.run6(df, zj=100000, kclimit=3, f=0.02, zs=0.02, usehl=True)



    @util.display_func_name
    def chl(self, n=10):
        '''前一天收盘价比前n天最高价高，开多，反之'''
        self.get_nhh(n)
        self.get_nll(n)
        df = deepcopy(self.df) 

        df['higher'] = df.c.shift(1) > df.nhh.shift(1)
        df['bksk'] = np.where(df['higher'], 'bk' , None)
        df['lower'] = df.c.shift(1) < df.nll.shift(1)
        df['bksk'] = np.where(df['lower'], 'sk' , df['bksk'])

        df['phigher'] = df.c.shift(1) > df.nhh.shift(1) 
        df['bpsp'] = np.where(df['phigher'], 'sp' , None)
        df['plower'] = df.c.shift(1) < df.nll.shift(1)
        df['bpsp'] = np.where(df['plower'], 'bp' , df['bpsp'])
        df.to_csv('tmp.csv')

        return self.run3b(df, zj=100000, f=0.02, zs=0.02)
        #self.run4(df, zj=100000, f=0.02, zs=0.02, ydzs=0.06)

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

        #df.to_csv('tmp.csv')
        #return self.run3b(df, zj=100000, f=0.02, zs=0.02, jiacang=0)
        #return self.run4(df, zj=100000, f=0.02, zs=0.02, ydzs=0.06,jiacang=0)

    @util.display_func_name
    def ma_cross_run3_shift(self, a=5, b=25):
        '''因为信号出来都是后一天处理，所以要shift 1 
        '''
        self.get_ma(a, b)
        df = deepcopy(self.df) 
        maa = 'ma%s' % a
        mab = 'ma%s' % b
        df['tmp1'] = df[maa].shift(2) < df[mab].shift(2)
        df['tmp2'] = df[maa].shift(1) > df[mab].shift(1)
        df['jincha'] = df.tmp1 & df.tmp2

        df['tmp1'] = df[maa].shift(2) > df[mab].shift(2)
        df['tmp2'] = df[maa].shift(1) < df[mab].shift(1)
        df['sicha'] = df.tmp1 & df.tmp2
        df['bksk'] = np.where(df['jincha'], 'bk' , None)
        df['bksk'] = np.where(df['sicha'], 'sk' , df['bksk'])

        df['tmp1'] = df[maa].shift(2) < df[mab].shift(2)
        df['tmp2'] = df[maa].shift(1) > df[mab].shift(1)
        df['pjincha'] = df.tmp1 & df.tmp2

        df['tmp1'] = df[maa].shift(2) > df[mab].shift(2)
        df['tmp2'] = df[maa].shift(1) < df[mab].shift(1)
        df['psicha'] = df.tmp1 & df.tmp2
        df['bpsp'] = np.where(df['pjincha'], 'sp' , None)
        df['bpsp'] = np.where(df['psicha'], 'bp' , df['bpsp'])

        df.to_csv('tmp.csv')
        return self.run3b(df, zj=100000, f=0.02, zs=0.03, jiacang=0)

        #self.run4(df, zj=100000, f=0.06, zs=0.02, ydzs=0.07,jiacang=0.2)


    @util.display_func_name
    def cross_ma(self, n=20):
        '''k线穿越ma, 定义，前一天开盘价在ma下，今天开盘在ma上为一次向上穿越，反之
        跑下来这个策略收益低?
        为什么低？其实不低，主要是这个策略开仓信号比较少，但平均收益还是不错的
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
    def ma_updown_run3(self, n=20):
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

        df['pmaup'] = df[ma] > df[ma].shift(1)
        df['pmadown'] = df[ma] < df[ma].shift(1)
        df['bpsp'] = np.where(df['pmaup'], 'sp' , None)
        df['bpsp'] = np.where(df['pmadown'], 'bp' , df['bpsp'])
        df.to_csv('tmp.csv')
        return self.run3b(df, zj=100000, f=0.02, zs=0.02)


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
        return self.run3b(df, zj=100000, f=0.02, zs=0.01)
        #return self.run4(df, zj=100000, f=0.02, zs=0.01, ydzs=0.06)

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
        #return self.run3b(df, zj=100000, f=0.06, zs=0.02)

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
    def ma_updown_run3(self, n=10, m=10):
        '''ma比昨天高开多，反之开空
        不管哪个品种，策略间比较，跑下来这个最好
        '''
        self.get_ma(n)
        self.get_ma(m)
        df = deepcopy(self.df) 
        ma1 = 'ma%s' % n
        ma2 = 'ma%s' % m

        df['maup'] = df[ma1] > df[ma1].shift(1)
        df['madown'] = df[ma1] < df[ma1].shift(1)
        df['bksk'] = np.where(df['maup'], 'bk' , None)
        df['bksk'] = np.where(df['madown'], 'sk' , df['bksk'])

        df['pmaup'] = df[ma2] > df[ma2].shift(1)
        df['pmadown'] = df[ma2] < df[ma2].shift(1)
        df['bpsp'] = np.where(df['pmaup'], 'sp' , None)
        df['bpsp'] = np.where(df['pmadown'], 'bp' , df['bpsp'])
        df.to_csv('tmp.csv')
        #return self.run3b(df, zj=100000, f=0.06, zs=0.02, jiacang=0.05) # 相同的策略不同的品种结果不一样，但同一种品种，f 和 zs还是有相对优势的参数
                            # zs 一般最优是0.02， f是越大收益越高，风险也越大，和资金管理书上说的如出一辙
        return self.run4(df, zj=100000, f=0.06, zs=0.02, ydzs=0.06, jiacang=0)



    @util.display_func_name
    def suijikaicang(self, n=10):
        '''
        随机平均n天开一仓，方向随机

        
        '''
        df = deepcopy(self.df)
        #print np.random.randint(n*2, size=len(df)) # 得到随机0 到2n-1的整数
        df['krandint'] = np.random.randint(n*2, size=len(df))
        df['prandint'] = np.random.randint(n*2, size=len(df))

        df['bksk'] = np.where(df['krandint']== 0, 'bk' , None)
        df['bksk'] = np.where(df['krandint']==2*n-1, 'sk' , df['bksk'])
        #df['bpsp'] = np.where(df['krandint'].shift(2)== 0, 'sp' , None)
        #df['bpsp'] = np.where(df['krandint'].shift(2)==2*n-1, 'bp' , df['bpsp'])
        df.to_csv('tmp.csv')
        #return self.run3b(df, zj=100000, f=0.06, zs=0.02, jiacang=0.1)

        return self.run4(df, zj=100000, f=0.02, zs=0.02, ydzs=0.06)

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
    def gtlt_ma(self, n=10, m=10):
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
        return self.run3b(df, zj=100000, f=0.02, zs=0.02)


    @util.display_func_name
    def qian_n_ri2_run3(self, n=10, m=10):
        '''比前n日高，买开仓，反之'''
        df = deepcopy(self.df) 
        df['higher'] = df.c > df.c.shift(n)
        df['lower'] = df.c < df.c.shift(n)
          
        df['bksk'] = np.where(df['higher'], 'bk' , None)
        # bk表示买开仓或买平仓，sk相反
        df['bksk'] = np.where(df['lower'], 'sk' , df['bksk'])

        df['higherp'] = df.c > df.c.shift(m)
        df['lowerp'] = df.c < df.c.shift(m)
          
        df['bpsp'] = np.where(df['higherp'], 'sp' , None)
        df['bpsp'] = np.where(df['lowerp'], 'bp' , df['bpsp'])
        df.to_csv('tmp.csv')
        return self.run3b(df, zj=100000, f=0.02, zs=0.02)

    @util.display_func_name
    def qian_n_ri2_run3_shift(self, n=10, m=10):
        '''比前n日高，买开仓，反之'''
        df = deepcopy(self.df) 
        df['higher'] = df.c.shift(1) > df.c.shift(n+1)
        df['lower'] = df.c.shift(1) < df.c.shift(n+1)
          
        df['bksk'] = np.where(df['higher'], 'bk' , None)
        # bk表示买开仓或买平仓，sk相反
        df['bksk'] = np.where(df['lower'], 'sk' , df['bksk'])

        df['higherp'] = df.c.shift(1) > df.c.shift(m+1)
        df['lowerp'] = df.c.shift(1) < df.c.shift(m+1)
          
        df['bpsp'] = np.where(df['higherp'], 'sp' , None)
        df['bpsp'] = np.where(df['lowerp'], 'bp' , df['bpsp'])
        df.to_csv('tmp.csv')
        return self.run3b(df, zj=100000, f=0.02, zs=0.02)

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
        '''n天ma向上，比m天前sdjj高，开多仓，反之开空仓
        '''
        self.get_ma(n)
        df = deepcopy(self.df) 
        ma1 = 'ma%s' % n

        df['maup'] = df[ma1].shift(1) > df[ma1].shift(2)
        df['madown'] = df[ma1].shift(1) < df[ma1].shift(2)
        df['higher'] = df.sdjj.shift(1) > df.sdjj.shift(m+1)
        df['lower'] = df.sdjj.shift(1) < df.sdjj.shift(m+1)
        df['bksk'] = np.where(df.maup & df.higher, 'bk' , None)
        df['bksk'] = np.where(df.madown & df.lower, 'sk' , df['bksk'])

        df['pmaup'] = df[ma1].shift(1) > df[ma1].shift(2)
        df['pmadown'] = df[ma1].shift(1) < df[ma1].shift(2)
        df['phigher'] = df.sdjj.shift(1) > df.sdjj.shift(m+1)
        df['plower'] = df.sdjj.shift(1) < df.sdjj.shift(m+1)
        df['bpsp'] = np.where(df.phigher & df.pmaup, 'sp' , None)
        df['bpsp'] = np.where(df.plower & df.pmadown, 'bp' , df['bpsp'])
        df.to_csv('tmp.csv')
        return self.run3b(df, zj=100000, f=0.02, zs=0.02)
        #return self.run4(df, zj=100000, f=0.06, zs=0.02, ydzs=0.06)

    @util.display_func_name
    def ma_updown_run3_shift(self, n=10, m=10): # 这个不行
        '''
        昨天ma比前天ma高，开多，反之开空
        这个跑下来 run4比run3b好？ 和其他相反？
        为什么ma_updown_run3_shift  和ma_updown_run3 相差那么大？
        '''
        self.get_ma(n)
        self.get_ma(m)
        df = deepcopy(self.df) 
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
        #df.to_csv('tmp.csv')
        return self.run3b(df, zj=100000, f=0.02, zs=0.02, jiacang=0) 
        #self.run3b(df, zj=100000, f=0.06, zs=0.01, jiacang=0.2)
        #self.run3b(df, zj=100000, f=0.06, zs=0.03, jiacang=0.1)
        #self.run3b(df, zj=100000, f=0.06, zs=0.03, jiacang=0.2)
        #self.run3b(df, zj=100000, f=0.06, zs=0.03, jiacang=0.3)
        #self.run3b(df, zj=100000, f=0.06, zs=0.03, jiacang=0.4)
        #return self.run4(df, zj=100000, f=0.02, zs=1, ydzs=1,jiacang=0)

    @util.display_func_name
    def ma_shangxia_ma(self, a=5, b=10):
        '''
        小ma在大ma上开多，反之开空
        ma_cross就等于这个的一种特殊情况
        '''
        self.get_ma(a)
        self.get_ma(b)
        
        df = deepcopy(self.df) 
        ma1 = 'ma%s' % a
        ma2 = 'ma%s' % b

        df['maup'] = df[ma1].shift(1) > df[ma2].shift(1)
        df['madown'] = df[ma1].shift(1) < df[ma2].shift(1)
        df['bksk'] = np.where(df['maup'], 'bk' , None)
        df['bksk'] = np.where(df['madown'], 'sk' , df['bksk'])

        df['bpsp'] = np.where(df['madown'], 'bp' , None)
        df['bpsp'] = np.where(df['maup'], 'sp' , df['bpsp'])

        df.to_csv('tmp.csv')
        return self.run3b(df, zj=100000, f=0.02, zs=0.02)

    @util.display_func_name
    def ma_shangxia_ma__3xian(self, a=5, b=10, c=20):
        '''
        小ma在大ma上开多，反之开空
        ma_cross就等于这个的一种特殊情况
        '''
        self.get_ma(a)
        self.get_ma(b)
        self.get_ma(c)
        df = deepcopy(self.df) 
        maa = 'ma%s' % a
        mab = 'ma%s' % b
        mac = 'ma%s' % c

        df['ab'] = df[maa].shift(1) > df[mab].shift(1)
        df['bc'] = df[mab].shift(1) > df[mac].shift(1)
        df['mabup'] = df[mab].shift(1) > df[mab].shift(2)
        df['ab2'] = df[maa].shift(1) < df[mab].shift(1)
        df['bc2'] = df[mab].shift(1) < df[mac].shift(1)
        df['mabdown'] = df[mab].shift(1) < df[mab].shift(2)

        df['bksk'] = np.where(df.ab & df.bc & df.mabup, 'bk' , None)
        df['bksk'] = np.where(df.ab2 & df.bc2 & df.mabdown, 'sk' , df['bksk'])

        df.to_csv('tmp.csv')
        return self.run4(df, zj=100000, f=0.02, zs=0.03, ydzs=0.07) 

    @util.display_func_name
    def maupdown_gtltma(self, n=10, m=10):
        '''
        ma向上，k线大于ma, 开多
        '''
        self.get_ma(n)
        self.get_ma(m)
        df = deepcopy(self.df) 
        ma1 = 'ma%s' % n
        ma2 = 'ma%s' % m

        df['maup'] = df[ma1].shift(1) > df[ma1].shift(2)
        df['gtma'] = df.l.shift(1) > df[ma1].shift(1)
        df['madown'] = df[ma1].shift(1) < df[ma1].shift(2)
        df['ltma'] = df.h.shift(1) < df[ma1].shift(1)
        df['bksk'] = np.where(df['maup'] & df.gtma, 'bk' , None)
        df['bksk'] = np.where(df['madown'] & df.ltma, 'sk' , df['bksk'])

        df['pmaup'] = df[ma2].shift(1) > df[ma2].shift(2)
        df['pgtma'] = df.l.shift(1) > df[ma2].shift(1)
        df['pmadown'] = df[ma2].shift(1) < df[ma2].shift(2)
        df['pltma'] = df.h.shift(1) < df[ma2].shift(1)
        df['bpsp'] = np.where(df['pmaup'] & df.pgtma, 'sp' , None)
        df['bpsp'] = np.where(df['pmadown'] & df.pltma, 'bp' , df['bpsp'])


        df.to_csv('tmp.csv')
        return self.run3b(df, zj=100000, f=0.02, zs=0.02)
        #self.run4(df, zj=100000, f=0.02, zs=0.02, ydzs=0.06)

    @util.display_func_name
    def maupdown_cgtltma(self, n=10, m=10):
        '''
        ma向上，收盘线大于ma, 开多
        '''
        self.get_ma(n)
        self.get_ma(m)
        df = deepcopy(self.df) 
        ma1 = 'ma%s' % n
        ma2 = 'ma%s' % m

        df['maup'] = df[ma1].shift(1) > df[ma1].shift(2)
        df['gtma'] = df.c.shift(1) > df[ma1].shift(1)
        df['madown'] = df[ma1].shift(1) < df[ma1].shift(2)
        df['ltma'] = df.c.shift(1) < df[ma1].shift(1)
        df['bksk'] = np.where(df['maup'] & df.gtma, 'bk' , None)
        df['bksk'] = np.where(df['madown'] & df.ltma, 'sk' , df['bksk'])

        df['pmaup'] = df[ma2].shift(1) > df[ma2].shift(2)
        df['pgtma'] = df.c.shift(1) > df[ma2].shift(1)
        df['pmadown'] = df[ma2].shift(1) < df[ma2].shift(2)
        df['pltma'] = df.c.shift(1) < df[ma2].shift(1)
        df['bpsp'] = np.where(df['pmaup'] & df.pgtma, 'sp' , None)
        df['bpsp'] = np.where(df['pmadown'] & df.pltma, 'bp' , df['bpsp'])


        df.to_csv('tmp.csv')
        return self.run3b(df, zj=100000, f=0.02, zs=1)
        #self.run4(df, zj=100000, f=0.02, zs=0.02, ydzs=0.06)

    def foo(self, n=2):
        self.get_nhh(n)
        self.get_nll(n)
        df = deepcopy(self.df) 
        df['higher'] = df.h >= df.nhh
        df['lower'] = df.l <= df.nll
        df['bpsp'] = np.where(df['higher'] & df['lower'], 1 , None)
        df['cumsum'] = df['bpsp'].cumsum()
        df.to_csv('tmp.csv')


    @util.display_func_name
    def hl2(self, n=5, m=10, zs=1, zj=100000, f=0.02 ):
        '''用runhl跑，runhl专为hl写的 
         突破n天高低点
         移动止损m天高低点
         zs 开仓止损
         zj 总资金量
         f 风险百分比
        '''
        self.get_nhh(n)
        self.get_nll(n)
        self.get_nch(n)
        self.get_ncl(n)
        self.get_nhhp(m)
        self.get_nllp(m)
        ma = 20
        ma_name = 'ma'+str(ma)
        self.get_ma(ma)
        if zs>=1 and type(zs) == int:
            self.get_zshh(zs)
            self.get_zsll(zs)
        df = deepcopy(self.df) 

        option = {
            'tupo_high': df.h > df.nhh,
            'tupo_low': df.l < df.nll,
            'tupo_high_c': df.c > df.nch, # 是不是用这个效果好
            'tupo_low_c': df.c < df.ncl,
            'higher_than_ma': df.l.shift(1) > df[ma_name].shift(1),
            'lower_than_ma': df.h.shift(1) < df[ma_name].shift(1),
            'higher_than_ma_c': df.c.shift(1) > df[ma_name].shift(1),
            'lower_than_ma_c': df.c.shift(1) < df[ma_name].shift(1),
            'maup': df[ma_name].shift(1) > df[ma_name].shift(2),
            'madown': df[ma_name].shift(1) < df[ma_name].shift(2),
            'hl_bothhigh': (df.h.shift(1) > df.h.shift(2)) & (df.h.shift(1) > df.h.shift(2)),
            'hl_bothlow': (df.l.shift(1) < df.l.shift(2)) & (df.l.shift(1) < df.l.shift(2)),

                  }

        df['higher'] = option['tupo_high_c'] #& option['higher_than_ma_c']
        df['lower'] = option['tupo_low_c']   #& option['lower_than_ma_c'] 

        #df['higher'] = option['tupo_high'] 
        #df['lower'] = option['tupo_low']   
        
        df['bksk'] = np.where(df['higher'], 'bk' , None)
        #df['bksk'] = np.where(df['lower'], 'sk' , None)
        df['bksk'] = np.where(df['lower'], 'sk' , df['bksk'])

        df['phigher'] = df.h >= df.nhhp 
        df['bpsp'] = np.where(df['phigher'], 'sp' , None)
        df['plower'] = df.l <= df.nllp
        df['bpsp'] = np.where(df['plower'], 'bp' , df['bpsp'])

        df.to_csv('tmp.csv')
        return self.runhl(df, zj, f, zs)


if __name__ == '__main__':
    k = Kxian('c') # ta rb c m a ma jd dy 999999 sr
    #k.hl2(3,3)
    #k.hl2(4,4) #
    #k.hl2(5,5)
    #k.hl2(6,6)
    #k.hl2(7,7)
    #k.hl2(8,8)
    #k.hl2(9,9)
    #k.hl2(11,10)
    #k.hl2(11,9)
    #k.hl2(11,8)
    #k.hl2(11,7)
    #k.hl2(11,6)
    #k.hl2(11,5)
    #k.hl2(11,4)
    #k.hl2(11,3)
    #k.hl2(17,15)
    #k.hl2(17,13)
    #k.hl2(17,11)
    #k.hl2(17,9)
    #k.hl2(17,7)
    #k.hl2(17,5)
    #k.hl2(17,4)
    #k.hl2(2,17,1)
    #k.foo(4)
    k.hl2(2,7,2)
    #k.hl2_hl(2,17,1)
    #k.chl(2,9)
    #k.hl2(2,7)
    #k.ma_updown_run3(9)
    #k.hl2(2,11)
    #k.hl2(2,10)
    #k.hl2(2,9)
    #k.hl2(2,8)
    #k.hl2(2,7)
    #k.hl2(2,6)
    #print '==========================='
    #k.hl2(3,11)
    #k.hl2(3,10)
    #k.hl2(3,9)
    #k.hl2(3,8)
    #k.hl2(3,7)
    #k.hl2(3,6)
    #k.hl2(2,5)
    #k.hl2(3,6)
    #k.hl2(3,9)
    #k.hl2(3,9)
    #k.hl2(3,8)
    #k.hl2(3,7)
    #k.hl2(12,6)
    #k.hl2(10,5)
    #k.hl2(8,4)
    #k.hl2(6,3)

    #k.hl2(6,12)
    #k.hl2(5,10)
    #k.hl2(4,8)
    #k.hl2(3,6)
    #k.hl2(2,9)
    #k.gtlt_ma(11,11)
    #k.maupdown_gtltma(15,15)
    #k.ma_cross_run3_shift(5,20)
#
    #k.hl(17)
    #k.gtlt_ma(17,17)
    #k.maupdown_gtltma(17,17)
    #k.ma_cross_run3_shift(5,30)

    #k.ma_shangxia_ma(5,40)# 这个不行
    #k.ma_shangxia_ma__3xian(5,10,20)
    #k.chl(11) 
    #print k.qian_n_ri2_run3(11,11)
    #print k.qian_n_ri2_run3_shift(11,11)
    # run3b   rb16  ta20  c16 m18 dy21  999999 20
    #k.gudingkaicang()

    #k.cross_ma()
    #k.tupo_hl(10)

    #k.ma_cross(5,10)
    #print k.hl_run3(2,2)
    #k.hl_run3(2)
    #print k.tupo_hl_run3(2)
    #print k.ma_updown_run3(2)
    #print k.ma_updown_run3_shift(9,9)# 这个不行
    
    #rangerun3(k.ma_updown_run3, range(2,20), range(8,9))

    #print k.suijikaicang(5)
    #print 
    
    #print k.maupdown_qiannri()

    
