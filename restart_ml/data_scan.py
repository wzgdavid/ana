import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


plt.rcParams['font.sans-serif'] = ['SimHei'] # 正常显示中文
hy = 'c' # rb ta m c jd dy cs
df = pd.read_csv(r'..\data\{}.csv'.format(hy))
#df = pd.read_csv(r'..\data\ta.csv')
#df = pd.read_csv(r'..\data\m.csv')
#df = pd.read_csv(r'..\data\c.csv')
#df = pd.read_csv(r'..\data\jd.csv')
# 一段时间买入持有
first_open = df.o.iloc[0]
last_close = df.c.iloc[-1]
#print(last_close - first_open)
# 每天开盘价买入，收盘价卖出
#df['daily_change'] = df.c - df.o
#print(df.daily_change.sum())


# 条件

cond = True  # 0 没条件
#cond = df.o > df.c.shift(1)  # 1 今天高开，即今天开盘大于昨天收盘
cond = df.o > df.h.shift(1)    # 1 今天高开，今天开盘大于昨天高点
#cond = df.o < df.h.shift(1)    #
#cond = df.o < df.c.shift(1)    #
cond = df.o < df.l.shift(1)    #
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
    plt.ylim(91,109)  #change the scale of the plot
    plt.show()
#boxplot1()


'''
---------------------------------------------------------------
---------------------------------------------------------------
---------------------------------------------------------------
'''
# 条件

#cond = True  # 0 没条件
cond = df.o > df.c.shift(1)  # 1 今天高开，即今天开盘大于昨天收盘

# 今天高点与昨天收盘百分比
#df['aa'] = df.o.shift(1)
df['hc_pct'] = np.where(cond, (df.h / df.c.shift(1)) * 100, np.nan)
# 今天低点与昨天收盘百分比
df['lc_pct'] = np.where(cond, (df.l / df.c.shift(1)) * 100, np.nan)
# 今天收盘与昨天收盘百分比
df['cc_pct'] = np.where(cond, (df.c / df.c.shift(1)) * 100, np.nan)

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
    plt.ylim(91,109)  #change the scale of the plot
    plt.show()
#boxplot1()





'''
看止损
---------------------------------------------------------------
---------------------------------------------------------------
---------------------------------------------------------------
'''
# 条件

cond = True  # 0 没条件
#cond = df.o > df.c.shift(1)  # 1 今天高开，即今天开盘大于昨天收盘
#cond = df.o < df.c.shift(1)    #
#cond = df.o > df.h.shift(1)    # 1 今天高开，今天开盘大于昨天高点
#cond = df.o < df.l.shift(1)    #

#cond = df.o < df.l.shift(1)    #
# 做多
# 今天低点与昨天低点百分比
df['ll_pct'] = np.where(cond, (df.l / df.l.shift(1)) * 100, np.nan)
# 今天低点与昨天收盘百分比
df['lc_pct'] = np.where(cond, (df.l / df.c.shift(1)) * 100, np.nan)
# 做空
# 今天高点与昨天高点百分比
df['hh_pct'] = np.where(cond, (df.h / df.h.shift(1)) * 100, np.nan)
# 今天高点与昨天收盘百分比
df['hc_pct'] = np.where(cond, (df.h / df.c.shift(1)) * 100, np.nan)
print(df[['ll_pct','lc_pct','hh_pct','hc_pct']].describe())
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
    df2 = df[['ll_pct','lc_pct','hh_pct','hc_pct']]
    # 箱型图
    # whis参数指胡须的长度是盒子长度的几倍，
    # 超出这个值被认为是离群点（异常值）
    # #默认1.5
    plt.title(hy)
    sns.boxplot(data=df2)
    plt.ylim(91,109)  #change the scale of the plot
    plt.show()
boxplot1()