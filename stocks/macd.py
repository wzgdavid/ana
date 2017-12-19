import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from common import get_DKX,result


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
    金叉日期 = []
    死叉日期 = []
    for i in rows_index:
        if i == 0:
            continue
        #if df.ix[i, 'macd金叉'] != None and hold==0 and (df.ix[i, 'b'] > df.ix[i, 'd']):
        if df.ix[i, 'macd金叉'] != None and hold==0:
            buy = df.ix[i, 'macd金叉']
            hold = 1
            金叉日期.append(df.ix[i, 'date'])
        #else:
        #    buy = df.ix[i-1, 'macd金叉']
    
        if df.ix[i, 'macd死叉'] != None and hold==1:
            rates.append(df.ix[i, 'macd死叉']/buy)
            hold = 0
            死叉日期.append(df.ix[i, 'date'])
    print(金叉日期)
    print(死叉日期)
    result(df, rates)

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
    
    result(df, rates)

if __name__ == '__main__':
    jiaocha(df)
    xielv(df)   # 效果不好