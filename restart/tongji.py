# encoding: utf-8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from general_index import General, GeneralIndex, rangerun, rangerun3
from copy import deepcopy

class Tongji(GeneralIndex):
    def __init__(self, daima):
        super(Tongji, self).__init__(daima)
        
        #self.get_sdjj()
        self.get_atr(50)

    def ratio(self, x):
        '''
        后x天平均价格与当天平均价格的比值
        '''
        title = 'ratio------%s-----'% (x)
        print title
        df = deepcopy(self.df)
        df['shiftx'] = df.sdjj.shift(-1*x)
        df['ratio'] = df.shiftx / df.sdjj
        self._to_result(df, title)

    def ratio_high(self, x):
        '''
        后x天最高价与当天价格的比值
        '''
        title = 'ratio_high------%s-----'% (x)
        print title
        self.get_mhh(x)
        df = deepcopy(self.df)
        df['ratio'] = df.mhh / df.sdjj
        self._to_result(df, title)

    def ratio_high_bl(self, x, bl):
        '''
        后x天最高价到一定比例(bl)后平仓， 与持仓到期的比值
        '''
        print 'ratio_high_bl------%s-----'% (x)
        self.get_mhh(x)
        df = deepcopy(self.df)
        df['ratioh'] = df.mhh / df.sdjj
        #df['daobili'] = np.where(df['ratioh'] > bl, df.ratioh ,None)
        df['daobili'] = np.where(df['ratioh'] > bl, 1 ,None)
        df['shiftx'] = df.sdjj.shift(-1*x)
        df['ratiox'] = df.shiftx / df.sdjj
        df['daobili_ratioh'] = np.where(df['daobili'], df.ratioh ,None)
        df['daobili_ratiox'] = np.where(df['daobili'], df.ratiox ,None)
        df['bl'] = np.where(df['daobili'], bl ,None)
        df['bz'] = df.bl / df.daobili_ratiox
        print df.daobili_ratiox.mean() # 这个比例和参数bl比较，bl大，则价格达到bl后平仓有利，否则，持仓
        
        df.to_csv('tmp.csv')

    def ratio_low(self, x):
        '''
        后x天最低价与当天平均价格的比值
        '''
        title = 'ratio_low------%s-----'% (x)
        print title
        self.get_mll(x)
        df = deepcopy(self.df)
        df['ratio'] = df.mll/df.sdjj 
        self._to_result(df,title)

    def ratio_low_tupohigh(self, x, n):
        '''
        突破高点后x天最低价与当天平均价格的比值
        '''
        title = 'ratio_low_tupohigh------%s----%s----'% (x, n)
        print title
        self.get_nhh(n)
        
        self.get_mll(x)
        df = deepcopy(self.df)
        df['higher'] = df.h > df.nhh
        df['ratio'] = np.where(df['higher'], df.mll/df.sdjj  ,None)
        self._to_result(df,title)

    def ratio_high_tupohigh(self, x, n):
        '''
        突破高点后x天最高价与当天价格的比值
        '''
        title = 'ratio_high_tupohigh------%s----%s----'% (x, n)
        print title
        self.get_nhh(n)
        
        self.get_mhh(x)
        df = deepcopy(self.df)
        df['higher'] = df.h > df.nhh
        df['ratio'] = np.where(df['higher'], df.mhh/df.sdjj  ,None)
        self._to_result(df,title)

    def close_ratio_tupoh(self, x, n):
        print 'close_ratio_tupoh------%s-----%s---'% (x, n)
        self.get_nhh(n)
        df = deepcopy(self.df)
        df['shiftx'] = df.sdjj.shift(-1*x)
        df['higher'] = df.h > df.nhh
        df['ratio'] = np.where(df['higher'], df.shiftx / df.sdjj, None)
        self._to_result(df)

    def close_ratio_tupol(self, x, n):
        title = 'close_ratio_tupol------%s-----%s---'% (x, n)
        print title
        self.get_nll(n)
        df = deepcopy(self.df)
        df['shiftx'] = df.sdjj.shift(-1*x)
        df['lower'] = df.l < df.nll
        df['ratio'] = np.where(df['lower'], df.sdjj / df.shiftx, None)
        self._to_result(df)
    
    def _to_result(self, df, title):
        mean = df.ratio.mean()
        median =  df.ratio.median()
        std = df.ratio.std()
        print '均值：%s，中位数：%s' % (round(mean, 5), round(median, 5))
        df.to_csv('tmp.csv')
        self._plot_histogram(mean, std, title)

    def _plot_histogram(self, mean, std, title):
        import matplotlib.mlab as mlab
        np.random.seed(0)
        
        # example data
        mu = mean  # mean of distribution
        sigma = std  # standard deviation of distribution
        x = mu + sigma * np.random.randn(99999)
        #big = [a for a in x if a > 1.0879]
        #print len(big)/float(len(x))
        num_bins = 99
        
        fig, ax = plt.subplots()
        # the histogram of the data
        n, bins, patches = ax.hist(x, num_bins, normed=1)
        # add a 'best fit' line
        y = mlab.normpdf(bins, mu, sigma)
        ax.plot(bins, y, '--')
        ax.set_xlabel('Smarts')
        ax.set_ylabel('Probability density')
        #ax.set_title(r'Histogram of IQ: $\mu=100$, $\sigma=15$')
        ax.set_title(title)
        # Tweak spacing to prevent clipping of ylabel
        fig.tight_layout()
        plt.show()

    '''
    ############################################################################################
    ############################################################################################
    ########################分割线要明显########################################################
    ############################################################################################
    ############################################################################################
    '''



    def close_ratio_foo(self, qlj, xqj, xj, n):
        '''
        '''
        print '权利金：%s， 行权价：%s， 现价：%s， n天：%s'% (qlj, xqj, xj, n)
        
        df = deepcopy(self.df)

        df['ratio'] = np.where(1, 'b' , None)
        df['cshiftn'] = df.c.shift(-1*n)
        df.to_csv('tmp.csv')
        self._run_close_ratio2(df, qlj, xqj, xj, n)

    def close_ratio_foo_s(self, qlj, xqj, xj, n):
        '''
        '''
        print 'close_ratio_foo_s------%s----%s---%s-----%s'% (qlj, xqj, xj, n)
        
        df = deepcopy(self.df)

        df['ratio'] = np.where(1, 's' , None)
        df['cshiftn'] = df.c.shift(-1*n)
        df.to_csv('tmp.csv')
        self._run_close_ratio2(df, qlj, xqj, xj, n)

    def close_ratio_ma(self,qlj, xqj, xj, n ,a=10, b=20):
        print 'close_ratio_ma------%s------%s------%s----%s---a:%s---b:%s----'% (qlj, xqj, xj, n, a, b)
        self.get_ma(a, b)
        df = deepcopy(self.df)
        maa = 'ma%s' % a
        mab = 'ma%s' % b
        df['higher'] = df[maa] > df[mab]
        df['ratio'] = np.where(df['higher'], 'b' , None)
        df['cshiftn'] = df.c.shift(-1*n)
        df.to_csv('tmp.csv')
        self._run_close_ratio(df, qlj, xqj, xj, n)

    def close_ratio_ma_s(self,qlj, xqj, xj, n ,a=10, b=20):
        print 'close_ratio_ma_s------%s------%s------%s----%s---a:%s---b:%s----'% (qlj, xqj, xj, n, a, b)
        self.get_ma(a, b)
        df = deepcopy(self.df)
        maa = 'ma%s' % a
        mab = 'ma%s' % b
        df['lower'] = df[maa] < df[mab]
        df['ratio'] = np.where(df['lower'], 's' , None)
        df['cshiftn'] = df.c.shift(-1*n)
        df.to_csv('tmp.csv')
        self._run_close_ratio(df, qlj, xqj, xj, n)

    def close_ratio_ma2(self, qlj, xqj, xj, n, a=10):
        '''
        k线在ma之上时，
        后n天close与当天close的比值
        r 行权价与现价的比值
        xqj 行权价
        qlj 权利金
        xj 现价
        权利金当亏损算， 实际情况可能平仓，不一定一笔权利金全亏
        '''
        print 'close_ratio_ma2------%s------%s------'% (n, a)
        self.get_ma(a)
        df = deepcopy(self.df)
        maa = 'ma%s' % a
        df['higher'] = df.l > df[maa]
        df['ratio'] = np.where(df['higher'], 'b' , None)
        df['lower'] = df.h < df[maa]
        df['ratio'] = np.where(df['lower'], 's' , df['ratio'])
        df['cshiftn'] = df.c.shift(-1*n)
        df.to_csv('tmp.csv')
        self._run_close_ratio(df, qlj, xqj, xj, n)

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

    def close_ratio_hl(self,qlj, xqj, xj, n ,a=10):
        print 'close_ratio_hl------%s----%s---%s-----%s--a:%s'% (qlj, xqj, xj, n, a)
        self.get_nhh(a)
        self.get_nll(a)
        df = deepcopy(self.df)
        df['higher'] = df.h > df.nhh
        df['ratio'] = np.where(df['higher'], 'b' , None)
        df['cshiftn'] = df.c.shift(-1*n)
        df.to_csv('tmp.csv')
        self._run_close_ratio(df, qlj, xqj, xj, n)

    def close_ratio_hl_s(self,qlj, xqj, xj, n ,a=10):
        print 'close_ratio_hl_s------%s----%s---%s-----%s--a:%s'% (qlj, xqj, xj, n, a)
        self.get_nhh(a)
        self.get_nll(a)
        df = deepcopy(self.df)
        df['lower'] = df.l < df.nll
        df['ratio'] = np.where(df['lower'], 's' , None)
        df['cshiftn'] = df.c.shift(-1*n)
        df.to_csv('tmp.csv')
        self._run_close_ratio(df, qlj, xqj, xj, n)

    def _run_close_ratio(self, df, qlj, xqj, xj, n):
        '''买方'''
        dflen = len(df)
        bratios = [] # n天后行权的价格 和 假设当时设置的行权价 的比例
        sratios = []
        r = xqj / float(xj)
        q = qlj / float(xqj)
        #print 'r,q----  ', r,q
        bcnt = 0
        scnt = 0
        for i, ratio in enumerate(df.ratio):
            if i >= dflen - n:
                continue
            idx = df.index[i]
            xjthantime = df.loc[idx, 'c']  # 用c代替当时的现价
            xqjthattime = xjthantime * r #按照现在比例模拟当时行权价
            cshiftn = df.loc[idx, 'cshiftn']
            if ratio == 'b':
                #print cshiftn / xqjthattime
                bratios.append(cshiftn / xqjthattime)
            elif ratio == 's':
                sratios.append(xqjthattime / cshiftn)
            else : pass

        if bratios:
            #print sorted(bratios)
            bigger = [x for x in bratios if x>1]
            biggerlen = len(bigger)
            biggersum = sum(bigger)
            bratioslen = len(bratios)
            bratiosum = sum(bratios)
            ylbl = biggerlen / float(bratioslen)
            ylsy = biggersum / biggerlen - 1
            #print np.mean(bratios)
            print round(ylbl, 2),'盈利比例'
            #print round(ylsy, 2), '盈利部分的平均收益'
            #print '前两者相乘------', round(ylbl * ylsy, 4)
            print '收益预期=====', round(ylbl * ylsy - q, 4)
            #print sorted(bigger),
        if sratios:
            #print sorted(sratios)
            sbigger = [x for x in sratios if x>1]
            sbiggerlen = len(sbigger)
            sbiggersum = sum(sbigger)
            sratioslen = len(sratios)
            ylbl = sbiggerlen / float(sratioslen)
            ylsy = sbiggersum / sbiggerlen - 1
            #print np.mean(sratios)
            print round(ylbl, 2),'盈利比例'
            #print round(ylsy, 2), '盈利部分的平均收益' 
            #print '前两者相乘------', round(ylbl * ylsy, 4)
            print '收益预期=====', round(ylbl * ylsy - q, 4)
            #print sorted(sbigger)


    def _run_close_ratio2(self, df, qlj, xqj, xj, n):
        '''买方  参照那个头寸损益图中的思路'''
        dflen = len(df)
        bratios = [] # n天后行权的价格 和 假设当时设置的行权价 的比例
        sratios = []
        r = xqj / float(xj)
        q = qlj / float(xqj)
        #print 'r,q----  ', r,q
        bcnt = 0
        scnt = 0
        for i, ratio in enumerate(df.ratio):
            if i >= dflen - n:
                continue
            idx = df.index[i]
            xjthantime = df.loc[idx, 'c']  # 用c代替当时的现价
            xqjthattime = xjthantime * r #按照现在比例模拟当时行权价
            cshiftn = df.loc[idx, 'cshiftn']
            if ratio == 'b':
                #print cshiftn / xqjthattime
                bratios.append(cshiftn / (xqjthattime * (1 + q)))
            elif ratio == 's':
                sratios.append(cshiftn / (xqjthattime * (1 - q)))
            else : pass

        if bratios:
            zzd = 1/(1+q) # q平衡点到行权价，多头损益图中1+q是损益平衡点，1是行权价点，
            bl = []
            for x in bratios:
                if x > zzd:
                    bl.append(x)
                else:
                    bl.append(zzd)
            #print bl
            print '收益预期==ratio2===', round(sum(bl)/len(bl), 4)
            #big = [x for x in bratios if x>1]
            #small = [x for x in bratios if x<1]
            #blen = float(len(bratios))
            #big_bl = len(big)/blen
            #small_bl = len(small)/blen
            #big_avg = sum(big)/len(big)
            #small_avg = sum(small)/len(small)
            #print '盈利比例', round(big_bl, 2), small_bl
            #print '收益预期==ratio2===', round(big_bl*big_avg+small_bl*small_avg, 4)



        if sratios:
            zzd = 1/(1-q) # 空头损益图中1-q是损益平衡点，1是行权价点，
            bl = []
            for x in sratios:
                if x > zzd:
                    bl.append(zzd)
                else:
                    bl.append(x)
            #print bl
            print '收益预期==ratio2===', round(sum(bl)/len(bl), 4)

    '''
    ############################################################################################
    ############################################################################################
    ########################分割线要明显########################################################
    ############################################################################################
    ############################################################################################
    '''
    def _get_hl_bkpoint(self, df, idx):
        ''''''
        nhh = df.loc[idx, 'nhh']
        o = df.loc[idx, 'o']
        return o if o > nhh else nhh

    def _get_hl_skpoint(self, df, idx):
        nll = df.loc[idx, 'nll']
        o = df.loc[idx, 'o']
        return o if o < nll else nll

    def _get_hl_bkpoint2(self, df, idx):
        ''''''
        lnhh = df.loc[idx, 'lnhh']
        o = df.loc[idx, 'o']
        return o if o > lnhh else lnhh

    def _get_hl_skpoint2(self, df, idx):
        hnll = df.loc[idx, 'hnll']
        o = df.loc[idx, 'o']
        return o if o < hnll else hnll

    def runevery_percent(self, n=3, kczs=0.02, zs=0.08, zy=9):
        '''用for循环逐个跑,开仓止损kczs，比例移动止损zs，比例主动止盈zy'''
        print 'runevery_percent-----n:%s---kczs:%s-----zs:%s--zy:%s'% (n,kczs,zs,zy) 
        self.get_nhh(n)
        self.get_nll(n)
        self.get_lnhh(n)
        self.get_hnll(n)
        ma = 20
        ma_small = 2
        ma_name = 'ma'+str(ma)
        ma_small_name = 'ma'+str(ma_small)
        self.get_ma(ma, ma_small)
        df = deepcopy(self.df)
        # 以下higher lower 选其一
        option = {
            'tupo_high': df.h.shift(1) > df.nhh.shift(1),
            'tupo_low': df.l.shift(1) < df.nll.shift(1),
            'low_tupo_high': df.l.shift(1) > df.lnhh.shift(1),
            'high_tupo_low': df.h.shift(1) < df.hnll.shift(1),
            'higher_than_ma': df.l.shift(1) > df[ma_name].shift(1),
            'lower_than_ma': df.h.shift(1) < df[ma_name].shift(1),
            'maup': df[ma_name].shift(1) > df[ma_name].shift(2),
            'madown': df[ma_name].shift(1) < df[ma_name].shift(2),
            'hl_bothhigh': (df.h.shift(1) > df.h.shift(2)) & (df.h.shift(1) > df.h.shift(2)),
            'hl_bothlow': (df.l.shift(1) < df.l.shift(2)) & (df.l.shift(1) < df.l.shift(2)),
            'small_maup': df[ma_small_name].shift(1) > df[ma_small_name].shift(2),
            'small_madown': df[ma_small_name].shift(1) < df[ma_small_name].shift(2),
        }


        df['higher'] = option['tupo_high'] & option['higher_than_ma'] 
        df['lower'] = option['tupo_low']   & option['lower_than_ma']
        #df['higher'] = option['tupo_high']  & option['maup'] 
        #df['lower'] = option['tupo_low']    & option['madown']
        #df['higher'] =  option['low_tupo_high'] #& option['higher_than_ma'] 
        #df['lower'] =  option['high_tupo_low']  #& option['lower_than_ma']
        #df['higher'] = option['low_tupo_high'] & option['maup'] 
        #df['lower'] = option['high_tupo_low']  & option['madown']
        #df['higher'] = option['tupo_high'] & option['low_tupo_high']
        #df['lower'] = option['tupo_low']   & option['high_tupo_low']
        #df['higher'] = option['higher_than_ma'] 
        #df['lower'] = option['lower_than_ma']
        #df['higher'] = option['maup']  & option['higher_than_ma'] 
        #df['lower'] = option['madown'] & option['lower_than_ma'] 
        df['bksk'] = np.where(df.higher, 'bk' , None)
        df['bksk'] = np.where(df.lower, 'sk' , df.bksk)   
        dflen = len(df)
        df.to_csv('tmp.csv')
        blist = []
        slist = []
        for i, bksk in enumerate(df.bksk):
            idx = df.index[i]
            r = range(i+1, dflen)

            if bksk=='bk':
                bkprice = df.loc[idx, 'o']
                #bkprice = self._get_hl_bkpoint(df,idx)
                #bkprice = self._get_hl_bkpoint2(df,idx)
                newhigh = df.loc[idx, 'h']
                #newlow = df.loc[idx, 'l']
                point_kczs = bkprice*(1-kczs)
                point_zs = bkprice*(1-zs)


                point_zy = bkprice*(1+zy)
                #print i, bkprice, point_kczs,point_zs,point_zy
                for j in r:
                    idxj = df.index[j]
                    high = df.loc[idxj, 'h']
                    low = df.loc[idxj, 'l']
                    atr = df.loc[idxj, 'atr']
                    newhigh = max(high, newhigh)
                    #newlow = min(df.loc[idxj, 'l'], newlow)

                    point_zs = max(newhigh*(1-zs), point_zs, point_kczs)
                    if high >= point_zy:
                        #print j, '止盈', newhigh,point_zs
                        blist.append(point_zy/bkprice)
                        break
                    if low <= point_zs:
                        #print j, '止损', newhigh,point_zs
                        blist.append(point_zs/bkprice)
                        break

            if bksk=='sk':
                skprice = df.loc[idx, 'o']
                #skprice = self._get_hl_skpoint(df,idx)
                #skprice = self._get_hl_skpoint2(df,idx)
                newlow = df.loc[idx, 'l']
                point_kczs = skprice*(1+kczs)
                point_zs = skprice*(1+zs)


                point_zy = skprice*(1-zy)
                for j in r:
                    idxj = df.index[j]
                    high = df.loc[idxj, 'h']
                    low = df.loc[idxj, 'l']  
                    atr = df.loc[idxj, 'atr']
                    newlow = min(low, newlow)
                    point_zs = min(newlow*(1+zs), point_zs, point_kczs)
                    point_zs = min(newlow+ (atr * zs), point_zs, point_kczs)
                    if low <= point_zy:
                        #print j, '止盈', newhigh,point_zs
                        slist.append(skprice/point_zy)
                        break
                    if high >= point_zs:
                        #print j, '止损', newhigh,point_zs
                        slist.append(skprice/point_zs)
                        break
        
        if blist:
            avg = round(np.average(blist), 3)
            std = round(np.std(blist), 3)
            print 'b均值：%s   标准差：%s  交易次数：%s' % (avg, std, len(blist))
        if slist:
            avg = round(np.average(slist), 3)
            std = round(np.std(slist), 3)
            print 's均值：%s   标准差：%s  交易次数：%s' % (avg, std, len(slist))
        #self._plot_histogram(mean, std, 'runevery_percent')


    def runevery_atr(self, n=3, kczs=1, zs=3, zy=1):
        '''用for循环逐个跑,开仓止损kczs，移动止损zs，主动止盈zy'''
        print 'runevery_atr-----n:%s---kczs:%s-----zs:%s--zy:%s'% (n,kczs,zs,zy) 
        self.get_nhh(n)
        self.get_nll(n)
        self.get_lnhh(n)
        self.get_hnll(n)
        self.get_nch(n)
        self.get_ncl(n)
        ma = 20
        ma_small = 2
        ma_name = 'ma'+str(ma)
        ma_small_name = 'ma'+str(ma_small)
        self.get_ma(ma, ma_small)
        df = deepcopy(self.df)

        # 以下higher lower 选其一
        option = {
            'tupo_high': df.h.shift(1) > df.nhh.shift(1),
            'tupo_low': df.l.shift(1) < df.nll.shift(1),
            #'tupo_high': df.h.shift(1) > df.nhh.shift(1),
            #'tupo_low': df.l.shift(1) < df.nll.shift(1),
            'low_tupo_high': df.l > df.lnhh,
            'high_tupo_low': df.h < df.hnll,
            'low_tupo_high': df.l.shift(1) > df.lnhh.shift(1),
            'high_tupo_low': df.h.shift(1) < df.hnll.shift(1),
            'higher_than_ma': df.l.shift(1) > df[ma_name].shift(1),
            'lower_than_ma': df.h.shift(1) < df[ma_name].shift(1),
            'maup': df[ma_name].shift(1) > df[ma_name].shift(2),
            'madown': df[ma_name].shift(1) < df[ma_name].shift(2),
            'hl_bothhigh': (df.h.shift(1) > df.h.shift(2)) & (df.h.shift(1) > df.h.shift(2)),
            'hl_bothlow': (df.l.shift(1) < df.l.shift(2)) & (df.l.shift(1) < df.l.shift(2)),
            'small_maup': df[ma_small_name].shift(1) > df[ma_small_name].shift(2),
            'small_madown': df[ma_small_name].shift(1) < df[ma_small_name].shift(2),
            'tupo_high_c': df.c.shift(1) > df.nch.shift(1), # 是不是用这个效果好
            'tupo_low_c': df.c.shift(1) < df.ncl.shift(1),
            'higher_than_ma_c': df.c.shift(1) > df[ma_name].shift(1),
            'lower_than_ma_c': df.c.shift(1) < df[ma_name].shift(1),
        }


        #df['higher'] = option['tupo_high'] & option['higher_than_ma'] 
        #df['lower'] = option['tupo_low']   & option['lower_than_ma']
        #df['higher'] = option['tupo_high']  & option['maup'] 
        #df['lower'] = option['tupo_low']    & option['madown']
        #df['higher'] =  option['low_tupo_high'] & option['higher_than_ma'] & option['maup'] 
        #df['lower'] =  option['high_tupo_low']  & option['lower_than_ma']  & option['madown']
        #df['higher'] = option['low_tupo_high'] & option['maup'] 
        #df['lower'] = option['high_tupo_low']  & option['madown']
        #df['higher'] = option['tupo_high'] & option['low_tupo_high']
        #df['lower'] = option['tupo_low']   & option['high_tupo_low']
        #df['higher'] = option['higher_than_ma'] 
        #df['lower'] = option['lower_than_ma']
        #df['higher'] = option['maup']  & option['higher_than_ma'] 
        #df['lower'] = option['madown'] & option['lower_than_ma'] 
        df['higher'] = option['tupo_high_c']  & option['higher_than_ma_c'] 
        df['lower'] = option['tupo_low_c']    & option['lower_than_ma_c']         
        df['bksk'] = np.where(df.higher, 'bk' , None)
        df['bksk'] = np.where(df.lower, 'sk' , df.bksk)   
        dflen = len(df)
        df.to_csv('tmp.csv')
        blist = []
        slist = []
        for i, bksk in enumerate(df.bksk):
            idx = df.index[i]
            r = range(i+1, dflen)

            if bksk=='bk':
                bkprice = df.loc[idx, 'o']
                #bkprice = self._get_hl_bkpoint(df,idx)
                #bkprice = self._get_hl_bkpoint2(df,idx)
                newhigh = df.loc[idx, 'h']
                #newlow = df.loc[idx, 'l']

                atr = df.loc[idx, 'atr']
                if not np.isnan(atr):
                    point_kczs = bkprice - (atr * kczs)
                    #point_kczs = df.loc[idx, 'ma20']
                    point_zs = bkprice - (atr * zs)
                    #print i, bkprice, point_kczs, point_zs
                else: continue

                point_zy = bkprice*(1+zy)
                #print i, bkprice, point_kczs,point_zs,point_zy
                for j in r:
                    idxj = df.index[j]
                    high = df.loc[idxj, 'h']
                    low = df.loc[idxj, 'l']
                    atr = df.loc[idxj, 'atr']
                    newhigh = max(high, newhigh)
                    #newlow = min(df.loc[idxj, 'l'], newlow)

                    point_zs = max(newhigh-(atr * zs), point_zs, point_kczs)

                    if high >= point_zy:
                        #print j, '止盈', newhigh,point_zs
                        blist.append(point_zy/bkprice)
                        break
                    if low <= point_zs:
                        #print j, '止损', newhigh,point_zs
                        blist.append(point_zs/bkprice)
                        break

            if bksk=='sk':
                skprice = df.loc[idx, 'o']
                #skprice = self._get_hl_skpoint(df,idx)
                #skprice = self._get_hl_skpoint2(df,idx)
                newlow = df.loc[idx, 'l']

                atr = df.loc[idx, 'atr']
                if not np.isnan(atr):
                    
                    point_kczs = skprice + (atr * kczs)
                    #point_kczs = df.loc[idx, 'ma20']
                    #print skprice, point_kczs
                    point_zs = skprice + (atr * zs)
                else: continue


                point_zy = skprice*(1-zy)
                for j in r:
                    idxj = df.index[j]
                    high = df.loc[idxj, 'h']
                    low = df.loc[idxj, 'l']  
                    atr = df.loc[idxj, 'atr']
                    newlow = min(low, newlow)

                    point_zs = min(newlow+ (atr * zs), point_zs, point_kczs)
                    if low <= point_zy:
                        #print j, '止盈', newhigh,point_zs
                        slist.append(skprice/point_zy)
                        break
                    if high >= point_zs:
                        #print j, '止损', newhigh,point_zs
                        slist.append(skprice/point_zs)
                        break
        self._plot_cummulti(blist)
        if blist:
            avg = round(np.average(blist), 3)
            std = round(np.std(blist), 3)
            print 'b均值：%s   标准差：%s  交易次数：%s' % (avg, std, len(blist))
        if slist:
            avg = round(np.average(slist), 3)
            std = round(np.std(slist), 3)
            print 's均值：%s   标准差：%s  交易次数：%s' % (avg, std, len(slist))
        #self._plot_histogram(mean, std, 'runevery_percent')                    


    '''
    ############################################################################################
    ############################################################################################
    ########################分割线要明显########################################################
    ############################################################################################
    ############################################################################################
    '''
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


