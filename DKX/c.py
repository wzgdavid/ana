'''
用tips中 的收益计算方式
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
df['总金额'] = 0

def run1(df, zj_init):
    '''zj_init 初始资金
    简单跑，只考虑做多 每次遇到信号开一手，没有开仓止损，没有资金管理 平仓信号全平
    只根据信号开平仓
    '''
    arr[0] = zj_init  # 
    df['可用余额'] = arr # 初始化可用余额
    rows_index = range(df.shape[0])
    for i in rows_index:
        row = df.iloc[i]  # 判断用row， 赋值用df.ix
        last_row = df.iloc[i-1] if i > 0 else row
    
        # 多
        #if row['开仓'] == 'bk':
        #    df.ix[i, 'bk总手数'] = last_row['bk总手数'] + 1
        #    # 简单计算， 保证金比例就一比十， 既价格就是保证金额
        #    df.ix[i, 'b保证金'] = last_row['b保证金'] + row.c  # 简单用c表示一次开仓的保证金
        #    df.ix[i, 'b合约金额'] = row.c * df.ix[i, 'bk总手数'] * 10 # 螺纹一手10吨
        #    df.ix[i, '可用余额'] = last_row['可用余额'] - row.c # 简单用c表示一次开仓的保证金
        #else: 
        #    df.ix[i, 'bk总手数'] = last_row['bk总手数']
        #    df.ix[i, 'b保证金'] = last_row['b保证金']
        #    df.ix[i, '可用余额'] = last_row['可用余额']
        #    df.ix[i, 'b合约金额'] = row.c * df.ix[i, 'bk总手数'] * 10 # 螺纹一手10吨
        #if row['平仓'] == 'bp':
        #    df.ix[i, 'bk总手数'] = 0
        #    df.ix[i, 'b保证金'] = 0
        #    #df.ix[i, '可用余额'] = last_row['可用余额'] + df.ix[i, 'b合约金额']/10
        #    df.ix[i, '可用余额'] = last_row['总金额']
        #    df.ix[i, 'b合约金额'] = 0
        
        # 空
        if row['开仓'] == 'sk':
            df.ix[i, 'sk总手数'] = last_row['sk总手数'] + 1
            df.ix[i, 's保证金'] = last_row['s保证金'] + row.c
            df.ix[i, 's合约金额'] = row.c * df.ix[i, 'sk总手数'] * 10 # 螺纹一手10吨
            df.ix[i, '可用余额'] = last_row['可用余额'] - row.c
        else:
            df.ix[i, 'sk总手数'] = last_row['sk总手数']
            df.ix[i, 's保证金'] = last_row['s保证金']
            df.ix[i, '可用余额'] = last_row['可用余额']
            df.ix[i, 's合约金额'] = row.c * df.ix[i, 'sk总手数'] * 10 # 螺纹一手10吨
        if row['平仓'] == 'sp':
            df.ix[i, 'sk总手数'] = 0
            df.ix[i, 's保证金'] = 0
            df.ix[i, '可用余额'] = last_row['总金额']
            df.ix[i, 's合约金额'] = 0

        df.ix[i, '总金额'] = df.ix[i, '可用余额'] + df.ix[i, 'b保证金'] + (df.ix[i, 'b合约金额']/ 10 - df.ix[i, 'b保证金'])*10 \
                               + df.ix[i, 's保证金'] + (df.ix[i, 's保证金'] - df.ix[i, 's合约金额']/ 10  )*10
    

    droplist = ['vol', 'b', 'nhh', 'nll', 'DKXb方向',  '高于前两天高点', '低于前两天低点']
    df = df.drop(droplist, axis=1)
    df.to_csv('tmp.csv')
    plt.plot(df['总金额'])
    plt.title('run1')
    plt.show()
    
run1(df, 200000)


def run2(df, zj_init, limit):
    '''zj_init 初始资金
    简单跑，只考虑做多 每次遇到信号开一手，没有开仓止损，没有资金管理 平仓信号全平
    1 比run1多一个条件， 每次同方向最多只能有limit个持仓
    只根据信号开平仓
    '''
    arr[0] = zj_init  # 
    df['可用余额'] = arr # 初始化可用余额
    rows_index = range(df.shape[0])
    for i in rows_index:
        row = df.iloc[i] # 不变化的用row 变化的数值直接用df.iloc[i]
        last_row = df.iloc[i-1] if i > 0 else row
        
        # df.iloc[i-1]['bk总手数'] == 0 表示有持仓  不同处
        if row['开仓'] == 'bk' and df.iloc[i-1]['bk总手数'] <= limit:
            df.ix[i, 'bk总手数'] = last_row['bk总手数'] + 1
            # 简单计算， 保证金比例就一比十， 既价格就是保证金额
            df.ix[i, 'b保证金'] = last_row['b保证金'] + row.c  # 简单用c表示一次开仓的保证金
            df.ix[i, 'b合约金额'] = row.c * df.ix[i, 'bk总手数'] * 10 # 螺纹一手10吨
            df.ix[i, '可用余额'] = last_row['可用余额'] - row.c # 简单用c表示一次开仓的保证金
        else: 
            df.ix[i, 'bk总手数'] = last_row['bk总手数']
            df.ix[i, 'b保证金'] = last_row['b保证金']
            df.ix[i, '可用余额'] = last_row['可用余额']
            df.ix[i, 'b合约金额'] = row.c * df.ix[i, 'bk总手数'] * 10 # 螺纹一手10吨
        if row['平仓'] == 'bp' and df.iloc[i]['bk总手数'] != 0:
            df.ix[i, 'bk总手数'] = 0
            df.ix[i, 'b保证金'] = 0
            #df.ix[i, '可用余额'] = last_row['可用余额'] + df.ix[i, 'b合约金额']/10
            df.ix[i, '可用余额'] = last_row['总金额']
            df.ix[i, 'b合约金额'] = 0
        
        # 空
        #if row['开仓'] == 'sk' and df.iloc[i-1]['sk总手数'] <= limit:
        #    df.ix[i, 'sk总手数'] = last_row['sk总手数'] + 1
        #    df.ix[i, 's保证金'] = last_row['s保证金'] + row.c
        #    df.ix[i, 's合约金额'] = row.c * df.ix[i, 'sk总手数'] * 10 # 螺纹一手10吨
        #    df.ix[i, '可用余额'] = last_row['可用余额'] - row.c
        #else:
        #    df.ix[i, 'sk总手数'] = last_row['sk总手数']
        #    df.ix[i, 's保证金'] = last_row['s保证金']
        #    df.ix[i, '可用余额'] = last_row['可用余额']
        #    df.ix[i, 's合约金额'] = row.c * df.ix[i, 'sk总手数'] * 10 # 螺纹一手10吨
        #if row['平仓'] == 'sp' and df.iloc[i]['sk总手数'] != 0:
        #    df.ix[i, 'sk总手数'] = 0
        #    df.ix[i, 's保证金'] = 0
        #    df.ix[i, '可用余额'] = last_row['总金额']
        #    df.ix[i, 's合约金额'] = 0

        df.ix[i, '总金额'] = df.ix[i, '可用余额'] + df.ix[i, 'b保证金'] + (df.ix[i, 'b合约金额']/ 10 - df.ix[i, 'b保证金'])*10 


    droplist = ['vol', 'b', 'nhh', 'nll', 'DKXb方向',  '高于前两天高点', '低于前两天低点']
    df = df.drop(droplist, axis=1)
    df.to_csv('tmp2.csv')
    plt.plot(df['总金额'])
    plt.title('limit: {}'.format(limit))
    plt.show()
    
#run2(df, 100000, limit=5)


def run3(df, zj_init):
    '''zj_init 初始资金
    简单跑，只考虑做多 每次遇到信号开一手，没有开仓止损，没有资金管理, 平仓信号全平
    
    在1的基础上有开仓止损
    '''
    arr[0] = zj_init  # 
    df['可用余额'] = arr # 初始化可用余额
    rows_index = range(df.shape[0])
    df['b开仓止损'] = ''
    for i in rows_index:
        row = df.iloc[i]  # 判断用row， 赋值用df.ix
        last_row = df.iloc[i-1] if i > 0 else row
    
        # 多
        if row['开仓'] == 'bk':
            df.ix[i, 'bk总手数'] = last_row['bk总手数'] + 1
            # 简单计算， 保证金比例就一比十， 既价格就是保证金额
            df.ix[i, 'b保证金'] = last_row['b保证金'] + row.c  # 简单用c表示一次开仓的保证金
            df.ix[i, 'b合约金额'] = row.c * df.ix[i, 'bk总手数'] * 10 # 螺纹一手10吨
            df.ix[i, '可用余额'] = last_row['可用余额'] - row.c # 简单用c表示一次开仓的保证金
            #df.ix[i, 'b开仓止损'] = last_row['b开仓止损'] + '-' + last_row.l
        else: 
            df.ix[i, 'bk总手数'] = last_row['bk总手数']
            df.ix[i, 'b保证金'] = last_row['b保证金']
            df.ix[i, '可用余额'] = last_row['可用余额']
            df.ix[i, 'b合约金额'] = row.c * df.ix[i, 'bk总手数'] * 10 # 螺纹一手10吨
            #df.ix[i, 'b开仓止损'] = last_row['b开仓止损']
        if row['平仓'] == 'bp' and df.iloc[i]['bk总手数'] != 0:
            df.ix[i, 'bk总手数'] = 0
            df.ix[i, 'b保证金'] = 0
            #df.ix[i, '可用余额'] = last_row['可用余额'] + df.ix[i, 'b合约金额']/10
            df.ix[i, '可用余额'] = last_row['总金额']
            df.ix[i, 'b合约金额'] = 0
            #df.ix[i, 'b开仓止损'] = []

        df.ix[i, '总金额'] = df.ix[i, '可用余额'] + df.ix[i, 'b保证金'] + (df.ix[i, 'b合约金额']/ 10 - df.ix[i, 'b保证金'])*10
        

    droplist = ['vol', 'b', 'nhh', 'nll', 'DKXb方向',  '高于前两天高点', '低于前两天低点']
    df = df.drop(droplist, axis=1)
    df.to_csv('tmp3.csv')
    plt.plot(df['总金额'])
    plt.show()
#run3(df, 100000)

def run4(df, zj_init, f=0.01):
    '''zj_init 初始资金
    简单跑，只考虑做多 每次遇到信号开一手，没有开仓止损，没有资金管理
    只根据信号开平仓 f 是总资金百分比
    在1的基础上有资金管理
    '''

    arr = np.zeros(df.shape[0])
    arr[0] = zj_init  # 
    df['可用余额'] = arr # 初始化可用余额
    df['b保证金'] = 0  # 
    df['s保证金'] = 0
    df['b合约金额'] = 0  # 比如3000点买的螺纹， 实际合约价值是10吨，3万元
    df['s合约金额'] = 0
    df['总金额'] = 0

    rows_index = range(df.shape[0])
    for i in rows_index:
        row = df.iloc[i]  # 判断用row， 赋值用df.ix
        last_row = df.iloc[i-1] if i > 0 else row
    
        # 多
        if row['开仓'] == 'bk':
        #if row['开仓'] == 'bk' and df.ix[i-1, '可用余额'] > 10000:

            df.ix[i, 'bk总手数'] = last_row['bk总手数'] + 1
            # 简单计算， 保证金比例就一比十， 既价格就是保证金额
            df.ix[i, 'b保证金'] = last_row['b保证金'] + row.c  # 简单用c表示一次开仓的保证金
            df.ix[i, 'b合约金额'] = row.c * df.ix[i, 'bk总手数'] * 10 # 螺纹一手10吨
            df.ix[i, '可用余额'] = last_row['可用余额'] - row.c # 简单用c表示一次开仓的保证金
        else: 
            df.ix[i, 'bk总手数'] = last_row['bk总手数']
            df.ix[i, 'b保证金'] = last_row['b保证金']
            df.ix[i, '可用余额'] = last_row['可用余额']
            df.ix[i, 'b合约金额'] = row.c * df.ix[i, 'bk总手数'] * 10 # 螺纹一手10吨
        if row['平仓'] == 'bp':
            df.ix[i, 'bk总手数'] = 0
            df.ix[i, 'b保证金'] = 0
            #df.ix[i, '可用余额'] = last_row['可用余额'] + df.ix[i, 'b合约金额']/10
            df.ix[i, '可用余额'] = last_row['总金额']
            df.ix[i, 'b合约金额'] = 0

        df.ix[i, '总金额'] = df.ix[i, '可用余额'] + df.ix[i, 'b保证金'] + (df.ix[i, 'b合约金额']/ 10 - df.ix[i, 'b保证金'])*10
        

        
        # 空
        #if row['开仓'] == 'sk':
        #    df.ix[i, 'sk总手数'] = last_row['sk总手数'] + 1
        #    df.ix[i, 's保证金'] = last_row['s保证金'] + row.c
        #    df.ix[i, 's合约金额'] = row.c * df.ix[i, 'sk总手数'] * 10 # 螺纹一手10吨
        #    df.ix[i, '可用余额'] = last_row['可用余额'] - df.ix[i, 's保证金']
        #else:
        #    df.ix[i, 'sk总手数'] = last_row['sk总手数']
        #    df.ix[i, 's保证金'] = last_row['s保证金']
        #    df.ix[i, '可用余额'] = last_row['可用余额']
        #    df.ix[i, 's合约金额'] = row.c * df.ix[i, 'sk总手数'] * 10 # 螺纹一手10吨
        #if row['平仓'] == 'sp':
        #    df.ix[i, 'sk总手数'] = 0
        #    df.ix[i, 's保证金'] = 0
        #    df.ix[i, '可用余额'] = last_row['可用余额'] + df.ix[i, 's合约金额']/10
        #    df.ix[i, 's合约金额'] = 0

    
    plt.plot(df['总金额'])
    plt.show()
    droplist = ['vol', 'b', 'nhh', 'nll',  'DKXb方向',  '高于前两天高点', '低于前两天低点']
    df = df.drop(droplist, axis=1)
    df.to_csv('tmp.csv')

