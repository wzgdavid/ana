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
    def hl2(self, n=5, m=10, zs=1, zj=100000, f=0.02):
        '''用runhl跑，runhl专为hl写的 
         突破n天高低点
         移动止损m高低点
         zs 开仓止损
         zj 总资金量
         f 风险百分比
        '''
        self.get_nhh(n)
        self.get_nll(n)
        self.get_nhhp(m)
        self.get_nllp(m)
        self.get_nch(n)
        self.get_ncl(n)
        self.get_nchp(m)
        self.get_nclp(m)
        self.get_nsthl(n)
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
            
            'tupo_high_c': df.h > df.nch, # 突破前几天收盘价的高点
            'tupo_low_c': df.l < df.ncl,
            
            'tupo_high_st': df.h > df.nsth, # 突破前几天实体的高点
            'tupo_low_st': df.l < df.nstl,

            'higher_than_ma': df.l.shift(1) > df[ma_name].shift(1),
            'lower_than_ma': df.h.shift(1) < df[ma_name].shift(1),
            'higher_than_ma_c': df.c.shift(1) > df[ma_name].shift(1),
            'lower_than_ma_c': df.c.shift(1) < df[ma_name].shift(1),
            'maup': df[ma_name].shift(1) > df[ma_name].shift(2),
            'madown': df[ma_name].shift(1) < df[ma_name].shift(2),
            'hl_bothhigh': (df.h.shift(1) > df.h.shift(2)) & (df.h.shift(1) > df.h.shift(2)),
            'hl_bothlow': (df.l.shift(1) < df.l.shift(2)) & (df.l.shift(1) < df.l.shift(2)),

            'last_yang': df.o.shift(1) > df.c.shift(1),
            'last_yin': df.o.shift(1) < df.c.shift(1),

            'higher_nll': df.nll> df.nll.shift(7),
            'lower_nhh': df.nhh< df.nhh.shift(7),
                  }
        # 别忘了在runhl中改nhh cnh等
        df['higher'] = option['tupo_high_c'] & option['higher_than_ma_c'] 
        df['lower'] = option['tupo_low_c']   & option['lower_than_ma_c']  
        # 别忘了在runhl中改nhh cnh等  还是这个稳点
        #df['higher'] = option['tupo_high'] & option['higher_than_ma_c'] 
        #df['lower'] = option['tupo_low']    & option['lower_than_ma_c'] 
        # 别忘了在runhl中改nhh cnh等
        #df['higher'] = option['tupo_high_st'] & option['higher_than_ma_c'] 
        #df['lower'] = option['tupo_low_st']    & option['lower_than_ma_c'] 

        #df['higher'] = option['tupo_high_c'] & option['higher_nll'] #&  option['last_yin']
        #df['lower'] = option['tupo_low_c']   & option['lower_nhh']  #&  option['last_yang']
        #df['higher'] = option['tupo_high'] 
        #df['lower'] = option['tupo_low']   
        
        df['bksk'] = np.where(df['higher'], 'bk' , None)
        df['bksk'] = np.where(df['lower'], 'sk' , df['bksk'])
        #df['bksk'] = np.where(df['lower'], 'sk' , None)
        #df['bksk'] = np.where(df['higher'], 'bk' , df['bksk'])



        df['phigher'] = df.h >= df.nhhp 
        df['bpsp'] = np.where(df['phigher'], 'sp' , None)
        df['plower'] = df.l <= df.nllp
        df['bpsp'] = np.where(df['plower'], 'bp' , df['bpsp'])

        df.to_csv('tmp.csv')
        return self.runhl(df, zj, f, zs)