def m80():
    # m跑下来，一到两个月的持仓期最好，实际操作是，固定一个持仓间隔，一个月
    t = Tongji('m')
    #t.ratio(            17)
    t.close_ratio_tupoh(17, 7)
    #t.close_ratio_tupoh(17, 20)
    #t.close_ratio_tupoh(17, 40)
    #t.close_ratio_tupol(17, 7)
    #t.close_ratio_tupol(17, 20)
    #t.close_ratio_tupol(17, 40)

def runcloseratio():
    t = Tongji('m')
    xianjia, n = 2745, 60
    #t.close_ratio_ma(290, 2600, 2820,   80,5,40)
    # m1709
    t.close_ratio_foo(213,  2550, xianjia, n)
    t.close_ratio_foo(172,  2600, xianjia, n)
    t.close_ratio_foo(138.5,  2650, xianjia, n)
    t.close_ratio_foo(108.5,  2700, xianjia, n)
    t.close_ratio_foo(84.5,  2750, xianjia, n)
    t.close_ratio_foo(65,   2800, xianjia, n)
    t.close_ratio_foo(48.5,   2850, xianjia, n)
    t.close_ratio_foo(37,   2900, xianjia, n)
    t.close_ratio_foo(27,   2950, xianjia, n)
    t.close_ratio_foo(20.5,   3000, xianjia, n)
    




