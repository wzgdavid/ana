'''
写到c就太复杂了，而且结果有不对，重写
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from common import get_DKX, get_nhh, get_nll, get_ma, avg
plt.rcParams['font.sans-serif'] = ['SimHei'] # 正常显示中文
df = pd.read_csv(r'..\data\rb\zs.csv')
#df = pd.read_csv(r'..\data\jd.csv')
df = get_DKX(df)
df = get_nhh(df, 2)
df = get_nll(df, 2)
df = get_ma(df, 20)


'''
--------------------------趋势判断1---------------------------------
'''
# 趋势判断，DKXb方向，1 向上   0向下  当天参照前两天
df['DKXb方向'] = np.where(df.b.shift(1)>df.b.shift(2), 1, 0) 
# 开仓条件
df = df.dropna(axis=0)
df['高于前两天高点'] = np.where(df.h > df.nhh2, 1, None)   # 看当天 
df['低于前两天低点'] = np.where(df.l < df.nll2, 1, None)
# 开仓  bk开多  sk开空
df['开仓'] = np.where((df['高于前两天高点'] == 1) & (df['DKXb方向']==1), 'bk', None)
df['开仓'] = np.where((df['低于前两天低点'] == 1) & (df['DKXb方向']==0), 'sk', df['开仓'] )
# 平仓 趋势反转 'bp' 平多  'sp' 平空
df['平仓'] = np.where((df.DKXb方向.shift(2) == 1) & (df.DKXb方向.shift(1) == 0), 'bp', None)
df['平仓'] = np.where((df.DKXb方向.shift(2) == 0) & (df.DKXb方向.shift(1) == 1), 'sp', df['平仓'])
#df['平仓'] = None # 没有平仓信号， 只用止损平仓

'''
--------------------------趋势判断2---------------------------------
'''
# 趋势判断，K线在ma20上下，1 上   0下  当天参照前一天
#df['condition'] = np.where(df.l.shift(1)>df.ma20.shift(1), 1, None) 
#df['condition'] = np.where(df.h.shift(1)<df.ma20.shift(1), 0, df['condition']) 
## 开仓条件
#df = df.dropna(axis=0)
#df['高于前两天高点'] = np.where(df.h > df.nhh2, 1, None)   # 看当天 
#df['低于前两天低点'] = np.where(df.l < df.nll2, 1, None)
## 开仓  bk开多  sk开空
#df['开仓'] = np.where((df['高于前两天高点'] == 1) & (df['condition']==1), 'bk', None)
#df['开仓'] = np.where((df['低于前两天低点'] == 1) & (df['condition']==0), 'sk', df['开仓'] )
## 平仓 趋势反转 'bp' 平多  'sp' 平空
##df['平仓'] = np.where((df['condition']==1, 'bp', None)
##df['平仓'] = np.where((df['低于前两天低点'] == 1) & (df['condition']==0), 'sp', df['平仓'])
#df['平仓'] = None


'''
--------------------------趋势判断end---------------------------------
'''

#平仓的同时不反向开仓
df['开仓'] = np.where(df['平仓'].isnull(), df['开仓'], None)

# 这个不能少
dates = pd.DatetimeIndex(df.date)
df.index = dates
df = df.drop('date', axis=1)

df['bk总手数'] = 0
df['bkprice'] = 0
df['b持仓均价'] = 0  # 
df['b保证金'] = 0  #
df['b合约金额'] = 0  # 比如3000点买的螺纹， 实际合约价值是10吨，3万元
df['是b止损'] = None
#df['sk总手数'] = 0
#df['skprice'] = 0 
#df['s保证金'] = 0
#df['s持仓均价'] = 0  #
#df['s合约金额'] = 0



def run1(df,zj_init):
    '''

    每次只开一手， 三天低点开仓止损和移动止损（先统一止损点跑，简单）
    不考虑滑点和交易费用
    '''
    arr = np.zeros(df.shape[0])
    arr[0] = zj_init  # 
    df['可用余额'] = arr # 初始化可用余额
    df['总金额'] = arr
    df = get_nhh(df, 3)  # 做空止损
    df = get_nll(df, 3)  # 做多止损
  
    #df['b止损'] = df['nll{}'.format(zs)] # 移动和开仓止损
    #df['s止损'] = df['nhh{}'.format(zs)]
    new_high = 0
    rows_index = range(df.shape[0])
    for i in rows_index:
        row = df.iloc[i]  # 不变动的值判断用row， 赋值用df.ix
        last_row = df.iloc[i-1] if i > 0 else row
        if i == 0:
            continue
        if row['开仓'] == 'bk':
            ss = 1 # 每次新开仓手数
            df.ix[i, 'bkprice'] = bkprice = row.o if row.o>row.nhh2 else row.nhh2 
            df.ix[i, 'bk总手数'] = df.ix[i-1, 'bk总手数'] + ss  # 等于上一日的bk总手数加1
            df.ix[i, 'b止损'] = row.nll3
            df.ix[i, '可用余额'] = df.ix[i-1, '可用余额'] - bkprice * ss
            df.ix[i, 'b保证金'] = df.ix[i-1, 'b保证金'] + bkprice * ss
            new_change = (row.c - bkprice) * ss * 10 # 新开仓价格变化
            old_change = (row.c - last_row.c) * df.ix[i-1, 'bk总手数'] *10# 旧开仓价格变化
            #print(new_change, old_change)
            df.ix[i, '总金额'] = df.ix[i-1, '总金额'] + new_change + old_change

        else: 
            df.ix[i, 'bk总手数'] = df.ix[i-1, 'bk总手数'] 
            df.ix[i, '可用余额'] = df.ix[i-1, '可用余额']
            df.ix[i, 'b保证金'] = df.ix[i-1, 'b保证金']
            if df.ix[i, 'bk总手数'] == 0:
                df.ix[i, 'b止损'] = new_high = 0
            else:
                df.ix[i, 'b止损'] = new_high = max(df.ix[i, 'nll3'],  new_high)
            old_change = (row.c - last_row.c) * df.ix[i-1, 'bk总手数']*10# 旧开仓价格变化
            df.ix[i, '总金额'] = df.ix[i-1, '总金额'] + old_change
        
        if row.l <= df.ix[i, 'b止损'] and df.ix[i, 'bk总手数'] !=0:
            df.ix[i, '是b止损'] = 1
            change = (df.ix[i, 'b止损'] - last_row.c)  * df.ix[i-1, 'bk总手数']* 10
            #print(change,  i)
            df.ix[i, '总金额'] = df.ix[i-1, '总金额'] + change
            df.ix[i, 'b止损'] = 0
            df.ix[i, 'bk总手数'] = 0
            df.ix[i, 'b保证金'] = 0
            df.ix[i, '可用余额'] = df.ix[i, '总金额']
    df.to_csv('tmp1.csv')
    plt.plot(df['总金额'])
    title = 'run1'
    plt.title(title)
    plt.show()

run1(df, 100000)