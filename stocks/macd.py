import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from common import get_DKX


daima = '000001'
df = pd.read_csv(r'..\data\stocks\{}.csv'.format(daima))



df['macd金叉'] = np.where( (df['MACD.DIF'].shift(2)<df['MACD.DEA'].shift(2)) & (df['MACD.DIF'].shift(1)>df['MACD.DEA'].shift(1)), df.o , None )
df['macd死叉'] = np.where( (df['MACD.DIF'].shift(2)>df['MACD.DEA'].shift(2)) & (df['MACD.DIF'].shift(1)<df['MACD.DEA'].shift(1)), df.o , None )

df['DIF向上'] = np.where( (df['MACD.DIF'].shift(3)>df['MACD.DIF'].shift(2)) & (df['MACD.DIF'].shift(1)>df['MACD.DIF'].shift(2)), df.o , None )
df['DIF向下'] = np.where( (df['MACD.DIF'].shift(3)<df['MACD.DIF'].shift(2)) & (df['MACD.DIF'].shift(1)<df['MACD.DIF'].shift(2)), df.o , None )
df['DEA向上'] = np.where( (df['MACD.DEA'].shift(3)>df['MACD.DEA'].shift(2)) & (df['MACD.DEA'].shift(1)>df['MACD.DEA'].shift(2)), df.o , None )
df['DEA向下'] = np.where( (df['MACD.DEA'].shift(3)<df['MACD.DEA'].shift(2)) & (df['MACD.DEA'].shift(1)<df['MACD.DEA'].shift(2)), df.o , None )


def jiaocha(df):
    rows_index = range(df.shape[0])
    rates = []
    hold = 0
    for i in rows_index:
        if i == 0:
            continue
        #if df.ix[i, 'macd金叉'] != None and hold==0 and (df.ix[i, 'b'] > df.ix[i, 'd']):
        if df.ix[i, 'macd金叉'] != None and hold==0:
            buy = df.ix[i, 'macd金叉']
            hold = 1
        #else:
        #    buy = df.ix[i-1, 'macd金叉']
    
        if df.ix[i, 'macd死叉'] != None and hold==1:
            rates.append(df.ix[i, 'macd死叉']/buy)
            hold = 0
    
    df = pd.DataFrame(rates, columns=['rates'])
    df['ret_index'] = (df['rates']).cumprod() # 曲线
    print(df.describe())
    df.to_csv('tmp.csv')  

def xielv(df):
    rows_index = range(df.shape[0])
    rates = []
    hold = 0
    for i in rows_index:
        if i == 0:
            continue
        if df.ix[i, 'DIF向上'] != None and hold==0:
    
            buy = df.ix[i, 'DIF向上']
            hold = 1
        #else:
        #    buy = df.ix[i-1, 'macd金叉']
    
        if df.ix[i, 'DIF向下'] != None and hold==1:
            rates.append(df.ix[i, 'DIF向下']/buy)
            hold = 0
    
    df = pd.DataFrame(rates, columns=['rates'])
    df['ret_index'] = (df['rates']).cumprod() # 曲线
    print(df.describe())
    df.to_csv('tmp.csv')

if __name__ == '__main__':
    #jiaocha(df)
    xielv(df)   # 效果不好