'''
验证是不是趋势越明显的情况下，后面也更容易有趋势
before = 今天的收盘除以前n天的收盘
after  = 后n天的收盘除以今天的收盘
看相关系数，如果相关系数高，说明有关系
'''
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from tool import *

plt.rcParams['font.sans-serif'] = ['SimHei'] # 正常显示中文
hy = 'cs' # rb ta m a ma c jd dy cs
df = pd.read_csv(r'..\data\{}.csv'.format(hy))
df = get_ma(df, 20)
df = get_nhh(df, 3)
#df = get_atr(df, 50)
#df['st_h'] = df[['o', 'c']].apply(lambda x: x.max(),axis=1)
#df['st_l'] = df[['o', 'c']].apply(lambda x: x.min(),axis=1)



n = 10
m = 10
df['before'] = df.c / df.c.shift(n)
df['after'] = df.c.shift(-1*m) / df.c
df = df.dropna()

#df = df[(df.l - df.ma) > 0]
df = df[(df.h - df.nhh) > 0]
print(df.shape[0])
print(df.head(10))
a = df.before.corr(df.after)
print(a)


