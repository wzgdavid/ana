import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


plt.rcParams['font.sans-serif'] = ['SimHei'] # 正常显示中文
hy = 'rb' # rb ta m a ma c jd dy cs
df = pd.read_csv(r'..\data\{}.csv'.format(hy))
df['ma'] = df.c.rolling(window=20, center=False).mean()
def get_atr(df, n):
    '''TR : MAX( MAX( (HIGH-LOW),ABS(REF(CLOSE,1)-HIGH) ), ABS(REF(CLOSE,1)-LOW));文华的公式
    '''
    df['hl'] = df.h - df.l
    df['ch'] = abs(df.c.shift(1) - df.h)
    df['cl'] = abs(df.c.shift(1) - df.l)
    df['tr'] = df.loc[:, ['hl','ch', 'cl']].apply(lambda x: x.max(), axis=1)
    df['atr'] = df.tr.rolling(window=n, center=False).mean()
    df = df.drop(['hl', 'ch','cl','tr'], axis=1)
    return df
df['st_h'] = df[['o', 'c']].apply(lambda x: x.max(),axis=1)
df['st_l'] = df[['o', 'c']].apply(lambda x: x.min(),axis=1)
df = get_atr(df, 50)
df = df.dropna()
print(df.head(9))
# 做多
# 一段时间买入持有
#first_open = df.o.iloc[0]
#last_close = df.c.iloc[-1]
#print('buy hold is {}'.format((last_close - first_open)))
# 每天开盘价买入，收盘价卖出
#df['daily_change'] = df.c - df.o
#print('daily change is {}'.format(df.daily_change.sum()))

# 条件
cond = True  # 0 没条件
#cond = df.o > df.c.shift(1)  # 
#cond = df.o > df.h.shift(1)    # 
#cond = df.o < df.h.shift(1)    #
#cond = df.o < df.c.shift(1)    #
#cond = df.o < df.l.shift(1)    #
# 今天高点与今天开盘价百分比
df['ho_pct'] = np.where(cond, (df.h / df.o) * 100, np.nan)
# 今天低点与今天开盘价百分比
df['lo_pct'] = np.where(cond, (df.l / df.o) * 100, np.nan)
# 今天收盘与今天开盘价百分比
df['co_pct'] = np.where(cond, (df.c / df.o) * 100, np.nan)

#print(df[['ho_pct','lo_pct','co_pct']].describe())
# 柱状图
def foo1(): # 写成函数加减注释容易
    bins=range(-3,3,1) # 范围0到200，每个柱的宽度20
    # hist画柱状图
    plt.hist(df["c_o_pct"],bins,color='#3333ee',width=0.8) 
    plt.xlabel('c_o_pct')
    plt.ylabel('计数')
    plt.plot()
    # 平均值
    plt.axvline(df['c_o_pct'].mean(),linestyle='dashed',color='red')
    plt.show()
#foo1()


def boxplot1():
    df2=df[['ho_pct','lo_pct','co_pct']]
    # 箱型图
    # whis参数指胡须的长度是盒子长度的几倍，
    # 超出这个值被认为是离群点（异常值）
    # #默认1.5
    plt.title(hy)
    sns.boxplot(data=df2)
    plt.ylim(95,105)  #change the scale of the plot
    plt.show()
#boxplot1()


'''
---------------------------------------------------------------
---------------------------------------------------------------
---------------------------------------------------------------
'''
# 条件

cond = True  # 0 没条件
#cond = df.o < df.c.shift(1)  #
# 今天高点与昨天收盘百分比
#df['aa'] = df.o.shift(1)
df['hc_pct'] = np.where(cond, (df.h / df.c.shift(1)) * 100, np.nan)
# 今天低点与昨天收盘百分比
df['lc_pct'] = np.where(cond, (df.l / df.c.shift(1)) * 100, np.nan)
# 今天收盘与昨天收盘百分比
df['cc_pct'] = np.where(cond, (df.c / df.c.shift(1)) * 100, np.nan)

df['tmp'] = df.c.shift(1) 
#print(df.head())
#print(df[['hc_pct','lc_pct','cc_pct']].describe())
# 柱状图
def foo1(): # 写成函数加减注释容易
    bins=range(-3,3,1) # 范围0到200，每个柱的宽度20
    # hist画柱状图
    plt.hist(df["c_o_pct"],bins,color='#3333ee',width=0.8) 
    plt.xlabel('c_o_pct')
    plt.ylabel('计数')
    plt.plot()
    # 平均值
    plt.axvline(df['c_o_pct'].mean(),linestyle='dashed',color='red')
    plt.show()
#foo1()


def boxplot1():
    df2=df[['hc_pct','lc_pct','cc_pct']]
    # 箱型图
    # whis参数指胡须的长度是盒子长度的几倍，
    # 超出这个值被认为是离群点（异常值）
    # #默认1.5
    plt.title(hy)
    sns.boxplot(data=df2)
    plt.ylim(95,105)  #change the scale of the plot
    plt.show()
#boxplot1()

def violinplot1():
    plt.title(hy)
    df2=df[['hc_pct','lc_pct','cc_pct']]
    sns.violinplot(data = df2)
    plt.ylim(95,105) 
    plt.show()
#violinplot1()

