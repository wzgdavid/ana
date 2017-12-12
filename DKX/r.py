'''
光有顺势方法，最好再弄个波动方法，两个结合，尽量使曲线平稳
'''
# 开仓条件 超过b线上3个atr, 以下一个工作日开盘价开空
#          超过b线下3个atr, 以下一个工作日开盘价开多
# 止损     多  开仓价下一个atr
#          空  开仓价上一个atr    
#          没有移动止损
# 止盈     做空时， b线下3个atr止盈
#          做多时， b线上3个atr止盈
# 同一时间只能有一份持仓

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from common import *#get_DKX, get_nhh, get_nll, get_ma, avg,get_nhhzs,get_nllzs,get_atr
plt.rcParams['font.sans-serif'] = ['SimHei'] # 正常显示中文
df = pd.read_csv(r'..\data\rb\zs.csv')
#df = pd.read_csv(r'..\data\ta.csv')
df = get_DKX(df)
df = get_nhh(df, 2)
df = get_nll(df, 2)
df = get_ma(df, 20)
df = get_atr(df, 50)


# atr 通道
df['atr3'] =  df.b + df.atr * 3  # DKX b 线上3个atr
df['atr2'] =  df.b + df.atr * 2  # DKX b 线上2个atr
df['atr1'] =  df.b + df.atr      # DKX b 线上1个atr
df['atr1m'] = df.b - df.atr      # DKX b 线下1个atr
df['atr2m'] = df.b - df.atr * 2  # DKX b 线下2个atr
df['atr3m'] = df.b - df.atr * 3  # DKX b 线下3个atr

df = df.dropna(axis=0)


'''
--------------------------波动判断1---------------------------------
'''
# 开仓条件 超过b线上3个atr, 以下一个工作日开盘价开空
#          超过b线下3个atr, 以下一个工作日开盘价开多
df['达到上3atr'] = np.where(df.c.shift(1) > df['atr3'].shift(1), 1, None)  
df['达到下3atr'] = np.where(df.c.shift(1) < df['atr3m'].shift(1), 1, None)
# 开仓  bk开多  sk开空
df['开仓'] = np.where(df.c.shift(1) > df['atr3'].shift(1), 'sk', None)
df['开仓'] = np.where(df.c.shift(1) < df['atr3m'].shift(1), 'bk', df['开仓'] )


# 平仓  'bp' 平多  'sp' 平空
#df['平仓'] = np.where((df.condition.shift(2) == 1) & (df.condition.shift(1) == 0), 'bp', None)
#df['平仓'] = np.where((df.condition.shift(2) == 0) & (df.condition.shift(1) == 1), 'sp', df['平仓'])
#df['平仓'] = None # 没有平仓信号， 只用止损平仓

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
df['b止损'] = None
df['是b止损'] = None  # debug csv文件时用
df['sk总手数'] = 0
df['skprice'] = 0 
#df['s保证金'] = 0
#df['s持仓均价'] = 0  #
#df['s合约金额'] = 0
df['s止损'] = None
df['是s止损'] = None # debug csv文件时用
df['余额占比'] = 0

#df.to_csv('tmp.csv')

def result(df, title):
    print(df['开仓'].value_counts())
    df['returns'] = df['总金额'].pct_change()
    df['ret_index'] = (1 + df['returns']).cumprod()
    #df.ret_index.plot()
    print(df.returns.values.size)
    print(df.returns[-500:].std())
    df['ret_index_log'] = np.log(df['ret_index'])
    df.ret_index_log.plot()
    plt.title('收益倍数: '+title)
    plt.show()
    

def run(df, zj_init=100000, f=0.02):
    arr = np.zeros(df.shape[0])
    arr[0] = zj_init  # 
    df['可用余额'] = arr # 初始化可用余额
    df['总金额'] = arr
    feiyong = 3 # 每次两个滑点， 再用一个滑点代替费用，共3点
    rows_index = range(df.shape[0])
    for i in rows_index:
        row = df.iloc[i]  # 不变动的值判断用row， 赋值用df.ix
        last_row = df.iloc[i-1] if i > 0 else row
        if i == 0:
            continue
        if df.ix[i-1, 'sk总手数'] == 0: 
            if row['开仓'] == 'bk' and df.ix[i-1, 'bk总手数'] == 0:
                df.ix[i, 'bkprice'] = bkprice = row.o + feiyong
                df.ix[i, 'b止损'] = int(row.o - row.atr)
                loss  = df.ix[i-1, '总金额'] * f
                zsrange = bkprice - df.ix[i, 'b止损']
                ss = int(loss / (zsrange * 10))
                df.ix[i, 'bk总手数'] = ss  
                df.ix[i, '可用余额'] = df.ix[i-1, '可用余额'] - bkprice * ss
                #df.ix[i, 'b保证金'] = df.ix[i-1, 'b保证金'] + bkprice * ss
                new_change = (row.c - bkprice) * ss * 10 # 新开仓价格变化
                #print(new_change, old_change)
                df.ix[i, '总金额'] = df.ix[i-1, '总金额'] + new_change
            else: 
                df.ix[i, 'bk总手数'] = df.ix[i-1, 'bk总手数'] 
                df.ix[i, '可用余额'] = df.ix[i-1, '可用余额']
                old_change = (row.c - last_row.c) * df.ix[i-1, 'bk总手数']*10# 旧开仓价格变化
                df.ix[i, '总金额'] = df.ix[i-1, '总金额'] + old_change
                df.ix[i, 'b止损'] = df.ix[i-1, 'b止损']

        # 处理止损
        if df.ix[i, 'bk总手数'] != 0: 
            if row.l <= df.ix[i, 'b止损']:
                df.ix[i, '是b止损'] = 1
                change = (df.ix[i, 'b止损'] - last_row.c - feiyong)  * df.ix[i-1, 'bk总手数']* 10
                df.ix[i, '总金额'] = df.ix[i-1, '总金额'] + change
                df.ix[i, 'bk总手数'] = 0
                #df.ix[i, 'b保证金'] = 0
                df.ix[i, '可用余额'] = df.ix[i, '总金额']
    df.to_csv('tmp.csv')

run(df)


