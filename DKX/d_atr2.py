
'''
在d_atr.py的基础上，再加上周线DKX顺势的过滤
'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from common import *#get_DKX, get_nhh, get_nll, get_ma, avg,get_nhhzs,get_nllzs,get_atr

pinzhong = 'y'
plt.rcParams['font.sans-serif'] = ['SimHei'] # 正常显示中文
if pinzhong == 'rb':
    df = pd.read_csv(r'..\data\rb\zs.csv')
else:
    df = pd.read_csv(r'..\data\{}.csv'.format(pinzhong))
df = get_DKX(df)
df = get_nhh(df, 2)
df = get_nll(df, 2)
df = get_ma(df, 20)

df = get_atr(df, 50)
'''
--------------------------趋势判断1---------------------------------
'''

df['日线DKX斜率'] = df.b.shift(1) / df.b.shift(2) 

df.index = pd.DatetimeIndex(df['date'])

# 周线顺势
kdata_week = df.c.resample('W').ohlc()
kdata_week.columns=list('ohlc')
kdata_week = kdata_week.dropna(axis=0) # 国庆长假啥的没数据，会出NaN
kdata_week = get_DKX(kdata_week).dropna(axis=0)
kdata_week['周线DKX斜率'] = (kdata_week.b.shift(1) / kdata_week.d.shift(2))  # 斜率指DKX的斜率
kdata_week = kdata_week.dropna(axis=0)
kdata_week_today = kdata_week.resample('D').ffill() # 把计算出来的周线的数据映射到日线上
#print(kdata_week_today)
df['周线DKX斜率'] = kdata_week_today.loc[df.index,:]['周线DKX斜率']

# 开仓条件
df = df.dropna(axis=0)
#print(df.head())
df['高于前两天高点'] = np.where(df.h > df.nhh2, 1, None)   # 看当天 
df['低于前两天低点'] = np.where(df.l < df.nll2, 1, None)

#多顺势 = (df['日线DKX斜率']>1) & (df['周线DKX斜率']<1)
#空顺势 = (df['日线DKX斜率']<1) & (df['周线DKX斜率']>1)
# 只考虑周
多顺势 = (df['周线DKX斜率']>1)
空顺势 = (df['周线DKX斜率']<1)

# 开仓  bk开多  sk开空
df['开仓'] = np.where((df['高于前两天高点'] == 1) & 多顺势, 'bk', None)
df['开仓'] = np.where((df['低于前两天低点'] == 1) & 空顺势, 'sk', df['开仓'] )

# 开仓  bk开多  sk开空
# 多一个条件前一次开仓的止损移动过了，才能开仓(或者说，前一天低点比前两天低点高（做多）)
# 这个开仓的次数少了，收益曲线的标准差小了
# 起个名字，叫 渐进式开仓
#df['开仓'] = np.where((df['高于前两天高点'] == 1) & (df['condition']==1) & (df.l.shift(1) > df.l.shift(2)), 'bk', None)
#df['开仓'] = np.where((df['低于前两天低点'] == 1) & (df['condition']==0) & (df.h.shift(1) < df.h.shift(2)), 'sk', df['开仓'] )

# 平仓 趋势反转 'bp' 平多  'sp' 平空
#df['平仓'] = np.where((df.condition.shift(2) == 1) & (df.condition.shift(1) == 0), 'bp', None)
#df['平仓'] = np.where((df.condition.shift(2) == 0) & (df.condition.shift(1) == 1), 'sp', df['平仓'])
#df['平仓'] = None # 没有平仓信号， 只用止损平仓



#平仓的同时不反向开仓
#df['开仓'] = np.where(df['平仓'].isnull(), df['开仓'], None)

# 这个不能少
dates = pd.DatetimeIndex(df.date)
df.index = dates
df = df.drop('date', axis=1)

df['bk总手数'] = 0
df['bkprice'] = 0
#df['b持仓均价'] = 0  # 
#df['b保证金'] = 0  #
#df['b合约金额'] = 0  # 比如3000点买的螺纹， 实际合约价值是10吨，3万元
df['是b止损'] = None
df['b止损'] = None
df['sk总手数'] = 0
df['skprice'] = 0 
#df['s保证金'] = 0
#df['s持仓均价'] = 0  #
#df['s合约金额'] = 0
df['s止损'] = None
df['是s止损'] = None
df['余额占比'] = 0



def run2b(df,zs, zj_init, f=0.01, maxcw=0.3, jiange=0):
    '''
    在run2的基础上，加上对周线的过滤
    '''
    arr = np.zeros(df.shape[0])
    arr[0] = zj_init  # 
    df['可用余额'] = arr # 初始化可用余额
    df['总金额'] = arr

    yue = 1 - maxcw # 反过来就是余额允许的最小比例
    feiyong = 3 # 每次两个滑点， 再用一个滑点代替费用，共3点
    new_high = 0
    new_low = 99999
    rows_index = range(df.shape[0])
    bk_idx = sk_idx = 0 # 每次开仓时的index
    b间隔 = s间隔 = jiange
    做多次数 = 做空次数 = 0
    for i in rows_index:
        row = df.iloc[i]  # 不变动的值判断用row， 赋值用df.ix
        last_row = df.iloc[i-1] if i > 0 else row
        if i == 0:
            continue
        if df.ix[i, 'sk总手数'] == 0: # 多空只能做一个方向
            bk_conditions = [
                row['开仓'] == 'bk',
                (df.ix[i-1, '可用余额'] / df.ix[i-1, '总金额']) > yue,
                i > (bk_idx + b间隔),
            ]
            #print('bk_idx',bk_idx, i)
            if all(bk_conditions):
            #if row['开仓'] == 'bk' and (df.ix[i-1, '可用余额'] / df.ix[i-1, '总金额']) > yue and i > bk_idx+b间隔:
                # 根据f算开几手
                bk_idx = i
                loss  = df.ix[i-1, '总金额'] * f
                zsrange = row.nhh2 - row.nll2
                ss = int(loss / (zsrange * 10))
                #print(loss,zsrange,ss)

                df.ix[i, 'bkprice'] = bkprice = row.o + feiyong if row.o>row.nhh2 else row.nhh2 + feiyong
                df.ix[i, 'bk总手数'] = df.ix[i-1, 'bk总手数'] + ss  # 等于上一日的bk总手数加1
                df.ix[i, 'b止损'] = int(row.nhh2 - row.atr*zs)  ##############################-10
                df.ix[i, '可用余额'] = df.ix[i-1, '可用余额'] - bkprice * ss
                #df.ix[i, 'b保证金'] = df.ix[i-1, 'b保证金'] + bkprice * ss
                new_change = (row.c - bkprice) * ss * 10 # 新开仓价格变化
                old_change = (row.c - last_row.c) * df.ix[i-1, 'bk总手数'] *10# 旧开仓价格变化
                #print(new_change, old_change)
                df.ix[i, '总金额'] = df.ix[i-1, '总金额'] + new_change + old_change
                做多次数 += 1
            else: 
                df.ix[i, 'bk总手数'] = df.ix[i-1, 'bk总手数'] 
                df.ix[i, '可用余额'] = df.ix[i-1, '可用余额']
                #df.ix[i, 'b保证金'] = df.ix[i-1, 'b保证金']
                if df.ix[i, 'bk总手数'] == 0:
                    df.ix[i, 'b止损'] = new_high = 0
                else:
                    df.ix[i, 'b止损'] = new_high = max(int(row.nhh2 - row.atr*zs),  new_high)
                old_change = (row.c - last_row.c) * df.ix[i-1, 'bk总手数']*10# 旧开仓价格变化
                df.ix[i, '总金额'] = df.ix[i-1, '总金额'] + old_change

        if df.ix[i, 'bk总手数'] == 0: # 多空只能做一个方向
            sk_conditions = [
                row['开仓'] == 'sk',
                (df.ix[i-1, '可用余额'] / df.ix[i-1, '总金额']) > yue,
                i > (sk_idx + s间隔),
            ]
            if all(sk_conditions):
            #if row['开仓'] == 'sk'and (df.ix[i-1, '可用余额'] / df.ix[i-1, '总金额']) > yue:
                # 根据f算开几手
                sk_idx = i
                loss  = df.ix[i-1, '总金额'] * f
                zsrange = row.nhh2 - row.nll2
                ss = int(loss / (zsrange * 10))
                #print(loss,zsrange,ss)
                df.ix[i, 'skprice'] = skprice = row.o -feiyong if row.o<row.nll2 else row.nll2 - feiyong
                df.ix[i, 'sk总手数'] = df.ix[i-1, 'sk总手数'] + ss  # 等于上一日的sk总手数加1
                df.ix[i, 's止损'] = int(row.nll2 + row.atr*zs) ################################+ 10
                df.ix[i, '可用余额'] = df.ix[i-1, '可用余额'] - skprice * ss
                #df.ix[i, 's保证金'] = df.ix[i-1, 's保证金'] + skprice * ss
                new_change = (skprice - row.c) * ss * 10 # 新开仓价格变化
                old_change = (last_row.c - row.c) * df.ix[i-1, 'sk总手数'] *10# 旧开仓价格变化
                #print(new_change, old_change)
                df.ix[i, '总金额'] = df.ix[i-1, '总金额'] + new_change + old_change
                做空次数 += 1
            else: 
                df.ix[i, 'sk总手数'] = df.ix[i-1, 'sk总手数'] 
                df.ix[i, '可用余额'] = df.ix[i-1, '可用余额']
                #df.ix[i, 's保证金'] = df.ix[i-1, 's保证金']
                if df.ix[i, 'sk总手数'] == 0:
                    df.ix[i, 's止损'] = new_low = 999999
                else:
                    df.ix[i, 's止损'] = new_low = min(int(row.nll2 + row.atr*zs),  new_low)
                    #print(df.ix[i, 's止损'],  i)
                old_change = (last_row.c - row.c) * df.ix[i-1, 'sk总手数'] *10# 旧开仓价格变化
                df.ix[i, '总金额'] = df.ix[i-1, '总金额'] + old_change

        # 处理止损
        if df.ix[i, 'bk总手数'] != 0: 
            if row.l <= df.ix[i, 'b止损']:
                df.ix[i, '是b止损'] = 1
                zsprice = df.ix[i, 'b止损'] if row.o >= df.ix[i, 'b止损'] else row.o
                change = (zsprice - last_row.c - feiyong)  * df.ix[i-1, 'bk总手数']* 10
                df.ix[i, '总金额'] = df.ix[i-1, '总金额'] + change
                df.ix[i, 'bk总手数'] = 0
                #df.ix[i, 'b保证金'] = 0
                df.ix[i, '可用余额'] = df.ix[i, '总金额']
        if df.ix[i, 'sk总手数'] != 0: 
            if row.h >= df.ix[i, 's止损']:
                df.ix[i, '是s止损'] = 1
                zsprice = df.ix[i, 's止损'] if row.o <= df.ix[i, 's止损'] else row.o
                change = (last_row.c - zsprice - feiyong)  * df.ix[i-1, 'sk总手数']* 10
                df.ix[i, '总金额'] = df.ix[i-1, '总金额'] + change
                df.ix[i, 'sk总手数'] = 0
                #df.ix[i, 's保证金'] = 0
                df.ix[i, '可用余额'] = df.ix[i, '总金额']

        #df.ix[i,'余额占比'] = df.ix[i, '可用余额'] / df.ix[i, '总金额']
        #if i > 100:
        #    break
    params = {
        'pinzhong': pinzhong,
        'zj_init': zj_init,
        'zs': zs,
        'f': f,
        'maxcw': maxcw,
        'jiange': jiange,
        '做多次数': 做多次数,
        '做空次数': 做空次数,
        
    }
    result_row = result(df, params)
    return result_row

run2b(df, 2, 100000, f=0.02, maxcw=0.3, jiange=0)  # rb是2atr最好 资金增长倍数：146.3   接着是3  资金增长倍数：106.7
'''
参数： run2 zs=2  开仓间隔=0 f=0.02  maxcw=0.3
资金增长倍数：12.8
做多次数:454 做空次数:394
标准差： 0.02582
'''

'''
几个品种结果都是日周都顺最好
参数： run2 zs=2  开仓间隔=0 f=0.02  maxcw=0.3

