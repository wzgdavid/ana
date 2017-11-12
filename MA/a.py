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

#df = pd.read_csv(r'..\data\rb\zs.csv')
df = pd.read_csv(r'..\data\c.csv')
# 构建指标

def get_nhh(df, n):
    '''前n天最高价最高点（不包含当天）'''
    df['nhh'] = df.h.shift(1).rolling(window=n, center=False).max()
    return df

def get_nll(df, n):
    '''前n天最低点（不包含当天）'''
    df['nll'] = df.l.shift(1).rolling(window=n, center=False).min()
    return df

df['ma小'] = df.c.rolling(window=5, center=False).mean()
df['ma大'] = df.c.rolling(window=20, center=False).mean()


df = get_nhh(df, 2)
df = get_nll(df, 2)


# 开仓  bk开多  sk开空

df['开仓'] = np.where((df.ma小.shift(2)<df.ma大.shift(2)) & (df.ma小.shift(1)>df.ma大.shift(1)), 'bk', None)
df['开仓'] = np.where((df.ma小.shift(2)>df.ma大.shift(2)) & (df.ma小.shift(1)<df.ma大.shift(1)), 'sk', df['开仓'])

sks = []
bks = []
for i in range(df.shape[0]):
    if df.开仓.iloc[i] == 'bk':
        bks.append(df.c.iloc[i])
    elif df.开仓.iloc[i] == 'sk':
        sks.append(df.c.iloc[i])

print(sks)
print(bks)
sks.append(np.nan)
rdf = pd.DataFrame()
rdf['sks'] = sks
rdf['bks'] = bks

rdf['se'] = rdf.sks-rdf.bks
rdf['be'] = rdf.sks-rdf.bks.shift(1)
print(rdf)
print(rdf.describe())
print(rdf.sum())
'''
删选出一部分试验 ，否则太慢， 注意以后要去掉
'''
#df = df.head(200) # 删选出一部分试验 ，否则太慢， 注意以后要去掉

#df.to_csv('tmp.csv')