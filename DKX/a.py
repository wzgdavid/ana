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

df = pd.read_csv(r'..\data\rb\zs.csv')

# 构建指标
def get_DKX(df, n=10):
    df['a'] = (df.c * 3 + df.l + df.o + df.h)/6
    df['b'] = (20*df.a + 19*df.a.shift(1) + 18*df.a.shift(2) + 17*df.a.shift(3) + 
        16*df.a.shift(4) + 15*df.a.shift(5) + 14*df.a.shift(6) + 
        13*df.a.shift(7) + 12*df.a.shift(8) + 11*df.a.shift(9) + 
        10*df.a.shift(10) + 9*df.a.shift(11) + 8*df.a.shift(12) + 7*df.a.shift(13) + 
        6*df.a.shift(14) + 5*df.a.shift(15) + 4*df.a.shift(16) + 
        3*df.a.shift(17) + 2*df.a.shift(18) + 1*df.a.shift(19))/210
    df['d'] = df.b.rolling(n).mean()
    return df.drop(['a'], axis=1)

def get_nhh(df, n):
    '''前n天最高价最高点（不包含当天）'''
    df['nhh'] = df.h.shift(1).rolling(window=n, center=False).max()
    return df

def get_nll(df, n):
    '''前n天最低点（不包含当天）'''
    df['nll'] = df.l.shift(1).rolling(window=n, center=False).min()
    return df




def run(zijin=100000, f=0.01):
    pass

df = get_DKX(df)
df = get_nhh(df, 2)
df = get_nll(df, 2)

print(df.head(50))