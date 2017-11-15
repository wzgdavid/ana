'''
20171110
python36
基于report/DKX_MA_趋势概率.ipynb策略
规则说明以多为例，空则反之
0 趋势定义：DKXb线方向向上
1 开仓止损：前一天最低点
2 平仓：趋势反转
3 资金管理：单次允许最大亏损f%
4 开仓方式：
5 想到再写


先写出测试的资金曲线
再根据不同参数，画曲线，看最优参数
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from common import get_DKX, get_nhh, get_nll

df = pd.read_csv(r'..\data\rb\zs.csv')


df = get_DKX(df)
df = get_nhh(df, 2)
df = get_nll(df, 2)
# 趋势判断，DKXb方向，1 向上   0向下  当天参照前两天
df['DKXb方向'] = np.where(df.b.shift(1)>df.b.shift(2), 1, 0) 
# 开仓条件
df['高于前两天高点'] = np.where(df.h > df.nhh, 1, None)   # 看当天 
df['低于前两天低点'] = np.where(df.l < df.nll, 1, None)
# 开仓  bk开多  sk开空
df['开仓'] = np.where((df['高于前两天高点'] == 1) & (df['DKXb方向']==1), 'bk', None)
df['开仓'] = np.where((df['低于前两天低点'] == 1) & (df['DKXb方向']==0), 'sk', df['开仓'] )
# 平仓 趋势反转 'bp' 平多  'sp' 平空
df['平仓'] = np.where((df.DKXb方向.shift(2) == 1) & (df.DKXb方向.shift(1) == 0), 'bp', None)
df['平仓'] = np.where((df.DKXb方向.shift(2) == 0) & (df.DKXb方向.shift(1) == 1), 'sp', df['平仓'])

#平仓的同时不反向开仓
df['开仓'] = np.where(df['平仓'].isnull(), df['开仓'], None)

# 多空持仓总手数
df['bk总手数'] = 0
df['sk总手数'] = 0

df['开仓手数'] = 1  # 目前简单处理，固定手数  后面加入资金管理

df['未持仓金额'] = 0
df.未持仓金额.iloc[0] = 200000  # 初始化
df['b持仓金额'] = 0
df['s持仓金额'] = 0
bk_cnt = 0 # 多仓开仓总数量
sk_cnt = 0 # 开空仓开仓总数量

'''
删选出一部分试验 ，否则太慢， 注意以后要去掉
'''
df = df.head(200) # 删选出一部分试验 ，否则太慢， 注意以后要去掉

点数 = 10 # 螺纹一手10吨
保证金 = 0.1 # 保证金10%
db = 点数*保证金
开仓间隔 = 2
kindex = 0 # 开仓时的index
for idx in range(df.shape[0]): # 
    row = df.iloc[idx]
    print(idx)
    if row.开仓 == 'bk':
        if idx > kindex + 开仓间隔:
            df.bk总手数.iloc[idx] = df.bk总手数.iloc[idx-1] + row.开仓手数
            kindex = idx
        else:
            df.bk总手数.iloc[idx] = df.bk总手数.iloc[idx-1]
    else:
        df.bk总手数.iloc[idx] = df.bk总手数.iloc[idx-1]

    if row.开仓 == 'sk':
        if idx > kindex + 开仓间隔:
            df.sk总手数.iloc[idx] = df.sk总手数.iloc[idx-1] + row.开仓手数
            kindex = idx
        else:
            df.sk总手数.iloc[idx] = df.sk总手数.iloc[idx-1]
    else:
        df.sk总手数.iloc[idx] = df.sk总手数.iloc[idx-1]

    if row.平仓 == 'bp': 
        #df.b持仓金额.iloc[idx] = 0
        df.bk总手数.iloc[idx] = 0
        kindex = idx
    elif row.平仓 == 'sp':
        df.sk总手数.iloc[idx] = 0
        kindex = idx

df['b持仓金额'] = df.bk总手数 * df.c * db
df['s持仓金额'] = df.sk总手数 * df.c * db
#df['总持仓金额'] = df.b持仓金额 + df.s持仓金额
# 计算未持仓金额
for idx in range(df.shape[0]): 
    row = df.iloc[idx]
    if idx == 0:
        continue
    print(idx)
    df['未持仓金额'].iloc[idx] = df['未持仓金额'].iloc[idx-1]
    if row.平仓 == 'bp':
        df['未持仓金额'].iloc[idx] = df['未持仓金额'].iloc[idx-1] + df['b持仓金额'].iloc[idx-1]
    if row.平仓 == 'sp':
        df['未持仓金额'].iloc[idx] = df['未持仓金额'].iloc[idx-1] + df['s持仓金额'].iloc[idx-1]
    if row.开仓 == 'bk':
        df['未持仓金额'].iloc[idx] = df['未持仓金额'].iloc[idx-1] - row.开仓手数 * row.c
    if row.开仓 == 'sk':
        df['未持仓金额'].iloc[idx] = df['未持仓金额'].iloc[idx-1] - row.开仓手数 * row.c



    
    

df['总金额'] = df.未持仓金额 + df['b持仓金额'] + df['s持仓金额']
df['持仓比例'] = (df['b持仓金额'] + df['s持仓金额']) / df['总金额']
#df.bk总手数 = np.where(df.开仓=='bk', df.bk总手数.shift(1)+df.开仓手数, df.bk总手数.shift(1))
#df.bk总手数 = df.bk总手数.shift(1)+df.开仓手数

df.to_csv('tmp.csv')