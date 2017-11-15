

import numpy as np
import pandas as pd

# 把csv中的date转成pandas的dateindex
df =  pd.read_csv(r'E:\python_files\csv\au.csv')
dates = pd.DatetimeIndex(df.date)
df.index = dates
df = df.drop('date', axis=1)
# 计算收益
df['returns'] = df.c.pct_change()
df['ret_index'] = (1 + df['returns']).cumprod()
df['ret_index'][0] = 1  # 每日收益
df['m_returns'] = df.ret_index.resample('BM').last().pct_change()
print(df.tail(10))
print(df.m_returns.dropna()) # 月收益变化