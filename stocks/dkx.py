import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from common import get_DKX, result

daima = '600096'
df = pd.read_csv(r'..\data\stocks\{}.csv'.format(daima))
#df = pd.read_csv(r'..\data\rb\zs.csv')

df = get_DKX(df)
df['dkx金叉'] = np.where( (df['b'].shift(2)<df['d'].shift(2)) & (df['b'].shift(1)>df['d'].shift(1)), df.o , None )
df['dkx死叉'] = np.where( (df['b'].shift(2)>df['d'].shift(2)) & (df['b'].shift(1)<df['d'].shift(1)), df.o , None )   # 这里好像买用c ，卖用o效果好点 
df['b向上'] = np.where( (df['b'].shift(3)>df['b'].shift(2)) & (df['b'].shift(1)>df['b'].shift(2)),   df.o , None )
df['b向下'] = np.where( (df['b'].shift(3)<df['b'].shift(2)) & (df['b'].shift(1)<df['b'].shift(2)),   df.c , None )
df['d向上'] = np.where( (df['d'].shift(3)>df['d'].shift(2)) & (df['d'].shift(1)>df['d'].shift(2)),   df.o , None )
df['d向下'] = np.where( (df['d'].shift(3)<df['d'].shift(2)) & (df['d'].shift(1)<df['d'].shift(2)),   df.c , None )


def jiaocha(df):
    rows_index = range(df.shape[0])
    rates = []
    hold = 0
    金叉日期 = []
    死叉日期 = []
    for i in rows_index:
        if i == 0:
            continue
        if df.ix[i, 'dkx金叉'] != None and hold==0:
        #if df.ix[i, 'macd金叉'] != None and hold==0:
            buy = df.ix[i, 'dkx金叉']
            hold = 1
            金叉日期.append(df.ix[i, 'date'])
        #else:
        #    buy = df.ix[i-1, 'macd金叉']
    
        if df.ix[i, 'dkx死叉'] != None and hold==1:
            rates.append(df.ix[i, 'dkx死叉']/buy)
            hold = 0
            死叉日期.append(df.ix[i, 'date'])
    
    #print(金叉日期)
    #print(死叉日期)
    result(df, rates)

def xielv_b(df):
    print('--------------------bb-----------------')
    rows_index = range(df.shape[0])
    rates = []
    hold = 0
    买入日期 = []
    卖出日期 = []
    for i in rows_index:
        if i == 0:
            continue
        if df.ix[i, 'b向上'] != None and hold==0:
            buy = df.ix[i, 'b向上']
            hold = 1
            买入日期.append(df.ix[i, 'date'])
    
        if df.ix[i, 'b向下'] != None and hold==1:
            rates.append(df.ix[i, 'b向下']/buy)
            hold = 0
            卖出日期.append(df.ix[i, 'date'])
    #print(买入日期)
    #print(卖出日期)
    result(df, rates)


def xielv_d(df):
    print('--------------------dd-----------------')
    rows_index = range(df.shape[0])
    rates = []
    hold = 0
    for i in rows_index:
        if i == 0:
            continue
        if df.ix[i, 'd向上'] != None and hold==0:
            buy = df.ix[i, 'o']
            hold = 1
        #else:
        #    buy = df.ix[i-1, 'macd金叉']
    
        if df.ix[i, 'd向下'] != None and hold==1:
            rates.append(df.ix[i, 'o']/buy)
            hold = 0
    
    result(df, rates)


def xielv_bd(df):
    print('--------------------bd-----------------')
    rows_index = range(df.shape[0])
    rates = []
    hold = 0
    for i in rows_index:
        if i == 0:
            continue
        if df.ix[i, 'b向上'] != None and hold==0:
            buy = df.ix[i, 'b向上']
            hold = 1
        #else:
        #    buy = df.ix[i-1, 'macd金叉']
    
        if df.ix[i, 'd向下'] != None and hold==1:
            rates.append(df.ix[i, 'd向下']/buy)
            hold = 0
    result(df, rates)

def xielv_db(df):
    '''慢买  快卖'''
    print('--------------------db-----------------')
    rows_index = range(df.shape[0])
    rates = []
    hold = 0
    for i in rows_index:
        if i == 0:
            continue
        if df.ix[i, 'd向上'] != None and hold==0:
            buy = df.ix[i, 'd向上']
            hold = 1
        #else:
        #    buy = df.ix[i-1, 'macd金叉']
    
        if df.ix[i, 'b向下'] != None and hold==1:
            rates.append(df.ix[i, 'b向下']/buy)
            hold = 0
    result(df, rates)

def xielv_b_reversed(df):
    
    print('--------------------b_reversed-----------------')
    rows_index = range(df.shape[0])
    rates = []
    hold = 0
    for i in rows_index:
        if i == 0:
            continue
        if df.ix[i, 'd向下'] != None and hold==0:
            buy = df.ix[i, 'd向下']
            hold = 1
    
        if df.ix[i, 'b向上'] != None and hold==1:
            rates.append(df.ix[i, 'b向上']/buy)
            hold = 0
    result(df, rates)


    '''
    计算股票的策略
    b转向上时，买入
    每次b转向下时，卖出一半
    d转向下时，卖出剩下的
    '''

if __name__ == '__main__':
    jiaocha(df)
    xielv_b(df)
    xielv_d(df)
    xielv_bd(df)
    xielv_db(df)
    xielv_b_reversed(df)