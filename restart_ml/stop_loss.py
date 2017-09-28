'''
看移动止损
都是以多为例
'''

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from tool import get_atr, get_ma, get_nhh, get_nhhst

plt.rcParams['font.sans-serif'] = ['SimHei'] # 正常显示中文
hy = 'm' # rb ta m a ma c jd dy cs
df = pd.read_csv(r'..\data\{}.csv'.format(hy))
df['ma'] = get_ma(df, 20)
df['atr'] = get_atr(df, 50)
df['nhh'] = get_nhh(df, 7)
df['st_h'] = df[['o', 'c']].apply(lambda x: x.max(),axis=1)
df['st_l'] = df[['o', 'c']].apply(lambda x: x.min(),axis=1)
df['nhhst'] = get_nhhst(df, 7)
df = df.dropna()


'''
突破高点开多，用后一天的低点除以高点，看百分比
'''

# 条件
n = 3
cond = True  # 0 没条件
cond = df.l.shift(1) > df.ma.shift(1)  #  昨天K线在ma之上
#cond = df.h.shift(1) < df.ma.shift(1)  #  昨天K线在ma之下
#cond = df.o < df.c.shift(1)  #
# 今天低点与昨天高点百分比
#df['lh_pct'] = np.where(cond, (df.l / df.nhh-3*df.atr) * 100, np.nan)
# 今天低点与昨天低点百分比
#df['ll_pct'] = np.where(cond, (df.l / df.l.shift(n)) * 100, np.nan)
# 今天低点与昨天实体高点百分比
#df['lsth_pct'] = np.where(cond, (df.l / df.nhhst-2*df.atr) * 100, np.nan)
# 今天低点与昨天实体低点百分比
#df['lstl_pct'] = np.where(cond, (df.l / df.st_l.shift(n)) * 100, np.nan)
# 今天低点与昨天高点减ATR后的百分比
df['hatr_pct'] = np.where(cond, (df.l / (df.nhh-df.atr*3)) * 100, np.nan)
# 今天低点与昨天高点一定百分比后的百分比
df['hpct_pct'] = np.where(cond, (df.l / (df.nhh*0.95)) * 100, np.nan)
# 今天低点与昨天实体高点减ATR后的百分比
df['sthatr_pct'] = np.where(cond, (df.l / (df.nhhst-df.atr*2)) * 100, np.nan)
# 今天低点与昨天实体高点一定百分比的百分比
df['sthpct_pct'] = np.where(cond, (df.l / (df.nhhst*0.96)) * 100, np.nan)
df['lma_pct'] = np.where(cond, (df.l / (df.ma)) * 100, np.nan)
#df['hma_pct'] = np.where(cond, (df.h / (df.ma)) * 100, np.nan)
df.to_csv('tmp.csv')
#df['tmp'] = df.c.shift(1) 
df = df[['hatr_pct','hpct_pct','sthatr_pct','sthpct_pct','lma_pct']]
#print(df.describe().T)
desc = df.describe().T
print(desc.sort_values(by='25%').T)



# 做空
n = 3
cond = True  # 0 没条件

cond = df.h.shift(1) < df.ma.shift(1)  #  昨天K线在ma之下

# 今天低点与昨天高点减ATR后的百分比
#df['hatr_pct'] = np.where(cond, (df.h / (df.nhh-df.atr*3)) * 100, np.nan)
# 今天低点与昨天高点一定百分比后的百分比
df['hpct_pct'] = np.where(cond, (df.h / (df.nhh*0.95)) * 100, np.nan)
# 今天低点与昨天实体高点减ATR后的百分比
#df['sthatr_pct'] = np.where(cond, (df.l / (df.nhhst-df.atr*2)) * 100, np.nan)
# 今天低点与昨天实体高点一定百分比的百分比
df['sthpct_pct'] = np.where(cond, (df.l / (df.nhhst*0.96)) * 100, np.nan)
#df['lma_pct'] = np.where(cond, (df.l / (df.ma)) * 100, np.nan)
#df['hma_pct'] = np.where(cond, (df.h / (df.ma)) * 100, np.nan)

df = df[['hatr_pct','hpct_pct','sthatr_pct','sthpct_pct','lma_pct']]
#print(df.describe().T)
desc = df.describe().T
print(desc.sort_values(by='25%').T)

def boxplot1():
    df2=df[['lh_pct','lsth_pct', 'hatr_pct','sthatr_pct','lma_pct','hma_pct']]
    # 箱型图
    # whis参数指胡须的长度是盒子长度的几倍，
    # 超出这个值被认为是离群点（异常值）
    # #默认1.5
    plt.title(hy)
    sns.boxplot(data=df2)
    plt.ylim(95,105)  #change the scale of the plot
    plt.show()
#boxplot1()