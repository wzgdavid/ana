# encoding: utf-8
import sys
sys.path.append("..")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from general_index import General, GeneralIndex, rangerun, rangerun3
from copy import deepcopy
import util

class Celue(GeneralIndex):
    def __init__(self, daima):
        super(Celue, self).__init__(daima)
        self.get_sdjj()


    def zdzy_hl(self, ydzs=False):
        '''主动止损主动止盈
        ydzs 是否有移动止损，结果显示，不要移动止损 好
        '''
        self.get_nhh(2)
        self.get_nll(2)
        self.get_nlh(2)
        self.get_nhl(2)
        self.get_nch(2)
        self.get_ncl(2)
        self.get_nhhp(7)
        self.get_nllp(7)

        self.get_mhh(7)
        self.get_mll(7)
        self.get_atr(50)
        #zy = 2
        #zs = 2
        zy = 0.02
        zs = 0.02 
        ma = 20
        ma_name = 'ma'+str(ma)
        ma2 = 5
        ma2_name = 'ma'+str(ma2)
        self.get_ma(ma, ma2)
        df = deepcopy(self.df)
        option = {
            'tupo_high': df.h > df.nhh,
            'tupo_low': df.l < df.nll,
            'tupo_high_c': df.h > df.nch,
            'tupo_low_c': df.l < df.ncl,  
            'tupo_high2': df.h > df.nlh,
            'tupo_low2': df.l < df.nhl,
            'gdd_low_last':(df.l.shift(3) > df.l.shift(2)) & (df.l.shift(1) > df.l.shift(2)), 
            'gdd_high_last': (df.h.shift(3) < df.h.shift(2)) & (df.h.shift(1) < df.h.shift(2)),
            'gdd_low_last2':(df.l.shift(4) > df.l.shift(3)) & (df.l.shift(2) > df.l.shift(3)),
            'gdd_high_last2': (df.h.shift(4) < df.h.shift(3)) & (df.h.shift(2) < df.h.shift(3)),
            'last_lowpoint':df.l.shift(1) < df.l.shift(2),
            'last_highpoint':df.h.shift(1) > df.h.shift(2),
            'low_1liangao':df.l.shift(1) > df.l.shift(2),
            'high_1liandi': df.h.shift(1) < df.h.shift(2),
            'low_2liangao':(df.l.shift(2) > df.l.shift(3)) & (df.l.shift(1) > df.l.shift(2)),
            'high_2liandi': (df.h.shift(2) < df.h.shift(3)) & (df.h.shift(1) < df.h.shift(2)),
            'low_3liangao':(df.l.shift(2) > df.l.shift(3)) & (df.l.shift(1) > df.l.shift(2)) & (df.l.shift(3) > df.l.shift(4)),
            'high_3liandi': (df.h.shift(2) < df.h.shift(3)) & (df.h.shift(1) < df.h.shift(2)) & (df.h.shift(3) < df.h.shift(4)),
            'higher_than_ma': df.l > df[ma_name],
            'lower_than_ma': df.h < df[ma_name],
            'higher_than_ma_lastday': df.l.shift(1) > df[ma_name].shift(1),
            'lower_than_ma_lastday': df.h.shift(1) < df[ma_name].shift(1),
            'close_higher_than_ma': df.c > df[ma_name],
            'close_lower_than_ma': df.c < df[ma_name],
            'close_higher_than_ma_lastday': (df.c.shift(1) > df[ma_name]),
            'close_lower_than_ma_lastday': (df.c.shift(1) < df[ma_name]),
            'close_higher_than_ma_lastday_1st': (df.c.shift(1) > df[ma_name]) & (df.c.shift(2) < df[ma_name]),
            'close_lower_than_ma_lastday_1st': (df.c.shift(1) < df[ma_name]) & (df.c.shift(2) > df[ma_name]),
            'bigger_than_nch': df.c > df.nch,
            'lower_than_ncl': df.c < df.ncl,
            'close_bigger_than_nch_lastday': df.c.shift(1) > df.nch.shift(1),
            'close_lower_than_ncl_lastday': df.c.shift(1) < df.ncl.shift(1),
            'bigger_than_nhh_lastday': df.c.shift(1) > df.nhh.shift(1),
            'lower_than_nll_lastday': df.c.shift(1) < df.nll.shift(1),

            'maup': df[ma_name] > df[ma_name].shift(1),
            'madown': df[ma_name] < df[ma_name].shift(1),
            'maup_lastday': df[ma_name].shift(1) > df[ma_name].shift(2),
            'madown_lastday': df[ma_name].shift(1) < df[ma_name].shift(2),
            '1liangyang':df.c > df.o,
            '1lianyin':df.c < df.o,
            'last_yang':df.c.shift(1) > df.o.shift(1),
            'last_yin':df.c.shift(1) < df.o.shift(1),
            'last_yy':df.c.shift(1) == df.o.shift(1),
            '2liangyang': (df.c > df.o) & (df.c.shift(1) > df.o.shift(1)),
            '2lianyin': (df.c < df.o) & (df.c.shift(1) < df.o.shift(1)),
            '2liangyang_lastday': (df.c.shift(1) > df.o.shift(1)) & (df.c.shift(2) > df.o.shift(2)),
            '2lianyin_lastday': (df.c.shift(1) < df.o.shift(1)) & (df.c.shift(2) < df.o.shift(2)),
            '3liangyang': (df.c > df.o) & (df.c.shift(1) > df.o.shift(1)) & (df.c.shift(2) > df.o.shift(2)),
            '3lianyin': (df.c < df.o) & (df.c.shift(1) < df.o.shift(1)) & (df.c.shift(2) < df.o.shift(2)),
            'high_2liangao':(df.h.shift(2) > df.h.shift(3)) & (df.h.shift(1) > df.h.shift(2)),
            'low_2liandi': (df.l.shift(2) < df.l.shift(3)) & (df.l.shift(1) < df.l.shift(2)),

            'duo_huitiao': (df.c < df[ma2_name]),         
            'kong_huitiao': (df.c > df[ma2_name]),  
                  }
        df['higher'] = option['tupo_high']  & option['higher_than_ma_lastday'] #& option['last_yin']
        df['lower'] = option['tupo_low'] & option['lower_than_ma_lastday']  #& option['last_yang'] 
        #df['higher'] = option['tupo_high'] & option['close_bigger_than_nch_lastday'] #& option['close_higher_than_ma_lastday']
        #df['lower'] = option['tupo_low'] & option['close_lower_than_ncl_lastday'] #& option['close_lower_than_ma_lastday']
        df['bksk'] = np.where(df['higher'] & df.atr, 'bk', None)
        df['bksk'] = np.where(df['lower'] & df.atr, 'sk', df['bksk'])
        #df['bksk'] = np.where(df['lower'] & df.atr, 'sk', None)
        df.to_csv('tmp.csv')
        self._run_zdzy(df, zy, zs, ydzs)
        
        
    def _get_hl_bkpoint(self, df, idx):
        ''''''
        nhh = df.loc[idx, 'nhh']
        o = df.loc[idx, 'o']
        return o if o > nhh else nhh

    def _get_hl2_bkpoint(self, df, idx):
        ''''''
        nlh = df.loc[idx, 'nlh']
        o = df.loc[idx, 'o']
        return o if o > nlh else nlh

    def _get_chl_bkpoint(self, df, idx):
        ''''''
        nch = df.loc[idx, 'nch']
        o = df.loc[idx, 'o']
        return o if o > nch else nch

    def _get_hl_skpoint(self, df, idx):
        nll = df.loc[idx, 'nll']
        o = df.loc[idx, 'o']
        return o if o < nll else nll

    def _get_hl2_skpoint(self, df, idx):
        nhl = df.loc[idx, 'nhl']
        o = df.loc[idx, 'o']
        return o if o < nhl else nhl

    def _get_chl_skpoint(self, df, idx):
        ncl = df.loc[idx, 'ncl']
        o = df.loc[idx, 'o']
        return o if o < ncl else ncl

    def _tongjilist(self, lst, zy=1, zs=1):
        #print sorted([round(x,3) for x in lst])
        m = np.mean(lst)
        s = np.std(lst)
        y = s/m
        print '均值:', round(m, 4)
        #print '标准差:', round(s, 4)
        #print '标准差/均值:', round(y, 4)
        
        #print sorted(lst)
        bigthanone = [n for n in lst if n > 1]
        srate = len(bigthanone) / float(len(lst))
        print 'success rate:', round(srate, 2) 
        #print 'exp', round(zy*srate-zs*(1-srate), 4)
        self._plot_cummulti(lst)
        return m, s, y
        
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

    def _run_zdzy(self, df, zy, zs, ydzs):
        move_len = 99
        bzlist = []
        move_i = 0
        move_j = 0
        last_bksk = 0
        for i, bksk in enumerate(df.bksk):
            #if i <= move_i: # 有持仓时不开仓, 
            #    continue
            if i <= move_j + 1: # 前一次开仓后1天里不开仓
                continue

            if i+move_len > len(df.bksk):
                break
            
            r = range(i+1, i+move_len)
            idx = df.index[i]

            if bksk == 'bk':
                move_j = i
                #print i                 
                bkpoint = self._get_hl_bkpoint(df, idx)
                #bkpoint = df.loc[idx, 'o']
                #if last_bksk != 0 and bkpoint/last_bksk < 1.005:
                #    continue
                #last_bksk = bkpoint
                nhh = df.loc[idx, 'nhh']

                atr = df.loc[idx, 'atr']
                if not atr:
                    atr = bkpoint * 0.015
                if zs < 1: # 百分比
                    zypoint = bkpoint * (1+zy)
                    zspoint = bkpoint * (1-zs)
                    #zypoint = nhh * (1+zy)
                    #zspoint = nhh * (1-zs)
                else: # atr 止盈止损
                    zypoint = bkpoint + atr * zy
                    zspoint = bkpoint - atr * zs
                    zy = atr * zy / float(bkpoint)
                    zs = atr * zs / float(bkpoint)
                for j in r:
                    move_low = df.loc[df.index[j], 'l']
                    move_high = df.loc[df.index[j], 'h']
                    #print i,j, bkpoint, zypoint, zspoint, move_low, move_high
                    o = float(df.loc[df.index[j], 'o'])

                    # 先止盈后止损 和先止损后止盈效果有区别
                    if move_low <= zspoint:
                        if o > zspoint:
                            bzlist.append(zspoint/bkpoint)
                        else:
                            bzlist.append(o/bkpoint)
                        move_i = j
                        break
                    if move_high >= zypoint:
                        if o < zypoint:
                            bzlist.append(zypoint/bkpoint)
                        else:
                            bzlist.append(o/bkpoint)
                        move_i = j
                        break

                    if ydzs: 
                        nllp = df.loc[df.index[j], 'nllp']
                        if move_low <= nllp:

                            if o > zspoint:
                                bzlist.append(nllp/bkpoint)
                            else:
                                bzlist.append(o/bkpoint)
                            break

                          

            if bksk == 'sk':
                #print i
                move_j = i 
                skpoint = self._get_hl_skpoint(df, idx)
                #skpoint = df.loc[idx, 'o']
                #if last_bksk != 0 and skpoint/last_bksk > 0.995:
                #    continue
                #last_bksk = skpoint
                nll = df.loc[idx, 'nll']
                atr = df.loc[idx, 'atr']
                if not atr:
                    atr = skpoint * 0.015
                if zs < 1 and zy<1: # 百分比
                    zypoint = skpoint * (1-zy)
                    zspoint = skpoint * (1+zs)
                    #zypoint = nll * (1-zy)
                    #zspoint = nll * (1+zs)
                else: # atr 止盈止损
                    zypoint = skpoint - atr*zy
                    zspoint = skpoint + atr*zs
                    zy = atr*zy / float(skpoint)
                    zs = atr*zs / float(skpoint)
                for j in r:
                    
                    move_low = df.loc[df.index[j], 'l']
                    move_high = df.loc[df.index[j], 'h']
                    o = float(df.loc[df.index[j], 'o'])
                    #print i,j, bkpoint, zypoint, zspoint, move_low, move_high
                    if move_high >= zspoint:
                        if o < zspoint:
                            bzlist.append(skpoint/zspoint)
                        else:
                            bzlist.append(skpoint/o)
                        move_i = j
                        break
                    if move_low <= zypoint:
                        
                        if o > zypoint:
                            bzlist.append(skpoint/zypoint)
                        else:
                            bzlist.append(skpoint/o)
                        move_i = j
                        break

                    if ydzs:
                        nhhp = df.loc[df.index[j], 'nhhp']
                        if move_high >= nhhp:
                            if o < zspoint:
                                bzlist.append(skpoint/nhhp)
                            else:
                                bzlist.append(skpoint/o)
                            break
        #print 'sortedbzlist', sorted(bzlist)
        self._cnt_lianxu_kuisun2(bzlist)
        return self._tongjilist(bzlist,zy,zs)


    def _run_zdzy2(self, df, zy, zs, ydzs):
        '''带资金管理'''
        move_len = 99
        zj = 100000
        f0 = 0.04
        f = f0
        zjqx = [zj]
        gain = 0
        move_i = 0
        klimit = 9999999
        cnts = [] # 连亏计数
        cnt = 0 # 连亏计数
        cnt2 = 0 # 连盈计数
        feiyong = 0.02 # 费用包括滑点，手续费
        zy0 = zy
        for i, bksk in enumerate(df.bksk):
            #print move_i
            #if i <= move_i: # 有持仓时不开仓, 
            #    continue
            #if i <= move_i + 1: # 前一次开仓后1天里不开仓
            #    continue
            if i+move_len > len(df.bksk):
                break
            '''开仓资金策略选其一或者不选'''
            kccl =0
            if kccl == 1:
                # 连盈时，f变大
                if cnt2 >=4:
                    f = f0 * 4
                elif cnt2 >= 3: 
                    f = f0 * 3
                elif cnt2 >= 2: 
                    f = f0 * 2
                elif cnt2 >= 1: 
                    f = f0 * 1
                else:
                    f = f0
            elif kccl == 2:
                # 连盈时，zy变大
                if cnt2 >=4:
                    zy = zy0 * 1.4
                elif cnt2 >= 3: 
                    zy = zy0 * 1.3
                elif cnt2 >= 2: 
                    zy = zy0 * 1.2
                elif cnt2 >= 1: 
                    zy = zy0 * 1.1
                else:
                    zy = zy0        


            r = range(i+1, i+move_len)
            idx = df.index[i]
            date = df.loc[idx, 'date']
            if bksk == 'bk':
               

                bkpoint = self._get_hl_bkpoint(df, idx)
                bkczs = bkpoint * zs *10 # 开仓止损幅度
                kjs = min(int((zj*f)/bkczs), klimit) # 开几手
                zypoint = bkpoint * (1+zy)
                zspoint = bkpoint * (1-zs)
                #print zy
                for j in r:
                    move_low = df.loc[df.index[j], 'l']
                    move_high = df.loc[df.index[j], 'h']
                    #print i,j, bkpoint, zypoint, zspoint, move_low, move_high
                    o = float(df.loc[df.index[j], 'o'])
                    if move_low <= zspoint:
                        if o > zspoint:
                            gain = (zspoint - bkpoint) * kjs* 10 # 平仓收益
                        else:
                            gain = (o - bkpoint) * kjs* 10 # 平仓收益
                        
                        cnt += 1
                        cnt2 = 0
                        zj += gain *(1+feiyong)
                        break
                    if move_high >= zypoint:
                        if o < zypoint:
                            gain = (zypoint - bkpoint) * kjs* 10 # 平仓收益
                        else:
                            gain = (o - bkpoint) * kjs* 10 # 平仓收益
                        move_i = j
                        if cnt>0:
                            cnts.append(cnt)
                            if cnt > 5: # 看连亏数多，是什么情况
                                print date
                            cnt = 0
                        cnt2 += 1
                        zj += gain *(1-feiyong)
                        break
                
                zjqx.append(zj)
            if bksk == 'sk':
                skpoint = self._get_hl_skpoint(df, idx)
                skczs = skpoint * zs * 10# 开仓止损
                kjs = min(int((zj*f)/skczs), klimit)
                zypoint = skpoint * (1-zy)
                zspoint = skpoint * (1+zs)
                for j in r:
                    move_low = df.loc[df.index[j], 'l']
                    move_high = df.loc[df.index[j], 'h']
                    o = float(df.loc[df.index[j], 'o'])
                    if move_high >= zspoint:
                        if o < zspoint:
                            gain = (skpoint - zspoint) * kjs* 10
                        else:
                            gain = (skpoint - o) * kjs* 10
                        move_i = j
                        cnt += 1
                        cnt2 =0
                        zj += gain*(1+feiyong)
                        break
                    if move_low <= zypoint:
                        if o > zypoint:
                            gain = (skpoint - zypoint) * kjs* 10
                        else:
                            gain = (skpoint - o) * kjs* 10
                        move_i = j
                        if cnt>0:
                            cnts.append(cnt)
                            if cnt > 5: # 看连亏数多，是什么情况
                                print date
                            cnt = 0
                        cnt2 += 1
                        zj += gain*(1-feiyong)
                        break
                
                zjqx.append(zj)
            #zjqx.append(zj)
        print zj
        #print zjqx

        print 'sorted_cnts', sorted(cnts) # 连亏计数
        data = {
            'total' : pd.Series(zjqx),
            }
        df2 = pd.DataFrame(data)
        df2.plot(x_compat=True)
        plt.show()
        return 


if __name__ == '__main__':
    
    #test()
    #run_ev_tupohl('ta')
    g = Celue('m') # ta rb c m a ma jd dy sr cs 999999
    #g.tupohl(3, 7, 1)
    #g.ev_ma(20,0.03)
    #g.ev_tupohl(3, 7, 0.01)
    #g.ev_tupohl(3, 17, 1) 
    #g.ev_tupohl(3, 17, 1)

    #g.zhisungailv()

    g.zdzy_hl(ydzs=0)
   
    

    