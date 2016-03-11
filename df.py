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

M = 4 

@util.display_func_name
def bar(daima, days=5):
    '''
    '''
    df = pd.read_csv('data/%s.xls' % daima)
    util.strip_columns(df)
    df = df.loc[:, ['date', 'open', 'high', 'close', 'low']]

    df['low_pct'] = (pd.rolling_min(df.low, days) - df.open) / df.open
    df['high_pct'] = (pd.rolling_max(df.high, days) - df.open) / df.open

    func_name = sys._getframe().f_code.co_name
    df = df.loc[days: , :]  # 因为近期的看不到n天后的数据，所以没收益，因此不计算
    
    df.to_csv('files_tmp/%s_%s.csv' % (func_name, daima))  # 以函数名作为文件名保存

    median_low =  df.low_pct.median()
    median_high =  df.high_pct.median()
    lowsorted = sorted(df.low_pct, reverse=True)

    highsorted = sorted(df.high_pct)
    #print lowsorted
    #print highsorted
    print lowsorted[len(lowsorted)*M/10],  highsorted[len(highsorted)*M/10]
    print median_low, median_high



    #return summ, average_earnings, summ2, average_earnings2, count
    
#bar('999999', days=10)



@util.display_func_name
def gt_ma(daima, ma='ma5', days=5):
    '''
    '''
    df = pd.read_csv('data/%s.xls' % daima)
    util.strip_columns(df)
    df = df.loc[:, ['date', 'open', 'high', 'close', 'low', 'ma5', 'ma10', 'ma20']]
    df['gt_ma'] = df.low.shift(-1) > df[ma].shift(-1)
    low_value = (pd.rolling_min(df.low, days) - df.open) / df.open
    high_value = (pd.rolling_max(df.high, days) - df.open) / df.open

    df['low_pct'] = np.where(df['gt_ma'], low_value , 9)
    df['high_pct'] = np.where(df['gt_ma'], high_value , 9)


    func_name = sys._getframe().f_code.co_name
    df = df.loc[days: , :]  # 因为近期的看不到n天后的数据，所以没收益，因此不计算
    df = df[df.low_pct < 9]
    df.to_csv('files_tmp/%s_%s.csv' % (func_name, daima))  # 以函数名作为文件名保存

    median_low =  df.low_pct.median()
    median_high =  df.high_pct.median()
    
    lowsorted = sorted(df.low_pct, reverse=True)
    highsorted = sorted(df.high_pct)

    #print lowsorted
    #print highsorted
    #print lowsorted[len(lowsorted)*2/3],  highsorted[len(highsorted)*2/3]
    print daima, ma, days
    print median_low, median_high


@util.display_func_name
def lt_ma(daima, ma='ma5', days=5):
    '''
    '''
    df = pd.read_csv('data/%s.xls' % daima)
    util.strip_columns(df)
    df = df.loc[:, ['date', 'open', 'high', 'close', 'low', 'ma5', 'ma10', 'ma20']]
    df['lt_ma'] = df.high.shift(-1) < df[ma].shift(-1)
    low_value = (pd.rolling_min(df.low, days) - df.open) / df.open
    high_value = (pd.rolling_max(df.high, days) - df.open) / df.open

    df['low_pct'] = np.where(df['lt_ma'], low_value , 9)
    df['high_pct'] = np.where(df['lt_ma'], high_value , 9)


    func_name = sys._getframe().f_code.co_name
    df = df.loc[days: , :]  # 因为近期的看不到n天后的数据，所以没收益，因此不计算
    df = df[df.low_pct < 9]
    df.to_csv('files_tmp/%s_%s.csv' % (func_name, daima))  # 以函数名作为文件名保存

    median_low =  df.low_pct.median()
    median_high =  df.high_pct.median()
    
    lowsorted = sorted(df.low_pct, reverse=True)
    highsorted = sorted(df.high_pct)

    #print lowsorted
    #print highsorted
    #print lowsorted[len(lowsorted)*2/3],  highsorted[len(highsorted)*2/3]
    print daima, ma, days
    print median_low, median_high
#bar('999999', days=10)
#gt_ma('999999', ma='ma5', days=10)
#lt_ma('999999', ma='ma5', days=10)

@util.display_func_name
def ma_up(daima, ma='ma5', days=5):
    '''
    '''
    df = pd.read_csv('data/%s.xls' % daima)
    util.strip_columns(df)
    df = df.loc[:, ['date', 'open', 'high', 'close', 'low', 'ma5', 'ma10', 'ma20']]
    df['ma_up'] = df[ma].shift(-1) > df[ma].shift(-2)
    low_value = (pd.rolling_min(df.low, days) - df.open) / df.open
    high_value = (pd.rolling_max(df.high, days) - df.open) / df.open

    df['low_pct'] = np.where(df['ma_up'], low_value , 9)
    df['high_pct'] = np.where(df['ma_up'], high_value , 9)


    func_name = sys._getframe().f_code.co_name
    df = df.loc[days: , :]  # 因为近期的看不到n天后的数据，所以没收益，因此不计算
    df = df[df.low_pct < 9]
    df.to_csv('files_tmp/%s_%s.csv' % (func_name, daima))  # 以函数名作为文件名保存

    median_low =  df.low_pct.median()
    median_high =  df.high_pct.median()
    
    lowsorted = sorted(df.low_pct, reverse=True)
    highsorted = sorted(df.high_pct)

    #print lowsorted
    #print highsorted
    #print lowsorted[len(lowsorted)*2/3],  highsorted[len(highsorted)*2/3]
    print daima, ma, days
    print median_low, median_high




@util.display_func_name
def ma_down(daima, ma='ma5', days=5):
    '''
    '''
    df = pd.read_csv('data/%s.xls' % daima)
    util.strip_columns(df)
    df = df.loc[:, ['date', 'open', 'high', 'close', 'low', 'ma5', 'ma10', 'ma20']]
    df['ma_down'] = df[ma].shift(-1) < df[ma].shift(-2)
    low_value = (pd.rolling_min(df.low, days) - df.open) / df.open
    high_value = (pd.rolling_max(df.high, days) - df.open) / df.open

    df['low_pct'] = np.where(df['ma_down'], low_value , 9)
    df['high_pct'] = np.where(df['ma_down'], high_value , 9)


    func_name = sys._getframe().f_code.co_name
    df = df.loc[days: , :]  # 因为近期的看不到n天后的数据，所以没收益，因此不计算
    df = df[df.low_pct < 9]
    df.to_csv('files_tmp/%s_%s.csv' % (func_name, daima))  # 以函数名作为文件名保存

    median_low =  df.low_pct.median()
    median_high =  df.high_pct.median()
    
    lowsorted = sorted(df.low_pct, reverse=True)
    highsorted = sorted(df.high_pct)

    #print lowsorted
    #print highsorted
    #print lowsorted[len(lowsorted)*2/3],  highsorted[len(highsorted)*2/3]
    print daima, ma, days
    print median_low, median_high

bar('999999', days=10)
ma_up('999999', ma='ma20', days=10)
gt_ma('999999', ma='ma20', days=10)
gt_ma('999999', ma='ma10', days=10)
gt_ma('999999', ma='ma5', days=10)

def run_gtma():
    daimas = ['999999', 'hs300', 'cyb', 'zxb']
    mas = ['ma5', 'ma10', 'ma20']
    days = 9
    for daima in daimas:
        bar(daima, days=days)
        for ma in mas:

            gt_ma(daima, ma=ma, days=days)

if __name__ == '__main__':
    #run_gtma()

    pass