def fuhe_liankui():
    c = [(' 2004/11/05', 0), (' 2004/11/15', 0), (' 2004/11/30', 0), (' 2004/12/28', 1), (' 2005/01/07', 0), (' 2005/01/19', 0), (' 2005/01/24', 0), (' 2005/01/28', 0), (' 2005/02/16', 0), (' 2005/02/22', 0), (' 2005/04/01', 1), (' 2005/04/14', 0), (' 2005/04/20', 0), (' 2005/05/24', 1), (' 2005/06/06', 0), (' 2005/06/28', 0), (' 2005/07/06', 0), (' 2005/07/14', 0), (' 2005/07/20', 0), (' 2005/09/02', 1), (' 2005/09/13', 0), (' 2005/09/27', 1), (' 2005/09/28', 0), (' 2005/10/20', 1), (' 2005/10/31', 0), (' 2005/11/14', 0), (' 2005/11/25', 0), (' 2005/12/01', 0), (' 2006/01/13', 1), (' 2006/03/01', 1), (' 2006/03/27', 1), (' 2006/03/28', 0), (' 2006/04/03', 0), (' 2006/04/27', 1), (' 2006/06/01', 1), (' 2006/06/14', 0), (' 2006/06/21', 0), (' 2006/07/03', 0), (' 2006/08/16', 1), (' 2006/08/29', 0), (' 2006/09/25', 1), (' 2006/11/29', 1), (' 2006/12/11', 0), (' 2007/01/04', 0), (' 2007/01/11', 0), (' 2007/02/13', 0), (' 2007/03/21', 1), (' 2007/04/09', 0), (' 2007/04/26', 0), (' 2007/05/29', 1), (' 2007/06/07', 0), (' 2007/06/08', 0), (' 2007/07/31', 1), (' 2007/08/17', 1), (' 2007/09/19', 1), (' 2007/11/16', 1), (' 2007/12/06', 1), (' 2007/12/11', 0), (' 2007/12/17', 0), (' 2007/12/24', 0), (' 2007/12/26', 0), (' 2007/12/27', 0), (' 2008/01/07', 0), (' 2008/01/16', 0), (' 2008/02/01', 1), (' 2008/02/28', 1), (' 2008/03/18', 0), (' 2008/03/31', 0), (' 2008/04/11', 0), (' 2008/05/15', 1), (' 2008/05/26', 0), (' 2008/06/06', 0), (' 2008/07/07', 1), (' 2008/07/11', 0), (' 2008/08/14', 1), (' 2008/08/26', 0), (' 2008/09/04', 0), (' 2008/09/19', 1), (' 2008/10/20', 0), (' 2008/12/18', 1), (' 2009/03/03', 1), (' 2009/03/27', 1), (' 2009/04/10', 0), (' 2009/04/24', 1), (' 2009/05/04', 0), (' 2009/05/14', 0), (' 2009/06/01', 0), (' 2009/06/05', 0), (' 2009/06/23', 0), (' 2009/07/01', 0), (' 2009/07/28', 0), (' 2009/09/11', 1), (' 2009/09/24', 0), (' 2009/10/13', 0), (' 2009/10/28', 1), (' 2009/12/23', 1), (' 2010/01/22', 1), (' 2010/02/03', 0), (' 2010/03/05', 0), (' 2010/04/08', 1), (' 2010/04/20', 0), (' 2010/04/27', 0), (' 2010/05/28', 1), (' 2010/06/25', 1), (' 2010/06/28', 0), (' 2010/07/05', 0), (' 2010/08/25', 1), (' 2010/11/26', 1), (' 2010/12/02', 0), (' 2010/12/29', 1), (' 2010/12/30', 0), (' 2011/01/07', 0), (' 2011/01/26', 1), (' 2011/02/23', 1), (' 2011/03/11', 0), (' 2011/04/11', 0), (' 2011/05/09', 0), (' 2011/06/07', 1), (' 2011/06/16', 0), (' 2011/07/13', 1), (' 2011/08/05', 0), (' 2011/08/24', 0), (' 2011/08/29', 0), (' 2011/09/14', 0), (' 2011/09/16', 0), (' 2011/10/28', 1), (' 2011/12/01', 1), (' 2012/02/16', 1), (' 2012/03/27', 1), (' 2012/03/28', 0), (' 2012/05/21', 1), (' 2012/06/05', 0), (' 2012/07/11', 1), (' 2012/07/24', 0), (' 2012/08/13', 0), (' 2012/08/23', 0), (' 2012/09/04', 0), (' 2012/09/20', 1), (' 2012/10/17', 1), (' 2012/11/13', 1), (' 2012/12/14', 1), (' 2012/12/24', 0), (' 2013/01/04', 0), (' 2013/01/17', 0), (' 2013/01/31', 0), (' 2013/02/05', 0), (' 2013/03/07', 1), (' 2013/03/29', 1), (' 2013/05/02', 1), (' 2013/05/20', 1), (' 2013/05/22', 0), (' 2013/06/05', 0), (' 2013/06/19', 0), (' 2013/07/04', 1), (' 2013/07/15', 0), (' 2013/08/20', 1), (' 2013/09/05', 0), (' 2013/09/24', 0), (' 2013/10/10', 0), (' 2013/10/24', 0), (' 2013/11/06', 0), (' 2013/12/06', 1), (' 2014/01/02', 1), (' 2014/01/17', 1), (' 2014/01/20', 0), (' 2014/02/10', 0), (' 2014/02/17', 0), (' 2014/03/03', 0), (' 2014/03/26', 0), (' 2014/04/14', 1), (' 2014/05/14', 0), (' 2014/05/22', 0), (' 2014/07/01', 1), (' 2014/07/22', 1), (' 2014/08/19', 0), (' 2014/08/29', 0), (' 2014/09/30', 1), (' 2014/10/20', 0), (' 2014/11/25', 1), (' 2014/12/15', 0), (' 2014/12/30', 0), (' 2015/01/19', 0), (' 2015/03/19', 1), (' 2015/03/23', 0), (' 2015/03/26', 0), (' 2015/04/13', 1), (' 2015/05/13', 1), (' 2015/07/17', 1), (' 2015/07/24', 0), (' 2015/08/18', 1), (' 2015/10/26', 1), (' 2015/11/20', 0), (' 2015/12/07', 0), (' 2015/12/23', 0), (' 2016/01/07', 1), (' 2016/01/25', 1), (' 2016/02/16', 1), (' 2016/03/18', 1), (' 2016/04/12', 1), (' 2016/04/28', 0), (' 2016/05/06', 0), (' 2016/05/11', 0), (' 2016/05/27', 0), (' 2016/06/15', 1), (' 2016/07/04', 0), (' 2016/08/16', 1), (' 2016/08/23', 0), (' 2016/09/19', 0), (' 2016/10/12', 0), (' 2016/11/24', 1), (' 2016/12/08', 0), (' 2016/12/16', 0), (' 2016/12/28', 0)]
    
    m = [(' 2000/08/28', 0), (' 2000/08/31', 0), (' 2000/09/14', 0), (' 2000/10/09', 0), (' 2000/10/25', 0), (' 2000/12/28', 1), (' 2001/04/26', 1), (' 2001/05/16', 0), (' 2001/05/28', 0), (' 2001/06/18', 1), (' 2001/08/06', 1), (' 2001/09/10', 1), (' 2001/09/21', 0), (' 2001/10/08', 0), (' 2001/10/29', 0), (' 2001/11/02', 0), (' 2001/11/19', 0), (' 2001/11/27', 0), (' 2001/12/10', 0), (' 2002/01/07', 0), (' 2002/01/25', 0), (' 2002/02/01', 0), (' 2002/03/19', 1), (' 2002/03/22', 0), (' 2002/03/28', 0), (' 2002/04/23', 1), (' 2002/04/29', 0), (' 2002/05/20', 0), (' 2002/05/24', 0), (' 2002/06/13', 1), (' 2002/07/01', 1), (' 2002/07/02', 0), (' 2002/07/12', 0), (' 2002/08/09', 1), (' 2002/09/04', 1), (' 2002/09/13', 0), (' 2002/09/18', 0), (' 2002/10/17', 1), (' 2002/10/22', 0), (' 2002/10/29', 0), (' 2002/11/11', 1), (' 2002/12/17', 1), (' 2003/01/09', 1), (' 2003/01/22', 1), (' 2003/02/13', 0), (' 2003/02/21', 0), (' 2003/02/26', 0), (' 2003/03/24', 1), (' 2003/03/28', 0), (' 2003/04/29', 1), (' 2003/05/13', 0), (' 2003/05/23', 0), (' 2003/06/05', 0), (' 2003/06/18', 0), (' 2003/07/04', 0), (' 2003/07/08', 0), (' 2003/07/16', 0), (' 2003/07/28', 0), (' 2003/08/28', 1), (' 2003/11/07', 1), (' 2003/11/12', 0), (' 2003/12/01', 1), (' 2003/12/03', 0), (' 2003/12/16', 0), (' 2003/12/26', 0), (' 2004/01/08', 0), (' 2004/01/30', 0), (' 2004/02/06', 0), (' 2004/04/08', 1), (' 2004/06/16', 1), (' 2004/07/07', 0), (' 2004/07/30', 1), (' 2004/08/13', 1), (' 2004/08/24', 0), (' 2004/08/31', 0), (' 2004/09/09', 0), (' 2004/10/26', 1), (' 2004/11/15', 1), (' 2004/11/29', 1), (' 2004/12/13', 0), (' 2004/12/27', 0), (' 2005/01/10', 0), (' 2005/02/16', 1), (' 2005/03/23', 1), (' 2005/04/04', 0), (' 2005/04/07', 0), (' 2005/04/20', 0), (' 2005/04/29', 0), (' 2005/05/23', 0), (' 2005/06/27', 1), (' 2005/06/30', 0), (' 2005/08/31', 1), (' 2005/09/12', 0), (' 2005/10/13', 0), (' 2005/10/21', 0), (' 2005/11/04', 0), (' 2005/12/09', 1), (' 2006/01/13', 1), (' 2006/01/17', 0), (' 2006/01/27', 0), (' 2006/02/23', 0), (' 2006/03/27', 1), (' 2006/04/27', 1), (' 2006/05/22', 1), (' 2006/06/01', 0), (' 2006/06/20', 0), (' 2006/07/03', 0), (' 2006/07/12', 0), (' 2006/08/18', 1), (' 2006/08/29', 0), (' 2006/09/11', 0), (' 2006/09/29', 0), (' 2006/11/24', 1), (' 2006/11/29', 0), (' 2006/12/25', 1), (' 2007/01/09', 0), (' 2007/03/14', 1), (' 2007/03/21', 0), (' 2007/03/30', 0), (' 2007/04/26', 1), (' 2007/05/08', 0), (' 2007/05/30', 0), (' 2007/06/07', 0), (' 2007/07/02', 0), (' 2007/07/09', 0), (' 2007/07/11', 0), (' 2007/07/24', 0), (' 2007/07/30', 0), (' 2007/10/08', 1), (' 2007/11/21', 1), (' 2007/11/28', 0), (' 2007/12/10', 0), (' 2007/12/21', 0), (' 2008/01/16', 1), (' 2008/02/05', 0), (' 2008/03/10', 0), (' 2008/04/10', 1), (' 2008/07/08', 1), (' 2008/08/14', 1), (' 2008/08/20', 0), (' 2008/09/04', 0), (' 2008/09/23', 0), (' 2008/10/28', 1), (' 2008/12/15', 1), (' 2009/01/21', 1), (' 2009/02/17', 0), (' 2009/03/10', 1), (' 2009/03/30', 1), (' 2009/04/20', 1), (' 2009/05/06', 0), (' 2009/06/12', 1), (' 2009/07/01', 0), (' 2009/07/29', 1), (' 2009/08/17', 0), (' 2009/08/24', 0), (' 2009/09/17', 1), (' 2009/10/12', 0), (' 2009/10/28', 0), (' 2009/11/11', 0), (' 2009/12/09', 1), (' 2009/12/15', 0), (' 2010/01/07', 0), (' 2010/02/11', 1), (' 2010/03/04', 0), (' 2010/03/17', 0), (' 2010/03/19', 0), (' 2010/05/06', 1), (' 2010/06/21', 1), (' 2010/07/27', 1), (' 2010/08/20', 1), (' 2010/08/27', 0), (' 2010/10/20', 1), (' 2010/10/27', 0), (' 2010/11/05', 0), (' 2010/11/15', 0), (' 2010/12/06', 1), (' 2010/12/13', 0), (' 2011/01/26', 1), (' 2011/02/16', 0), (' 2011/03/04', 1), (' 2011/03/23', 1), (' 2011/04/12', 0), (' 2011/04/22', 0), (' 2011/05/20', 1), (' 2011/06/16', 0), (' 2011/06/30', 1), (' 2011/07/08', 0), (' 2011/07/25', 1), (' 2011/08/04', 0), (' 2011/08/16', 0), (' 2011/08/22', 0), (' 2011/09/13', 0), (' 2011/10/14', 1), (' 2011/10/27', 0), (' 2011/11/04', 0), (' 2011/12/01', 1), (' 2011/12/19', 0), (' 2012/01/13', 1), (' 2012/04/18', 1), (' 2012/05/09', 0), (' 2012/05/11', 0), (' 2012/06/06', 1), (' 2012/07/25', 1), (' 2012/08/14', 1), (' 2012/09/06', 1), (' 2012/11/26', 1), (' 2012/12/03', 0), (' 2012/12/19', 0), (' 2013/01/15', 1), (' 2013/01/21', 0), (' 2013/01/24', 0), (' 2013/02/18', 1), (' 2013/02/25', 0), (' 2013/03/13', 0), (' 2013/03/28', 1), (' 2013/04/18', 1), (' 2013/05/08', 0), (' 2013/05/13', 0), (' 2013/06/17', 1), (' 2013/07/09', 0), (' 2013/07/25', 0), (' 2013/08/09', 1), (' 2013/09/23', 1), (' 2013/10/11', 0), (' 2013/11/11', 1), (' 2013/11/27', 0), (' 2013/12/12', 0), (' 2013/12/30', 0), (' 2014/01/15', 1), (' 2014/01/22', 0), (' 2014/02/07', 0), (' 2014/02/28', 0), (' 2014/03/20', 0), (' 2014/04/14', 1), (' 2014/06/04', 1), (' 2014/06/23', 0), (' 2014/07/29', 1), (' 2014/08/12', 0), (' 2014/10/14', 1), (' 2014/11/04', 0), (' 2014/11/18', 0), (' 2014/11/28', 0), (' 2014/12/10', 0), (' 2014/12/16', 0), (' 2014/12/29', 0), (' 2015/01/05', 0), (' 2015/02/04', 1), (' 2015/03/06', 1), (' 2015/03/09', 0), (' 2015/03/18', 0), (' 2015/04/22', 1), (' 2015/05/04', 0), (' 2015/05/12', 0), (' 2015/06/05', 1), (' 2015/06/23', 0), (' 2015/06/30', 0), (' 2015/07/01', 0), (' 2015/07/09', 0), (' 2015/07/27', 0), (' 2015/08/05', 0), (' 2015/08/10', 0), (' 2015/08/19', 0), (' 2015/08/28', 0), (' 2015/09/14', 0), (' 2015/09/21', 0), (' 2015/10/14', 0), (' 2015/12/01', 1), (' 2015/12/21', 0), (' 2016/01/04', 0), (' 2016/01/29', 1), (' 2016/02/16', 0), (' 2016/03/07', 1), (' 2016/03/22', 1), (' 2016/03/31', 0), (' 2016/04/05', 0), (' 2016/05/24', 1), (' 2016/06/24', 1), (' 2016/06/27', 0), (' 2016/07/07', 0), (' 2016/08/10', 1), (' 2016/08/15', 0), (' 2016/08/19', 0), (' 2016/09/07', 1), (' 2016/09/13', 0), (' 2016/09/19', 0), (' 2016/09/22', 0), (' 2016/10/21', 1), (' 2016/11/02', 0), (' 2016/11/10', 0), (' 2016/11/14', 0), (' 2016/12/02', 1), (' 2016/12/09', 0), (' 2016/12/20', 0), (' 2016/12/28', 0)]
    
    a = [(' 2000/02/24', 0), (' 2000/03/14', 0), (' 2000/03/30', 0), (' 2000/04/07', 0), (' 2000/04/26', 0), (' 2000/05/08', 0), (' 2000/05/17', 0), (' 2000/06/22', 1), (' 2000/07/14', 1), (' 2000/08/28', 1), (' 2000/09/15', 1), (' 2000/10/09', 1), (' 2000/10/17', 0), (' 2000/10/31', 0), (' 2000/12/29', 1), (' 2001/03/07', 1), (' 2001/03/30', 1), (' 2001/04/27', 1), (' 2001/05/30', 1), (' 2001/06/29', 1), (' 2001/07/12', 0), (' 2001/07/23', 0), (' 2001/07/30', 0), (' 2001/08/13', 0), (' 2001/09/10', 0), (' 2001/10/09', 1), (' 2001/11/12', 1), (' 2001/11/22', 0), (' 2001/12/10', 0), (' 2002/01/07', 1), (' 2002/01/25', 1), (' 2002/02/08', 0), (' 2002/03/01', 0), (' 2002/03/07', 0), (' 2002/03/20', 0), (' 2002/04/11', 0), (' 2002/04/24', 0), (' 2002/04/30', 0), (' 2002/05/15', 0), (' 2002/05/22', 0), (' 2002/05/29', 0), (' 2002/06/10', 0), (' 2002/07/01', 0), (' 2002/07/18', 0), (' 2002/08/12', 1), (' 2002/09/02', 1), (' 2002/09/26', 1), (' 2002/10/16', 0), (' 2003/01/14', 1), (' 2003/02/11', 0), (' 2003/02/13', 0), (' 2003/03/04', 0), (' 2003/03/14', 0), (' 2003/03/20', 0), (' 2003/04/21', 1), (' 2003/05/19', 0), (' 2003/06/11', 1), (' 2003/06/30', 1), (' 2003/07/08', 0), (' 2003/08/04', 1), (' 2003/09/02', 1), (' 2003/11/06', 1), (' 2003/12/01', 1), (' 2003/12/12', 0), (' 2003/12/29', 0), (' 2004/01/07', 0), (' 2004/01/30', 0), (' 2004/02/06', 0), (' 2004/03/08', 1), (' 2004/03/09', 0), (' 2004/03/30', 1), (' 2004/04/09', 0), (' 2004/04/15', 0), (' 2004/06/02', 1), (' 2004/06/07', 0), (' 2004/06/10', 0), (' 2004/06/24', 0), (' 2004/06/29', 0), (' 2004/08/24', 1), (' 2004/09/10', 1), (' 2004/09/13', 0), (' 2004/10/11', 1), (' 2004/10/12', 0), (' 2004/10/25', 0), (' 2004/11/11', 0), (' 2004/11/29', 1), (' 2004/12/13', 0), (' 2004/12/29', 0), (' 2005/01/10', 0), (' 2005/02/16', 1), (' 2005/04/15', 1), (' 2005/04/20', 0), (' 2005/05/13', 0), (' 2005/05/23', 0), (' 2005/06/03', 0), (' 2005/06/27', 0), (' 2005/08/31', 1), (' 2005/09/12', 0), (' 2005/09/22', 0), (' 2005/10/11', 0), (' 2005/10/21', 0), (' 2005/11/02', 0), (' 2005/11/14', 0), (' 2005/12/09', 1), (' 2005/12/30', 1), (' 2006/01/13', 0), (' 2006/01/24', 0), (' 2006/01/27', 0), (' 2006/02/23', 0), (' 2006/03/03', 0), (' 2006/03/27', 1), (' 2006/04/27', 1), (' 2006/06/01', 1), (' 2006/06/14', 0), (' 2006/06/20', 0), (' 2006/07/03', 0), (' 2006/08/03', 1), (' 2006/08/23', 0), (' 2006/08/28', 0), (' 2006/08/31', 0), (' 2006/09/12', 0), (' 2006/09/13', 0), (' 2006/09/28', 1), (' 2006/12/01', 1), (' 2006/12/25', 0), (' 2007/01/10', 0), (' 2007/03/16', 1), (' 2007/03/27', 0), (' 2007/04/12', 0), (' 2007/05/09', 1), (' 2007/06/12', 1), (' 2007/06/18', 0), (' 2007/07/02', 0), (' 2007/07/09', 0), (' 2007/07/24', 0), (' 2007/11/20', 1), (' 2007/12/10', 1), (' 2008/01/10', 1), (' 2008/01/18', 0), (' 2008/01/30', 0), (' 2008/03/07', 1), (' 2008/04/10', 1), (' 2008/04/28', 0), (' 2008/05/30', 1), (' 2008/06/23', 1), (' 2008/07/08', 0), (' 2008/08/14', 1), (' 2008/08/20', 0), (' 2008/08/22', 0), (' 2008/08/26', 0), (' 2008/09/02', 0), (' 2008/09/23', 1), (' 2008/10/21', 1), (' 2008/12/17', 1), (' 2009/01/23', 1), (' 2009/02/17', 1), (' 2009/03/17', 0), (' 2009/03/30', 0), (' 2009/04/07', 0), (' 2009/04/20', 0), (' 2009/05/04', 0), (' 2009/06/10', 1), (' 2009/06/26', 0), (' 2009/07/01', 0), (' 2009/07/20', 1), (' 2009/07/31', 0), (' 2009/08/17', 0), (' 2009/08/31', 0), (' 2009/09/16', 0), (' 2009/09/28', 0), (' 2009/10/12', 0), (' 2009/10/28', 1), (' 2009/11/02', 0), (' 2009/12/10', 1), (' 2009/12/18', 0), (' 2009/12/29', 0), (' 2010/01/07', 0), (' 2010/02/22', 1), (' 2010/03/05', 0), (' 2010/03/12', 0), (' 2010/03/22', 0), (' 2010/04/01', 0), (' 2010/05/07', 1), (' 2010/05/28', 1), (' 2010/06/21', 1), (' 2010/07/08', 0), (' 2010/08/24', 1), (' 2010/08/30', 0), (' 2010/09/09', 0), (' 2010/09/15', 0), (' 2010/11/17', 1), (' 2010/11/24', 0), (' 2010/12/03', 0), (' 2010/12/15', 0), (' 2010/12/20', 0), (' 2011/01/07', 1), (' 2011/01/26', 0), (' 2011/02/21', 1), (' 2011/03/04', 0), (' 2011/03/18', 1), (' 2011/04/13', 1), (' 2011/04/25', 0), (' 2011/05/23', 1), (' 2011/06/16', 1), (' 2011/06/29', 1), (' 2011/07/04', 0), (' 2011/07/25', 1), (' 2011/08/05', 0), (' 2011/08/23', 0), (' 2011/09/13', 1), (' 2011/10/13', 1), (' 2011/10/17', 0), (' 2011/10/27', 0), (' 2011/11/08', 0), (' 2011/12/15', 1), (' 2012/01/13', 1), (' 2012/03/20', 1), (' 2012/04/18', 1), (' 2012/05/03', 0), (' 2012/06/06', 1), (' 2012/07/24', 1), (' 2012/08/03', 0), (' 2012/09/10', 1), (' 2012/09/17', 0), (' 2012/09/26', 0), (' 2012/10/24', 1), (' 2012/11/09', 0), (' 2012/11/23', 0), (' 2012/12/03', 0), (' 2012/12/07', 0), (' 2012/12/20', 0), (' 2013/01/11', 0), (' 2013/01/24', 0), (' 2013/02/18', 0), (' 2013/03/21', 1), (' 2013/04/03', 0), (' 2013/04/15', 0), (' 2013/04/19', 0), (' 2013/05/10', 1), (' 2013/05/20', 0), (' 2013/05/23', 0), (' 2013/06/13', 0), (' 2013/06/19', 0), (' 2013/07/10', 1), (' 2013/08/13', 1), (' 2013/09/17', 1), (' 2013/10/17', 1), (' 2013/10/22', 0), (' 2013/11/11', 1), (' 2013/12/05', 1), (' 2013/12/10', 0), (' 2013/12/27', 1), (' 2014/01/30', 1), (' 2014/02/19', 0), (' 2014/04/14', 1), (' 2014/05/07', 0), (' 2014/05/30', 1), (' 2014/06/23', 0), (' 2014/07/21', 1), (' 2014/08/20', 1), (' 2014/09/05', 0), (' 2014/09/12', 0), (' 2014/09/22', 0), (' 2014/09/29', 0), (' 2014/10/24', 1), (' 2014/10/31', 0), (' 2014/12/04', 0), (' 2014/12/16', 0), (' 2014/12/25', 0), (' 2015/01/13', 0), (' 2015/01/20', 0), (' 2015/03/17', 1), (' 2015/04/14', 1), (' 2015/04/20', 0), (' 2015/06/04', 1), (' 2015/06/23', 1), (' 2015/07/13', 1), (' 2015/07/29', 0), (' 2015/08/19', 1), (' 2015/11/25', 1), (' 2015/12/02', 0), (' 2015/12/09', 0), (' 2015/12/21', 0), (' 2016/01/19', 1), (' 2016/02/22', 1), (' 2016/03/03', 0), (' 2016/03/14', 0), (' 2016/03/23', 0), (' 2016/04/14', 1), (' 2016/04/18', 0), (' 2016/05/06', 1), (' 2016/05/11', 0), (' 2016/05/24', 0), (' 2016/06/17', 1), (' 2016/07/06', 0), (' 2016/07/15', 0), (' 2016/08/05', 1), (' 2016/08/25', 1), (' 2016/09/14', 1), (' 2016/09/28', 0), (' 2016/10/12', 0), (' 2016/10/21', 0), (' 2016/11/07', 0), (' 2016/11/14', 0), (' 2016/11/24', 0), (' 2016/11/25', 0), (' 2016/12/26', 1)]
    
    ta = [(' 2007/02/02', 1), (' 2007/02/09', 0), (' 2007/03/12', 1), (' 2007/03/15', 0), (' 2007/03/23', 0), (' 2007/04/02', 0), (' 2007/05/10', 1), (' 2007/05/15', 0), (' 2007/06/01', 0), (' 2007/06/19', 1), (' 2007/06/20', 0), (' 2007/07/12', 1), (' 2007/07/27', 0), (' 2007/09/03', 1), (' 2007/09/11', 0), (' 2007/09/25', 0), (' 2007/10/15', 0), (' 2007/11/06', 1), (' 2007/11/15', 0), (' 2007/12/14', 1), (' 2007/12/24', 0), (' 2008/01/22', 0), (' 2008/04/01', 1), (' 2008/04/24', 1), (' 2008/06/24', 1), (' 2008/07/09', 0), (' 2008/08/04', 1), (' 2008/08/20', 1), (' 2008/11/25', 1), (' 2008/12/29', 1), (' 2009/01/07', 0), (' 2009/02/16', 1), (' 2009/03/13', 0), (' 2009/04/13', 1), (' 2009/05/12', 1), (' 2009/06/02', 0), (' 2009/06/19', 1), (' 2009/08/19', 1), (' 2009/10/12', 1), (' 2009/11/27', 1), (' 2009/12/10', 0), (' 2009/12/15', 0), (' 2009/12/17', 0), (' 2009/12/29', 0), (' 2010/01/25', 1), (' 2010/02/10', 1), (' 2010/03/04', 1), (' 2010/03/15', 0), (' 2010/03/26', 0), (' 2010/04/19', 1), (' 2010/04/23', 0), (' 2010/05/31', 1), (' 2010/06/21', 1), (' 2010/06/29', 0), (' 2010/07/09', 0), (' 2010/07/23', 0), (' 2010/08/12', 1), (' 2010/08/25', 0), (' 2010/11/17', 1), (' 2010/12/09', 0), (' 2011/02/21', 1), (' 2011/02/22', 0), (' 2011/03/03', 0), (' 2011/03/18', 1), (' 2011/03/24', 0), (' 2011/05/23', 1), (' 2011/05/26', 0), (' 2011/06/02', 0), (' 2011/06/08', 0), (' 2011/07/07', 1), (' 2011/07/13', 0), (' 2011/08/05', 1), (' 2011/08/11', 0), (' 2011/09/06', 1), (' 2011/09/19', 0), (' 2011/10/28', 1), (' 2011/11/24', 1), (' 2011/12/01', 0), (' 2011/12/13', 0), (' 2012/02/15', 1), (' 2012/02/27', 0), (' 2012/03/12', 0), (' 2012/03/28', 1), (' 2012/04/16', 1), (' 2012/04/24', 0), (' 2012/06/18', 1), (' 2012/07/02', 0), (' 2012/07/23', 1), (' 2012/08/01', 0), (' 2012/08/06', 0), (' 2012/08/20', 0), (' 2012/08/27', 0), (' 2012/09/03', 0), (' 2012/09/10', 0), (' 2012/09/21', 1), (' 2012/09/27', 0), (' 2012/10/22', 0), (' 2012/11/20', 1), (' 2013/01/15', 1), (' 2013/02/21', 1), (' 2013/03/15', 1), (' 2013/04/09', 1), (' 2013/04/25', 0), (' 2013/05/06', 0), (' 2013/05/16', 0), (' 2013/06/21', 0), (' 2013/07/03', 0), (' 2013/07/11', 0), (' 2013/07/29', 0), (' 2013/08/20', 1), (' 2013/08/28', 0), (' 2013/08/29', 0), (' 2013/09/11', 0), (' 2013/11/08', 1), (' 2013/11/19', 0), (' 2013/12/03', 0), (' 2013/12/16', 0), (' 2013/12/27', 1), (' 2014/03/06', 1), (' 2014/03/07', 0), (' 2014/03/25', 1), (' 2014/04/09', 0), (' 2014/05/14', 1), (' 2014/07/02', 1), (' 2014/07/08', 0), (' 2014/07/17', 0), (' 2014/08/06', 0), (' 2014/08/13', 0), (' 2014/10/24', 1), (' 2014/11/12', 1), (' 2014/11/18', 0), (' 2014/11/28', 0), (' 2015/01/21', 1), (' 2015/01/26', 0), (' 2015/02/03', 0), (' 2015/03/06', 1), (' 2015/03/24', 0), (' 2015/04/08', 0), (' 2015/04/29', 1), (' 2015/05/14', 1), (' 2015/06/02', 1), (' 2015/06/12', 0), (' 2015/06/25', 0), (' 2015/07/22', 1), (' 2015/08/05', 0), (' 2015/08/21', 0), (' 2015/09/01', 0), (' 2015/09/09', 0), (' 2015/09/25', 0), (' 2015/10/08', 0), (' 2015/10/20', 0), (' 2015/10/27', 0), (' 2015/11/02', 0), (' 2015/11/11', 0), (' 2015/11/25', 0), (' 2015/12/21', 1), (' 2015/12/30', 0), (' 2016/01/07', 0), (' 2016/01/22', 1), (' 2016/01/29', 0), (' 2016/02/26', 1), (' 2016/03/16', 0), (' 2016/04/08', 1), (' 2016/05/05', 1), (' 2016/06/03', 1), (' 2016/06/17', 0), (' 2016/07/06', 0), (' 2016/08/04', 1), (' 2016/08/25', 1), (' 2016/09/02', 0), (' 2016/09/13', 0), (' 2016/10/11', 0), (' 2016/11/02', 1), (' 2016/12/26', 1)]
    
    dy = [(' 2006/03/17', 1), (' 2006/04/19', 1), (' 2006/04/24', 0), (' 2006/06/01', 1), (' 2006/06/06', 0), (' 2006/06/28', 1), (' 2006/08/14', 1), (' 2006/08/28', 0), (' 2006/09/01', 0), (' 2006/09/20', 0), (' 2006/10/10', 0), (' 2006/12/07', 1), (' 2006/12/19', 0), (' 2007/01/04', 0), (' 2007/01/15', 0), (' 2007/02/05', 1), (' 2007/02/13', 0), (' 2007/03/02', 0), (' 2007/03/13', 0), (' 2007/06/12', 1), (' 2007/06/29', 0), (' 2007/08/16', 1), (' 2007/09/10', 0), (' 2007/09/26', 1), (' 2007/11/20', 1), (' 2008/01/22', 1), (' 2008/01/25', 0), (' 2008/03/07', 1), (' 2008/04/10', 1), (' 2008/04/29', 0), (' 2008/05/12', 0), (' 2008/05/21', 0), (' 2008/05/30', 0), (' 2008/06/23', 1), (' 2008/07/07', 0), (' 2008/07/11', 0), (' 2008/08/20', 1), (' 2008/09/04', 0), (' 2008/10/31', 1), (' 2008/11/06', 0), (' 2008/11/12', 0), (' 2008/11/27', 0), (' 2008/12/22', 1), (' 2009/01/15', 1), (' 2009/02/05', 0), (' 2009/02/18', 0), (' 2009/03/10', 0), (' 2009/03/19', 0), (' 2009/04/27', 1), (' 2009/05/18', 1), (' 2009/06/12', 1), (' 2009/07/20', 1), (' 2009/07/31', 0), (' 2009/08/17', 0), (' 2009/08/31', 0), (' 2009/10/12', 1), (' 2009/10/29', 1), (' 2009/11/27', 1), (' 2009/12/14', 0), (' 2009/12/22', 0), (' 2010/01/07', 0), (' 2010/02/08', 1), (' 2010/03/05', 1), (' 2010/04/19', 1), (' 2010/05/05', 1), (' 2010/05/28', 1), (' 2010/06/04', 0), (' 2010/06/10', 0), (' 2010/06/17', 0), (' 2010/06/29', 0), (' 2010/07/12', 0), (' 2010/08/20', 1), (' 2010/08/30', 0), (' 2010/09/09', 0), (' 2010/11/16', 1), (' 2010/12/01', 0), (' 2011/01/18', 1), (' 2011/01/26', 0), (' 2011/02/17', 0), (' 2011/03/04', 0), (' 2011/03/21', 1), (' 2011/03/30', 0), (' 2011/04/14', 0), (' 2011/04/21', 0), (' 2011/04/29', 0), (' 2011/05/19', 0), (' 2011/06/10', 1), (' 2011/06/16', 0), (' 2011/07/07', 1), (' 2011/07/25', 1), (' 2011/07/29', 0), (' 2011/08/04', 0), (' 2011/08/18', 0), (' 2011/08/23', 0), (' 2011/09/14', 1), (' 2011/10/17', 1), (' 2011/10/27', 0), (' 2011/11/16', 0), (' 2011/12/05', 1), (' 2011/12/21', 1), (' 2012/01/13', 1), (' 2012/03/07', 1), (' 2012/04/18', 1), (' 2012/05/03', 0), (' 2012/06/11', 1), (' 2012/07/12', 1), (' 2012/07/24', 0), (' 2012/08/07', 0), (' 2012/09/12', 1), (' 2012/09/17', 0), (' 2012/10/18', 1), (' 2012/10/23', 0), (' 2012/11/26', 1), (' 2012/12/13', 1), (' 2012/12/14', 0), (' 2012/12/20', 0), (' 2012/12/31', 0), (' 2013/01/18', 0), (' 2013/02/18', 0), (' 2013/05/07', 1), (' 2013/06/04', 1), (' 2013/06/18', 0), (' 2013/06/21', 0), (' 2013/08/13', 1), (' 2013/08/22', 0), (' 2013/09/16', 1), (' 2013/10/11', 0), (' 2013/10/16', 0), (' 2013/10/28', 0), (' 2013/11/11', 0), (' 2013/12/05', 1), (' 2014/02/10', 1), (' 2014/03/17', 1), (' 2014/04/02', 0), (' 2014/04/11', 0), (' 2014/05/05', 0), (' 2014/06/20', 1), (' 2014/07/01', 0), (' 2014/07/29', 1), (' 2014/08/27', 1), (' 2014/09/16', 0), (' 2014/09/19', 0), (' 2014/10/14', 0), (' 2014/10/29', 1), (' 2014/11/18', 0), (' 2014/11/24', 0), (' 2014/12/29', 1), (' 2015/01/14', 0), (' 2015/01/16', 0), (' 2015/01/19', 0), (' 2015/02/06', 1), (' 2015/02/13', 0), (' 2015/03/09', 0), (' 2015/03/24', 0), (' 2015/04/15', 0), (' 2015/05/19', 1), (' 2015/06/01', 0), (' 2015/06/12', 0), (' 2015/06/26', 0), (' 2015/07/01', 0), (' 2015/08/10', 1), (' 2015/08/24', 0), (' 2015/09/11', 0), (' 2015/09/15', 0), (' 2015/09/25', 0), (' 2015/10/27', 1), (' 2015/11/04', 0), (' 2015/11/23', 1), (' 2015/12/10', 0), (' 2015/12/11', 0), (' 2015/12/22', 0), (' 2015/12/28', 0), (' 2016/01/11', 0), (' 2016/01/20', 0), (' 2016/01/28', 0), (' 2016/02/24', 1), (' 2016/03/02', 0), (' 2016/04/28', 1), (' 2016/05/06', 0), (' 2016/05/13', 0), (' 2016/05/31', 0), (' 2016/06/16', 0), (' 2016/06/28', 0), (' 2016/07/07', 0), (' 2016/07/21', 0), (' 2016/08/04', 0), (' 2016/08/25', 1), (' 2016/08/31', 0), (' 2016/09/06', 0), (' 2016/09/20', 0), (' 2016/09/28', 0), (' 2016/11/04', 1), (' 2016/11/14', 0), (' 2016/11/21', 0), (' 2016/12/20', 1)]

    yinkuilist = c+m+ta+dy+a
    sortedyk = sorted(yinkuilist, key=lambda yinkuilist: yinkuilist[0])
    print sortedyk

    cnts = []
    cnt = 0
    for n in sortedyk:
        if n[1] == 0:
            cnt += 1
        else:
            if cnt>0:
                cnts.append(cnt)
                cnt = 0
    mean = round(np.mean(cnts), 1)
    median = np.median(cnts)
    #print yinkuilist
    print cnts
    print '最大连亏次数:%s, 平均连亏:%s, 连亏中位数:%s' %  (max(cnts) , mean, median) # 

if __name__ == '__main__':
    k = Kxian('ta') # ta rb c m a ma jd dy 999999 sr au

    k.hl2(2,7,2)

    #fuhe_liankui()

    