'''
看止损,移动止损,选移动止损的止损依据
---------------------------------------------------------------
---------------------------------------------------------------
---------------------------------------------------------------
'''
# 条件
cond = True  # 0 没条件
#cond = df.o > df.c.shift(1)  #  今天开盘大于昨天收盘，今天向上的概率更大
#cond = df.o < df.c.shift(1)    # 反之，今天开盘大于昨天收盘，今天向上的概率更小
#cond = df.o > df.h.shift(1)    # 今天高开
#cond = df.o < df.l.shift(1)    # 今天低开
#cond = df.o.shift(1)   > df.h.shift(2)    # 昨天高开
#cond = df.o.shift(1)   < df.l.shift(2)    # 昨天低开
#cond = df.l.shift(1) > df.ma.shift(1)  #  昨天K线在ma之上   这两个区别不大
#cond = df.h.shift(1) < df.ma.shift(1)  #  昨天K线在ma之下
# 做多
# 今天低点与昨天低点百分比
df['ll_pct'] = np.where(cond, (df.l / df.l.shift(1)) * 100, np.nan)
# 今天低点与昨天收盘百分比
df['lc_pct'] = np.where(cond, (df.l / (df.c.shift(1)*0.97)) * 100, np.nan)
# 今天低点与昨天收盘减atr的百分比
df['lcatr_pct'] = np.where(cond, (df.l / (df.c.shift(1)-df.atr.shift(1))) * 100, np.nan)
# 今天低点与昨天最高减atr的百分比   这个就是之前用的3atr移动止损依据
df['lhatr_pct'] = np.where(cond, (df.l / (df.h.shift(1)-df.atr.shift(1))) * 100, np.nan)
# 今天低点与昨天实体高点的百分比   
df['lsthatr_pct'] = np.where(cond, (df.l / (df.st_h.shift(1)-df.atr.shift(1))) * 100, np.nan)
# 做空
# 今天高点与昨天高点百分比
df['hh_pct'] = np.where(cond, (df.h / df.h.shift(1)) * 100, np.nan)
# 今天高点与昨天收盘百分比
df['hc_pct'] = np.where(cond, (df.h / df.c.shift(1)) * 100, np.nan)

print(df[['ll_pct','lc_pct','lcatr_pct','lhatr_pct','lsthatr_pct','hh_pct','hc_pct']].describe())

# 第百分之n个数据
getn = int((float(5)/100) * (df.shape[0]))
#print(df['ll_pct'].sort_values().iloc[getn])
#print(df['lc_pct'].sort_values().iloc[getn])
# 柱状图
def foo1(): # 写成函数加减注释容易
    bins=range(-3,3,1) # 范围0到200，每个柱的宽度20
    # hist画柱状图
    plt.hist(df["c_o_pct"],bins,color='#3333ee',width=0.8) 
    plt.xlabel('c_o_pct')
    plt.ylabel('计数')
    plt.plot()
    # 平均值
    plt.axvline(df['c_o_pct'].mean(),linestyle='dashed',color='red')
    plt.show()
#foo1()


def boxplot1():
    df2 = df[['ll_pct','lc_pct','lcatr_pct','lhatr_pct','lsthatr_pct','hh_pct','hc_pct']]
    # 箱型图
    # whis参数指胡须的长度是盒子长度的几倍，
    # 超出这个值被认为是离群点（异常值）
    # #默认1.5
    plt.title(hy)
    sns.boxplot(data=df2)
    plt.ylim(95,105)  #change the scale of the plot
    plt.show()
boxplot1()

def violinplot1():
    plt.title(hy)
    df2 = df[['ll_pct','lc_pct','lcatr_pct','hh_pct','hc_pct']]
    sns.violinplot(data = df2)
    plt.ylim(95,105) 
    plt.show()
#violinplot1()


'''
根据条件看今天是阴还是阳
---------------------------------------------------------------
---------------------------------------------------------------
---------------------------------------------------------------
'''
# 条件

#cond = True  # 0 没条件
cond = df.c.shift(1) > df.o.shift(1)  #  昨天阳线
#cond = df.c.shift(1) < df.o.shift(1)    # 昨天阴线
cond = df.l.shift(1) > df.ma.shift(1)  #  昨天K线在ma之上
cond = df.h.shift(1) < df.ma.shift(1)  #  昨天K线在ma之下
df['pct'] = np.where(cond, (df.c / df.o) * 100, np.nan)

#print(df.pct.describe())
# 柱状图
def foo1(): # 写成函数加减注释容易
    bins=range(-3,3,1) # 范围0到200，每个柱的宽度20
    # hist画柱状图
    plt.hist(df["c_o_pct"],bins,color='#3333ee',width=0.8) 
    plt.xlabel('c_o_pct')
    plt.ylabel('计数')
    plt.plot()
    # 平均值
    plt.axvline(df['c_o_pct'].mean(),linestyle='dashed',color='red')
    plt.show()
#foo1()


def boxplot1():
    df2 = df[['pct']]
    # 箱型图
    # whis参数指胡须的长度是盒子长度的几倍，
    # 超出这个值被认为是离群点（异常值）
    # #默认1.5
    plt.title(hy)
    sns.boxplot(data=df2)
    plt.ylim(95,105)  #change the scale of the plot
    plt.show()
#boxplot1()