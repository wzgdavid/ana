'''
没办法，还是要写循环跑
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from common import get_DKX, get_nhh, get_nll, get_ma

df = pd.read_csv(r'..\data\rb\zs.csv')


df = get_DKX(df)
df = get_nhh(df, 2)
df = get_nll(df, 2)
df = get_ma(df, 20)
#df['returns'] = df.c.pct_change()
#df['ret_index'] = (1 + df['returns']).cumprod()
##df['ret_index'][0] = 1  # 每日收益
#df.loc[0,'ret_index'] = 1

'''
--------------------------趋势判断1---------------------------------
'''
# 趋势判断，DKXb方向，1 向上   0向下  当天参照前两天
df['DKXb方向'] = np.where(df.b.shift(1)>df.b.shift(2), 1, 0) 
# 开仓条件
df = df.dropna(axis=0)
df['高于前两天高点'] = np.where(df.h > df.nhh, 1, None)   # 看当天 
df['低于前两天低点'] = np.where(df.l < df.nll, 1, None)
# 开仓  bk开多  sk开空
df['开仓'] = np.where((df['高于前两天高点'] == 1) & (df['DKXb方向']==1), 'bk', None)
df['开仓'] = np.where((df['低于前两天低点'] == 1) & (df['DKXb方向']==0), 'sk', df['开仓'] )
# 平仓 趋势反转 'bp' 平多  'sp' 平空
df['平仓'] = np.where((df.DKXb方向.shift(2) == 1) & (df.DKXb方向.shift(1) == 0), 'bp', None)
df['平仓'] = np.where((df.DKXb方向.shift(2) == 0) & (df.DKXb方向.shift(1) == 1), 'sp', df['平仓'])

'''
--------------------------趋势判断2---------------------------------
'''
## 趋势判断，K线在ma20上下，1 上   0下  当天参照前一天
#df['condition'] = np.where(df.l.shift(1)>df.ma20.shift(1), 1, None) 
#df['condition'] = np.where(df.h.shift(1)<df.ma20.shift(1), 0, df['condition']) 
## 开仓条件
#df = df.dropna(axis=0)
#df['高于前两天高点'] = np.where(df.h > df.nhh, 1, None)   # 看当天 
#df['低于前两天低点'] = np.where(df.l < df.nll, 1, None)
## 开仓  bk开多  sk开空
#df['开仓'] = np.where((df['高于前两天高点'] == 1) & (df['condition']==1), 'bk', None)
#df['开仓'] = np.where((df['低于前两天低点'] == 1) & (df['condition']==0), 'sk', df['开仓'] )
## 平仓 趋势反转 'bp' 平多  'sp' 平空
#df['平仓'] = np.where((df['condition']==1, 'bp', None)
#df['平仓'] = np.where((df['低于前两天低点'] == 1) & (df['condition']==0), 'sp', df['平仓'])



'''
--------------------------趋势判断end---------------------------------
'''

#平仓的同时不反向开仓
df['开仓'] = np.where(df['平仓'].isnull(), df['开仓'], None)


#df['开仓手数'] = 1  # 目前简单处理，固定手数  后面加入资金管理


dates = pd.DatetimeIndex(df.date)
df.index = dates
df = df.drop('date', axis=1)
# 计算收益

arr = np.zeros(df.shape[0])

# 多空持仓总手数
df['bk总手数'] = 0
df['sk总手数'] = 0

df['b保证金'] = 0  # 
df['s保证金'] = 0
df['b合约金额'] = 0  # 比如3000点买的螺纹， 实际合约价值是10吨，3万元
df['s合约金额'] = 0


def run1(df, zj_init,f=0.01):
    '''zj_init 初始资金, f 每次开仓允许的最大亏损百分比
    简单跑，只考虑做多 每次遇到信号开一手，没有开仓止损，没有资金管理 平仓信号全平
    只根据信号开平仓
    '''
    arr[0] = zj_init  # 
    df['可用余额'] = arr # 初始化可用余额
    df['总金额'] = arr
    rows_index = range(df.shape[0])
    for i in rows_index:
        row = df.iloc[i]  # 判断用row， 赋值用df.ix
        last_row = df.iloc[i-1] if i > 0 else row
        if row['开仓'] == 'bk':
            df.ix[i, 'bk总手数'] = last_row['bk总手数'] + 1

        else: 
            df.ix[i, 'bk总手数'] = last_row['bk总手数']
            df.ix[i, 'b保证金'] = last_row['b保证金']
            df.ix[i, '可用余额'] = last_row['可用余额']
            # df.ix[i, 'b合约金额'] = row.c * df.ix[i, 'bk总手数'] * 10 # 螺纹一手10吨

    

    droplist = ['vol', 'b', 'nhh', 'nll', 'DKXb方向',  '高于前两天高点', '低于前两天低点']
    df = df.drop(droplist, axis=1)
    df.to_csv('tmp.csv')
    plt.plot(df['总金额'])
    plt.title('run1')
    plt.show()
    
run1(df, 200000)