if __name__ == '__main__':
    #m80()
    #runcloseratio()
    t = Tongji('m')
    #t.ratio(5)
    #t.ratio_high_bl(90, 1.4)
    #t.ratio_high(5)
    #t.ratio_low(7)
    #t.ratio_low_tupohigh(7, 13)
    #t.ratio_high_tupohigh(5, 5)

    #t.runevery_percent(2, 0.03, 0.08, 0.99)
    #t.runevery_percent(3, 0.03, 0.07, 0.99)
    #t.runevery_percent(3, 0.02, 0.07, 0.99)
    #t.runevery_percent(3, 0.03, 0.08, 0.99)
    #t.runevery_atr(3, 2, 6,0.99)
    #t.runevery_atr(3, 2, 5,0.99)
    #t.runevery_atr(3, 1, 6,0.99)
    #t.runevery_atr(3, 1, 5,0.99)
    t.runevery_atr(3, 1, 4,0.99)
    t.runevery_atr(3, 1, 3,0.99)
    t.runevery_atr(3, 2, 4,0.99)
    t.runevery_atr(3, 2, 3,0.99)
    
    

    #t.runevery_percent(2, 0.02, 0.07, 0.99)
    #t.runevery_percent(2, 0.03, 0.07, 0.99)
    #t.runevery_percent(2, 0.04, 0.07, 0.99)
    #t.runevery_percent(3, 0.03, 0.06, 0.99)
    #t.runevery_percent(3, 0.02, 0.06, 0.99)
    