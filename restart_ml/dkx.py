'''
训练集   当天的四个价格和DKX的b线的比值
         当天b线和昨天b线的比值
结果集    
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

df = get_DKX(df) 
df['ma'] = df.c.rolling(window=10, center=False).mean()


df['ob'] = df.o / df.b
df['cb'] = df.c / df.b
df['hb'] = df.h / df.b
df['lb'] = df.l / df.b
#df['ob2'] = df.o.shift(1) / df.b.shift(1)
#df['cb2'] = df.c.shift(1) / df.b.shift(1)
#df['hb2'] = df.h.shift(1) / df.b.shift(1)
#df['lb2'] = df.l.shift(1) / df.b.shift(1)

df['bb'] = df.b / df.b.shift(1)# b比值
#df['bshift1'] = df.b.shift(1)

# 标签规则
n = 1
# label 1
df['label'] = df.c.shift(-1 * n) / df.c # 后n天收盘价除今天收盘价
df.label = np.where(df.label>1, 1, 0)
# label 2
#df['label'] = np.where(df.bb>1, 1, 0)

#print(df.label)

#过滤数据
df['DKX_b_up'] = np.where(df.b > df.b.shift(1), 1, 0)
#df = df.ix[df.DKX_b_up==1,:]  # 过滤出DKXb 向上的数据

df['higher_DKX'] = np.where(df.h<df.b, 1, 0)
#df = df.ix[df.higher_DKX==1,:]  # 过滤出k线比DKXb 高的数据

df['chigher_DKX'] = np.where(df.c>df.b, 1, 0)
#df = df.ix[df.chigher_DKX==1,:]  # 过滤close比DKXb 高的数据

# 过滤出ma向上的数据
df['ma_up'] = np.where(df.ma > df.ma.shift(1), 1, 0)
#df = df.ix[df.ma_up==1, :]
# k线在ma上的数据
df['ma_up'] = np.where(df.l > df.ma, 1, 0)
df = df.ix[df.ma_up==1, :]
df['chigher_ma'] = np.where(df.c>df.ma, 1, 0)
#df = df.ix[df.chigher_ma==1,:]  # 过滤close比DKXb 高的数据

df['lhb'] = df.l / df.h.shift(1)
df['cc'] = df.c / df.c.shift(1)
print(df.lhb.describe())

data = df.cc.dropna(axis=0)
sns.distplot(data)
plt.show()

# 过滤条件后的结果
def result(df):
    '''df is dataframe'''
    df['c_up'] = np.where( df.c/df.c.shift(1)>1, 1, 0 )
    gailv = np.round(df.c_up.sum()/df.shape[0], 3) * 100
    gailv = str(gailv)[:4]
    print( 'c比前一天高的概率 {}% '.format(gailv)) # 某条件下   c比前一天高的概率
    
    df['l_up'] = np.where( df.l/df.l.shift(1)>1, 1, 0 )
    gailv = round(df.l_up.sum()/df.shape[0], 3) * 100
    gailv = str(gailv)[:4]
    print('low比前一天高的概率 {}%'.format(gailv)) # 某条件下   low比前一天高的概率
result(df)

#df.to_csv('tmp.csv')
#df = df.dropna(axis=0)


def plot_heatmap(data, title):
    plt.rcParams['font.sans-serif'] = ['SimHei'] 
    plt.title(title)
    data = data.astype(float)
    ax = sns.heatmap(data, center=60, linewidths=1, 
                     cmap="RdBu", vmin=50, vmax=70, annot=True)
    ax.set_xticklabels(ax.xaxis.get_majorticklabels(), rotation=0)
    ax.set_yticklabels(ax.yaxis.get_majorticklabels(), rotation=0)
    plt.show()