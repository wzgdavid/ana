
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def get_DKX(df, n):
    df['a'] = (df.c * 3 + df.l + df.o + df.h)/6
    df['b'] = (20*df.a + 19*df.a.shift(1) + 18*df.a.shift(2) + 17*df.a.shift(3) + 
        16*df.a.shift(4) + 15*df.a.shift(5) + 14*df.a.shift(6) + 
        13*df.a.shift(7) + 12*df.a.shift(8) + 11*df.a.shift(9) + 
        10*df.a.shift(10) + 9*df.a.shift(11) + 8*df.a.shift(12) + 7*df.a.shift(13) + 
        6*df.a.shift(14) + 5*df.a.shift(15) + 4*df.a.shift(16) + 
        3*df.a.shift(17) + 2*df.a.shift(18) + 1*df.a.shift(19))/210
    df['d'] = df.b.rolling(n).mean()
    df = df.drop(['a'], axis=1)

plt.rcParams['font.sans-serif'] = ['SimHei'] # 正常显示中文
hy = 'ta' # rb ta m a ma c jd dy cs
df = pd.read_csv(r'..\data\{}.csv'.format(hy))

# 以多为例
df['ma'] = df.c.rolling(20).mean()
#df['k线在ma上'] = np.where(df.l.shift(1) > df.ma.shift(1), True, False)
周期 = 20
df['next50low'] = df.l.shift(-1 * 周期).rolling(周期).min() # 后50周期的最低点

df['止损点'] = df.o*0.99

#df['结果无条件'] = np.where((df.next50low > df['止损点']) , 1, 0)
#df['结果k线在ma上'] = np.where((df.next50low > df['止损']) & df['k线在ma上'], 1, 0)
df['ma向上'] = df.ma.shift(1) > df.ma.shift(2)
#df['结果ma向上'] = np.where((df.next50low > df['止损点']) & df['ma向上'], 1, 0)
#print(df.head(50))
#print(df.l.rolling(3).min().head(50))


df['开仓价'] = df.o
df['平仓价'] = df['c'].shift(-1 * 周期)
df['不带止损平仓比例'] = df['平仓价'] / df['开仓价']

df['止损比例'] = 0.99
#df['带止损平'] = np.max(df['止损比例'], df['不带止损平仓比例'] )
#df['带止损平比例'] = df[['不带止损平仓比例', '止损比例']].max(axis=1)
df['带止损平比例'] = np.where((df['next50low'] > df['止损点']) & df['ma向上'], df['不带止损平仓比例'], df['止损比例'])
df['带止损平比例盈利数'] = np.where((df['next50low'] > df['止损点']) & df['ma向上'], 1, 0)
df['带止损平比例盈利数2'] = np.where((df['next50low'] > df['止损点']), 1, 0)
df = df.dropna().drop(['date', ], axis=1)
get_DKX(df, 10)
print(df.head(150))
#print(df.ix[300:400, :])
print(df.describe())  # mean 无条件成功率
print(df['带止损平比例盈利数'].sum() / df['ma向上'].sum()) # 有条件的成功率
print(df['带止损平比例盈利数2'].sum() / df.index.size) # 有条件的成功率

df.ix[:,['b','c','d']].plot()

plt.show()