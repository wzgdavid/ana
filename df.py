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
    df = df.loc[:, ['date', 'open', 'close', 'low']]

    df['low_pct'] = (df.open - pd.rolling_min(df.low, days)) / df.open
    rolling_low = pd.rolling_min(df.low, days)

    func_name = sys._getframe().f_code.co_name
    df = df.loc[days: , :]  # 因为近期的看不到n天后的数据，所以没收益，因此不计算
    
    df.to_csv('files_tmp/%s_%s.csv' % (func_name, daima))  # 以函数名作为文件名保存

    avg6 =  df.low_pct.median()

    s = sorted(df.low_pct)
    print s[len(s)*2/3]
    print avg6


    
    #return summ, average_earnings, summ2, average_earnings2, count
    
bar('cyb', days=10)