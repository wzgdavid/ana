# encoding: utf-8
#import sys
#sys.path.append("..")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


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

    def run3b(self, df, zj=50000, f=0.02, zs=0.02):
        '''带开仓止损的资金管理，没资金管理跑出来的曲线不现实
        
        资金管理方式，有持仓不开仓(加仓)，不对冲，没持仓，按照f算能开几手
        zj 总资金
        zs  开仓止损幅度， 如果是小于1，代表开仓价的百分比， 如果是整数，代表几个atr（100天参数）
        f  总资金固定百分比风险  每次不能超过这个百分比
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
        klimit = 999999999 # 单次交易开仓手数限制， 无限制才厉害,但好像不太现实，
                        # 跑策略时不限制才能看出策略本身好坏
                        # 不限制，时间长一点，可能会有大回撤
        bpoint = 0
        spoint = 0
        # 做多
        for i, bksk in enumerate(df.bksk):
            
            idx = df.index[i]
            bpsp = df.loc[idx, 'bpsp']

            if bpoint!=0 and kjs!=0 and bs=='b': # 多头止损平仓
                if df.loc[idx, 'l'] <= bpoint: 
                    gain = (bpoint  - bkprice) * kjs* 10 # 平仓收益
                    print '止损bp', gain
                    sxf = bkprice/1000 * kjs# 手续费定为开仓价格的0.1%
                    hd = bkprice/100 * kjs  # 滑点定为1%
                    zj += gain - sxf - hd
                    ibcnt += kjs
                    bpoint = 0
                    kjs = 0
                    bs = ''
                    #continue

            if bpsp == 'bp' and kjs != 0 and bs == 'b': # 多头信号平仓
                
                # 在开仓的index到平仓信号的index间，检查是否碰到开仓止损
                # 如果最低点小于买开仓止损，则以最低点平仓
                #bmin = df.loc[bki:i,'l'].min()  # 买开仓之后的最低点
                # 买开仓止损的点位
                #if bmin <= bpoint: # 碰到止损   平仓
                #    gain = (bpoint  - bkprice) * kjs* 10 # 平仓收益
                #    print '止损bp', gain 
                #else: # 信号平仓
                bpprice = df.loc[idx, 'sdjj']  # 平仓价格
                gain = (bpprice  - bkprice) * kjs* 10 # 平仓收益
                print '信号bp', bpprice, gain
                sxf = bkprice/1000 * kjs# 手续费定为开仓价格的0.1%
                hd = bkprice/100 * kjs  # 滑点定为1%
                zj += gain - sxf - hd
                ibcnt += kjs
                bpoint = 0
                kjs = 0
                bs = ''
                #print zj
                #continue

            if spoint!=0 and kjs!=0 and bs=='s': # 空头止损平仓
                if df.loc[idx, 'h'] >= spoint: 
                    gain = (skprice - spoint)  * kjs * 10
                    print '止损sp', gain
                    sxf = skprice/1000 * kjs# 手续费定为开仓价格的0.1%
                    hd = skprice/100 * kjs  # 滑点定为1%
                    zj += gain - sxf - hd
                    ibcnt += kjs
                    spoint = 0
                    kjs = 0
                    bs = ''
                    #continue

            if bpsp == 'sp' and kjs != 0 and bs == 's': # 空头信号平仓
                #smax = df.loc[ski:i,'h'].max()  # 卖开仓之后  价格的最高点
                #if smax >= spoint:
                #    gain = (skprice - spoint)  * kjs * 10
                #    print '止损sp', gain
                #else:
                spprice = df.loc[idx, 'sdjj']
                gain = (skprice - spprice) * kjs * 10 
                print '信号sp', spprice, gain
                sxf = skprice/1000 * kjs# 手续费定为开仓价格的0.1%
                hd = skprice/100 * kjs # 滑点
                zj += gain - sxf - hd
                iscnt += kjs
                spoint = 0
                kjs = 0
                bs = ''
                
            if bksk=='bk' and kjs==0: # 开多
               
                bkprice = df.loc[idx, 'sdjj']
                #print bkprice
                if zs < 1: # 百分比开仓止损
                    bkczs = bkprice * zs *10 # 开仓止损幅度
                    bpoint =bkprice - bkprice * zs # 开仓止损点位
                else: # atr开仓止损
                    bkczs = df.loc[idx, 'atr'] * zs * 10 # 开仓止损幅度
                    
                    bpoint =bkprice - df.loc[idx, 'atr'] # 开仓止损点位
                kjs = min(int((zj*f)/bkczs), klimit)  # 这次可开几手, 最大限制100手
                bs = 'b'
                bki = i
                print 'bk  ', bkprice, bpoint,kjs
                kccnt += 1
                #kccs.append(kccnt)

            if bksk=='sk' and kjs==0:  # 开空
                
           
                skprice = df.loc[idx, 'sdjj']
                if zs < 1:
                    skczs = skprice * zs * 10# 开仓止损
                    spoint =skprice + skprice * zs # 开仓止损点位
                else:
                    #print 'atr', df.loc[idx, 'atr']
                    skczs = df.loc[idx, 'atr'] * zs * 10 # 开仓止损幅度
                    spoint =skprice + df.loc[idx, 'atr'] # 开仓止损点位
                kjs = min(int((zj*f)/skczs), klimit)  # 这次可开几手
                bs = 's'
                ski = i
                print 'sk  ', skprice,  spoint, kjs
                # keyong = zj - chicang
                kccnt += 1
            zjqx.append(zj)
            if kccnt >0:
                kccs.append((zj-zj_init)/kccnt)
            else:
                kccs.append(0)
                #print zj
        #avg = zj/(ibcnt + iscnt)
        
        # 开始画资金曲线
        df2 = pd.DataFrame(index=df.date,
                      columns=['total'])
        #print index
        data = {
            'total' : pd.Series(zjqx, index=df.date),
            
            }
        
        df2 = pd.DataFrame(data)
        #print df
        
        # 开始画平均每次开仓盈利
        df3 = pd.DataFrame(index=df.date,
                      columns=['avg'])
        #print index
        data = {
            'avg' : pd.Series(kccs, index=df.date),
            
            }
        
        df3 = pd.DataFrame(data)
        #print df
        df2.plot();plt.show()
        #df3.plot();plt.show()
        return zj


    def run4(self, df, zj=100000, f=0.06, zs=0.02, ydzs=0.06):
        '''
        资金管理方式，有持仓不开仓(加仓)，不对冲，没持仓，按照f算能开几手
        zj 总资金
        zs  开仓止损幅度， 代表开仓价的百分比，
        f  总资金固定百分比风险  每次不能超过这个百分比
        保证金为10%
    
        开仓方式， 信号开仓
        平仓方式，  开仓止损价平仓（zs）,移动止损平仓（ydzs）
        开仓写在平仓前面，效果是平仓日 不再开仓
        开仓写在平仓后面，效果是平仓日 还能开仓。 跑下来好像这个收益高

        跑下来还是信号平仓的效果好啊，再花点时间研究研究
        '''
        zj_init = zj
        zjqx = [] # 资金曲线，画图用
        kccs = [] # 开仓次数
        kccnt = 0  # 开仓计数
        ibcnt = 0 # 买开仓手数
        iscnt = 0 # 卖开仓手数
        kjs = 0 # 一次开仓几手
        bs = '' # 表示多头还是空头
        klimit = 999999999 # 单次交易开仓手数限制， 无限制才厉害,但好像不太现实，
        bpoint = 0
        spoint = 0
        byd_point = 0 # 多头移动止损
        syd_point = 0 # 空头移动止损
        newhigh = 0 # 多头开仓之后，点位的新高
        newlow = 0 # 空头开仓之后，点位的新低
        # 做多
        for i, bksk in enumerate(df.bksk):
            
            idx = df.index[i]
            bpsp = df.loc[idx, 'bpsp']

            if bpoint!=0 and kjs!=0 and bs=='b': # 多头止损平仓
                byd_point = max(byd_point, df.loc[idx, 'h'] * (1-ydzs)) #
                bzs = max(bpoint, byd_point)
                print 'byd_point', byd_point, bpoint
                if df.loc[idx, 'l'] <= bzs: 
                    gain = (bzs  - bkprice) * kjs* 10 # 平仓收益
                    print '止损bp', bzs, gain
                    sxf = bkprice/1000 * kjs# 手续费定为开仓价格的0.1%
                    hd = bkprice/100 * kjs  # 滑点定为1%
                    zj += gain - sxf - hd
                    ibcnt += kjs
                    bpoint = 0
                    byd_point = 0
                    kjs = 0
                    bs = ''

            if spoint!=0 and kjs!=0 and bs=='s': # 空头止损平仓
                syd_point = min(syd_point, df.loc[idx, 'l'] * (1+ydzs)) #
                szs = min(spoint, syd_point)
                print 'syd_point', syd_point
                if df.loc[idx, 'h'] >= szs: 
                    gain = (skprice - szs)  * kjs * 10
                    print '止损sp', szs, gain
                    sxf = skprice/1000 * kjs# 手续费定为开仓价格的0.1%
                    hd = skprice/100 * kjs  # 滑点定为1%
                    zj += gain - sxf - hd
                    ibcnt += kjs
                    spoint = 0
                    syd_point = 0
                    kjs = 0
                    bs = ''
                 
            if bksk=='bk' and kjs==0: # 开多
                bkprice = df.loc[idx, 'sdjj']
                if zs < 1: # 百分比开仓止损
                    bkczs = bkprice * zs *10 # 开仓止损幅度
                    bpoint =bkprice - bkprice * zs # 开仓止损点位
                else: # atr开仓止损
                    bkczs = df.loc[idx, 'atr'] * zs * 10 # 开仓止损幅度
                    bpoint =bkprice - df.loc[idx, 'atr'] # 开仓止损点位
                kjs = min(int((zj*f)/bkczs), klimit)  # 这次可开几手, 最大限制100手
                byd_point = df.loc[idx, 'h'] * (1-ydzs)
                bs = 'b'
                bki = i
                print 'bk  ', bkprice, bpoint,kjs
                kccnt += 1

            if bksk=='sk' and kjs==0:  # 开空
                skprice = df.loc[idx, 'sdjj']
                if zs < 1:
                    skczs = skprice * zs * 10# 开仓止损
                    spoint =skprice + skprice * zs # 开仓止损点位
                else:
                    skczs = df.loc[idx, 'atr'] * zs * 10 # 开仓止损幅度
                    spoint =skprice + df.loc[idx, 'atr'] # 开仓止损点位
                kjs = min(int((zj*f)/skczs), klimit)  # 这次可开几手
                syd_point = df.loc[idx, 'l'] * (1+ydzs)
                bs = 's'
                ski = i
                print 'sk  ', skprice,  spoint,kjs

                kccnt += 1
            zjqx.append(zj)
            if kccnt >0:
                kccs.append((zj-zj_init)/kccnt)
            else:
                kccs.append(0)

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

        df2.plot();plt.show()
        #df3.plot();plt.show()
        return zj


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

    def get_nll(self, n):
        '''前n天最低价最低点（不包含当天）'''
        self.df['nll'] = self.df.l.shift(1).rolling(window=n, center=False).min()

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

    跑了几次，结果， 相同的策略不同的品种结果不一样， 没有最优参数
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
