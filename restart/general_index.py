# encoding: utf-8
#import sys
#sys.path.append("..")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

KLIMIT = 9999999999

class General(object):
    def __init__(self, daima):
        #df = pd.read_csv('../data/%s.xls' % daima) # windows excel 制表符\t 影响读取
        df = pd.read_csv('../data/%s.csv' % daima)
        self.df = df
        self.daima = daima

    def foo(self):
        print self.df['o']

    def run(self, df):
        '''没有资金管理，没有止损，每出现一次开仓信号，就开一手，一旦出现相反信号全平仓
        开平仓参数一样
        '''

        cnt = 0 # 每出一次开仓信号，就开一手，共几手的计数。一旦相反信号出来全平仓
        kprice = 0 # 所有持仓的开仓价格之和，不是多仓就是空仓
        total = 0
        icnt = 0 # 开仓手数
        # 做多
        for i, bksk in enumerate(df.bksk):
            
            idx = df.index[i]
            
            if bksk == 'bk':
                
                bkprice = df.loc[idx, 'sdjj'] # 买开仓的价位
                #print bkprice
                kprice += bkprice
                cnt += 1
                
            elif bksk == 'sk' and cnt != 0:
                skprice = df.loc[idx, 'sdjj']
                gain = skprice*cnt - kprice # 平仓盈亏
                #print skprice, kprice, gain
                total += gain
                icnt += cnt
                #print icnt, cnt, total
                cnt = 0
                kprice = 0
                
        
        cnt = 0 # 每出一次开仓信号，就开一手，共几手的计数。一旦相反信号出来全平仓
        kprice = 0 # 所有持仓的开仓价格之和，不是多仓就是空仓
        total2 = 0

        #print '------------------------------------'
        # 做空 分开计算容易写
        for i, bksk in enumerate(df.bksk):  #[:90]

            idx = df.index[i]
            
            if bksk == 'sk':
                
                skprice = df.loc[idx, 'sdjj'] # 开仓的价位, 目前跑任何，开仓平仓价格默认四点均价
                #print skprice
                kprice += skprice
                cnt += 1
            elif bksk == 'bk' and cnt != 0:
                bkprice = df.loc[idx, 'sdjj'] # 平仓价格
                gain = kprice - bkprice*cnt # 平仓盈亏
                #print skprice, kprice, gain
                total2 += gain
                icnt += cnt
                #print icnt, cnt, total2
                cnt = 0
                kprice = 0
        total =  total + total2
        avg = total/icnt
        print total, avg 

    def run2(self, df):
        '''
        开仓和平仓信号参数不同，也就是开仓平仓分开，而不是像run那样平仓了马上反向开仓
        比如
        开慢平快：大于前20天高点，开多，小于前10日低点平仓，小于前20日低点开仓，大于前10日高点平仓
        反过来就是，开快平慢：大于前10天高点，开多，小于前20日低点平仓，小于前10日低点开仓，大于前20日高点平仓
        买开仓bk  卖开仓sk  多头平仓bp 空头平仓sp  
        '''
        if 'bpsp' not in df.columns:
            print 'df has no bpsp'
            return
        cnt = 0 # 每出一次开仓信号，就开一手，共几手的计数。一旦相反信号出来全平仓
        kprice = 0 # 所有持仓的开仓价格之和，不是多仓就是空仓
        total = 0
        icnt = 0 # 开仓手数
        # 做多
        for i, bksk in enumerate(df.bksk):
            
            idx = df.index[i]
            bpsp = df.loc[idx, 'bpsp']
            if bksk == 'bk':
                
                bkprice = df.loc[idx, 'sdjj'] # 买开仓的价位
                #print bkprice
                kprice += bkprice
                cnt += 1
                
            elif bpsp == 'bp' and cnt != 0:
                skprice = df.loc[idx, 'sdjj']
                gain = skprice*cnt - kprice # 平仓盈亏
                #print skprice, kprice, gain
                total += gain
                icnt += cnt
                #print icnt, cnt, total
                cnt = 0
                kprice = 0


        #print '------------------------------------'
        # 做空 分开计算容易写
        cnt = 0 # 每出一次开仓信号，就开一手，共几手的计数。一旦相反信号出来全平仓
        kprice = 0 # 所有持仓的开仓价格之和，不是多仓就是空仓
        total2 = 0
        for i, bksk in enumerate(df.bksk):  #[:90]

            idx = df.index[i]
            bpsp = df.loc[idx, 'bpsp']
            if bksk == 'sk':
                
                skprice = df.loc[idx, 'sdjj'] # 开仓的价位, 目前跑任何，开仓平仓价格默认四点均价
                #print skprice
                kprice += skprice
                cnt += 1
            elif bpsp == 'sp' and cnt != 0:
                bkprice = df.loc[idx, 'sdjj'] # 平仓价格
                gain = kprice - bkprice*cnt # 平仓盈亏
                #print skprice, kprice, gain
                total2 += gain
                icnt += cnt
                #print icnt, cnt, total2
                cnt = 0
                kprice = 0
        total =  total + total2
        avg = total/icnt
        print total, avg 

    def run2b(self, df):
        ''' 把run2的买卖写在一个for里
        开仓和平仓信号参数不同，也就是开仓平仓分开，而不是像run那样平仓了马上反向开仓
        比如
        开慢平快：大于前20天高点，开多，小于前10日低点平仓，小于前20日低点开仓，大于前10日高点平仓
        反过来就是，开快平慢：大于前10天高点，开多，小于前20日低点平仓，小于前10日低点开仓，大于前20日高点平仓
        买开仓bk  卖开仓sk  多头平仓bp 空头平仓sp  
        '''
        if 'bpsp' not in df.columns:
            print 'df has no bpsp'
            return
        bcnt = 0 # 每出一次开仓信号，就开一手，共几手的计数。一旦相反信号出来全平仓
        bhprice = 0 # 所有多仓持仓的开仓价格之和
        total = 0
        ibcnt = 0 # 开仓手数
        scnt = 0 # 每出一次开仓信号，就开一手，共几手的计数。一旦相反信号出来全平仓
        shprice = 0 # 所有空仓持仓的开仓价格之和，
        iscnt = 0 # 开仓手数
        # 做多
        for i, bksk in enumerate(df.bksk):
            
            idx = df.index[i]
            bpsp = df.loc[idx, 'bpsp']
            if bksk == 'bk':
                
                bkprice = df.loc[idx, 'sdjj'] # 买开仓的价位
                #print bkprice
                bhprice += bkprice
                bcnt += 1
                #print total
                
            elif bpsp == 'bp' and bcnt != 0:
                skprice = df.loc[idx, 'sdjj']
                gain = skprice * bcnt - bhprice # 平仓盈亏
                #print skprice, bhprice, gain
                total += gain
                ibcnt += bcnt
                #print ibcnt, bcnt, total
                bcnt = 0
                bhprice = 0

            if bksk == 'sk':
                
                skprice = df.loc[idx, 'sdjj'] # 开仓的价位, 目前跑任何，开仓平仓价格默认四点均价
                #print skprice
                shprice += skprice
                scnt += 1
            elif bpsp == 'sp' and scnt != 0:
                bkprice = df.loc[idx, 'sdjj'] # 平仓价格
                gain = shprice - bkprice*scnt # 平仓盈亏
                #print skprice, shprice, gain
                total += gain
                iscnt += scnt
                #print iscnt, scnt, total
                scnt = 0
                shprice = 0

                #print total
        avg = total/(ibcnt + iscnt)
        #print total, avg
        return total, avg

    def run3b(self, df, zj=50000, f=0.02, zs=0.02, jiacang=0, usehl=False):
        print 'run3b'
        '''带开仓止损的资金管理，没资金管理跑出来的曲线不现实
        
        参数 
        zj 总资金
        zs  开仓止损幅度， 如果是小于1，代表开仓价的百分比， 如果是整数，代表几个atr（100天参数）
        f  总资金固定百分比风险  每次不能超过这个百分比，没持仓，按照f算能开几手
        jiacang  为一个大于0的数， 表示开仓的点位走多少加仓， 比如0.2表示平均持仓价格走20%加仓
                 加仓为开仓手数的一半，
                 加仓不设止损，
        保证金为10%
        
        开仓方式， 信号开仓
        平仓方式， 信号平仓， 开仓止损价平仓（zs）
        开仓写在平仓前面，效果是平仓日 不再开仓
        开仓写在平仓后面，效果是平仓日 还能开仓。 跑下来好像这个收益高

        
        '''

        if 'bpsp' not in df.columns:
            print 'df has no bpsp'
            return
        
        #print 'run3b'
        #bcnt = 0 # 每出一次开仓信号，就开一手，共几手的计数。一旦相反信号出来全平仓
        #bhprice = 0 # 所有多仓持仓的开仓价格之和
        zj_init = zj
        zjqx = [] # 资金曲线，画图用
        kccs = [] # 开仓次数
        kccnt = 0  # 开仓计数
        ibcnt = 0 # 买开仓手数
        #scnt = 0 # 每出一次开仓信号，就开一手，共几手的计数。一旦相反信号出来全平仓
        #shprice = 0 # 所有空仓持仓的开仓价格之和，
        iscnt = 0 # 卖开仓手数
        chicang = 0 # 持仓资金
        keyong = 0 # 可用资金
        kjs = 0 # 一次开仓几手
        bs = '' # 表示多头还是空头
        klimit = KLIMIT # 单次交易开仓手数限制， 无限制才厉害,但好像不太现实，
                        # 跑策略时不限制才能看出策略本身好坏
                        # 不限制，时间长一点，可能会有大回撤
        bpoint = 0
        spoint = 0
        jcjs = 0 # 加仓几手
        bjccnt = 0 # 加仓计数
        sjccnt = 0 # 加仓计数
        sscnt = 0 # 总交易手数计数
        sxfbl = 200 # 手续费比例
        huadianbl = 200 # 滑点比例
        # 做多
        for i, bksk in enumerate(df.bksk):
            
            idx = df.index[i]
            bpsp = df.loc[idx, 'bpsp']

            if bpoint!=0 and kjs!=0 and bs=='b': # 多头止损平仓
                if df.loc[idx, 'l'] <= bpoint: 
                    gain = (bpoint  - bkprice) * kjs* 10 # 平仓收益
                    print i, '止损bp', gain
                    sxf = bkprice/sxfbl * kjs
                    hd = bkprice/huadianbl * kjs  
                    zj += gain - sxf - hd
                    sscnt += kjs
                    bpoint = 0
                    kjs = 0
                    bs = ''
                    jcjs = 0
                    bjccnt = 0

            if spoint!=0 and kjs!=0 and bs=='s': # 空头止损平仓
                if df.loc[idx, 'h'] >= spoint: 
                    gain = (skprice - spoint)  * kjs * 10
                    print i, '止损sp', gain
                    sxf = skprice/sxfbl * kjs# 
                    hd = skprice/huadianbl * kjs  # 
                    zj += gain - sxf - hd
                    sscnt += kjs
                    spoint = 0
                    kjs = 0
                    bs = ''
                    jcjs = 0
                    sjccnt = 0

            if bpsp == 'bp' and kjs != 0 and bs == 'b': # 多头信号平仓
                bpprice = df.loc[idx, 'sdjj']  # 平仓价格
                #if df.loc[idx, 'l'] < df.loc[idx, 'nll'] < df.loc[idx, 'h']: # 
                #    bpprice = df.loc[idx, 'nll'] # 
                #else:  
                #    bpprice = df.loc[idx, 'sdjj']
                gain = (bpprice  - bkprice) * kjs* 10 # 平仓收益
                print i, '信号bp', bpprice, gain
                sxf = bkprice/sxfbl * kjs
                hd = bkprice/huadianbl * kjs  
                zj += gain - sxf - hd
                sscnt += kjs
                bpoint = 0
                kjs = 0
                bs = ''
                jcjs = 0
                bjccnt = 0

            if bpsp == 'sp' and kjs != 0 and bs == 's': # 空头信号平仓
                spprice = df.loc[idx, 'sdjj']
                #if df.loc[idx, 'l'] < df.loc[idx, 'nhh'] < df.loc[idx, 'h']: # 用前n天高价开多
                #    spprice = df.loc[idx, 'nhh'] # 
                #else:  
                #    spprice = df.loc[idx, 'sdjj']
                gain = (skprice - spprice) * kjs * 10 
                print i, '信号sp', spprice, gain
                sxf = skprice/sxfbl * kjs
                hd = skprice/huadianbl * kjs 
                zj += gain - sxf - hd
                sscnt += kjs
                spoint = 0
                kjs = 0
                bs = ''
                jcjs = 0
                sjccnt = 0
                
            if bksk=='bk' and kjs==0: # 开多
                #bkprice = df.loc[idx, 'sdjj']
                # hl用这个开仓价
                if usehl and df.loc[idx, 'l'] < df.loc[idx, 'nhh'] < df.loc[idx, 'h']: # 用前n天高价开多
                    bkprice = df.loc[idx, 'nhh'] # 
                else:  
                    bkprice = df.loc[idx, 'sdjj']
                #print bkprice
                if zs < 1: # 百分比开仓止损
                    bkczs = bkprice * zs *10 # 开仓止损幅度
                    bpoint =bkprice - bkprice * zs # 开仓止损点位
                else: # atr开仓止损
                    bkczs = df.loc[idx, 'atr'] * zs * 10 # 开仓止损幅度
                    
                    bpoint =bkprice - zs * df.loc[idx, 'atr'] # 开仓止损点位
                kjs = min(int((zj*f)/bkczs), klimit)  # 这次可开几手, 最大限制100手
                bs = 'b'
                bki = i
                print i, 'bk  ', bkprice, bpoint,kjs
                kccnt += 1

            if bksk=='sk' and kjs==0:  # 开空
                #skprice = df.loc[idx, 'sdjj']
                # hl用这个开仓价
                if usehl and df.loc[idx, 'l'] < df.loc[idx, 'nll'] < df.loc[idx, 'h']: # 
                    skprice = df.loc[idx, 'nll'] # 
                else:  
                    skprice = df.loc[idx, 'sdjj']

                if zs < 1:
                    skczs = skprice * zs * 10# 开仓止损
                    spoint =skprice + skprice * zs # 开仓止损点位
                else:
                    #print 'atr', df.loc[idx, 'atr']
                    skczs = df.loc[idx, 'atr'] * zs * 10 # 开仓止损幅度
                    spoint =skprice + zs * df.loc[idx, 'atr'] # 开仓止损点位
                kjs = min(int((zj*f)/skczs), klimit)  # 这次可开几手
                bs = 's'
                ski = i
                print i, 'sk  ', skprice,  spoint, kjs
                kccnt += 1

            # 检查当天开仓的止损
            if bpoint!=0 and kjs!=0 and bs=='b': # 多头止损平仓
                if df.loc[idx, 'l'] <= bpoint: 
                    gain = (bpoint  - bkprice) * kjs* 10 # 平仓收益
                    print i, '止损bp', gain
                    sxf = bkprice/sxfbl * kjs
                    hd = bkprice/huadianbl * kjs  
                    zj += gain - sxf - hd
                    sscnt += kjs
                    bpoint = 0
                    kjs = 0
                    bs = ''
                    jcjs = 0
                    bjccnt = 0

            if spoint!=0 and kjs!=0 and bs=='s': # 空头止损平仓
                if df.loc[idx, 'h'] >= spoint: 
                    gain = (skprice - spoint)  * kjs * 10
                    print i, '止损sp', gain
                    sxf = skprice/sxfbl * kjs# 
                    hd = skprice/huadianbl * kjs  # 
                    zj += gain - sxf - hd
                    
                    sscnt += kjs
                    spoint = 0
                    kjs = 0
                    bs = ''
                    jcjs = 0
                    sjccnt = 0

            #if jiacang:  # 加仓
            #    if bs=='b':
            #        if bjccnt == 0:
            #            jcprice = (1+jiacang) * bkprice # 加仓的价格
            #        if df.loc[idx, 'h'] >= jcprice: # 某天的最高价超过加仓点，加仓
            #            if bjccnt == 0:
            #                jcjs = int(kjs/2)  # 加仓几手
            #            else:
            #                jcjs = int(jcjs/2)
            #            bkprice = (bkprice*kjs + jcprice*jcjs) / (kjs + jcjs) # 平均持仓价格
            #            #print i, 'b加仓', jcprice, jcjs
            #            jcprice = (1+jiacang) * jcprice
            #            kjs += jcjs
            #            bjccnt += 1
            #            kccnt += 1
            #    elif bs=='s':
            #        if sjccnt == 0:
            #            jcprice = (1-jiacang) * skprice # 加仓的价格
            #        #print '加仓bs==s',df.loc[idx, 'l'], jcprice
            #        if df.loc[idx, 'l'] <= jcprice: # 某天的最高价超过加仓点，加仓
            #            if sjccnt == 0:
            #                jcjs = int(kjs/2)  # 加仓几手
            #            else:
            #                jcjs = int(jcjs/2)
            #            skprice = (skprice*kjs + jcprice*jcjs) / (kjs + jcjs)
            #            #print i, 's加仓', jcprice, jcjs
            #            jcprice = (1-jiacang) * jcprice
            #            kjs += jcjs
            #            sjccnt += 1
            #            kccnt += 1

            zjqx.append(zj)
            if sscnt >0:
                kccs.append((zj-zj_init)/sscnt)
            else:
                kccs.append(0)

        self._plot(df, zjqx, kccs)
        print int(zj-zj_init), int((zj-zj_init)/sscnt), kccnt
        return zj-zj_init,(zj-zj_init)/sscnt


    def run4(self, df, zj=100000, f=0.06, zs=0.02, ydzs=0.06, jiacang=0, usehl=False):
        print 'run4'
        '''
        按照f算能开几手
        zj 总资金
        zs  开仓止损幅度， 代表开仓价的百分比，
        f  总资金固定百分比风险  每次不能超过这个百分比
        保证金为10%
    
        开仓方式， 信号开仓
        平仓方式，  开仓止损价平仓（zs）,移动止损平仓（ydzs）
        开仓写在平仓前面，效果是平仓日 不再开仓
        开仓写在平仓后面，效果是平仓日 还能开仓。 跑下来好像这个收益高

        跑下来还是信号平仓的效果好啊，再花点时间研究研究?
        '''
        zj_init = zj
        zjqx = [] # 资金曲线，画图用
        kccs = [] # 开仓次数
        kccnt = 0  # 开仓计数
        ibcnt = 0 # 买开仓手数
        iscnt = 0 # 卖开仓手数
        sscnt = 0 # 总交易手数计数
        kjs = 0 # 一次开仓几手
        bs = '' # 表示多头还是空头
        klimit = KLIMIT # 单次交易开仓手数限制， 无限制才厉害,但好像不太现实，
        bpoint = 0
        spoint = 0
        byd_point = 0 # 多头移动止损
        syd_point = 0 # 空头移动止损
        newhigh = 0 # 多头开仓之后，点位的新高
        newlow = 0 # 空头开仓之后，点位的新低
        bjccnt = 0 # 加仓计数
        sjccnt = 0 # 加仓计数
        sxfbl = 100 # 手续费比例
        huadianbl = 100 # 滑点比例
        # 做多
        for i, bksk in enumerate(df.bksk):
            
            idx = df.index[i]
            #bpsp = df.loc[idx, 'bpsp']

            if bpoint!=0 and kjs!=0 and bs=='b': # 多头止损平仓
                if ydzs < 1:# 百分比
                    byd_point = max(byd_point, df.loc[idx, 'h'] * (1-ydzs)) #
                else: #atr
                    atr = df.loc[idx, 'atr']
                    if pd.isnull(atr):
                        atr = df.loc[idx, 'tr']
                    byd_point = max(byd_point, df.loc[idx, 'h'] - ydzs*atr) #
                bzs = max(bpoint, byd_point)
                #print 'byd_point', byd_point, bpoint
                if df.loc[idx, 'l'] <= bzs: 
                    gain = (bzs  - bkprice) * kjs* 10 # 平仓收益
                    print i, '止损bp', bzs, gain
                    sxf = bkprice/sxfbl * kjs# 手续费定为开仓价格的0.1%
                    hd = bkprice/huadianbl * kjs  #
                    zj += gain - sxf - hd
                    sscnt += kjs
                    bpoint = 0
                    byd_point = 0
                    kjs = 0
                    bs = ''

            if spoint!=0 and kjs!=0 and bs=='s': # 空头止损平仓
                if ydzs < 1:# 百分比
                    syd_point = min(syd_point, df.loc[idx, 'l'] * (1+ydzs)) #
                else: # atr
                    atr = df.loc[idx, 'atr']
                    if pd.isnull(atr):
                        atr = df.loc[idx, 'tr']
                    syd_point = min(syd_point, df.loc[idx, 'l'] + ydzs*atr) #
                szs = min(spoint, syd_point)
                #print 'syd_point', syd_point, spoint
                if df.loc[idx, 'h'] >= szs: 
                    gain = (skprice - szs)  * kjs * 10
                    print i, '止损sp', szs, gain
                    sxf = skprice/sxfbl * kjs# 手续费定为开仓价格的0.1%
                    hd = skprice/huadianbl * kjs  #
                    zj += gain - sxf - hd
                    sscnt += kjs
                    spoint = 0
                    syd_point = 0
                    kjs = 0
                    bs = ''
                 
            if bksk=='bk' and kjs==0: # 开多
                #bkprice = df.loc[idx, 'sdjj']
                # hl用这个开仓价
                if usehl and df.loc[idx, 'l'] < df.loc[idx, 'nhh'] < df.loc[idx, 'h']: # 用前n天高价价开多
                    bkprice = df.loc[idx, 'nhh'] # 
                else:  
                    bkprice = df.loc[idx, 'sdjj']

                atr = df.loc[idx, 'atr']
                if pd.isnull(atr):
                    atr = df.loc[idx, 'tr']
                if zs < 1: # 百分比开仓止损
                    bkczs = bkprice * zs *10 # 开仓止损幅度
                    bpoint =bkprice - bkprice * zs # 开仓止损点位
                else: # atr开仓止损
                    #print 'atr', atr
                    bkczs = atr * zs * 10 # 开仓止损幅度
                    bpoint =bkprice - zs * atr # 开仓止损点位
                if ydzs < 1:
                    byd_point = df.loc[idx, 'h'] * (1-ydzs)
                    
                else:
                    byd_point = df.loc[idx, 'h'] - ydzs * atr
                #print 'byd_point', byd_point
                kjs = min(int((zj*f)/bkczs), klimit)  # 这次可开几手, 最大限制100手
            
                bs = 'b'
                #bki = i
                print i, 'bk  ', bkprice, bpoint, kjs
                #kccnt += 1

            if bksk=='sk' and kjs==0:  # 开空
                #skprice = df.loc[idx, 'sdjj']
                # hl用这个开仓价
                if usehl and df.loc[idx, 'l'] < df.loc[idx, 'nll'] < df.loc[idx, 'h']: # 
                    skprice = df.loc[idx, 'nll'] # 
                else:  
                    skprice = df.loc[idx, 'sdjj']
                
                atr = df.loc[idx, 'atr']
                if pd.isnull(atr):
                    atr = df.loc[idx, 'tr']
                if zs < 1:
                    skczs = skprice * zs * 10# 开仓止损
                    spoint =skprice + skprice * zs # 开仓止损点位
                else:
                    #print 'atr', atr
                    skczs = atr * zs * 10 # 开仓止损幅度
                    spoint =skprice + zs * atr # 开仓止损点位
                if ydzs < 1: # 百分比移动止损
                    syd_point = df.loc[idx, 'l'] * (1+ydzs)
                else: # atr移动止损
                    syd_point = df.loc[idx, 'l'] + ydzs * atr
                #print 'syd_point', syd_point
                kjs = min(int((zj*f)/skczs), klimit)  # 这次可开几手
            
                bs = 's'
                #ski = i
                print i, 'sk  ', skprice,  spoint, kjs

                #kccnt += 1
            if jiacang:  # 加仓
                if bs=='b':
                    if bjccnt == 0:
                        jcprice = (1+jiacang) * bkprice # 加仓的价格
                    if df.loc[idx, 'h'] >= jcprice: # 某天的最高价超过加仓点，加仓
                        if bjccnt == 0:
                            jcjs = int(kjs/2)  # 加仓几手
                        else:
                            jcjs = int(jcjs/2)
                        bkprice = (bkprice*kjs + jcprice*jcjs) / (kjs + jcjs) # 平均持仓价格
                        print i, 'b加仓', jcprice, jcjs
                        jcprice = (1+jiacang) * jcprice
                        kjs += jcjs
                        bjccnt += 1
                        #kccnt += 1
                elif bs=='s':
                    if sjccnt == 0:
                        jcprice = (1-jiacang) * skprice # 加仓的价格
                    #print '加仓bs==s',df.loc[idx, 'l'], jcprice
                    if df.loc[idx, 'l'] <= jcprice: # 某天的最高价超过加仓点，加仓
                        if sjccnt == 0:
                            jcjs = int(kjs/2)  # 加仓几手
                        else:
                            jcjs = int(jcjs/2)
                        skprice = (skprice*kjs + jcprice*jcjs) / (kjs + jcjs)
                        print i, 's加仓', jcprice, jcjs
                        jcprice = (1-jiacang) * jcprice
                        kjs += jcjs
                        sjccnt += 1
                        #kccnt += 1

            zjqx.append(zj)
            if sscnt >0:
                kccs.append((zj-zj_init)/sscnt)
            else:
                kccs.append(0)

        self._plot(df, zjqx, kccs)
        print zj-zj_init,(zj-zj_init)/sscnt, sscnt
        return zj-zj_init,(zj-zj_init)/sscnt

    def run5(self, df, zj=100000, f=0.02, zs=0.01, ydzs=0.01, usehl=False):
        '''
        按照f算能开几手
        zj 总资金
        zs  开仓止损幅度， 代表开仓价的百分比，
        f  总资金固定百分比风险  每次不能超过这个百分比
        保证金为10%
    
        开仓方式， 信号开仓
        平仓方式，  开仓止损价平仓（zs）,移动止损平仓（ydzs）,信号止损， 出任何一个止损都平仓
        开仓写在平仓前面，效果是平仓日 不再开仓
        开仓写在平仓后面，效果是平仓日 还能开仓。

        基本上是run3b和run4的折中

        '''
        zj_init = zj
        zjqx = [] # 资金曲线，画图用
        kccs = [] # 开仓次数
        kccnt = 0  # 开仓计数
        ibcnt = 0 # 买开仓手数
        iscnt = 0 # 卖开仓手数
        sscnt = 0 # 总交易手数计数
        kjs = 0 # 一次开仓几手
        bs = '' # 表示多头还是空头
        klimit = KLIMIT # 单次交易开仓手数限制， 无限制才厉害,但好像不太现实，
        bpoint = 0
        spoint = 0
        byd_point = 0 # 多头移动止损
        syd_point = 0 # 空头移动止损
        newhigh = 0 # 多头开仓之后，点位的新高
        newlow = 0 # 空头开仓之后，点位的新低
        bjccnt = 0 # 加仓计数
        sjccnt = 0 # 加仓计数
        sxfbl = 100 # 手续费比例
        huadianbl = 100 # 滑点比例

        for i, bksk in enumerate(df.bksk):
            
            idx = df.index[i]
            bpsp = df.loc[idx, 'bpsp']

            if bpsp == 'bp' and kjs != 0 and bs == 'b': # 多头信号平仓
                
                bpprice = df.loc[idx, 'sdjj']  # 平仓价格
                gain = (bpprice  - bkprice) * kjs* 10 # 平仓收益
                print i, '信号bp', bpprice, gain
                sxf = bkprice/sxfbl * kjs# 手续费定为开仓价格的0.1%
                hd = bkprice/huadianbl * kjs  # 
                zj += gain - sxf - hd
                
                sscnt += kjs
                bpoint = 0
                kjs = 0
                bs = ''
                

            if bpsp == 'sp' and kjs != 0 and bs == 's': # 空头信号平仓
                spprice = df.loc[idx, 'sdjj']
                gain = (skprice - spprice) * kjs * 10 
                print i, '信号sp', spprice, gain
                sxf = skprice/sxfbl * kjs# 手续费定为开仓价格的0.1%
                hd = skprice/huadianbl * kjs # 滑点
                zj += gain - sxf - hd
                sscnt += kjs
                spoint = 0
                kjs = 0
                bs = ''

            if bpoint!=0 and kjs!=0 and bs=='b': # 多头止损平仓
                if ydzs < 1:# 百分比
                    byd_point = max(byd_point, df.loc[idx, 'h'] * (1-ydzs)) #
                else: #atr
                    atr = df.loc[idx, 'atr']
                    if pd.isnull(atr):
                        atr = df.loc[idx, 'tr']
                    byd_point = max(byd_point, df.loc[idx, 'h'] - ydzs*atr) #
                bzs = max(bpoint, byd_point)
                print 'byd_point', byd_point, bpoint
                if df.loc[idx, 'l'] <= bzs: 
                    gain = (bzs  - bkprice) * kjs* 10 # 平仓收益
                    #print '止损bp', bzs, gain
                    sxf = bkprice/sxfbl * kjs# 手续费定为开仓价格的0.1%
                    hd = bkprice/huadianbl * kjs  #
                    zj += gain - sxf - hd
                    sscnt += kjs
                    bpoint = 0
                    byd_point = 0
                    kjs = 0
                    bs = ''

            if spoint!=0 and kjs!=0 and bs=='s': # 空头止损平仓
                if ydzs < 1:# 百分比
                    syd_point = min(syd_point, df.loc[idx, 'l'] * (1+ydzs)) #
                else: # atr
                    atr = df.loc[idx, 'atr']
                    if pd.isnull(atr):
                        atr = df.loc[idx, 'tr']
                    syd_point = min(syd_point, df.loc[idx, 'l'] + ydzs*atr) #
                szs = min(spoint, syd_point)
                #print 'syd_point', syd_point, spoint
                if df.loc[idx, 'h'] >= szs: 
                    gain = (skprice - szs)  * kjs * 10
                    #print '止损sp', szs, gain
                    sxf = skprice/sxfbl * kjs# 手续费定为开仓价格的0.1%
                    hd = skprice/huadianbl * kjs  #
                    zj += gain - sxf - hd
                    sscnt += kjs
                    spoint = 0
                    syd_point = 0
                    kjs = 0
                    bs = ''
                 
            if bksk=='bk' and kjs==0: # 开多
                #bkprice = df.loc[idx, 'sdjj']
                if usehl and df.loc[idx, 'l'] < df.loc[idx, 'nhh'] < df.loc[idx, 'h']: # 用前n天高价价开多
                    bkprice = df.loc[idx, 'nhh'] # 
                else:  
                    bkprice = df.loc[idx, 'sdjj']
                atr = df.loc[idx, 'atr']
                if pd.isnull(atr):
                    atr = df.loc[idx, 'tr']
                if zs < 1: # 百分比开仓止损
                    bkczs = bkprice * zs *10 # 开仓止损幅度
                    bpoint =bkprice - bkprice * zs # 开仓止损点位
                else: # atr开仓止损
                    #print 'atr', atr
                    bkczs = atr * zs * 10 # 开仓止损幅度
                    bpoint =bkprice - zs * atr # 开仓止损点位
                if ydzs < 1:
                    byd_point = df.loc[idx, 'h'] * (1-ydzs)
                else:
                    byd_point = df.loc[idx, 'h'] - ydzs * atr
                #print 'byd_point', byd_point
                kjs = min(int((zj*f)/bkczs), klimit)  # 这次可开几手, 最大限制100手
                bs = 'b'
                print 'bk  ', bkprice, bpoint, kjs
                #kccnt += 1

            if bksk=='sk' and kjs==0:  # 开空
                #skprice = df.loc[idx, 'sdjj']
                if usehl and df.loc[idx, 'l'] < df.loc[idx, 'nll'] < df.loc[idx, 'h']: # 
                    skprice = df.loc[idx, 'nll'] # 
                else:  
                    skprice = df.loc[idx, 'sdjj']
                
                atr = df.loc[idx, 'atr']
                if pd.isnull(atr):
                    atr = df.loc[idx, 'tr']
                if zs < 1:
                    skczs = skprice * zs * 10# 开仓止损
                    spoint =skprice + skprice * zs # 开仓止损点位
                else:
                    #print 'atr', atr
                    skczs = atr * zs * 10 # 开仓止损幅度
                    spoint =skprice + zs * atr # 开仓止损点位
                if ydzs < 1: # 百分比移动止损
                    syd_point = df.loc[idx, 'l'] * (1+ydzs)
                else: # atr移动止损
                    syd_point = df.loc[idx, 'l'] + ydzs * atr
                #print 'syd_point', syd_point
                kjs = min(int((zj*f)/skczs), klimit)  # 这次可开几手
                bs = 's'
                print 'sk  ', skprice,  spoint, kjs
                #kccnt += 1

            zjqx.append(zj)
            if sscnt >0:
                kccs.append((zj-zj_init)/sscnt)
            else:
                kccs.append(0)

        self._plot(df, zjqx, kccs)
        print zj-zj_init,(zj-zj_init)/sscnt
        return zj-zj_init,(zj-zj_init)/sscnt


    def run6(self, df, zj=50000, kclimit=4, f=0.01, zs=0.02, usehl=False):
        print 'run6'
        '''
        每次用f=0.01开仓，直到开仓数到达限定kclimit, zs以持仓均价为准
      
        参数 
        zj 总资金
        zs  开仓止损幅度， 代表开仓价的百分比
        f  每次开仓固定百分比风险  每次不能超过这个百分比，没持仓，按照f算能开几手
       
        保证金为10%
        
        开仓方式， 信号开仓
        平仓方式， 信号平仓
        '''
        if 'bpsp' not in df.columns:
            print 'df has no bpsp'
            return
        
        #bcnt = 0 # 每出一次开仓信号，就开一手，共几手的计数。一旦相反信号出来全平仓
        #bhprice = 0 # 所有多仓持仓的开仓价格之和
        zj_init = zj
        zjqx = [] # 资金曲线，画图用
        kccs = [] # 开仓次数
        kccnt = 0  # 开仓计数
        ibcnt = 0 # 买开仓手数
        #scnt = 0 # 每出一次开仓信号，就开一手，共几手的计数。一旦相反信号出来全平仓
        #shprice = 0 # 所有空仓持仓的开仓价格之和，
        iscnt = 0 # 卖开仓手数
        chicang = 0 # 持仓资金
        keyong = 0 # 可用资金
        kjs = 0 # 一次开仓几手
        bs = '' # 表示多头还是空头
        klimit = KLIMIT # 单次交易开仓手数限制， 无限制才厉害,但好像不太现实，
                        # 跑策略时不限制才能看出策略本身好坏
                        # 不限制，时间长一点，可能会有大回撤
        bpoint = 0
        spoint = 0
        jcjs = 0 # 加仓几手
        bkccnt = 0 # 买开仓计数
        skccnt = 0 # 卖开仓计数
        sscnt = 0 # 总交易手数计数
        sxfbl = 100 # 手续费比例
        huadianbl = 100 # 滑点比例
        bkprice = 0
        skprice = 0
        # 做多
        for i, bksk in enumerate(df.bksk):
            
            idx = df.index[i]
            bpsp = df.loc[idx, 'bpsp']

            if bpoint!=0 and kjs!=0 and bs=='b': # 多头止损平仓
                if df.loc[idx, 'l'] <= bpoint: 
                    gain = (bpoint  - bkprice) * kjs* 10 # 平仓收益
                    print i, '止损bp', gain, kjs
                    sxf = bkprice/sxfbl * kjs# 手续费定为开仓价格的0.1%
                    hd = bkprice/huadianbl * kjs  # 滑点定为0.1%
                    zj += gain - sxf - hd
                    sscnt += kjs
                    bpoint = 0
                    kjs = 0
                    bs = ''
                    jcjs = 0
                    bkccnt = 0
                    bkprice = 0
                    #continue

            if bpsp == 'bp' and kjs != 0 and bs == 'b': # 多头信号平仓
                
                bpprice = df.loc[idx, 'sdjj']  # 平仓价格
                gain = (bpprice  - bkprice) * kjs* 10 # 平仓收益
                print i, '信号bp', bpprice, gain, kjs
                sxf = bkprice/sxfbl * kjs# 手续费定为开仓价格的0.1%
                hd = bkprice/huadianbl * kjs  # 
                zj += gain - sxf - hd
                
                sscnt += kjs
                bpoint = 0
                kjs = 0
                bs = ''
                jcjs = 0
                bkccnt = 0
                bkprice = 0

            if spoint!=0 and kjs!=0 and bs=='s': # 空头止损平仓
                if df.loc[idx, 'h'] >= spoint: 
                    gain = (skprice - spoint)  * kjs * 10
                    print i, '止损sp', gain, kjs
                    sxf = skprice/sxfbl * kjs# 
                    hd = skprice/huadianbl * kjs  # 
                    zj += gain - sxf - hd
                    
                    sscnt += kjs
                    spoint = 0
                    kjs = 0
                    bs = ''
                    jcjs = 0
                    skccnt = 0
                    skprice = 0

            if bpsp == 'sp' and kjs != 0 and bs == 's': # 空头信号平仓
                spprice = df.loc[idx, 'sdjj']
                gain = (skprice - spprice) * kjs * 10 
                print i, '信号sp', spprice, gain, kjs
                sxf = skprice/sxfbl * kjs# 手续费定为开仓价格的0.1%
                hd = skprice/huadianbl * kjs # 滑点
                zj += gain - sxf - hd
                sscnt += kjs
                spoint = 0
                kjs = 0
                bs = ''
                jcjs = 0
                skccnt = 0
                skprice = 0
                
            if bksk=='bk': # 开多
                print 'bkprice', bkprice
                if bkprice == 0:# 初次开仓
                    if usehl and df.loc[idx, 'l'] < df.loc[idx, 'nhh'] < df.loc[idx, 'h']: # 用前n天高价开多
                        bkprice = df.loc[idx, 'nhh'] # 
                    else:  
                        bkprice = df.loc[idx, 'sdjj']
                    bkczs = bkprice * zs *10 # 开仓止损幅度
                    bpoint =bkprice - bkprice * zs # 开仓止损点位
                    kjs = min(int((zj*f)/bkczs), klimit)  # 这次可开几手, 最大限制100手
                    bs = 'b'
                    bki = i
                    bkccnt += 1
                    print i, 'bk first  ', bkprice, bpoint,kjs
                   
                else:

                    if bkccnt <= kclimit:
                       
                        if usehl and df.loc[idx, 'l'] < df.loc[idx, 'nhh'] < df.loc[idx, 'h']: # 用前n天高价开多
                            this_bkprice = df.loc[idx, 'nhh'] # 
                        else:  
                            this_bkprice = df.loc[idx, 'sdjj']
                        this_bkczs = this_bkprice * zs *10 # 开仓止损幅度
                        
                        this_kjs = min(int((zj*f)/this_bkczs), klimit)
                        print 'sdf', this_bkprice, this_bkczs,this_kjs
                        #print i, bkprice, this_bkprice, '-----dd------', this_bkczs, this_kjs, kjs
                        bkprice = (bkprice*kjs + this_bkprice*this_kjs) / (kjs + this_kjs) # 平均持仓价格
                        bpoint =bkprice - bkprice * zs # 持仓均价为新的止损点
                        bkccnt += 1
                        print i, 'bk after ', bkprice, bpoint,kjs


                #print i, 'bk  ', bkprice, bpoint,kjs
                
                #kccs.append(kccnt)

            if bksk=='sk':  # 开空
                if skprice == 0:# 初次开仓
                    if usehl and df.loc[idx, 'l'] < df.loc[idx, 'nll'] < df.loc[idx, 'h']: # 
                        skprice = df.loc[idx, 'nll'] # 
                    else:  
                        skprice = df.loc[idx, 'sdjj']
    
                    skczs = skprice * zs * 10# 开仓止损
                    spoint =skprice + skprice * zs # 开仓止损点位
                
                    kjs = min(int((zj*f)/skczs), klimit)  # 这次可开几手
                    bs = 's'
                    ski = i
                    skccnt += 1
                    print i, 'sk first ', skprice,  spoint, kjs

                else:
                    if skccnt <= kclimit:
                        
                        if usehl and df.loc[idx, 'l'] < df.loc[idx, 'nll'] < df.loc[idx, 'h']: # 
                            this_skprice = df.loc[idx, 'nll'] # 
                        else:  
                            this_skprice = df.loc[idx, 'sdjj']
                        this_skczs = this_skprice * zs *10 # 开仓止损幅度
                        this_kjs = min(int((zj*f)/this_skczs), klimit)
                        skprice = (skprice*kjs + this_skprice*this_kjs) / (kjs + this_kjs) # 平均持仓价格
                        spoint = skprice + skprice * zs # 持仓均价为新的止损点
                        skccnt += 1
                        print i, 'sk after ', skprice,  spoint, kjs
                

            zjqx.append(zj)
            if sscnt >0:
                kccs.append((zj-zj_init)/sscnt)
            else:
                kccs.append(0)

        self._plot(df, zjqx, kccs)
        print zj-zj_init,(zj-zj_init)/sscnt, kccnt
        return zj-zj_init,(zj-zj_init)/sscnt


    def runhl(self, df, zj=50000, f=0.02, zs=0.02):
        print 'runhl'
        '''
        参数 
        zj 总资金
        zs  开仓止损幅度， 小于1代表开仓价的百分比，等于1表示用开仓当时的较小参数的n天最高最低值
        f  总资金固定百分比风险  每次不能超过这个百分比，没持仓，按照f算能开几手

        保证金为10%
        
        开仓方式， 信号开仓
        平仓方式， 信号平仓， 开仓止损价平仓（zs）
        开仓写在平仓前面，效果是平仓日 不再开仓
        开仓写在平仓后面，效果是平仓日 还能开仓。
        
        '''
        if 'bpsp' not in df.columns:
            print 'df has no bpsp'
            return
        zj_init = zj
        zjqx = [] # 资金曲线，画图用
        kccs = [] # 开仓次数
        kccnt = 0  # 开仓计数
        kjs = 0 # 一次开仓几手
        bs = '' # 表示多头还是空头
        klimit = KLIMIT # 单次交易开仓手数限制， 无限制才厉害,但好像不太现实，
                        # 跑策略时不限制才能看出策略本身好坏
                        # 不限制，时间长一点，可能会有大回撤
        bpoint = 0
        spoint = 0
        sscnt = 0 # 总交易手数计数
        sxfbl = 800 # 手续费比例   
        huadianbl = 500 # 滑点比例
        yinkuilist = [] # 盈亏计数用 [1,0,0,1] 1盈利，0亏损

        for i, bksk in enumerate(df.bksk):
            
            idx = df.index[i]
            bpsp = df.loc[idx, 'bpsp']
            date = df.loc[idx, 'date']

            if bksk=='bk' and kjs==0: # 开多
                if df.loc[idx, 'o'] > df.loc[idx, 'nch']: # 用前n天高价开多
                    bkprice = df.loc[idx, 'o'] # 
                else:  
                    bkprice = df.loc[idx, 'nch']

                if zs<1:
                    bkczs = bkprice * zs *10 # 开仓止损幅度
                    bpoint =bkprice - bkprice * zs # 开仓止损点位
                elif zs >= 1:
                    bpoint = df.loc[df.index[i], 'zsll']  
                    bkczs = (bkprice - bpoint) * 10
                #print bkprice, bkczs, bpoint

                kjs = min(int((zj*f)/bkczs), klimit)  # 这次可开几手
                if kjs > 0:
                    
                    bs = 'b'
                    print i, date, 'bk  ', bkprice, bpoint,kjs, zj
                    kccnt += 1

            if bksk=='sk' and kjs==0:  # 开空
                #skprice = df.loc[idx, 'sdjj']
                # hl用这个开仓价
                if df.loc[idx, 'o'] < df.loc[idx, 'ncl']: # 
                    skprice = df.loc[idx, 'o'] # 
                    #print 'skprice is o'
                else:  
                    skprice = df.loc[idx, 'ncl']
                    #print 'skprice is ncl'

                if zs<1:
                    skczs = skprice * zs * 10# 开仓止损
                    spoint =skprice + skprice * zs # 开仓止损点位
                elif zs>=1:
                    spoint = df.loc[df.index[i], 'zshh'] 
                    skczs = (spoint - skprice) * 10
                #print skprice, skczs, klimit
                kjs = min(int((zj*f)/skczs), klimit)  # 这次可开几手
                if kjs > 0:
                    bs = 's'
                    print i, date, 'sk  ', skprice,  spoint, kjs, zj
                    kccnt += 1

            # 当天开仓的止损
            if bpoint!=0 and kjs!=0 and bs=='b': # 多头止损平仓

                if df.loc[idx, 'l'] <= bpoint:# <= df.loc[idx, 'l']: 
                    
                    if df.loc[idx, 'o'] < bpoint:
                        bpoint = df.loc[idx, 'o']
                    gain = (bpoint  - bkprice) * kjs* 10 # 平仓收益
                    print i,date, '止损bp',bpoint, gain
                    sxf = bkprice/sxfbl * kjs# 
                    hd = bkprice/huadianbl * kjs  # 
                    shouyi = gain - sxf - hd
                    zj += shouyi
                    sscnt += kjs
                    bpoint = 0
                    kjs = 0
                    bs = ''
                    #yinkuilist.append(1) if shouyi > 0 else yinkuilist.append(0)
                    yinkuilist.append((date, 1)) if shouyi > 0 else yinkuilist.append((date, 0))
                    
            if spoint!=0 and kjs!=0 and bs=='s': # 空头止损平仓
                if df.loc[idx, 'h'] >= spoint: 
                    if df.loc[idx, 'o'] > spoint:
                        spoint = df.loc[idx, 'o']
                    gain = (skprice - spoint)  * kjs * 10
                    print i,date, '止损sp', spoint, gain
                    sxf = skprice/sxfbl * kjs# 
                    hd = skprice/huadianbl * kjs  # 
                    shouyi = gain - sxf - hd
                    zj += shouyi
                    sscnt += kjs
                    spoint = 0
                    kjs = 0
                    bs = ''
                    #yinkuilist.append(1) if shouyi > 0 else yinkuilist.append(0)
                    yinkuilist.append((date, 1)) if shouyi > 0 else yinkuilist.append((date, 0))


            if bpsp == 'bp' and kjs != 0 and bs == 'b': # 多头信号平仓(移动止损)
                
                #bpprice = df.loc[idx, 'sdjj']  # 平仓价格  平仓价也应该用最低价，可开仓一样
                if df.loc[idx, 'o'] <= df.loc[idx, 'nclp']: #< df.loc[idx, 'h']: # 
                    bpprice = df.loc[idx, 'o'] # 
                else:  
                    bpprice = df.loc[idx, 'nclp']
                gain = (bpprice  - bkprice) * kjs* 10 # 平仓收益
                print i,date, '信号bp', bpprice, gain
                sxf = bkprice/sxfbl * kjs# 
                hd = bkprice/huadianbl * kjs  # 
                shouyi = gain - sxf - hd
                zj += shouyi
                sscnt += kjs
                bpoint = 0
                kjs = 0
                bs = ''
                #yinkuilist.append(1) if shouyi > 0 else yinkuilist.append(0)
                yinkuilist.append((date, 1)) if shouyi > 0 else yinkuilist.append((date, 0))

            if bpsp == 'sp' and kjs != 0 and bs == 's': # 空头信号平仓

                # spprice = df.loc[idx, 'sdjj']
                if df.loc[idx, 'o'] >= df.loc[idx, 'nchp']:# < df.loc[idx, 'h']: # 
                    spprice = df.loc[idx, 'o'] # 
                else:  
                    spprice = df.loc[idx, 'nchp']
                gain = (skprice - spprice) * kjs * 10 
                print i, date,'信号sp', spprice, gain
                sxf = skprice/sxfbl * kjs# 
                hd = skprice/huadianbl * kjs # 滑点
                shouyi = gain - sxf - hd
                zj += shouyi
                sscnt += kjs
                spoint = 0
                kjs = 0
                bs = ''
                #yinkuilist.append(1) if shouyi > 0 else yinkuilist.append(0)
                yinkuilist.append((date, 1)) if shouyi > 0 else yinkuilist.append((date, 0))
            
            zjqx.append(zj)
            if sscnt >0:
                kccs.append((zj-zj_init)/sscnt)
            else:
                kccs.append(0)

        self._cnt_lianxu_kuisun(yinkuilist)
        #self._cnt_lianxu_kuisun2(yinkuilist)
        self._plot(df, zjqx, kccs)
        print int(zj-zj_init), '平均每手收益：',int((zj-zj_init)/sscnt), '交易次数：',kccnt
        return zj-zj_init,(zj-zj_init)/sscnt

    def _cnt_lianxu_kuisun2(self, yinkuilist):
        #cnts = []
        #cnt = 0
        #for n in yinkuilist:
        #    if n == 0:
        #        cnt += 1
        #    else:
        #        if cnt>0:
        #            cnts.append(cnt)
        #            cnt = 0
        #mean = round(np.mean(cnts), 1)
        #median = np.median(cnts)
        print yinkuilist
        #print cnts
        #print '最大连亏次数:%s, 平均连亏:%s, 连亏中位数:%s' %  (max(cnts) , mean, median) # 

    def _cnt_lianxu_kuisun(self, yinkuilist):
        cnts = []
        cnt = 0
        for n in yinkuilist:
            if n[1] == 0: # 0连亏  1连盈
                cnt += 1
            else:
                if cnt>0:
                    cnts.append(cnt)
                    cnt = 0
        mean = round(np.mean(cnts), 1)
        median = np.median(cnts)
        print yinkuilist
        print cnts
        print '最大连亏次数:%s, 平均连亏:%s, 连亏中位数:%s' %  (max(cnts) , mean, median) # 

    def runhl2(self, df, zj=50000, f=0.01, zs=0.02):
        print 'runhl2'
        '''
        有开仓间隔
        参数 
        zj 总资金
        zs  开仓止损幅度， 小于1代表开仓价的百分比，等于1表示用开仓当时的较小参数的n天最高最低值
        f  总资金固定百分比风险  每次不能超过这个百分比，没持仓，按照f算能开几手

        操作方式，同一方向信号可开仓，每次开一个f的仓位，全部持仓的开仓止损位最近一次开仓的开仓止损，全部平仓后，可开相反方向仓位
        

        '''
        if 'bpsp' not in df.columns:
            print 'df has no bpsp'
            return
        zj_init = zj
        zjqx = [] # 资金曲线，画图用
        kccs = [] # 开仓次数
        kccnt = 0  # 开仓计数
        thiskccnt = 0 # 一次平仓前的开仓次数
        thiskjs = 0 # 一次开仓的开仓手数
        kjs = 0 # 一次开仓几手
        bs = '' # 表示多头还是空头
        klimit = KLIMIT # 单次交易开仓手数限制， 无限制才厉害,但好像不太现实，
                        # 跑策略时不限制才能看出策略本身好坏
                        # 不限制，时间长一点，可能会有大回撤
        skprice = 0
        bkprice = 0
        bpoint = 0
        spoint = 0
        sscnt = 0 # 总交易手数计数
        sxfbl = 200 # 手续费比例   
        huadianbl = 200 # 滑点比例  越是短周期的操作，越是明显  
        # 日内没有手续费和滑点的话，很多办法有很大优势，一有费用就完了
        kclimit = 2 # 同方向开仓次数限制
        jiange = 10 # 两次同向开仓的时间间隔（几根k线）这个无限大就等于runhl
        #jiange_jiage = 0.1 # 两次同向开仓的价格间隔 （跑了前一次开仓的比例）
        bkci = -5
        skci = -5
        this_skprice = 9999999999
        this_bkprice = 0

        for i, bksk in enumerate(df.bksk):
            idx = df.index[i]
            bpsp = df.loc[idx, 'bpsp']

            ccfd = 0.1
            # 持仓跑过一定幅度后，开仓止损移到开仓点,看收盘价
            #if df.loc[idx, 'c'] >= bkprice*(1+ccfd):
