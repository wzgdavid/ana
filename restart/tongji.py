# encoding: utf-8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from general_index import General, GeneralIndex, rangerun, rangerun3
from copy import deepcopy

class Tongji(GeneralIndex):
    def __init__(self, daima):
        super(Tongji, self).__init__(daima)
        
        self.get_sdjj()

    def ratio(self, x):
        '''
        后x天平均价格与当天平均价格的比值
        '''
        print 'ratio------%s-----'% (x)
        df = deepcopy(self.df)
        df['shiftx'] = df.sdjj.shift(-1*x)
        df['ratio'] = df.shiftx / df.sdjj
        self._to_result(df)

    def ratio_high(self, x):
        '''
        后x天最高价与当天平均价格的比值
        '''
        print 'ratio_high------%s-----'% (x)
        self.get_mhh(x)
        df = deepcopy(self.df)
        df['ratio'] = df.mhh / df.sdjj
        self._to_result(df)

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
        print df.daobili_ratiox.mean() # 这个比例和bl比较，bl大，则价格达到bl后平仓，否则，持仓
        
        df.to_csv('tmp.csv')

    def ratio_low(self, x):
        '''
        后x天最低价与当天平均价格的比值
        '''
        print 'ratio_low------%s-----'% (x)
        self.get_mll(x)
        df = deepcopy(self.df)
        df['ratio'] = df.sdjj / df.mll 
        self._to_result(df)
        
    def close_ratio_tupoh(self, x, n):
        print 'close_ratio_tupoh------%s-----%s---'% (x, n)
        self.get_nhh(n)
        df = deepcopy(self.df)
        df['shiftx'] = df.sdjj.shift(-1*x)
        df['higher'] = df.h > df.nhh
        df['ratio'] = np.where(df['higher'], df.shiftx / df.sdjj, None)
        self._to_result(df)

    def close_ratio_tupol(self, x, n):
        print 'close_ratio_tupol------%s-----%s---'% (x, n)
        self.get_nll(n)
        df = deepcopy(self.df)
        df['shiftx'] = df.sdjj.shift(-1*x)
        df['lower'] = df.l < df.nll
        df['ratio'] = np.where(df['lower'], df.sdjj / df.shiftx, None)
        self._to_result(df)
    
    def _to_result(self, df):
        mean = df.ratio.mean()
        median =  df.ratio.median()
        std = df.ratio.std()
        print '均值：%s，中位数：%s' % (round(mean, 5), round(median, 5))
        df.to_csv('tmp.csv')
        self._plot_histogram(mean, std)

    def _plot_histogram(self, mean, std):
        import matplotlib.mlab as mlab
        np.random.seed(0)
        
        # example data
        mu = mean  # mean of distribution
        sigma = std  # standard deviation of distribution
        x = mu + sigma * np.random.randn(9999)
        
        num_bins = 50
        
        fig, ax = plt.subplots()
        # the histogram of the data
        n, bins, patches = ax.hist(x, num_bins, normed=1)
        # add a 'best fit' line
        y = mlab.normpdf(bins, mu, sigma)
        ax.plot(bins, y, '--')
        ax.set_xlabel('Smarts')
        ax.set_ylabel('Probability density')
        #ax.set_title(r'Histogram of IQ: $\mu=100$, $\sigma=15$')
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
        for i, bksk in enumerate(df.ratio):
            if i >= dflen - n:
                continue
            idx = df.index[i]
            ratio = df.loc[idx, 'ratio']
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
        dflen = len(df)
        bratios = [] # n天后行权的价格 和 假设当时设置的行权价 的比例
        sratios = []
        r = xqj / float(xj)
        q = qlj / float(xqj)
        #print 'r,q----  ', r,q
        bcnt = 0
        scnt = 0
        for i, bksk in enumerate(df.ratio):
            if i >= dflen - n:
                continue
            idx = df.index[i]
            ratio = df.loc[idx, 'ratio']
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
    def get_qlj(self, xqj, xj, x):
        '''
        '''
        print '行权价：%s， 现价：%s， x天：%s'% (xqj, xj, x)
        
        df = deepcopy(self.df)

        df['ratio'] = np.where(1, 'b' , None)
        df['shiftx'] = df.sdjj.shift(-1*x)
        self._run_get_qlj(xqj, xj, x)


    def _run_get_qlj(self, df, qlj, xqj, xj, n):
        df.to_csv('tmp.csv')
        dflen = len(df)
        bratios = []
        sratios = []
        r = xqj / float(xj)
        q = qlj / float(xqj)
        #print 'r,q----  ', r,q
        bcnt = 0
        scnt = 0
        for i, bksk in enumerate(df.ratio):
            if i >= dflen - n:
                continue
            idx = df.index[i]
            ratio = df.loc[idx, 'ratio']
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
            bigger = [x for x in bratios if x>r]
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
            sbigger = [x for x in sratios if x>r]
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


    '''
    ############################################################################################
    ############################################################################################
    ########################分割线要明显########################################################
    ############################################################################################
    ############################################################################################
    '''

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
    xianjia, n = 2747, 80
    #t.close_ratio_ma(290, 2600, 2820,   80,5,40)
    # m1709
    t.close_ratio_foo(226,  2550, xianjia, n)
    t.close_ratio_foo(188,  2600, xianjia, n)
    t.close_ratio_foo(156,  2650, xianjia, n)
    t.close_ratio_foo(128,  2700, xianjia, n)
    t.close_ratio_foo(102.5,  2750, xianjia, n)
    t.close_ratio_foo(82,   2800, xianjia, n)
    t.close_ratio_foo(64.5,   2850, xianjia, n)
    t.close_ratio_foo(50,   2900, xianjia, n)
    t.close_ratio_foo(38.5,   2950, xianjia, n)
    t.close_ratio_foo(29,   3000, xianjia, n)
    
    #t.close_ratio_foo_s(27.5, 2550, xianjia, n)
    #t.close_ratio_foo_s(41, 2600, xianjia, n)
    #t.close_ratio_foo_s(58.5, 2650, xianjia, n)
    #t.close_ratio_foo_s(80, 2700, xianjia, n)
    #t.close_ratio_foo_s(105, 2750, xianjia, n)
    #t.close_ratio_foo_s(134, 2800, xianjia, n)
    #t.close_ratio_foo_s(167, 2850, xianjia, n)
    #t.close_ratio_foo_s(203.5, 2900, xianjia, n)
    #t.close_ratio_foo_s(241.5, 2950, xianjia, n)
    #t.close_ratio_foo_s(282, 3000, xianjia, n)

    #t.close_ratio_hl(290, 2600, 2820,   80, 11)
    #t.close_ratio_hl(258, 2650, 2820,   80, 11)
    #t.close_ratio_hl(225.5, 2700, 2820, 80, 11)
    #t.close_ratio_hl(201, 2750, 2820,   80, 11)
    #t.close_ratio_hl(175, 2800, 2820,   80, 11)
    #t.close_ratio_hl(150, 2850, 2820,   80, 11)
    #t.close_ratio_hl(131, 2900, 2820,   80, 11)
    #t.close_ratio_hl(114.5, 2950, 2820, 80, 11)
    #t.close_ratio_hl(98, 3000, 2820,    80, 11)
    #t.close_ratio_hl(84, 3050, 2820,    80, 11)

    #t.close_ratio_hl_s(25, 2550, 2780,   150, 3)
    #t.close_ratio_hl_s(38.5, 2600, 2780, 150, 3)
    #t.close_ratio_hl_s(54.5, 2650, 2780, 150, 3)
    #t.close_ratio_hl_s(74.5, 2700, 2780, 150, 3)
    #t.close_ratio_hl_s(97.5, 2750, 2780, 150, 3)
    #t.close_ratio_hl_s(125.5, 2800, 2780,150, 3)
    #t.close_ratio_hl_s(154, 2850, 2780,  150, 3)
    #t.close_ratio_hl_s(184.5, 2900, 2780,150, 3)
    #t.close_ratio_hl_s(222, 2950, 2780,  150, 3)
    #t.close_ratio_hl_s(261, 3000, 2780,  150, 3)




if __name__ == '__main__':
    #m80()
    runcloseratio()
    t = Tongji('m')
    #t.ratio(     60)
    #t.ratio_high_bl(80, 1.4)
    #t.ratio_high(60)
    #t.ratio_low( 30)
    #foo()