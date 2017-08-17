'''
看移动止损
说明都是以多为例
'''

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from tool import get_atr, get_ma

plt.rcParams['font.sans-serif'] = ['SimHei'] # 正常显示中文
hy = 'ta' # rb ta m a ma c jd dy cs
df = pd.read_csv(r'..\data\{}.csv'.format(hy))
df['ma'] = get_ma(df, 20)
df['atr'] = get_atr(df, 50)
df['st_h'] = df[['o', 'c']].apply(lambda x: x.max(),axis=1)
df['st_l'] = df[['o', 'c']].apply(lambda x: x.min(),axis=1)
df = df.dropna()

print(df.l.dtype)

'''
突破高点开多，用后一天的低点除以高点，看百分比
'''

# 条件

cond = True  # 0 没条件
cond = df.l.shift(1) > df.ma.shift(1)  #  昨天K线在ma之上
#cond = df.o < df.c.shift(1)  #
# 今天低点与昨天高点百分比
df['lh_pct'] = np.where(cond, (df.l / df.h.shift(1)) * 100, np.nan)
# 今天低点与昨天低点百分比
df['ll_pct'] = np.where(cond, (df.l / df.l.shift(1)) * 100, np.nan)
# 今天低点与昨天实体高点百分比
df['lsth_pct'] = np.where(cond, (df.l / df.st_h.shift(1)) * 100, np.nan)
# 今天低点与昨天实体低点百分比
df['lstl_pct'] = np.where(cond, (df.l / df.st_l.shift(1)) * 100, np.nan)

df['tmp'] = df.c.shift(1) 

print(df.describe())

def boxplot1():
    df2=df[['lh_pct','ll_pct','lsth_pct','lstl_pct']]
    # 箱型图
    # whis参数指胡须的长度是盒子长度的几倍，
    # 超出这个值被认为是离群点（异常值）
    # #默认1.5
    plt.title(hy)
    sns.boxplot(data=df2)
    plt.ylim(95,105)  #change the scale of the plot
    plt.show()
boxplot1()