#
            #    bpoint = bkprice
            #    print 'new bpoint', bpoint
            #elif df.loc[idx, 'c'] <= skprice*(1-ccfd):
            #    spoint = skprice
            #    print 'new spoint', spoint


            if bpoint!=0 and kjs!=0 and bs=='b': # 多头止损平仓
                if df.loc[idx, 'l'] <= bpoint: 
                    gain = (bpoint  - bkprice) * kjs* 10 # 平仓收益
                    print i, '止损bp', bkprice, gain
                    sxf = bkprice/sxfbl * kjs# 
                    hd = bkprice/huadianbl * kjs  # 
                    zj += gain - sxf - hd
                    sscnt += kjs
                    bpoint = 0
                    kjs = 0
                    bs = ''
                    thiskccnt = 0
                    thiskjs = 0
            if spoint!=0 and kjs!=0 and bs=='s': # 空头止损平仓
                if df.loc[idx, 'h'] >= spoint: 
                    
                    gain = (skprice - spoint)  * kjs * 10
                    print i, '止损sp', skprice, gain
                    sxf = skprice/sxfbl * kjs# 
                    hd = skprice/huadianbl * kjs  # 
                    zj += gain - sxf - hd
                    sscnt += kjs
                    spoint = 0
                    kjs = 0
                    bs = ''
                    thiskccnt = 0
                    thiskjs = 0
            if bpsp == 'bp' and kjs != 0 and bs == 'b': # 多头信号平仓
                #bpprice = df.loc[idx, 'sdjj']  # 平仓价格  平仓价也应该用最低价，可开仓一样
                if df.loc[idx, 'l'] < df.loc[idx, 'nll'] < df.loc[idx, 'h']: # 
                    bpprice = df.loc[idx, 'nll'] # 
                else:  
                    bpprice = df.loc[idx, 'sdjj']
                gain = (bpprice  - bkprice) * kjs* 10 # 平仓收益
                print i, '信号bp', bpprice, gain
                sxf = bkprice/sxfbl * kjs# 
                hd = bkprice/huadianbl * kjs  # 
                zj += gain - sxf - hd
                sscnt += kjs
                bpoint = 0
                kjs = 0
                bs = ''
                thiskccnt = 0
                thiskjs = 0
            if bpsp == 'sp' and kjs != 0 and bs == 's': # 空头信号平仓
                # spprice = df.loc[idx, 'sdjj']
                if df.loc[idx, 'l'] < df.loc[idx, 'nhh'] < df.loc[idx, 'h']: # 用前n天高价开多
                    spprice = df.loc[idx, 'nhh'] # 
                else:  
                    spprice = df.loc[idx, 'sdjj']
                gain = (skprice - spprice) * kjs * 10 
                print i, '信号sp', spprice, gain
                sxf = skprice/sxfbl * kjs# 手续费定为开仓价格的0.1%
                hd = skprice/huadianbl * kjs # 滑点
                zj += gain - sxf - hd
                sscnt += kjs
                spoint = 0
                kjs = 0
                bs = ''
                thiskccnt = 0
                thiskjs = 0
                

            if bksk=='bk' and bs=='b' and thiskccnt < kclimit and i-bkci>=jiange: # 后开  开多 
                if df.loc[idx, 'l'] < df.loc[idx, 'nhh'] < df.loc[idx, 'h']: # 用前n天高价开多
                    this_bkprice = df.loc[idx, 'nhh'] # 这一次的持仓价格
                else:  
                    this_bkprice = df.loc[idx, 'sdjj']
                if zs<1:
                    bkczs = this_bkprice * zs *10 # 开仓止损幅度
                    this_bpoint =this_bkprice - this_bkprice * zs # 开仓止损点位
                    bpoint = this_bpoint # 所有持仓的止损价都变为这次的开仓止损
                    #bpoint = df.loc[idx, 'nllp']  # 用原仓大参数的止损
                elif zs == 1:
                    this_bpoint = df.loc[df.index[i], 'nll']  
                    bpoint = this_bpoint # 所有持仓的止损价都变为这次的开仓止损
                    #bpoint = (this_bkprice + bkprice)/2 # 所有持仓的止损价都变持仓均价
                    bkczs = (this_bkprice - bpoint) * 10
                    #this_bpoint = df.loc[df.index[i+1], 'nll'] # 开仓之后一天，止损设为开仓当天在内的两天的低点
                thiskjs = min(int((zj*f)/bkczs), klimit)  # 这次可开几手
                bkprice = (this_bkprice*thiskjs + bkprice*kjs)/(thiskjs + kjs)
                
                kjs += thiskjs
                bs = 'b'
                print i, 'bk  after ', this_bkprice, bpoint,kjs
                kccnt += 1
                thiskccnt += 1
                bkci = i # 这一次买开仓的index

            if bksk=='sk' and bs=='s' and thiskccnt < kclimit and i-skci>=jiange:  # 后开 开空 
                if df.loc[idx, 'l'] < df.loc[idx, 'nll'] < df.loc[idx, 'h']: # 
                    this_skprice = df.loc[idx, 'nll'] # 
                else:  
                    this_skprice = df.loc[idx, 'sdjj']
                if zs<1:
                    skczs = this_skprice * zs * 10# 开仓止损
                    this_spoint =this_skprice + this_skprice * zs # 开仓止损点位
                    spoint = this_spoint # 所有持仓的止损价都变为这次的开仓止损
                    #spoint = df.loc[idx, 'nhhp'] # 用原仓大参数的止损
                elif zs==1:
                    this_spoint = df.loc[df.index[i], 'nhh']  
                    spoint = this_spoint # 所有持仓的止损价都变为这次的开仓止损
                    #spoint = (this_skprice + skprice)/2 # 所有持仓的止损价都变持仓均价
                    skczs = (spoint - this_skprice) * 10
                    #this_spoint = df.loc[df.index[i+1], 'nhh'] # 开仓之后一天，止损设为开仓当天在内的两天的高点
                
                
                thiskjs = min(int((zj*f)/skczs), klimit)  # 这次可开几手
                skprice = (this_skprice*thiskjs + skprice*kjs)/(thiskjs + kjs)
                kjs += thiskjs
                
                bs = 's'
                print i, 'sk after ', this_skprice,  spoint, kjs
                kccnt += 1
                thiskccnt += 1
                skci = i # 这一次卖开仓的index

            if bksk=='bk' and kjs==0: #  首开 开多
                #bkprice = df.loc[idx, 'sdjj']
                # hl用这个开仓价
                if df.loc[idx, 'l'] < df.loc[idx, 'nhh'] < df.loc[idx, 'h']: # 用前n天高价开多
                    bkprice = df.loc[idx, 'nhh']
                    #bkprice = df.loc[idx, 'nhh']
                else:  
                    bkprice = df.loc[idx, 'sdjj']

                if zs<1:
                    bkczs = bkprice * zs *10 # 开仓止损幅度
                    bpoint =bkprice - bkprice * zs # 开仓止损点位
                elif zs == 1:
                    bpoint = df.loc[df.index[i], 'nll']  
                    bkczs = (bkprice - bpoint) * 10
                    #bpoint = df.loc[df.index[i+1], 'nll'] # 开仓之后一天，止损设为开仓当天在内的两天的低点

                kjs = min(int((zj*f)/bkczs), klimit)  # 这次可开几手
                bs = 'b'
                print i, 'bk  first', bkprice, bpoint,kjs, zj
                kccnt += 1
                bkci = i

            if bksk=='sk' and kjs==0:  # 首开 开空
                #skprice = df.loc[idx, 'sdjj']
                # hl用这个开仓价
                if df.loc[idx, 'l'] < df.loc[idx, 'nll'] < df.loc[idx, 'h']: # 
                    skprice = df.loc[idx, 'nll'] # 
                else:  
                    skprice = df.loc[idx, 'sdjj']

                if zs<1:
                    skczs = skprice * zs * 10# 开仓止损
                    spoint =skprice + skprice * zs # 开仓止损点位
                elif zs==1:
                    spoint = df.loc[df.index[i], 'nhh']  
                    skczs = (spoint - skprice) * 10
                    #spoint = df.loc[df.index[i+1], 'nhh']
                kjs = min(int((zj*f)/skczs), klimit)  # 这次可开几手
                bs = 's'
                print i, 'sk  first', skprice,  spoint, kjs, zj
                kccnt += 1
                skci = i



            # 判断当天开仓 当天止损平仓
            if bpoint!=0 and kjs!=0 and bs=='b': # 多头止损平仓
                if df.loc[idx, 'l'] <= bpoint: 
                    gain = (bpoint  - bkprice) * kjs* 10 # 平仓收益
                    print i, '止损bp', bkprice, gain
                    sxf = bkprice/sxfbl * kjs# 
                    hd = bkprice/huadianbl * kjs  # 
                    zj += gain - sxf - hd
                    sscnt += kjs
                    bpoint = 0
                    kjs = 0
                    bs = ''
                    thiskccnt = 0
                    thiskjs = 0
            if spoint!=0 and kjs!=0 and bs=='s': # 空头止损平仓
                if df.loc[idx, 'h'] >= spoint: 
                    
                    gain = (skprice - spoint)  * kjs * 10
                    print i, '止损sp', skprice, gain
                    sxf = skprice/sxfbl * kjs# 
                    hd = skprice/huadianbl * kjs  # 
                    zj += gain - sxf - hd
                    sscnt += kjs
                    spoint = 0
                    kjs = 0
                    bs = ''
                    thiskccnt = 0
                    thiskjs = 0

            zjqx.append(zj)
            if sscnt >0:
                kccs.append((zj-zj_init)/sscnt)
            else:
                kccs.append(0)
        self._plot(df, zjqx, kccs)
        print int(zj-zj_init), int((zj-zj_init)/sscnt), kccnt
        return zj-zj_init,(zj-zj_init)/sscnt


    def runhl2b(self, df, zj=50000, f=0.01, zs=0.02):
        print 'runhl2b'
        '''
        和runhl2不同处是开仓间隔都一起算，多空之间，前后之间都一起算

        '''
        if 'bpsp' not in df.columns:
            print 'df has no bpsp'
            return
        zj_init = zj
        zjqx = [] # 资金曲线，画图用
        kccs = [] # 开仓次数
        kccnt = 0  # 开仓计数
        thiskccnt = 0 # 一次平仓前的开仓次数
        thiskjs = 0 # 一次开仓的开仓手数
        kjs = 0 # 一次开仓几手
        bs = '' # 表示多头还是空头
        klimit = KLIMIT # 单次交易开仓手数限制， 无限制才厉害,但好像不太现实，
                        # 跑策略时不限制才能看出策略本身好坏
                        # 不限制，时间长一点，可能会有大回撤
        skprice = 0
        bkprice = 0
        bpoint = 0
        spoint = 0
        sscnt = 0 # 总交易手数计数
        sxfbl = 200 # 手续费比例   
        huadianbl = 200 # 滑点比例  越是短周期的操作，越是明显  
        # 日内没有手续费和滑点的话，很多办法有很大优势，一有费用就完了
        kclimit = 3 # 同方向开仓次数限制   一般3好一点
        jiange = 9 # 两次同向开仓的时间间隔（几根k线）
        #jiange_jiage = 0.1 # 两次同向开仓的价格间隔 （跑了前一次开仓的比例）
        kci = -5 # 开仓的index
        this_skprice = 9999999999
        this_bkprice = 0
        #for i, bksk in enumerate(df.bksk): # 减少一些开仓信号
        #    if i%2 == 0:
        #        df.loc[df.index[i], 'bksk'] = ''
        for i, bksk in enumerate(df.bksk):
            idx = df.index[i]
            bpsp = df.loc[idx, 'bpsp']
            if bpoint!=0 and kjs!=0 and bs=='b': # 多头止损平仓
                if df.loc[idx, 'l'] <= bpoint: 
                    gain = (bpoint  - bkprice) * kjs* 10 # 平仓收益
                    print i, '止损bp', bkprice, gain
                    sxf = bkprice/sxfbl * kjs# 
                    hd = bkprice/huadianbl * kjs  # 
                    zj += gain - sxf - hd
                    sscnt += kjs
                    bpoint = 0
                    kjs = 0
                    bs = ''
                    thiskccnt = 0
                    thiskjs = 0

            if bpsp == 'bp' and kjs != 0 and bs == 'b': # 多头信号平仓
                #bpprice = df.loc[idx, 'sdjj']  # 平仓价格  平仓价也应该用最低价，可开仓一样
                if df.loc[idx, 'l'] < df.loc[idx, 'nll'] < df.loc[idx, 'h']: # 
                    bpprice = df.loc[idx, 'nll'] # 
                else:  
                    bpprice = df.loc[idx, 'sdjj']
                gain = (bpprice  - bkprice) * kjs* 10 # 平仓收益
                print i, '信号bp', bpprice, gain
                sxf = bkprice/sxfbl * kjs# 
                hd = bkprice/huadianbl * kjs  # 
                zj += gain - sxf - hd
                sscnt += kjs
                bpoint = 0
                kjs = 0
                bs = ''
                thiskccnt = 0
                thiskjs = 0

            if spoint!=0 and kjs!=0 and bs=='s': # 空头止损平仓
                if df.loc[idx, 'h'] >= spoint: 
                    #print skprice, spoint, kjs
                    gain = (skprice - spoint)  * kjs * 10
                    print i, '止损sp', skprice, gain
                    sxf = skprice/sxfbl * kjs# 
                    hd = skprice/huadianbl * kjs  # 
                    zj += gain - sxf - hd
                    sscnt += kjs
                    spoint = 0
                    kjs = 0
                    bs = ''
                    thiskccnt = 0
                    thiskjs = 0

            if bpsp == 'sp' and kjs != 0 and bs == 's': # 空头信号平仓
                # spprice = df.loc[idx, 'sdjj']
                if df.loc[idx, 'l'] < df.loc[idx, 'nhh'] < df.loc[idx, 'h']: # 用前n天高价开多
                    spprice = df.loc[idx, 'nhh'] # 
                else:  
                    spprice = df.loc[idx, 'sdjj']
                gain = (skprice - spprice) * kjs * 10 
                print i, '信号sp', spprice, gain
                sxf = skprice/sxfbl * kjs# 手续费定为开仓价格的0.1%
                hd = skprice/huadianbl * kjs # 滑点
                zj += gain - sxf - hd
                sscnt += kjs
                spoint = 0
                kjs = 0
                bs = ''
                thiskccnt = 0
                thiskjs = 0
                

            if bksk=='bk' and bs=='b' and thiskccnt < kclimit and i-kci>=jiange: # 后开  开多 
                if df.loc[idx, 'l'] < df.loc[idx, 'nhh'] < df.loc[idx, 'h']: # 用前n天高价开多
                    this_bkprice = df.loc[idx, 'nhh'] # 这一次的持仓价格
                else:  
                    this_bkprice = df.loc[idx, 'sdjj']
                if zs<1:
                    bkczs = this_bkprice * zs *10 # 开仓止损幅度
                    bpoint =this_bkprice - this_bkprice * zs # 开仓止损点位
                elif zs == 1:
                    bpoint = df.loc[df.index[i], 'nll']  
                    bkczs = (this_bkprice - bpoint) * 10
                thiskjs = min(int((zj*f)/bkczs), klimit)  # 这次可开几手
                bkprice = (this_bkprice*thiskjs + bkprice*kjs)/(thiskjs + kjs)
                
                kjs += thiskjs
                #print kjs,'bkjs'
                bs = 'b'
                print i, 'bk  after ', this_bkprice, bpoint,kjs
                kccnt += 1
                thiskccnt += 1
                kci = i # 这一次买开仓的index

            if bksk=='sk' and bs=='s' and thiskccnt < kclimit and i-kci>=jiange:  # 后开 开空 
                if df.loc[idx, 'l'] < df.loc[idx, 'nll'] < df.loc[idx, 'h']: # 
                    this_skprice = df.loc[idx, 'nll'] # 
                else:  
                    this_skprice = df.loc[idx, 'sdjj']
                if zs<1:
                    skczs = this_skprice * zs * 10# 开仓止损
                    spoint =this_skprice + this_skprice * zs # 开仓止损点位
                elif zs==1:
                    spoint = df.loc[df.index[i], 'nhh']  
                    skczs = (spoint - this_skprice) * 10
                thiskjs = min(int((zj*f)/skczs), klimit)  # 这次可开几手
                skprice = (this_skprice*thiskjs + skprice*kjs)/(thiskjs + kjs)
                #print 'skprice', skprice
                
                kjs += thiskjs
                #print kjs,'skjs'
                bs = 's'
                print i, 'sk after ', this_skprice,  spoint, kjs
                kccnt += 1
                thiskccnt += 1
                kci = i # 这一次卖开仓的index

            if bksk=='bk' and kjs==0 and i-kci>=jiange: #  首开 开多
                #bkprice = df.loc[idx, 'sdjj']
                # hl用这个开仓价
                if df.loc[idx, 'l'] < df.loc[idx, 'nhh'] < df.loc[idx, 'h']: # 用前n天高价开多
                    bkprice = df.loc[idx, 'nhh'] # 
                else:  
                    bkprice = df.loc[idx, 'sdjj']

                if zs<1:
                    bkczs = bkprice * zs *10 # 开仓止损幅度
                    bpoint =bkprice - bkprice * zs # 开仓止损点位
                elif zs == 1:
                    bpoint = df.loc[df.index[i], 'nll']
                    bkczs = (bkprice - bpoint) * 10

                kjs = min(int((zj*f)/bkczs), klimit)  # 这次可开几手
                bs = 'b'
                print i, 'bk  first', bkprice, bpoint,kjs
                kccnt += 1
                kci = i

            if bksk=='sk' and kjs==0  and i-kci>=jiange:  # 首开 开空
                #skprice = df.loc[idx, 'sdjj']
                # hl用这个开仓价
                if df.loc[idx, 'l'] < df.loc[idx, 'nll'] < df.loc[idx, 'h']: # 
                    skprice = df.loc[idx, 'nll'] # 
                else:  
                    skprice = df.loc[idx, 'sdjj']

                if zs<1:
                    skczs = skprice * zs * 10# 开仓止损
                    spoint =skprice + skprice * zs # 开仓止损点位
                elif zs==1:
                    spoint = df.loc[df.index[i], 'nhh']  
                    skczs = (spoint - skprice) * 10
                kjs = min(int((zj*f)/skczs), klimit)  # 这次可开几手
                bs = 's'
                print i, 'sk  first', skprice,  spoint, kjs
                kccnt += 1
                kci = i

            # 判断当天开仓 当天平仓
            if bpoint!=0 and kjs!=0 and bs=='b': # 多头止损平仓
                if df.loc[idx, 'l'] <= bpoint: 
                    gain = (bpoint  - bkprice) * kjs* 10 # 平仓收益
                    print i, '止损bp', bkprice, gain
                    sxf = bkprice/sxfbl * kjs# 
                    hd = bkprice/huadianbl * kjs  # 
                    zj += gain - sxf - hd
                    sscnt += kjs
                    bpoint = 0
                    kjs = 0
                    bs = ''
                    thiskccnt = 0
                    thiskjs = 0
            if spoint!=0 and kjs!=0 and bs=='s': # 空头止损平仓
                if df.loc[idx, 'h'] >= spoint: 
                    #print skprice, spoint, kjs
                    gain = (skprice - spoint)  * kjs * 10
                    print i, '止损sp', skprice, gain
                    sxf = skprice/sxfbl * kjs# 
                    hd = skprice/huadianbl * kjs  # 
                    zj += gain - sxf - hd
                    sscnt += kjs
                    spoint = 0
                    kjs = 0
                    bs = ''
                    thiskccnt = 0
                    thiskjs = 0

            zjqx.append(zj)
            if sscnt >0:
                kccs.append((zj-zj_init)/sscnt)
            else:
                kccs.append(0)

        self._plot(df, zjqx, kccs)
        print int(zj-zj_init), int((zj-zj_init)/sscnt), kccnt
        return zj-zj_init,(zj-zj_init)/sscnt


    def _plot(self, df, zjqx, kccs):
        # 开始画资金曲线
        df2 = pd.DataFrame(index=df.date,
                      columns=['total'])
        data = {
            'total' : pd.Series(zjqx, index=df.date),
            }
        
        df2 = pd.DataFrame(data)
        
        # 开始画平均每次开仓盈利
        df3 = pd.DataFrame(index=df.date,
                      columns=['avg'])
        #print index
        data = {
            'avg' : pd.Series(kccs, index=df.date),
            }
        df3 = pd.DataFrame(data)

        df2.plot(x_compat=True)
        plt.show()