m
日周都顺势
多顺势 = (df['日线DKX斜率']>1) & (df['周线DKX斜率']>1)
空顺势 = (df['日线DKX斜率']<1) & (df['周线DKX斜率']<1)
资金增长倍数：2.9
做多次数:270 做空次数:201
标准差： 0.02016

日逆周顺
多顺势 = (df['日线DKX斜率']<1) & (df['周线DKX斜率']>1)
空顺势 = (df['日线DKX斜率']>1) & (df['周线DKX斜率']<1)
资金增长倍数：0.6
做多次数:204 做空次数:198
标准差： 0.0176

日顺周逆
多顺势 = (df['日线DKX斜率']>1) & (df['周线DKX斜率']<1)
空顺势 = (df['日线DKX斜率']<1) & (df['周线DKX斜率']>1)
资金增长倍数：2.3
做多次数:220 做空次数:206
标准差： 0.01852

都逆
多顺势 = (df['日线DKX斜率']<1) & (df['周线DKX斜率']<1)
空顺势 = (df['日线DKX斜率']>1) & (df['周线DKX斜率']>1)
资金增长倍数：0.6
做多次数:257 做空次数:263
标准差： 0.01864

只考虑日顺势
资金增长倍数：6.6
做多次数:459 做空次数:389
标准差： 0.02628

