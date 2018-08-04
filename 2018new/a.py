
'''
算盈亏比
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from common import *#get_DKX, get_nhh, get_nll, get_ma, avg,get_nhhzs,get_nllzs,get_atr


def foo():

    '''
    一小时线为主周期，固定时间持仓
    计算盈亏比，
    '''
 
    pinzhong = 'ml91h'
    plt.rcParams['font.sans-serif'] = ['SimHei']
    df = pd.read_csv(r'..\data\{}.csv'.format(pinzhong))

    df = get_ma(df, 20)
    df['ma1'] = df.ma
    df = get_ma(df, 200)
    df['ma2'] = df.ma

    df = get_atr(df, 50)

    df['condition1'] = np.where(df.ma1.shift(1)>df.ma1.shift(2), 1, None) # df.ma.shift(1)>df.ma.shift(2)  ma斜率向上
    df['condition2'] = np.where(df.ma2.shift(1)>df.ma2.shift(2), 1, None)

    #df['condition3'] = np.where(df.c.shift(1)>df.ma1.shift(1), 1, None) # 在ma上下
    #df['condition4'] = np.where(df.c.shift(1)>df.ma2.shift(1), 1, None)


    #df['不能浮亏'] = np.where(df.c>df.c.shift(2), 1, None)   # df.c>df.c.shift(2)  做多不能浮亏
    时长 = 30
    df['平仓价'] = df['c'].shift(-时长)
    df['winloss'] = (df['平仓价'] - df['c']) 
    df['winloss_atr'] = (df['c'].shift(-时长) - df['c']) / df.atr
    df.to_csv('tmp.csv')
    df = df.dropna()

    # 统计盈亏比
    df['win'] = np.where(df.winloss>0, df.winloss, None)

    df['loss'] = np.where(df.winloss<=0, df.winloss, None)

    win = df['win'].count()
    loss = df['loss'].count()
    winp = win/(win+loss)   # 盈利比例
    lossp = loss/(win+loss)  # 亏损 比例
    winm = df['win'].mean()   # 平均盈利
    lossm = abs(df['loss'].mean())  # 平均亏损
    盈亏比 = (winm*winp) / (lossm*lossp)
    print(盈亏比)
    
    
    


    print(df.describe()[['winloss','winloss_atr']])
foo()


def foo2():