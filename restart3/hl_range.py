#波动范围分布
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.sans-serif'] = ['SimHei'] # 正常显示中文


df = pd.read_csv(r'E:\workspace\ana\data\ma.csv')
#df = df.iloc[-300:,:] # 选最近一段数据
df['c_last'] = df.c.shift(1)
df['h_lastc_pct'] = (df.h/df.c_last - 1) * 100
df['l_lastc_pct'] = (df.l/df.c_last - 1) * 100

# 当天波动幅度
## 最低点
#df['ol_pct'] = (df.o/df.l - 1) * 100
#df['cl_pct'] = (df.c/df.l - 1) * 100
## 最高点
#df['oh_pct'] = (df.h/df.o - 1) * 100
#df['ch_pct'] = (df.h/df.c - 1) * 100
# 当天波动幅度 开盘以昨收
# 最低点
df['ol_pct'] = (df.c_last/df.l - 1) * 100
df['cl_pct'] = (df.c/df.l - 1) * 100
# 最高点
df['oh_pct'] = (df.h/df.c_last - 1) * 100
df['ch_pct'] = (df.h/df.c - 1) * 100

df['big_low'] = np.where((df.ol_pct>=3) & (df.cl_pct>=3), True, np.nan) # 长下影线
df['big_high'] = np.where((df.oh_pct>=3) & (df.ch_pct>=3), True, np.nan)   # 长上影线
# 用来看开仓和止损的百分比
print(df.describe())
print('----------------------------------')
#print(df.head())
