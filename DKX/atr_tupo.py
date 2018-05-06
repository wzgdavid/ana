'''
从d_atr.py 拷贝过来改动的，只不过不是突破前几天高低点开仓 
而是突破前几天收盘价的一个距离atr开仓，
'''



import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from common import *#get_DKX, get_n_atr_up_l, get_n_atr_down_h, get_ma, avg,get_n_atr_up_lzs,get_n_atr_down_hzs,get_atr

pinzhong = 'ma'
plt.rcParams['font.sans-serif'] = ['SimHei'] # 正常显示中文
df = pd.read_csv(r'..\data\{}.csv'.format(pinzhong))

df = get_ma(df, 20)
df = get_nhh(df, 3)
df = get_nll(df, 3)
df = get_atr(df, 50)

df['atr_up'] = df.c + df.atr
df['atr_down'] = df.c - df.atr

nn = 3
# 前几天c加一个atr的最低值 开多用
df['n_atr_up_l'] = df.atr_up.shift(1).rolling(window=nn, center=False).min()
# 前几天c减一个atr的最高值  开空用
df['n_atr_down_h'] = df.atr_down.shift(1).rolling(window=nn, center=False).max()
df.to_csv('tmp.csv')
'''
--------------------------趋势判断  用ma---------------------------------
'''

df['condition'] = np.where(df.c.shift(1)>df.ma.shift(1), 1, None) 
df['condition'] = np.where(df.c.shift(1)<df.ma.shift(1), 0, df['condition']) 
## 开仓条件
df = df.dropna(axis=0)
df['高于前两天高点'] = np.where(df.h > df.n_atr_up_l, 1, None)   # 看当天 
df['低于前两天低点'] = np.where(df.l < df.n_atr_down_h, 1, None)
## 开仓  bk开多  sk开空
df['开仓'] = np.where((df['高于前两天高点'] == 1) & (df['condition']==1), 'bk', None)
df['开仓'] = np.where((df['低于前两天低点'] == 1) & (df['condition']==0), 'sk', df['开仓'] )


'''
--------------------------趋势判断  无过滤---------------------------------
'''

 
# 开仓条件
#df = df.dropna(axis=0)
#df['高于前两天高点'] = np.where(df.h > df.n_atr_up_l, 1, None)   # 看当天 
#df['低于前两天低点'] = np.where(df.l < df.n_atr_down_h, 1, None)
### 开仓  bk开多  sk开空
#df['开仓'] = np.where(df['高于前两天高点'] == 1, 'bk', None)
#df['开仓'] = np.where(df['低于前两天低点'] == 1, 'sk', df['开仓'] )

#df['开仓'] = np.where(df['低于前两天低点'] == 1, 'sk', None)
'''
--------------------------趋势判断end---------------------------------
'''

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



def run2(df,kczs, zs, zj_init, f=0.01, maxcw=0.3, jiange=0):
    '''
    d 中 run2 的atr止损版本
    有资金管理
    zs 指n个ATR移动止损
    每次开仓允许的损失，f（当前总金额的百分比）
    maxcw, 允许最大仓位（当前总金额的百分比）
    '''
    arr = np.zeros(df.shape[0])
    arr[0] = zj_init  # 
    df['可用余额'] = arr # 初始化可用余额
    df['总金额'] = arr

    开仓止损 = kczs

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
                #zsrange = row.n_atr_up_l - row.n_atr_down_h
                zsrange = row.atr*开仓止损
                ss = int(loss / (zsrange * 10))
                #print(loss,zsrange,ss)
                bkj = row.n_atr_up_l 
                #bkj = row.n_atr_up_l-1 # 前两天高低点提前一跳
                #bkj = df.ix[i-1, 'c'] + df.ix[i-1, 'atr']  # 距前一天收盘价一个atr
                df.ix[i, 'bkprice'] = bkprice = row.o + feiyong if row.o>bkj else bkj + feiyong
                df.ix[i, 'bk总手数'] = df.ix[i-1, 'bk总手数'] + ss  # 等于上一日的bk总手数加1
                df.ix[i, 'b止损'] = int(bkprice - zsrange)  ##############################-10  开仓止损 1atr
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
                    
                    df.ix[i, 'b止损'] = max(int(row.nhh - row.atr*zs),  df.ix[i-1, 'b止损'])
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
                #zsrange = row.n_atr_up_l - row.n_atr_down_h
                zsrange = row.atr*开仓止损
                ss = int(loss / (zsrange * 10))
                #print(loss,zsrange,ss)
                skj = row.n_atr_down_h 
                #skj = row.n_atr_down_h+1 # 前两天高低点提前一跳
                #skj = df.ix[i-1, 'c'] - df.ix[i-1, 'atr']  # 距前一天收盘价一个atr
                df.ix[i, 'skprice'] = skprice = row.o - feiyong if row.o<skj else skj - feiyong
                df.ix[i, 'sk总手数'] = df.ix[i-1, 'sk总手数'] + ss  # 等于上一日的sk总手数加1
                df.ix[i, 's止损'] = int(skprice + zsrange) ################################+ 10  开仓止损 1atr
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
                    df.ix[i, 's止损'] = min(int(row.nll + row.atr*zs),  df.ix[i-1, 's止损'])
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
    df.to_csv('tmp.csv')
        #df.ix[i,'余额占比'] = df.ix[i, '可用余额'] / df.ix[i, '总金额']
        #if i > 100:
        #    break
    params = {
        'pinzhong': pinzhong,
        'zj_init': zj_init,
        '开仓止损': 开仓止损,
        'zs': zs,
        'f': f,
        'maxcw': maxcw,
        'jiange': jiange,
        '做多次数': 做多次数,
        '做空次数': 做空次数,

        
    }
    result_row = result(df, params)
    return result_row

#run2(df, 2, 100000, f=0.02, maxcw=0.3)
#run2(df, 2, 100000, f=0.02, maxcw=0.4)
run2(df, 0.5, 2, 100000, f=0.01, maxcw=0.3, jiange=0)  
'''

'''