
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
 
    pinzhong = 'pp'
    plt.rcParams['font.sans-serif'] = ['SimHei']
    df = pd.read_csv(r'..\data\{}.csv'.format(pinzhong))

    df = get_ma(df, 5)
    df['ma1'] = df.ma
    df = get_ma(df, 11)
    df['ma2'] = df.ma
    df = get_ma(df, 17)
    df['ma3'] = df.ma
    df = get_ma(df, 17)
    df['ma4'] = df.ma

    df = get_atr(df, 50)


    '''以做多为例'''
    时长 =10

    df = get_nll2(df, 时长)  # 作为时长期内的止损
    df = get_nhh2(df, 时长)  # 作为时长期内的止盈
    df['平仓价'] = df['c'].shift(-时长)
    费用 = 4 # 考虑有滑点和手续费 平均算4点     能看出用的周期越大（盈亏幅度大），费用的影响越小
    df['winloss'] = (df['平仓价'] - df['c'] - 费用)   # 不算止损止盈   盈亏
    n = 1 # atr止损倍数
    df['止损价'] = df.c - df.atr * n # 以多少倍的ATR作为止损
    
    df['winloss_zs'] = np.where(df.nll2 < df.止损价, -(df.atr*n+费用), df.winloss)  #   算上止损  盈亏   

    df.to_csv('tmp.csv')



    '''
    过滤  start
    '''
    #df = df.iloc[2500:3000,  :]  #选择部分

    #df['condition'] = np.where(df.l.shift(1)>df.ma.shift(1), 1, None) #  df.c.shift(1)>df.ma.shift(1)  在ma上
    #df['condition1'] = np.where(df.ma.shift(1)>df.ma.shift(2), 1, None) # df.ma.shift(1)>df.ma.shift(2)  ma斜率向上
    #df['condition2'] = np.where(df.c.shift(1) < df.o.shift(1),1, None)   # 前一根是阴线
    #df['condition2b'] = np.where((df.c.shift(1) < df.o.shift(1))  & (df.c.shift(2) < df.o.shift(2)),1, None) #前面连着两根阴线
    #df['condition2c'] = np.where( ( df.c.shift(1) < df.o.shift(1)) & (df.c.shift(2) < df.o.shift(2)) & (df.c.shift(3) < df.o.shift(3)),1, None)  #前面连着3根阴线
    #df['condition3'] = np.where(df.c < df.c.shift(2)    ,1,None)  # 在前两周期内下跌超过一个ATR
    #df['condition4'] = np.where(df.c.shift(1) - df.c.shift(7) > df.atr*0.2, 1, None)
    #df['condition5'] = np.where( (df.ma1.shift(1) > df.ma2.shift(1))  &
    #        (df.ma2.shift(1)  > df.ma3.shift(1)) &
    #        (df.ma2.shift(1)  > df.ma3.shift(1)), 1, None)  # ma多头排列

    #df['condition6'] = np.where((df.c > df.c.shift(2)) & (df.c.shift(2) > df.c.shift(4)) , 1, None)  # 前仓浮盈， 才能开后仓  df.c 这次开仓价   df.c.shift(n) 代表上次开仓价
    #df['condition5b'] = np.where( (df.ma1.shift(1) < df.ma2.shift(1))  &
    #        (df.ma2.shift(1)  < df.ma3.shift(1)) &
    #        (df.ma3.shift(1)  < df.ma4.shift(1)), 1, None)  # ma空头排列

    #df['condition5c'] = np.where( ~ ((df.ma1.shift(1) < df.ma2.shift(1))  &
    #        (df.ma2.shift(1)  < df.ma3.shift(1)) &
    #        (df.ma3.shift(1)  < df.ma4.shift(1))), 1, None)  # 非 ma空头排列
    df = df.dropna()

    '''
    过滤 end
    '''



    # 统计盈亏比
    df['win'] = np.where(df.winloss>0, df.winloss, None)
    df['loss'] = np.where(df.winloss<=0, df.winloss, None)
    df['win_zs'] = np.where(df.winloss_zs>0, df.winloss_zs, None)
    df['loss_zs'] = np.where(df.winloss_zs<=0, df.winloss_zs, None)


    win = df['win'].count()
    loss = df['loss'].count()
    winp = win/(win+loss)   # 盈利比例
    print('不带止损止盈胜率  ', winp)

    win2 = df['win_zs'].count()
    loss2 = df['loss_zs'].count()
    winp2 = win2/(win2+loss2)   # 盈利比例
    print('带止损胜率  ', winp2)


    盈亏比 = df['win'].sum() / abs(df['loss'].sum())
    print('不带止损盈亏比  ', 盈亏比)
    盈亏比 = df['win_zs'].sum() / abs(df['loss_zs'].sum())
    print('带止损盈亏比  ', 盈亏比)
    print('交易次数',df.shape[0])
    #print(df.describe()[['winloss','winloss_zs']])
    return 盈亏比, df.shape[0]
b1,b2 = foo()


print('-----------------------------------')

