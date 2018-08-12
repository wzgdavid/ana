
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


    #df = df.iloc[4000:,  :]  #选择部分
    #df['condition1'] = np.where(df.ma1.shift(1)>df.ma1.shift(2), 1, None) # df.ma.shift(1)>df.ma.shift(2)  ma斜率向上
    #df['condition2'] = np.where(df.ma2.shift(1)>df.ma2.shift(2), 1, None)

    #df['condition3'] = np.where(df.c.shift(1)>df.ma1.shift(1), 1, None) # 在ma上下
    #df['condition4'] = np.where(df.c.shift(1)>df.ma2.shift(1), 1, None)
    
    # 以特定时间
    #df['condition5'] = np.where(df.date.str.contains('10:45', regex=False), 1, None)
    #df['condition5b'] = np.where(df.date.str.contains('13:45', regex=False), 1, None)
    #df['condition5c'] = np.where(df.date.str.contains('14:45', regex=False), 1, None)
    #df['condition5d'] = np.where(df.date.str.contains('15:00', regex=False), 1, None)
    #df['condition5e'] = np.where(df.date.str.contains('22:00', regex=False), 1, None)
    #df['condition5f'] = np.where(df.date.str.contains('23:00', regex=False), 1, None)


    #df['不能浮亏'] = np.where(df.c>df.c.shift(2), 1, None)   # df.c>df.c.shift(2)  做多不能浮亏

    '''以做多为例'''
    时长 = 8

    df = get_nll2(df, 时长)  # 作为时长期内的止损
    df['平仓价'] = df['c'].shift(-时长)
    df['winloss'] = (df['平仓价'] - df['c']) 
    df['止损价'] = df.c - df.atr * 1 # 以多少倍的ATR作为止损
    df['winloss_zs'] = np.where(df.止损价 > df.平仓价, -df.atr, df.winloss)

    df['winloss_atr'] = (df['c'].shift(-时长) - df['c']) / df.atr  # 盈亏占多少ATR

    df.to_csv('tmp.csv')
    df = df.dropna()

    # 统计盈亏比
    df['win'] = np.where(df.winloss>0, df.winloss, None)
    df['loss'] = np.where(df.winloss<=0, df.winloss, None)
    df['win_zs'] = np.where(df.winloss_zs>0, df.winloss_zs, None)
    df['loss_zs'] = np.where(df.winloss_zs<=0, df.winloss_zs, None)
    #win = df['win'].count()
    #loss = df['loss'].count()
    #winp = win/(win+loss)   # 盈利比例
    #lossp = loss/(win+loss)  # 亏损 比例
    #winm = df['win'].mean()   # 平均盈利
    #lossm = abs(df['loss'].mean())  # 平均亏损
    #盈亏比 = (winm*winp) / (lossm*lossp)
    #print(盈亏比)
    盈亏比 = df['win'].sum() / abs(df['loss'].sum())
    print('不带止损盈亏比  ', 盈亏比)
    盈亏比 = df['win_zs'].sum() / abs(df['loss_zs'].sum())
    print('带止损盈亏比  ', 盈亏比)
    
    
    print(df.describe()[['winloss','winloss_zs','winloss_atr']])
foo()


#def foo2():