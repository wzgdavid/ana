# encoding: utf-8
import sys
from itertools import combinations
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import util
'''
看n天里最低，最高点,变动范围
'''

@util.display_func_name
def bar(daima, days=5):
    '''
    '''
    df = pd.read_csv('data/%s.xls' % daima)
    util.strip_columns(df)
    df = df.loc[:, ['date', 'open', 'high', 'close', 'low']]

    df['low_pct'] = (df.open - pd.rolling_min(df.low, days)) / df.open
    df['high_pct'] = (pd.rolling_max(df.high, days) - df.open) / df.open
    rolling_low = pd.rolling_min(df.low, days)

    func_name = sys._getframe().f_code.co_name
    df = df.loc[days: , :]  # 因为近期的看不到n天后的数据，所以没收益，因此不计算
    
    df.to_csv('files_tmp/%s_%s.csv' % (func_name, daima))  # 以函数名作为文件名保存

    median =  df.low_pct.median()
    median2 =  df.high_pct.median()
    lowsorted = sorted(df.low_pct)

    highsorted = sorted(df.high_pct)
    print lowsorted[len(lowsorted)*2/3],  highsorted[len(lowsorted)*2/3]
    print median, median2



    #return summ, average_earnings, summ2, average_earnings2, count
    
#bar('cyb', days=10)



@util.display_func_name
def foo3(daima, ma='ma5', days=5):
    '''
    '''
    df = pd.read_csv('data/%s.xls' % daima)
    util.strip_columns(df)
    df = df.loc[:, ['date', 'open', 'high', 'close', 'low']]
    df['gt_ma'] = df.low.shift(-1) > df[ma].shift(-1)
    df['low_pct'] = (df.open - pd.rolling_min(df.low, days)) / df.open
    df['high_pct'] = (pd.rolling_max(df.high, days) - df.open) / df.open
    rolling_low = pd.rolling_min(df.low, days)

    func_name = sys._getframe().f_code.co_name
    df = df.loc[days: , :]  # 因为近期的看不到n天后的数据，所以没收益，因此不计算
    
    df.to_csv('files_tmp/%s_%s.csv' % (func_name, daima))  # 以函数名作为文件名保存

    median =  df.low_pct.median()
    median2 =  df.high_pct.median()
    lowsorted = sorted(df.low_pct)

    highsorted = sorted(df.high_pct)
    print lowsorted[len(lowsorted)*2/3],  highsorted[len(lowsorted)*2/3]
    print median, median2


    # yesterday greater than ma
    df['gt_ma'] = df.low.shift(-1) > df[ma].shift(-1)
    df['earning'] = np.where(df['gt_ma'], df.close.shift(days) - df.open, 0)
    #df['earning2'] = np.where(df.close < df[ma], df.close.shift(days) - df.close, 0)
    #print df['earning'].sum()
    df['stoploss_point'] = df.open * (1-scope)
    rolling_low = pd.rolling_min(df.low, days)
    df['stoploss'] = np.where(df['gt_ma'], df.stoploss_point - df.open , 0)

    df['earning_with_stoploss'] = np.where(rolling_low > df.stoploss_point, df.earning, df.stoploss)
    
    func_name = sys._getframe().f_code.co_name
    df = df.loc[days: , :]  # 因为近期的看不到n天后的数据，所以没收益，因此不计算
    
    df.to_csv('files_tmp/%s_%s.csv' % (func_name, daima))  # 以函数名作为文件名保存

    df = df.where(df.earning != 0) # for count
    summ = df.earning.sum()
    summ2 = df.earning_with_stoploss.sum()

    count = df.earning.count() # count is same
    count2 = df.earning_with_stoploss.count()

    average_earnings =  summ / count
    average_earnings2 =  summ2 / count #

    print average_earnings, average_earnings2
    print summ, summ2
    print count, count2
    
    return summ, average_earnings, summ2, average_earnings2, count
#print foo3('999999', ma='ma20', days=250, scope=0.05)