def foo2():

    '''
    一小时线为主周期，固定时间持仓
    计算盈亏比，
    '''
 
    pinzhong = 'y'
    plt.rcParams['font.sans-serif'] = ['SimHei']
    df = pd.read_csv(r'..\data\{}.csv'.format(pinzhong))

    df = get_ma(df, 5)
    df['ma1'] = df.ma
    df = get_ma(df, 11)
    df['ma2'] = df.ma
    df = get_ma(df, 17)
    df['ma3'] = df.ma
    df = get_ma(df, 17)
    df['ma4'] = df.ma

    df = get_atr(df, 50)


   
    时长 =10

    df = get_nll2(df, 时长)  # 作为时长期内的止损
    df = get_nhh2(df, 时长)  # 作为时长期内的止盈
    df['平仓价'] = df['c'].shift(-时长)
    费用 = 4 # 考虑有滑点和手续费 平均算4点     能看出用的周期越大（盈亏幅度大），费用的影响越小
    df['winloss'] = (df['c'] - df['平仓价'] - 费用 )    # 不算止损止盈   盈亏
    n = 1  # atr止损倍数
    df['止损价'] = df.c + df.atr * n # 以多少倍的ATR作为止损
    
    df['winloss_zs'] = np.where(df.nhh2 > df.止损价, -(df.atr*n+费用), df.winloss)
    df.to_csv('tmp.csv')



    '''
    过滤  start
    '''
    df = df.iloc[2500:3000,  :]  #选择部分

    df['condition'] = np.where(df.c.shift(1)<df.ma.shift(1), 1, None) #  df.c.shift(1)>df.ma.shift(1)  在ma下
    df['condition1'] = np.where(df.ma.shift(1)<df.ma.shift(2), 1, None) # df.ma.shift(1)>df.ma.shift(2)  ma斜率向下
    #df['condition2'] = np.where(df.c.shift(1) < df.o.shift(1),1, None)   # 前一根是阴线
    #df['condition2b'] = np.where((df.c.shift(1) < df.o.shift(1))  & (df.c.shift(2) < df.o.shift(2)),1, None) #前面连着两根阴线
    #df['condition2c'] = np.where( ( df.c.shift(1) < df.o.shift(1)) & (df.c.shift(2) < df.o.shift(2)) & (df.c.shift(3) < df.o.shift(3)),1, None)  #前面连着3根阴线
    #df['condition3'] = np.where(df.c < df.c.shift(2)    ,1,None)  # 在前两周期内下跌超过一个ATR
    #df['condition4'] = np.where(df.c.shift(1) - df.c.shift(7) > df.atr*0.2, 1, None)
    #df['condition5'] = np.where( (df.ma1.shift(1) > df.ma2.shift(1))  &
    #        (df.ma2.shift(1)  > df.ma3.shift(1)) &
    #        (df.ma2.shift(1)  > df.ma3.shift(1)), 1, None)  # ma多头排列

    #df['condition6'] = np.where((df.c > df.c.shift(2)) & (df.c.shift(2) > df.c.shift(4)) , 1, None)  # 前仓浮盈， 才能开后仓  df.c 这次开仓价   df.c.shift(n) 代表上次开仓价
    #df['condition5b'] = np.where( (df.ma1.shift(1) < df.ma2.shift(1))  &
    #        (df.ma2.shift(1)  < df.ma3.shift(1)) &
    #        (df.ma3.shift(1)  < df.ma4.shift(1)), 1, None)  # ma空头排列

    #df['condition5c'] = np.where( ~ ((df.ma1.shift(1) < df.ma2.shift(1))  &
    #        (df.ma2.shift(1)  < df.ma3.shift(1)) &
    #        (df.ma3.shift(1)  < df.ma4.shift(1))), 1, None)  # 非 ma空头排列
    df = df.dropna()

    '''
    过滤 end
    '''



    # 统计盈亏比
    df['win'] = np.where(df.winloss>0, df.winloss, None)
    df['loss'] = np.where(df.winloss<=0, df.winloss, None)
    df['win_zs'] = np.where(df.winloss_zs>0, df.winloss_zs, None)
    df['loss_zs'] = np.where(df.winloss_zs<=0, df.winloss_zs, None)


    win = df['win'].count()
    loss = df['loss'].count()
    winp = win/(win+loss)   # 盈利比例
    print('不带止损止盈胜率  ', winp)

    win2 = df['win_zs'].count()
    loss2 = df['loss_zs'].count()
    winp2 = win2/(win2+loss2)   # 盈利比例
    print('带止损胜率  ', winp2)


    盈亏比 = df['win'].sum() / abs(df['loss'].sum())
    print('不带止损盈亏比  ', 盈亏比)
    盈亏比 = df['win_zs'].sum() / abs(df['loss_zs'].sum())
    print('带止损盈亏比  ', 盈亏比)
    print('交易次数',df.shape[0])
    return 盈亏比, df.shape[0]
    #print(df.describe()[['winloss','winloss_zs']])
#s1,s2 = foo2()

#
#多空总体盈亏比 = (b1*b2 + s1*s2)/(b2+s2)

#print('多空总体盈亏比',多空总体盈亏比)
