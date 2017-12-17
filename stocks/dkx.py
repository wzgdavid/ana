import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from common import get_DKX, result
from functools import reduce

def ready(daima):
    df = pd.read_csv(r'..\data\stocks\{}.csv'.format(daima))
    df = get_DKX(df)
    df['b向上'] = np.where( (df['b'].shift(3)>df['b'].shift(2)) & (df['b'].shift(1)>df['b'].shift(2)),   df.o , None )
    df['b向下'] = np.where( (df['b'].shift(3)<df['b'].shift(2)) & (df['b'].shift(1)<df['b'].shift(2)),   df.c , None )
    return df

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

# 验证收益大于一定幅度的年度是不是和指数有关
# 是有关， 所以要在大环境好的时候入市做股票，选股不是最重要
def xielv_b_look_date(df):
    print('--------------------bb-----------------')
    rows_index = range(df.shape[0])
    rates = []
    hold = 0
    
    for i in rows_index:
        if i == 0:
            continue
        if df.ix[i, 'b向上'] != None and hold==0:
            buy = df.ix[i, 'b向上']
            buy_date = df.ix[i, 'date']
            hold = 1
           
    
        if df.ix[i, 'b向下'] != None and hold==1:
            if df.ix[i, 'b向下']/buy > 1.05:
                rates.append(buy_date.split('/')[0])
            hold = 0
    rates = pd.Series(rates).value_counts()
    rates = rates.sort_index()
    #rates.plot()
    #plt.show()
    #print(rates)
    return rates
    #result(df, rates)

if __name__ == '__main__':
    #jiaocha(df)
    #xielv_b(df)
    #xielv_d(df)
    #xielv_bd(df)
    #xielv_db(df)
    #xielv_b_reversed(df)
    a = xielv_b_look_date(ready('000001'))
    b = xielv_b_look_date(ready('000002'))
    c = xielv_b_look_date(ready('000004'))
    d = xielv_b_look_date(ready('600096'))
    e = xielv_b_look_date(ready('600361'))
    f = xielv_b_look_date(ready('600712'))
    #help(a.add)
    total = a.add(b, fill_value=0).add(c, fill_value=0).add(c, fill_value=0).add(d, fill_value=0).add(e, fill_value=0).add(f, fill_value=0)
    #total = reduce(pd.Series.add, [a,b,c,d,e,f])
    total.plot(kind='bar')
    #print(total)
    plt.show()
    

