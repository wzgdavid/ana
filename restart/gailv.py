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
        print str(hgl)[:4], len1, '肯定打开仓止损的单数', len1*(1-hgl)#, hgl*len1

        #print df.lbz.mean() # 应该小于1
        llist = [x for x in sorted(df.lbz) if x>0]
        len2 = len(llist)
        llistsmallerthan1 = [x for x in llist if x<1]
        lgl = len(llistsmallerthan1)/float(len2) # 小于1 的概率(在m天里没止损de概率)
        print str(lgl)[:4], len2, '肯定打开仓止损的单数', len2*(1-lgl)#, hgl*len1

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
        self.get_nhhp(y)
        self.get_nllp(y)
        if zs >= 1:
            self.get_zshh(zs)
            self.get_zsll(zs)
        df = deepcopy(self.df) 
        df['higher'] = df.h > df.nhh
        df['lower'] = df.l < df.nll
        df['bksk'] = np.where(df['higher'], 'bk', None)
        df['bksk'] = np.where(df['lower'], 'sk', df['bksk'])

        df['higherp'] = df.h >= df.nhhp
        df['lowerp'] = df.l <= df.nllp
        df['bpsp'] = np.where(df['higherp'], 'sp', None)
        df['bpsp'] = np.where(df['lowerp'], 'bp', df['bpsp'])
        df.to_csv('tmp.csv')
        self._runev(df,zs)


    def ev_ma(self, n, zs=0.01):
        '''所有符合条件的，平仓点与开仓点的比值
        跑出来ma没用
        '''
        print 'ev_ma------%s-------------'% (n)
        self.get_ma(n)
        ma = 'ma%s' % n
        if zs >= 1:
            self.get_zshh(zs)
            self.get_zsll(zs)
        df = deepcopy(self.df) 
        # K线在ma之上开多
        #df['higher'] = df.l > df[ma]
        #df['lower'] = df.h < df[ma]
        # K线向上穿越ma开多 与上选其一跑
        df['higher'] = (df.h.shift(1) < df[ma]) &  (df.h > df[ma]) 
        df['lower'] = (df.l.shift(1) > df[ma]) &  (df.l < df[ma])
        df['bksk'] = np.where(df['higher'], 'bk', None)
        df['bksk'] = np.where(df['lower'], 'sk', df['bksk'])

        df['higherp'] = (df.h.shift(1) < df[ma]) &  (df.h > df[ma])    # 空单平仓
        df['lowerp'] = (df.l.shift(1) > df[ma]) &  (df.l < df[ma])
        df['bpsp'] = np.where(df['higherp'], 'sp', None)
        df['bpsp'] = np.where(df['lowerp'], 'bp', df['bpsp'])
        df.to_csv('tmp.csv')
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
                    bkpoints[idx] = df.loc[idx, 'o']
    
                if bksk == 'sk':
                    skpoints[idx] = df.loc[idx, 'o']
                    
                if bpsp == 'bp' and bkpoints:
                    pingcang = df.loc[idx, 'o']
                    
                    bbz = list()
                    for x in bkpoints.values():
                        bbz.append(max(pingcang/x, 1-zs))
                    bbzs.extend(bbz)
                    bsbzs.extend(bbz)
                    bkpoints = dict()
                elif bpsp == 'sp' and skpoints:
                    pingcang = df.loc[idx, 'o']
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
                    bkpoints[idx] = (df.loc[idx, 'o'], df.loc[idx, 'zsll']) # (开仓点，开仓止损点)
            
                if bksk == 'sk':
                    skpoints[idx] = (df.loc[idx, 'o'], df.loc[idx, 'zshh'])
                    
                if bpsp == 'bp' and bkpoints:
                    pingcang = df.loc[idx, 'o']
                    #bbz = [d/x for x in bkpoints.values()]
                    bbz = list()
                    for x in bkpoints.values():
                        bbz.append(max(pingcang/x[0]*FEIYONG, x[1]/x[0]*FEIYONG ))
                
                    bbzs.extend(bbz)
                    #bzlen.append(len(bbz))
                    bsbzs.extend(bbz)
                    bkpoints = dict()
                    
                elif bpsp == 'sp' and skpoints:
                    pingcang = df.loc[idx, 'o']
                    #sbz = [x/d for x in skpoints.values()] # 为了看起来方便，用x/d
                    sbz = list()
                    for x in skpoints.values():
                        #bz = x/d # 为了看起来方便，用x/d
                        sbz.append(max(x[0]/pingcang*FEIYONG, x[0]/x[1]*FEIYONG))
                    sbzs.extend(sbz)
                    bsbzs.extend(sbz)
                    skpoints = dict()
        br = reduce(lambda x,y:x*y,bbzs)
        print br , '--------br--------'
        #print str(sum(sbzs)/len(sbzs))[:6], len(sbzs)
        sr = reduce(lambda x,y:x*y,sbzs)
        print sr , '--------sr--------'
        #print sorted(sbzs)

        # 累计相乘，看曲线，看回撤
        every = list()
        cummulti=1
        
        #for n in bbzs:
        for n in bsbzs:
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
        FEIYONG = 0.999
        for i, bksk in enumerate(df.bksk):
            idx = df.index[i]
            bpsp = df.loc[idx, 'bpsp']
            #print idx, bpsp
            if zs < 1:
                if bksk == 'bk':
                    #bkpoints.append([idx, df.loc[idx, 'nhh']])
                    nhh = df.loc[idx, 'nhh']
                    o = df.loc[idx, 'o']
                    bkpoints[idx] = o if o > nhh else nhh
    
                if bksk == 'sk':
                    nll = df.loc[idx, 'nll']
                    o = df.loc[idx, 'o']
                    skpoints[idx] = o if o < nll else nll
                    
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
                    nhh = df.loc[idx, 'nhh']
                    o = df.loc[idx, 'o']
                    bkp = o if o > nhh else nhh
                    bkpoints[idx] = (bkp, df.loc[idx, 'zsll']) # (开仓点，开仓止损点)
                    #bkpoints[idx] = (nhh, df.loc[idx, 'zsll'])
                    
                if bksk == 'sk':
                    nll = df.loc[idx, 'nll']
                    o = df.loc[idx, 'o']
                    skp = o if o < nll else nll
                    skpoints[idx] = (skp, df.loc[idx, 'zshh'])
                    #skpoints[idx] = (nll, df.loc[idx, 'zshh'])
                    
                    
                if bpsp == 'bp' and bkpoints:
                    nllp = df.loc[idx, 'nllp']
                    o = df.loc[idx, 'o']
                    pingcang = o if o < nllp else nllp
                    #bbz = [d/x for x in bkpoints.values()]
                    bbz = list()
                    for x in bkpoints.values():
                        bbz.append(max(pingcang/x[0]*FEIYONG, x[1]/x[0]*FEIYONG ))
                
                    bbzs.extend(bbz)
                    #bzlen.append(len(bbz))
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
                        sbz.append(max(x[0]/pingcang*FEIYONG, x[0]/x[1]*FEIYONG))
                    sbzs.extend(sbz)
                    bsbzs.extend(sbz)
                    skpoints = dict()
        #print sum(bzlen)/float(len(bzlen)), '一次bp前的平均开仓次数' # 这个值大，说明真实情况下这样做，可能的持仓会大，有可能超出资金能力
        #print bzlen[len(bzlen)/2],    '一次bp前的中位数开仓次数'     # 与上同样的道理，中位数
        #print bbzs
        #print str(sum(bbzs)/len(bbzs))[:6], len(bbzs)#, sum(bbzs)*len(bbzs)
        #print sorted(bbzs)
        br = reduce(lambda x,y:x*y,bbzs)
        print br , '--------br--------'
        #print str(sum(sbzs)/len(sbzs))[:6], len(sbzs)
        sr = reduce(lambda x,y:x*y,sbzs)
        print sr , '--------sr--------'
        #print sorted(sbzs)

        # 累计相乘，看曲线，看回撤
        every = list()
        cummulti=1
        print sorted(bsbzs)
        #for n in bbzs:
        for n in bsbzs:
            cummulti = n*cummulti
            every.append(cummulti)
        #print every

        s = pd.Series(every)
        s.plot()
        plt.show()
        

    def ev_tupohl2(self, n, m, y=1, zs=0.02):
        '''所有平仓点与开仓点的比值
        以多为例，
        突破前n天的高点，以这个高点开多，
        后m天高点超过zy，止盈，跌破zs，止损
        还没做
        '''
        print 'ev_tupohl------%s------%s------%s-----'% (n, y, zs)
        self.get_nhh(n)
        self.get_nll(n)
        self.get_mhh(m)
        self.get_mll(m)
        self.get_nhhp(y)
        self.get_nllp(y)
        if zs >= 1:
            self.get_zshh(zs)
            self.get_zsll(zs)
        df = deepcopy(self.df) 
        df['higher'] = df.h > df.nhh
        df['lower'] = df.l < df.nll
        df['bksk'] = np.where(df['higher'], 'bk', None)
        df['bksk'] = np.where(df['lower'], 'sk', df['bksk'])

        df['higherp'] = df.h >= df.nhhp
        df['lowerp'] = df.l <= df.nllp
        df['bpsp'] = np.where(df['higherp'], 'bp', None)
        df['bpsp'] = np.where(df['lowerp'], 'sp', df['bpsp'])
        df.to_csv('tmp.csv')
        self._runev(df,zs)


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

    def close_ratio_foo(self, n, r=1.03):
        '''
        '''
        print 'close_ratio_foo------%s----%s---'% (n, r)
        
        df = deepcopy(self.df)

        df['ratio'] = np.where(1, 'b' , None)
        df['cshiftn'] = df.c.shift(-1*n)
        df.to_csv('tmp.csv')
        self._run_close_ratio(df,n,r)

    def close_ratio_ma(self,n,a=10,b=20,r=1.03):
        '''
        不考虑开仓和平仓中间价格的波动，既不考虑中间止损的情况
        较小的ma(a)大于较大的ma(b)时，
        后n天close与当天close的比值
        '''
        print 'close_ratio_ma------%s------%s------%s----%s----'% (n, a, b, r)
        self.get_ma(a, b)
        df = deepcopy(self.df)
        maa = 'ma%s' % a
        mab = 'ma%s' % b
        df['higher'] = df[maa] > df[mab]
        df['ratio'] = np.where(df['higher'], 'b' , None)
        df['lower'] = df[maa] < df[mab]
        df['ratio'] = np.where(df['lower'], 's' , df['ratio'])
        df['cshiftn'] = df.c.shift(-1*n)
        df.to_csv('tmp.csv')
        self._run_close_ratio(df,n,r)

    def close_ratio_ma2(self, n, a=10, r=1.03):
        '''
        k线在ma之上时，
        后n天close与当天close的比值
        '''
        print 'close_ratio_ma2------%s------%s-----%s---'% (n, a, r)
        self.get_ma(a)
        df = deepcopy(self.df)
        maa = 'ma%s' % a
        df['higher'] = df.l > df[maa]
        df['ratio'] = np.where(df['higher'], 'b' , None)
        df['lower'] = df.h < df[maa]
        df['ratio'] = np.where(df['lower'], 's' , df['ratio'])
        df['cshiftn'] = df.c.shift(-1*n)
        df.to_csv('tmp.csv')
        self._run_close_ratio(df, n, r)

    def close_ratio_ma3(self, n, a=10, r=1.03):
        '''
        ma向上时，
        后n天close与当天close的比值
        '''
        print 'close_ratio_ma3------%s------%s-----%s----'% (n, a, r)
        self.get_ma(a)
        df = deepcopy(self.df)
        maa = 'ma%s' % a
        df['higher'] = df[maa] > df[maa].shift(1)
        df['ratio'] = np.where(df['higher'], 'b' , None)
        df['lower'] = df[maa] < df[maa].shift(1)
        df['ratio'] = np.where(df['lower'], 's' , df['ratio'])
        df['cshiftn'] = df.c.shift(-1*n)
        df.to_csv('tmp.csv')
        self._run_close_ratio(df, n, r)

    def close_ratio_hl(self, n, a=3, r=1.03):
        '''
        突破前a天高点，
        后n天close与当天close的比值
        '''
        print 'close_ratio_hl------%s------%s-----%s----'% (n, a, r)
        self.get_nhh(a)
        self.get_nll(a)
        df = deepcopy(self.df)
        df['higher'] = df.h > df.nhh
        df['ratio'] = np.where(df['higher'], 'b' , None)
        df['lower'] = df.l < df.nll
        df['ratio'] = np.where(df['lower'], 's' , df['ratio'])
        df['cshiftn'] = df.c.shift(-1*n)
        df.to_csv('tmp.csv')
        self._run_close_ratio(df, n, r)

    def _run_close_ratio(self, df, n, r):
        dflen = len(df)
        bratios = []
        sratios = []
        for i, bksk in enumerate(df.ratio):
            if i >= dflen - n:
                continue
            idx = df.index[i]
            ratio = df.loc[idx, 'ratio']
            c = float(df.loc[idx, 'c'])
            cshiftn = df.loc[idx, 'cshiftn']
            if ratio == 'b':
                bratios.append(cshiftn / c)
            elif ratio == 's':
                sratios.append(c / cshiftn )
            else : pass

        
        #print sorted(bratios)
        bigger = [x for x in bratios if x>r]
        print str(len(bigger) / float(len(bratios)))[:4]
        
        #print sorted(sratios)
        bigger2 = [x for x in sratios if x>r]
        print str(len(bigger2) / float(len(sratios)))[:4]

        print '全部   累乘', reduce(lambda x,y:x*y,bratios)
        print '大于r的累乘', reduce(lambda x,y:x*y,bigger)
        print '全部   累乘', reduce(lambda x,y:x*y,sratios)
        print '大于r的累乘', reduce(lambda x,y:x*y,bigger2)

