'''
看价格在n天后回来的概率

'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from common import *#get_DKX, get_nhh, get_nll, get_ma, avg,get_nhhzs,get_nllzs,get_atr

def foo():
    pinzhong = 'pp'
    plt.rcParams['font.sans-serif'] = ['SimHei'] # 正常显示中文
    df = pd.read_csv(r'..\data\{}.csv'.format(pinzhong))
    df = get_DKX(df)
    
    nn = 50
    df = get_nhh(df, nn)
    df = get_nll(df, nn)
    df = get_nhh2(df, nn)
    df = get_nll2(df, nn)
    df = get_nhh3(df, 1, nn)  # 隔几天后nn个周期内价格回来的情况
    df = get_nll3(df, 1, nn)
    #df['在n天内'] = np.where((df.c > df.nll)&(df.c < df.nhh) , 1,0)
    #df['在n天内'] = np.where((df.c > df.nll2)&(df.c < df.nhh2) , 1,0)
    df['在n天内'] = np.where((df.o > df.nll3)&(df.o < df.nhh3) , 1,0)
    df = df.dropna()
    df.to_csv('tmp.csv')
    #print(df.sum(axis=0))
    sum_ = df.sum(axis=0)
    print(sum_['在n天内'] / df.shape[0], 'n天内概率')

#foo()


def foo1():
    pass