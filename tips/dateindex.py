# 这个收益其实指的是做多的情况

import numpy as np
import pandas as pd

# 把csv中的date转成pandas的dateindex
df =  pd.read_csv(r'..\data\au.csv')
#print(df.date)
dates = pd.DatetimeIndex(df.date)
df.index = dates
df = df.drop('date', axis=1)
# 计算收益

df['returns'] = df.c.pct_change()
df['ret_index'] = (1 + df['returns']).cumprod()
df['ret_index'][0] = 1  # 每日收益
df['month_returns'] = df.ret_index.resample('M').last().pct_change()
#print(df.tail(10))
#print(df.m_returns.dropna()) # 月收益变化

#df.to_csv('tmp.csv')

np.random.seed(3)
#np.random.seed()
ts = pd.Series(np.random.rand(20),
            index = pd.date_range('2012-6-13',periods=20,freq='W-WED')

    )

print(type(ts.index)) #<class 'pandas.core.indexes.datetimes.DatetimeIndex'>
print(ts)               
print(ts.resample('M').sum())


