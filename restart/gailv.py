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
        self.get_sdjj()

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
        # kong tou  
        df['lower'] = df.l < df.nll
        df['ll'] = df.h.shift(1) < df.h.shift(2)
        df['lbz'] = np.where(df['lower'] & df.ll, df.mhh/df.zshh , None)

        self._to_result(df)

    def tupohl_close(self, n, m, zs=2):
        print 'tupohl_close------%s------%s-----------'% (n, m)
        df = self._init_data(n, m, zs)
        # duo tou
        df['higher'] = df.h > df.nhh
        df['hh'] = df.c.shift(1) > df.c.shift(2)
        df['hbz'] = np.where(df['higher'] & df.hh, df.mll/df.zsll , None)
        # kong tou  
        df['lower'] = df.l < df.nll
        df['ll'] = df.c.shift(1) < df.c.shift(2)
        df['lbz'] = np.where(df['lower'] & df.ll, df.mhh/df.zshh , None)
        self._to_result(df)

    def tupohl_high(self, n, m, zs=2):
        print 'tupohl_high------%s------%s-----------'% (n, m)
        df = self._init_data(n, m, zs)

        # duo tou
        df['higher'] = df.h > df.nhh
        df['hh'] = df.h.shift(1) > df.h.shift(2)
        df['hbz'] = np.where(df['higher'] & df.hh, df.mll/df.zsll , None)
        # kong tou  
        df['lower'] = df.l < df.nll
        df['ll'] = df.l.shift(1) < df.l.shift(2)
        df['lbz'] = np.where(df['lower'] & df.ll, df.mhh/df.zshh , None)
        self._to_result(df)

    def tupohl_lowclose(self, n, m, zs=2):
        print 'tupohl_lowclose------%s------%s-----------'% (n, m)
        df = self._init_data(n, m, zs)
        # duo tou
        df['higher'] = df.h > df.nhh
        df['hh1'] = df.l.shift(1) > df.l.shift(2)
        df['hh2'] = df.c.shift(1) > df.c.shift(2)
        df['hbz'] = np.where(df['higher'] & df.hh1 & df.hh2, df.mll/df.zsll , None)
        # kong tou  
        df['lower'] = df.l < df.nll
        df['ll1'] = df.h.shift(1) < df.h.shift(2)
        df['ll2'] = df.c.shift(1) < df.c.shift(2)
        df['lbz'] = np.where(df['lower'] & df.ll1 & df.ll2, df.mhh/df.zshh , None)
        self._to_result(df)

    def tupohl_highclose(self, n, m, zs=2):
        print 'tupohl_highclose------%s------%s-----------'% (n, m)
        df = self._init_data(n, m, zs)
        # duo tou
        df['higher'] = df.h > df.nhh
        df['hh1'] = df.h.shift(1) > df.h.shift(2)
        df['hh2'] = df.c.shift(1) > df.c.shift(2)
        df['hbz'] = np.where(df['higher'] & df.hh1 & df.hh2, df.mll/df.zsll , None)
        # kong tou  
        df['lower'] = df.l < df.nll
        df['ll1'] = df.l.shift(1) < df.l.shift(2)
        df['ll2'] = df.c.shift(1) < df.c.shift(2)
        df['lbz'] = np.where(df['lower'] & df.ll1 & df.ll2, df.mhh/df.zshh , None)
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
        # kong tou  
        df['lower'] = df.l < df.nll
        df['ll1'] = df.h.shift(1) < df.h.shift(2)
        df['ll2'] = df.l.shift(1) < df.l.shift(2)
        df['lbz'] = np.where(df['lower'] & df.ll1 & df.ll2, df.mhh/df.zshh , None)
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
        # kong tou  
        df['lower'] = df.l < df.nll
        df['ll1'] = df.h.shift(1) < df.h.shift(2)
        df['ll2'] = df.l.shift(1) < df.l.shift(2)
        df['ll3'] = df.c.shift(1) < df.c.shift(2)
        df['lbz'] = np.where(df['lower'] & df.ll1 & df.ll2 & df.ll3, df.mhh/df.zshh , None)
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
        df['lbz'] = np.where(df['lower'] & df.ll1, df.mhh/df.zshh , None)
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
        print round(hgl, 3), len1, len1*(1-hgl)#'没打开仓止损的概率'，' 总单数'' 肯定打开仓止损的单数'

        #print df.lbz.mean() # 应该小于1
        llist = [x for x in sorted(df.lbz) if x>0]
        len2 = len(llist)
        llistsmallerthan1 = [x for x in llist if x<1]
        lgl = len(llistsmallerthan1)/float(len2) # 小于1 的概率(在m天里没止损de概率)
        print round(lgl, 3), len2,  len2*(1-lgl)#, hgl*len1

        df.to_csv('tmp.csv')

    '''
    ############################################################################################
    ############################################################################################
    ########################分割线要明显########################################################
    ############################################################################################
    ############################################################################################
    '''

    def ev_tupohl(self, n, y, zs=0.01):
        '''所有符合条件的，平仓点与开仓点的比值
        以多为例，
        突破前n天的高点，以这个高点开多，
        开仓止损zs，小数的话，为开仓点的百分比，整数的话，为开仓前zs天的低点
        移动止损为前y天的低点
        信号开仓
        开仓止损，移动止损（被动止盈）

        不能只看跑出来的结果就，因为程序没有限制，而真实情况持仓总有个限制，不可能无限大的持仓
        '''
        print 'ev_tupohl------%s------%s------%s-----'% (n, y, zs)
        self.get_nhh(n)
        self.get_nll(n)
        self.get_nch(n)
        self.get_ncl(n)
        self.get_nhhp(y)
        self.get_nllp(y)
        ma = 20
        ma_name = 'ma'+str(ma)
        self.get_ma(ma)
        if zs >= 1:
            self.get_zshh(zs)
            self.get_zsll(zs)
        df = deepcopy(self.df) 
        
        option = {
            'tupo_high': df.h > df.nhh,
            'tuo_low': df.l < df.nll,
            'higher_than_ma': df.l.shift(1) > df[ma_name].shift(1),
            'lower_than_ma': df.h.shift(1) < df[ma_name].shift(1),
            'maup': df[ma_name].shift(1) > df[ma_name].shift(2),
            'madown': df[ma_name].shift(1) < df[ma_name].shift(2),
            'hl_bothhigh': (df.h.shift(1) > df.h.shift(2)) & (df.h.shift(1) > df.h.shift(2)),
            'hl_bothlow': (df.l.shift(1) < df.l.shift(2)) & (df.l.shift(1) < df.l.shift(2)),
            'tupo_high_c': df.h > df.nch, # 突破前几天收盘价的高点
            'tupo_low_c': df.l < df.ncl,

            'close_higher_than_ma': df.c.shift(1) > df[ma_name].shift(1),
            'close_lower_than_ma': df.c.shift(1) < df[ma_name].shift(1),
                  }

        df['higher'] = option['tupo_high'] & option['higher_than_ma'] #& option['maup']
        df['lower'] = option['tuo_low']    & option['lower_than_ma']  #& option['madown']
        df['higher'] = option['tupo_high_c'] & option['close_higher_than_ma'] #& option['higher_than_ma']
        df['lower'] = option['tupo_low_c']    & option['close_lower_than_ma']  #& option['lower_than_ma']

        df['bksk'] = np.where(df['higher'], 'bk', None)
        df['bksk'] = np.where(df['lower'], 'sk', df['bksk'])

        df['higherp'] = df.h >= df.nhhp
        df['lowerp'] = df.l <= df.nllp
        df['bpsp'] = np.where(df['higherp'], 'sp', None)
        df['bpsp'] = np.where(df['lowerp'], 'bp', df['bpsp'])
        df.to_csv('tmp.csv')
        return self._runev(df,zs)

    def _plot_cummulti(self, lst):
        # 累计相乘，看曲线，看回撤
        every = list()
        cummulti=1
        
        #for n in bbzs:
        for n in lst:
            cummulti = n*cummulti
            every.append(cummulti)
        #print every

        s = pd.Series(every)
        s.plot()
        plt.show()  

    def _runev(self, df, zs=0.01):
        '''zs为开仓止损的百分比'''
        bkpoints = dict() # 每次开多的价格等一些数值
        skpoints = dict() # 空
        bbzs = list() # 每次多单平仓价与开仓价的比值
        sbzs = list()
        bsbzs = list()
        has = 1
        bzlen = list()
        FEIYONG = 1
        for i, bksk in enumerate(df.bksk):
            idx = df.index[i]
            bpsp = df.loc[idx, 'bpsp']
            #print idx, bpsp
            if zs < 1:
                if bksk == 'bk':
                    bkpoints[idx] = self._get_hl_bkpoint(df, idx)
                    bkpoints[idx] = self._get_chl_bkpoint(df, idx)
                if bksk == 'sk':
                    skpoints[idx] = self._get_hl_skpoint(df, idx)
                    skpoints[idx] = self._get_chl_skpoint(df, idx)
                    
                if bpsp == 'bp' and bkpoints:
                    nllp = df.loc[idx, 'nllp']
                    o = df.loc[idx, 'o']
                    pingcang = o if o < nllp else nllp
                    #bbz = [d/x for x in bkpoints.values()]
                    bbz = list()
                    for x in bkpoints.values():
                        bbz.append(max(pingcang/x, 1-zs))
                    bbzs.extend(bbz)
                    bsbzs.extend(bbz)
                    bkpoints = dict()
                elif bpsp == 'sp' and skpoints:
                    nhhp = df.loc[idx, 'nhhp']
                    o = df.loc[idx, 'o']
                    pingcang = o if o > nhhp else nhhp
                    #sbz = [x/d for x in skpoints.values()] # 为了看起来方便，用x/d
                    sbz = list()
                    for x in skpoints.values():
                        #bz = x/d # 为了看起来方便，用x/d
                        sbz.append(max(x/pingcang, 1-zs))
                    sbzs.extend(sbz)
                    bsbzs.extend(sbz)
                    skpoints = dict()
            elif zs>=1 and type(zs)==int:
                if bksk == 'bk':
                    bkp = self._get_hl_bkpoint(df, idx)
                    bkp = self._get_chl_bkpoint(df, idx)
                    bkpoints[idx] = (bkp, df.loc[idx, 'zsll']) # (开仓点，开仓止损点)
                    
                if bksk == 'sk':
                    skp = self._get_hl_skpoint(df, idx)
                    skp = self._get_chl_skpoint(df, idx)
                    skpoints[idx] = (skp, df.loc[idx, 'zshh'])
                    
                if bpsp == 'bp' and bkpoints:
                    nllp = df.loc[idx, 'nllp']
                    o = df.loc[idx, 'o']
                    pingcang = o if o < nllp else nllp
                    bbz = list()
                    for x in bkpoints.values():
                        bbz.append(max(pingcang/x[0]*FEIYONG, x[1]/x[0]*FEIYONG ))
                    bbzs.extend(bbz)
                    bsbzs.extend(bbz)
                    bkpoints = dict()
                    
                elif bpsp == 'sp' and skpoints:
                    nhhp = df.loc[idx, 'nhhp']
                    o = df.loc[idx, 'o']
                    pingcang = o if o > nhhp else nhhp
                    sbz = list()
                    for x in skpoints.values():
                        #bz = x/d # 为了看起来方便，用x/d
                        sbz.append(max(x[0]/pingcang*FEIYONG, x[0]/x[1]*FEIYONG))
                    sbzs.extend(sbz)
                    bsbzs.extend(sbz)
                    skpoints = dict()
        return self._tongjilist(bsbzs)
        
    '''
    ############################################################################################
    ############################################################################################
    ########################分割线要明显########################################################
    ############################################################################################
    ############################################################################################
    '''

    def handl(self, n):
        '''某天k线包含前n天'''
        self.get_nhh(n)
        self.get_nll(n)
        df = deepcopy(self.df)
        df['higher'] = df.h > df.nhh
        df['lower'] = df.l < df.nll
        df['rr'] = np.where(df['higher'] & df.lower, 1 , 0)
        df['rrcumsum'] = df.rr.cumsum()

        df.to_csv('tmp.csv')


    '''
    ############################################################################################
    ############################################################################################
    ########################分割线要明显########################################################
    ############################################################################################
    ############################################################################################
    '''

    def zdzy_hl(self, n, zy=0.04, zs=0.02):
        '''主动止损主动止盈'''
        print 'zdzy_hl------%s------%s------%s-----'% (n, zy, zs)
        self.get_nhh(n)
        self.get_nll(n)
        df = deepcopy(self.df) 
        df['higher'] = df.h > df.nhh
        df['lower'] = df.l < df.nll
        df['bksk'] = np.where(df['higher'], 'bk', None)
        df['bksk'] = np.where(df['lower'], 'sk', df['bksk'])
        df.to_csv('tmp.csv')
        self._run_zdzy(df, zy, zs)
  
    def zdzy_maupdown(self, n, m, zy=0.04, zs=0.02):
        '''主动止损主动止盈'''
        print 'zdzy_maupdown------%s------%s------%s-----'% (n, zy, zs)
        self.get_nhh(n)
        self.get_nll(n)
        self.get_ma(m)
        df = deepcopy(self.df)
        ma = 'ma%s' % m
        df['higher'] = (df[ma] > df[ma].shift(1)) & (df.h > df.nhh)
        df['lower'] = (df[ma] < df[ma].shift(1)) & (df.l < df.nll)
        df['bksk'] = np.where(df['higher'], 'bk', None)
        df['bksk'] = np.where(df['lower'], 'sk', df['bksk'])
        df.to_csv('tmp.csv')
        self._run_zdzy(df, zy, zs)

    def zdzy_highlow(self, n, zy=0.04, zs=0.02):
        '''主动止损主动止盈'''
        print 'zdzy_highlow------%s------%s------%s-----'% (n, zy, zs)
        self.get_nhh(n)
        self.get_nll(n)
        df = deepcopy(self.df)
        df['higher'] = (df.l.shift(1) > df.l.shift(2)) & (df.h > df.nhh)
        df['lower'] = (df.h.shift(1) < df.h.shift(2)) & (df.l < df.nll)
        df['bksk'] = np.where(df['higher'], 'bk', None)
        df['bksk'] = np.where(df['lower'], 'sk', df['bksk'])
        df.to_csv('tmp.csv')
        self._run_zdzy(df, zy, zs)

    def _get_hl_bkpoint(self, df, idx):
        ''''''
        nhh = df.loc[idx, 'nhh']
        o = df.loc[idx, 'o']
        return o if o > nhh else nhh

    def _get_chl_bkpoint(self, df, idx):
        ''''''
        nch = df.loc[idx, 'nch']
        o = df.loc[idx, 'o']
        return o if o > nch else nch

    def _get_hl_skpoint(self, df, idx):
        nll = df.loc[idx, 'nll']
        o = df.loc[idx, 'o']
        return o if o < nll else nll

    def _get_chl_skpoint(self, df, idx):
        ncl = df.loc[idx, 'ncl']
        o = df.loc[idx, 'o']
        return o if o < ncl else ncl

    def _tongjilist(self, lst):
        #print sorted([round(x,3) for x in lst])
        m = np.mean(lst)
        s = np.std(lst)
        y = s/m
        print '均值', round(m, 4)
        print '标准差', round(s, 4)
        print '标准差/均值', round(y, 4)
        #self._plot_cummulti(lst)
        return m, s, y
        

    def _run_zdzy(self, df, zy, zs):
        move_len = 99
        bzlist = []
        for i, bksk in enumerate(df.bksk):

            if i+move_len > len(df.bksk):
                break
            r = range(i+1, i+move_len)
            idx = df.index[i]
            if bksk == 'bk':
                bkpoint = self._get_hl_bkpoint(df, idx)
                bkpoint = df.loc[idx, 'o']
                zypoint = bkpoint * (1+zy)
                zspoint = bkpoint * (1-zs)
                for j in r:
                    
                    move_low = df.loc[df.index[j], 'l']
                    move_high = df.loc[df.index[j], 'h']
                    #print i,j, bkpoint, zypoint, zspoint, move_low, move_high
                    if move_low <= zspoint:
                        bzlist.append(zspoint/bkpoint)
                        break
                    if move_high >= zypoint:
                        bzlist.append(zypoint/bkpoint)
                        break
            if bksk == 'sk':
                skpoint = self._get_hl_skpoint(df, idx)
                skpoint = df.loc[idx, 'o']
                zypoint = skpoint * (1-zy)
                zspoint = skpoint * (1+zs)
                for j in r:
                    
                    move_low = df.loc[df.index[j], 'l']
                    move_high = df.loc[df.index[j], 'h']
                    #print i,j, bkpoint, zypoint, zspoint, move_low, move_high
                    if move_high >= zspoint:
                        bzlist.append(skpoint/zspoint)
                        break
                    if move_low <= zypoint:
                        bzlist.append(skpoint/zypoint)
                        break
        return self._tongjilist(bzlist)

    '''
    ############################################################################################
    ############################################################################################
    ########################分割线要明显########################################################
    ############################################################################################
    ############################################################################################
    '''

    def zhisungailv(self):
        '''今天l大于前一天，后一天l大于今天l的概率'''
        self.get_nhh(2)
        self.get_nll(2)
        self.get_nch(2)
        self.get_ncl(2)
        self.get_mhh(7)
        self.get_mll(7)
        ma = 20
        ma_name = 'ma'+str(ma)
        self.get_ma(ma)
        df = deepcopy(self.df)
        option = {
            'tupo_high': df.h > df.nhh,
            'tupo_low': df.l < df.nll,
            


            'higher_than_ma': df.l > df[ma_name],
            'lower_than_ma': df.h < df[ma_name],
            'close_higher_than_ma': df.c > df[ma_name],
            'close_lower_than_ma': df.c < df[ma_name],
            'maup': df[ma_name] > df[ma_name].shift(1),
            'madown': df[ma_name] < df[ma_name].shift(1),
            '2liangyang': (df.c > df.o) & (df.c.shift(1) > df.o.shift(1)),
            '2lianyin': (df.c < df.o) & (df.c.shift(1) < df.o.shift(1)),
            '3liangyang': (df.c > df.o) & (df.c.shift(1) > df.o.shift(1)) & (df.c.shift(2) > df.o.shift(2)),
            '3lianyin': (df.c < df.o) & (df.c.shift(1) < df.o.shift(1)) & (df.c.shift(2) < df.o.shift(2)),
                  }
        df['higher'] = (df.h > df.nhh)
        #df['higher'] =   option['close_higher_than_ma']
        df['higher'] = (df.c > df.nch) & option['2liangyang'] #& option['close_higher_than_ma']
        df['higher1'] = np.where(df.higher, 1, None)
        df['higher2'] = np.where(df.higher & (df.mll.shift(-1) > df.l), 1, None)
        
        print 'duo', round(df.higher2.sum() / float(df.higher1.sum()), 2)

        df['lower'] = (df.l < df.nll)
        #df['lower'] =  option['close_lower_than_ma']
        df['lower'] =  (df.c < df.ncl) & option['2lianyin'] #& option['close_lower_than_ma']
        df['lower1'] = np.where(df.lower, 1, None)
        df['lower2'] = np.where(df.lower & (df.mhh.shift(-1) < df.h), 1, None)
        
        print 'kong', round(df.lower2.sum() / float(df.lower1.sum()), 2)
        print '次数', df.lower2.sum() + df.higher2.sum()

        df.to_csv('tmp.csv')

if __name__ == '__main__':
    
    #test()
    #run_ev_tupohl('ta')
    g = GL('ma') # ta rb c m a ma jd dy sr 999999
    #g.tupohl(3, 7, 1)
    #g.ev_ma(20,0.03)
    #g.ev_tupohl(2, 7, 1)
    #g.ev_tupohl(3, 11, 1) 
    #g.ev_tupohl(3, 17, 1)

    g.zhisungailv()
   
    

    