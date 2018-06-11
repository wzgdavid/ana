'''
每天的平均波幅
因为这个取中位数比较的，所以用主连也问题不大，主连真实点，下次弄主连数据
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from common import *#get_DKX, get_nhh, get_nll, get_ma, avg,get_nhhzs,get_nllzs,get_atr

def foo1():
    pinzhong = 'y'
    plt.rcParams['font.sans-serif'] = ['SimHei']
    df = pd.read_csv(r'..\data\{}.csv'.format(pinzhong))
    df = get_ma(df, 20)
    #df['condition'] = np.where(df.c.shift(1)<df.ma.shift(1), 1, None) 
    
    df = df.dropna()
    df['收盘的波幅'] = df.c/df.c.shift(1)
    df['高价的波幅'] = df.h/df.c.shift(1)-1
    df['低价的波幅'] = 1-df.l/df.c.shift(1)


    print(df.describe()[['收盘的波幅','高价的波幅','低价的波幅']])
    df.to_csv('tmp.csv')
foo1()



'''
==============================================================================
'''

def foo2():
    pinzhong = 'rb'
    plt.rcParams['font.sans-serif'] = ['SimHei']
    df = pd.read_csv(r'..\data\{}.csv'.format(pinzhong))
    df = get_ma(df, 20)
    #df['condition'] = np.where(df.c.shift(1)>df.ma.shift(1), 1, None) 
    #df = df.dropna()

    df['阴阳'] = np.where(df.c>df.o, 1, None) 
    df['阴阳'] = np.where(df.c<df.o, 0, df['阴阳']) 
    df['h_to_c'] = df.h/df.c - 1
    df['l_to_c'] = 1 - df.l/df.c
    yang = df[df['阴阳']==1]
    yin = df[df['阴阳']==0]
    need_list = ['h_to_c','l_to_c']
    print(df.describe()[need_list])
    print(yang.describe()[need_list])
    print(yin.describe()[need_list])
    df.to_csv('tmp.csv')
    #df['aa'] = # 阳线高点到当天收盘价波幅
#foo2()