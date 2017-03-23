# encoding: utf-8
import sys
sys.path.append("..")
import collections
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
        '''所有平仓点与开仓点的比值
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


    def ev_tupohl_highlow(self, n, m, y, zs=0.01):
        '''所有平仓点与开仓点的比值
        '''
        print 'ev_tupohl_highlow------%s------%s-----------'% (n, y)
        self.get_nhh(n)
        self.get_nll(n)
        self.get_nhhp(y)
        self.get_nllp(y)
        self.get_ma(m)
        if zs >= 1:
            self.get_zshh(zs)
            self.get_zsll(zs)
        df = deepcopy(self.df) 
        df['higher'] = df.h > df.nhh
        df['hh1'] = df.l.shift(1) > df.l.shift(2)
        df['hh2'] = df.h.shift(1) > df.h.shift(2)
        df['hh3'] = df.c.shift(1) > df.c.shift(2)
        df['hh4'] = df.c.shift(1) > df.o.shift(1)
        df['lower'] = df.l < df.nll
        df['ll1'] = df.h.shift(1) < df.h.shift(2)
        df['ll2'] = df.l.shift(1) < df.l.shift(2)
        df['bksk'] = np.where(df['higher'] & df.hh1 & df.hh2, 'bk', None)
        df['bksk'] = np.where(df['lower'] & df.ll1 & df.ll2, 'sk', df['bksk'])

        df['higherp'] = df.h >= df.nhhp
        df['lowerp'] = df.l <= df.nllp
        df['bpsp'] = np.where(df['higherp'], 'sp', None)
        df['bpsp'] = np.where(df['lowerp'], 'bp', df['bpsp'])
        df.to_csv('tmp.csv')
        self._runev(df, zs)


    def _runev(self, df, zs=0.01):
        '''zs为开仓止损的百分比'''
        bkpoints = dict() # 每次开多的价格等一些数值
        skpoints = dict() # 空
        bbzs = list() # 每次多单平仓价与开仓价的比值
        sbzs = list()
        allbz = collections.OrderedDict() # 多空平仓的比值放在一起
        has = 1
        bzlen = list()
        FEIYONG = 0.999 # 如果是分钟线的话，加上费用损失，预期马上变成负的，所以根据这个结果，做日内很难，而且日内涨跌有限，交易次数相对较多，不适合做趋势
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
                    bbzdict = dict()
                    for bkidx, bkpoint in bkpoints.items():
                        bz = max(pingcang/bkpoint, 1-zs)
                        bbz.append(bz)
                        bbzdict[bkidx] = bz
                    bbzs.extend(bbz)
                    allbz.update(bbzdict)
                    bkpoints = dict()
                elif bpsp == 'sp' and skpoints:
                    nhhp = df.loc[idx, 'nhhp']
                    o = df.loc[idx, 'o']
                    pingcang = o if o > nhhp else nhhp
                    #sbz = [x/d for x in skpoints.values()] # 为了看起来方便，用x/d
                    sbz = list()
                    sbzdict = dict()
                    for skidx, skpoint in skpoints.items():
                        #bz = x/d # 为了看起来方便，用x/d
                        bz = max(skpoint/pingcang, 1-zs)
                        sbz.append(bz)
                        sbzdict[skidx] = bz
                    sbzs.extend(sbz)
                    allbz.update(sbzdict)
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
                    bbzdict = dict()
                    for bkidx, x in bkpoints.items():
                        bz = max(pingcang/x[0]*FEIYONG, x[1]/x[0]*FEIYONG)
                        bbz.append(bz)
                        bbzdict[bkidx] = bz
                    bbzs.extend(bbz)
                    #bzlen.append(len(bbz))
                    allbz.update(bbzdict)
                    bkpoints = dict()
                    
                elif bpsp == 'sp' and skpoints:
                    nhhp = df.loc[idx, 'nhhp']
                    o = df.loc[idx, 'o']
                    pingcang = o if o > nhhp else nhhp
                    #sbz = [x/d for x in skpoints.values()] # 为了看起来方便，用x/d
                    sbz = list()
                    sbzdict = dict()
                    for skidx, x in skpoints.items():
                        #bz = x/d # 为了看起来方便，用x/d
                        bz = max(x[0]/pingcang*FEIYONG, x[0]/x[1]*FEIYONG)
                        sbz.append(bz)
                        sbzdict[skidx] = bz
                    sbzs.extend(sbz)
                    allbz.update(sbzdict)
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
        #for n in bbzs:
        for k,v in allbz.items():
            print k,v
            cummulti = v*cummulti
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

    


if __name__ == '__main__':
    g = GL('m') # ta rb c m a ma jd dy 999999

    g.ev_tupohl(3, 7, 1)

    

    