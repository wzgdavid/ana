import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
daima = '000001'
df = pd.read_csv(r'..\data\stocks\{}.csv'.format(daima))



def get_DKX(df, n=10):
    df['a'] = (df.c * 3 + df.l + df.o + df.h)/6
    #df['b'] = (20*df.a + 19*df.a.shift(1) + 18*df.a.shift(2) + 17*df.a.shift(3) + 
    #    16*df.a.shift(4) + 15*df.a.shift(5) + 14*df.a.shift(6) + 
    #    13*df.a.shift(7) + 12*df.a.shift(8) + 11*df.a.shift(9) + 
    #    10*df.a.shift(10) + 9*df.a.shift(11) + 8*df.a.shift(12) + 7*df.a.shift(13) + 
    #    6*df.a.shift(14) + 5*df.a.shift(15) + 4*df.a.shift(16) + 
    #    3*df.a.shift(17) + 2*df.a.shift(18) + 1*df.a.shift(19))/210
    sum_ = '+'.join(['{}*df.a.shift({})'.format(20-i, i) for i in range(0, 20)]) 
    eval_str = '({})/210'.format(sum_)
    df['b'] = eval(eval_str)
    df['d'] = df.b.rolling(n).mean()
    return df.drop(['a'], axis=1)
df = get_DKX(df)
df['dkx金叉'] = np.where( (df['b'].shift(2)<df['d'].shift(2)) & (df['b'].shift(1)>df['d'].shift(1)), df.o , None )
df['dkx死叉'] = np.where( (df['b'].shift(2)>df['d'].shift(2)) & (df['b'].shift(1)<df['d'].shift(1)), df.o , None )
df['b向上'] = np.where( (df['b'].shift(3)>df['b'].shift(2)) & (df['b'].shift(1)>df['b'].shift(2)), df.o , None )
df['b向下'] = np.where( (df['b'].shift(3)<df['b'].shift(2)) & (df['b'].shift(1)<df['b'].shift(2)), df.o , None )
df['d向上'] = np.where( (df['d'].shift(3)>df['d'].shift(2)) & (df['d'].shift(1)>df['d'].shift(2)), df.o , None )
df['d向下'] = np.where( (df['d'].shift(3)<df['d'].shift(2)) & (df['d'].shift(1)<df['d'].shift(2)), df.o , None )


def jiaocha(df):
    rows_index = range(df.shape[0])
    rates = []
    hold = 0
    for i in rows_index:
        if i == 0:
            continue
        if df.ix[i, 'dkx金叉'] != None and hold==0:
        #if df.ix[i, 'macd金叉'] != None and hold==0:
            buy = df.ix[i, 'dkx金叉']
            hold = 1
        #else:
        #    buy = df.ix[i-1, 'macd金叉']
    
        if df.ix[i, 'dkx死叉'] != None and hold==1:
            rates.append(df.ix[i, 'dkx死叉']/buy)
            hold = 0
    
    df = pd.DataFrame(rates, columns=['rates'])
    df['ret_index'] = (df['rates']).cumprod() # 曲线
    print(df.describe())
    df.to_csv('tmp.csv')

def xielvb(df):
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
    
        if df.ix[i, 'b向下'] != None and hold==1:
            rates.append(df.ix[i, 'b向下']/buy)
            hold = 0
    
    df = pd.DataFrame(rates, columns=['rates'])
    df['ret_index'] = (df['rates']).cumprod() # 曲线
    print(df.describe())
    df.to_csv('tmp.csv')

def xielvd(df):
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
    
        if df.ix[i, 'd向下'] != None and hold==1:
            rates.append(df.ix[i, 'd向下']/buy)
            hold = 0
    
    df = pd.DataFrame(rates, columns=['rates'])
    df['ret_index'] = (df['rates']).cumprod() # 曲线
    print(df.describe())
    df.to_csv('tmp.csv')

if __name__ == '__main__':
    #jiaocha(df)
    xielvb(df)
    xielvd(df)