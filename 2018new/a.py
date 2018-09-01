
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
 
    pinzhong = 'sr'
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
    时长 =20

    df = get_nll2(df, 时长)  # 作为时长期内的止损
    df = get_nhh2(df, 时长)  # 作为时长期内的止盈
    df['平仓价'] = df['c'].shift(-时长)
    费用 = 4 # 考虑有滑点和手续费 平均算4点     能看出用的周期越大（盈亏幅度大），费用的影响越小
    df['winloss'] = (df['平仓价'] - df['c'] - 费用)   # 不算止损止盈   盈亏
    n = 1  # atr止损倍数
    m = 2  # atr止盈倍数
    df['止损价'] = df.c - df.atr * n # 以多少倍的ATR作为止损
    df['止盈价'] = df.c + df.atr * m # 以多少倍的ATR作为止盈
    
    df['winloss_zs'] = np.where(df.nll2 < df.止损价, -(df.atr*n+费用), df.winloss)  #   算上止损  盈亏   
    df['winloss_zy'] = np.where(df.nhh2 > df.止盈价, df.atr*m-费用, df.winloss)  #   算上止盈  盈亏
    #df['winloss_atr'] = (df['平仓价'] - df['c']) / df.atr  # 盈亏占多少ATR


    df['winloss_zszy'] = np.where(df.nhh2 > df.止盈价, df.atr*m-费用, df.winloss_zs)  # 止损 止盈 都有 看哪个比例好   先计止盈
    df['winloss_zszy1'] = np.where(df.nll2 < df.止损价, -(df.atr+费用), df.winloss_zy) # 先计止损    结果这个应该比前者好， 但这是bug，真实结果介于两者之间

    df.to_csv('tmp.csv')



    '''
    过滤  start
    '''
    #df = df.iloc[:4000,  :]  #选择部分

    df['condition'] = np.where(df.l.shift(1)>df.ma.shift(1), 1, None) #  df.c.shift(1)>df.ma.shift(1)  在ma上
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
    df['win_zy'] = np.where(df.winloss_zy>0, df.winloss_zy, None)
    df['loss_zy'] = np.where(df.winloss_zy<=0, df.winloss_zy, None)
    df['win_zszy'] = np.where(df.winloss_zszy>0, df.winloss_zszy, None)
    df['loss_zszy'] = np.where(df.winloss_zszy<=0, df.winloss_zszy, None)
    df['win_zszy1'] = np.where(df.winloss_zszy1>0, df.winloss_zszy1, None)
    df['loss_zszy1'] = np.where(df.winloss_zszy1<=0, df.winloss_zszy1, None)

    win = df['win'].count()
    loss = df['loss'].count()
    winp = win/(win+loss)   # 盈利比例
    print('不带止损止盈胜率  ', winp)

    win2 = df['win_zs'].count()
    loss2 = df['loss_zs'].count()
    winp2 = win2/(win2+loss2)   # 盈利比例
    print('只带带止损胜率  ', winp2)

    win3 = df['win_zszy'].count()
    loss3 = df['loss_zszy'].count()
    winp3 = win3/(win3+loss3)   # 盈利比例
    print('带止盈止损胜率  先记止盈', winp3)

    win3 = df['win_zszy1'].count()
    loss3 = df['loss_zszy1'].count()
    winp3 = win3/(win3+loss3)   # 盈利比例
    print('带止盈止损胜率  先记止损 ', winp3)

    盈亏比 = df['win'].sum() / abs(df['loss'].sum())
    print('不带止损盈亏比  ', 盈亏比)
    盈亏比 = df['win_zs'].sum() / abs(df['loss_zs'].sum())
    print('只带止损盈亏比  ', 盈亏比)
    盈亏比 = df['win_zy'].sum() / abs(df['loss_zy'].sum())
    print('只带止盈的盈亏比  ', 盈亏比)
    盈亏比 = df['win_zszy'].sum() / abs(df['loss_zszy'].sum())
    print('带止盈止损的盈亏比 先记止盈 ', 盈亏比)
    盈亏比 = df['win_zszy1'].sum() / abs(df['loss_zszy1'].sum())
    print('带止盈止损的盈亏比 先记止损  ', 盈亏比)
    
    #print(df.describe()[['winloss','winloss_zs']])