class GeneralIndex(General):
    def __init__(self, daima):
        super(GeneralIndex, self).__init__(daima)

    def get_sdjj(self):
        '''
        四点均价  开收盘价，最高价，最低价
        '''
        self.df['sdjj'] = (self.df['o'] + self.df['c'] + self.df['h'] + self.df['l']) / 4

    #def get_ma5(self):
        #df['ma5'] = pd.rolling(self.df.c.shift(-1*5), 5).mean()
        
    #    self.df['ma5'] = self.df.c.rolling(window=5,center=False).mean()

    def get_ma(self, *malist):
        '''get_ma(5,10,20)  得到5,10,20周期的ma
        '''
        for n in malist:
            self.df['ma%s' % n]  = self.df.c.rolling(window=n, center=False).mean()

    def get_ma_sdjj(self, *malist):
        '''四点均价的ma
        '''
        for n in malist:
            self.df['sdjjma%s' % n]  = self.df.sdjj.rolling(window=n, center=False).mean()

    def get_high_percent(self, n):
        '''最高点向下百分比
        '''
        self.df['hp'] = self.df.h * (1 - float(n)/100)

    def get_low_percent(self, n):
        '''最低点向上百分比
        '''
        self.df['lp'] = self.df.l * (1 + float(n)/100)

    def get_atr(self, n):
        '''TR : MAX( MAX( (HIGH-LOW),ABS(REF(CLOSE,1)-HIGH) ), ABS(REF(CLOSE,1)-LOW));文华的公式
        '''
        self.df['hl'] = self.df.h - self.df.l
        self.df['ch'] = abs(self.df.c.shift(1) - self.df.h)
        self.df['cl'] = abs(self.df.c.shift(1) - self.df.l)
        #self.df['tr'] = max(self.df.hl, self.df.ch, self.df.cl)
        #
        self.df['tr'] = self.df.loc[:, ['hl','ch', 'cl']].apply(lambda x: x.max(), axis=1)
        self.df['atr'] = self.df.tr.rolling(window=n, center=False).mean()

    def get_nhh(self, n):
        '''前n天最高价最高点（不包含当天）'''
        self.df['nhh'] = self.df.h.shift(1).rolling(window=n, center=False).max()
    

    def get_lnhh(self, n):
        '''前n天最低价最高点（不包含当天）'''
        self.df['lnhh'] = self.df.l.shift(1).rolling(window=n, center=False).max()

    def get_zshh(self, n):
        '''前n天最高价最高点（不包含当天）(开仓止损用)'''
        self.df['zshh'] = self.df.h.shift(1).rolling(window=n, center=False).max()

    def get_mll(self, m):
        '''后n天最低价最低点（包含当天）'''
        self.df['mll'] = self.df.l.shift(-1*(m-1)).rolling(window=m, center=False).min()

    def get_nhhp(self, n):
        '''前n天最高价最高点（不包含当天）, 平仓用'''
        self.df['nhhp'] = self.df.h.shift(1).rolling(window=n, center=False).max()

    def get_nhh_ma(self, n):
        self.df['nhh_ma']  = self.df.nhh.rolling(window=n, center=False).mean()

    def get_nll(self, n):
        '''前n天最低价最低点（不包含当天）'''
        self.df['nll'] = self.df.l.shift(1).rolling(window=n, center=False).min()

    def get_hnll(self, n):
        '''前n天最高价的最低点（不包含当天）'''
        self.df['hnll'] = self.df.h.shift(1).rolling(window=n, center=False).min()

    def get_zsll(self, n):
        '''前n天最低价最低点（不包含当天）(开仓止损用)'''
        self.df['zsll'] = self.df.l.shift(1).rolling(window=n, center=False).min()
    def get_mhh(self, m):
        '''后n天最高价最高点（包含当天）'''
        self.df['mhh'] = self.df.h.shift(-1*(m-1)).rolling(window=m, center=False).max()

    def get_nllp(self, n):
        '''前n天最低价最低点（不包含当天）, 平仓用'''
        self.df['nllp'] = self.df.l.shift(1).rolling(window=n, center=False).min()

    def get_nll_ma(self, n):
        self.df['nll_ma'] = self.df.nll.rolling(window=n, center=False).mean()

    def get_nsdh(self, n):
        '''前n天四点均价最高点（不包含当天）'''
        self.df['nsdh'] = self.df.sdjj.shift(1).rolling(window=n, center=False).max()

    def get_nsdl(self, n):
        '''前n天四点均价最低点（不包含当天）'''
        self.df['nsdl'] = self.df.sdjj.shift(1).rolling(window=n, center=False).min()

    def get_nsdhp(self, n):
        '''前n天四点均价最高点（不包含当天） 平仓用'''
        self.df['nsdhp'] = self.df.sdjj.shift(1).rolling(window=n, center=False).max()

    def get_nsdlp(self, n):
        '''前n天四点均价最低点（不包含当天） 平仓用'''
        self.df['nsdlp'] = self.df.sdjj.shift(1).rolling(window=n, center=False).min()

    def get_nch(self, n):
        '''前n天c最高点（不包含当天）'''
        self.df['nch'] = self.df.c.shift(1).rolling(window=n, center=False).max()

    def get_nchp(self, n):
        '''前n天c最高点（不包含当天）, 平仓用'''
        self.df['nchp'] = self.df.c.shift(1).rolling(window=n, center=False).max()

    def get_ncl(self, n):
        '''前n天c的最低点（不包含当天）'''
        self.df['ncl'] = self.df.c.shift(1).rolling(window=n, center=False).min()

    def get_nclp(self, n):
        '''前n天c最低点（不包含当天）, 平仓用'''
        self.df['nclp'] = self.df.c.shift(1).rolling(window=n, center=False).min()