只考虑周顺势
资金增长倍数：1.3
做多次数:397 做空次数:313
标准差： 0.02351


rb
日周都顺势
资金增长倍数：12.5
做多次数:115 做空次数:136
标准差： 0.028

日逆周顺
资金增长倍数：1.4
做多次数:82 做空次数:115
标准差： 0.01995

日顺周逆
资金增长倍数：5.1
做多次数:106 做空次数:81
标准差： 0.01922

都逆
资金增长倍数：1.5
做多次数:136 做空次数:104
标准差： 0.01874

只考虑日顺势
资金增长倍数：54.3
做多次数:201 做空次数:206
标准差： 0.03333
只考虑周顺势
资金增长倍数：6.3
做多次数:171 做空次数:205
标准差： 0.03057

c
日周都顺势
资金增长倍数：1.5
做多次数:163 做空次数:96
标准差： 0.01884

日逆周顺
资金增长倍数：0.1
做多次数:158 做空次数:97
标准差： 0.0099

日顺周逆
资金增长倍数：0.2
做多次数:109 做空次数:156
标准差： 0.01283

都逆
资金增长倍数：0.1
做多次数:112 做空次数:182
标准差： 0.01372

只考虑日顺势
资金增长倍数：0.4
做多次数:258 做空次数:236
标准差： 0.02212

只考虑周顺势
资金增长倍数：0.2
做多次数:260 做空次数:180
标准差： 0.01794

y
日周都顺势
资金增长倍数：2.5
做多次数:202 做空次数:140
标准差： 0.0178

日逆周顺
资金增长倍数：2.0
做多次数:165 做空次数:118
标准差： 0.01672

日顺周逆
资金增长倍数：0.6
做多次数:158 做空次数:175
标准差： 0.01226

都逆
资金增长倍数：0.6
做多次数:158 做空次数:220
标准差： 0.0174

只考虑日顺势
资金增长倍数：1.6
做多次数:332 做空次数:251
标准差： 0.02191

只考虑周顺势
资金增长倍数：1.6
做多次数:300 做空次数:228
标准差： 0.0227
'''