foo()


print('-----------------------------------')

def foo2():

    '''
    同foo， 不过是只看做空
    '''
 
    pinzhong = 'rbl91h'
    plt.rcParams['font.sans-serif'] = ['SimHei']
    df = pd.read_csv(r'..\data\{}.csv'.format(pinzhong))

    df = get_ma(df, 5)
    df['ma1'] = df.ma
    df = get_ma(df, 10)
    df['ma2'] = df.ma
    df = get_ma(df, 20)
    df['ma3'] = df.ma
    df = get_ma(df, 30)
    df['ma4'] = df.ma
    df = get_atr(df, 50)


    '''以做多为例'''
    时长 = 7

    df = get_nll2(df, 时长)  # 作为时长期内的止损
    df = get_nhh2(df, 时长)  # 作为时长期内的止盈
    df['平仓价'] = df['c'].shift(-时长)
    费用 = 3 # 考虑有滑点和手续费 平均算4点     能看出用的周期越大（盈亏幅度大），费用的影响越小
    df['winloss'] = (df['c'] - df['平仓价']-费用 )   # 不算止损止盈   盈亏
    df['止损价'] = df.c + df.atr * 2 # 以多少倍的ATR作为止损
    df['止盈价'] = df.c - df.atr * 2 # 以多少倍的ATR作为止盈
    #df['winloss_zs'] = np.where(df.止损价 < df.平仓价, -df.atr, df.winloss)  #   算上止损  盈亏
    df['winloss_zs'] = np.where(df.nhh2 > df.止损价, -(df.atr+费用), df.winloss)
    df['winloss_zy'] = np.where(df.nll2 < df.止盈价, (df.atr - 费用), df.winloss)  #   算上止盈  盈亏

    df['winloss_zszy'] = np.where(df.nhh2 > df.止损价, -(df.atr+费用), df.winloss)  # 止损 止盈 都有 看哪个比例好 
    #df['winloss_atr'] = (df['c'] - df['平仓价']) / df.atr  # 盈亏占多少ATR

    df.to_csv('tmp.csv')
    #df = df.iloc[4000:,  :]  #选择部分

    #df['condition'] = np.where(df.c.shift(1)>df.ma.shift(1), 1, None) #  df.c.shift(1)>df.ma.shift(1)  在ma上
    #df['condition1'] = np.where(df.ma.shift(1)>df.ma.shift(2), 1, None) # df.ma.shift(1)>df.ma.shift(2)  ma斜率向上
    #df['condition2'] = np.where(df.c.shift(1) < df.o.shift(1),1, None)   # 前一根是阴线
    #df['condition2b'] = np.where((df.c.shift(1) < df.o.shift(1))  & (df.c.shift(2) < df.o.shift(2)),1, None) #前面连着两根阴线
    #df['condition2c'] = np.where( ( df.c.shift(1) < df.o.shift(1)) & (df.c.shift(2) < df.o.shift(2)) & (df.c.shift(3) < df.o.shift(3)),1, None)  #前面连着3根阴线
    #df['condition3'] = np.where(df.c < df.c.shift(2)    ,1,None)  # 在前两周期内下跌超过一个ATR
    df['condition4'] = np.where(df.c < df.c.shift(2)    ,1,None)    # ma
    df = df.dropna()

    # 统计盈亏比
    df['win'] = np.where(df.winloss>0, df.winloss, None)
    df['loss'] = np.where(df.winloss<=0, df.winloss, None)
    df['win_zs'] = np.where(df.winloss_zs>0, df.winloss_zs, None)
    df['loss_zs'] = np.where(df.winloss_zs<=0, df.winloss_zs, None)
    df['win_zy'] = np.where(df.winloss_zy>0, df.winloss_zy, None)
    df['loss_zy'] = np.where(df.winloss_zy<=0, df.winloss_zy, None)

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
    盈亏比 = df['win_zy'].sum() / abs(df['loss_zy'].sum())
    print('带止盈的盈亏比  ', 盈亏比)
    
    print(df.describe()[['winloss','winloss_zs']])
#foo2()