def rangerun(foo):
    '''选择最优参数, 画图看起来清晰'''
    r1 = range(11, 15)   # max 11 到 15， 
    r2 = range(11,15, 1)# max 11 到 15
    index = []
    total = []
    avg = []
    for a in r1:
        for b in r2:
            index.append('%s-%s' % (a, b))
            #print a, b
            rtn = foo(a,b)

            total.append(rtn[0])
            avg.append(rtn[1])
    df = pd.DataFrame(index=index,
                  columns=['total', 'avg'])
    #print index
    data = {
        'total' : pd.Series(total, index=index),
        'avg' : pd.Series(avg, index=index)
        }
    
    df = pd.DataFrame(data)
    df['avg'] = df.avg*100
    print df
    df.plot();plt.show()


def rangerun3(foo, r1, r2):
    '''选择最优参数, 画图看起来清晰,  跑run3的结果

    先用这个函数选择优势的参数， 然后用这个参数看具体的资金曲线，回撤什么的

    跑了几次，结果， 相同的策略不同的品种结果不一样， 发现没有最优参数
    '''
    #r1 = range(1,17)   # max 11 到 15， 
    #r2 = range(1,17, 1)# max 11 到 15
    index = []
    zj = []

    for a in r1:
        for b in r2:
            index.append('%s-%s' % (a, b))
            #print a, b
            rtn = foo(a,b)
            zj.append(rtn)
            
    df = pd.DataFrame(index=index,
                  columns=['zj'])
    #print index
    data = {
        'zj' : pd.Series(zj, index=index),
        
        }
    
    df = pd.DataFrame(data)
    #print df
    df.plot();plt.show()


if __name__ == '__main__':

    #g = General('rb')
    #g.foo()
    gi = GeneralIndex('rb')
    #gi.get_atr(99)
    #gi.df.to_csv('tmp.csv')
    #print gi.df['sdjj']
    #gi.get_ma5()
    #print gi.df.loc[:, ['c','ma5']]
    #print gi.df.describe()
    #gi.sdjj
    #gi.get_ma(5,10,20)
    
    #print gi.df.loc[:,['c','ma5', 'ma10', 'ma20']]
    #gi.get_nsdl(10)
    #print gi.df.loc[:, ['date','sdjj','nsdl']]
    #print gi.df.describe()