if __name__ == '__main__':
    g = GL('m') # ta rb c m a ma jd dy 999999
    #g.ev_tupohl(3, 7, 0.03)
    #g.ev_ma(20,0.03)
    #g.ev_tupohl(2, 5, 1)
    #g.ev_tupohl(3, 4, 1)
    #g.ev_tupohl_highlow(3, 7, 1)
    #g.tupohl(3, 7,1)
    #g.ev_tupohl(5, 11)
    #g.ev_tupohl(2, 4)
    #g.tupohl(7,10,1)
    #g.handl(5)
    #g.close_ratio_ma(50, 10, 40)
    
    g.close_ratio_ma(60, 10, 20)
    g.close_ratio_ma(60, 20, 40)
    g.close_ratio_ma(60, 30, 60)
    g.close_ratio_ma(60, 40, 80)
    g.close_ratio_ma(60, 50, 100)
    g.close_ratio_ma(60, 60, 120)
    
    #g.close_ratio_hl(55, 10, 1.03)
    #g.close_ratio_hl(65, 10, 1.03)
    #g.close_ratio_hl(75, 10, 1.03)
    #g.close_ratio_hl(85, 10, 1.03)
    #g.close_ratio_hl(95, 10, 1.03)
    #g.close_ratio_hl(100,10, 1.03)
    #g.close_ratio_foo(30)
    
    #g.close_ratio_ma3(30, 10)
    #g.close_ratio_ma3(30, 20)
    #g.close_ratio_ma3(30, 30)
    #g.close_ratio_ma3(30, 40)

    