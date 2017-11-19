'''
用tips中 的收益计算方式
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from common import get_DKX, get_nhh, get_nll, get_ma
plt.rcParams['font.sans-serif'] = ['SimHei'] # 正常显示中文
df = pd.read_csv(r'..\data\rb\zl.csv')
#df = pd.read_csv(r'..\data\dy.csv')
df = get_DKX(df)
df = get_nhh(df, 2)
df = get_nll(df, 2)
df = get_ma(df, 20)


'''
--------------------------趋势判断1---------------------------------
'''
# 趋势判断，DKXb方向，1 向上   0向下  当天参照前两天
df['DKXb方向'] = np.where(df.b.shift(1)>df.b.shift(2), 1, 0) 
# 开仓条件
df = df.dropna(axis=0)
df['高于前两天高点'] = np.where(df.h > df.nhh2, 1, None)   # 看当天 
df['低于前两天低点'] = np.where(df.l < df.nll2, 1, None)
# 开仓  bk开多  sk开空
df['开仓'] = np.where((df['高于前两天高点'] == 1) & (df['DKXb方向']==1), 'bk', None)
df['开仓'] = np.where((df['低于前两天低点'] == 1) & (df['DKXb方向']==0), 'sk', df['开仓'] )
# 平仓 趋势反转 'bp' 平多  'sp' 平空
df['平仓'] = np.where((df.DKXb方向.shift(2) == 1) & (df.DKXb方向.shift(1) == 0), 'bp', None)
df['平仓'] = np.where((df.DKXb方向.shift(2) == 0) & (df.DKXb方向.shift(1) == 1), 'sp', df['平仓'])
#df['平仓'] = None # 没有平仓信号， 只用止损平仓
'''
--------------------------趋势判断2---------------------------------
'''
# 趋势判断，K线在ma20上下，1 上   0下  当天参照前一天
#df['condition'] = np.where(df.l.shift(1)>df.ma20.shift(1), 1, None) 
#df['condition'] = np.where(df.h.shift(1)<df.ma20.shift(1), 0, df['condition']) 
## 开仓条件
#df = df.dropna(axis=0)
#df['高于前两天高点'] = np.where(df.h > df.nhh2, 1, None)   # 看当天 
#df['低于前两天低点'] = np.where(df.l < df.nll2, 1, None)
## 开仓  bk开多  sk开空
#df['开仓'] = np.where((df['高于前两天高点'] == 1) & (df['condition']==1), 'bk', None)
#df['开仓'] = np.where((df['低于前两天低点'] == 1) & (df['condition']==0), 'sk', df['开仓'] )
## 平仓 趋势反转 'bp' 平多  'sp' 平空
##df['平仓'] = np.where((df['condition']==1, 'bp', None)
##df['平仓'] = np.where((df['低于前两天低点'] == 1) & (df['condition']==0), 'sp', df['平仓'])
#df['平仓'] = None


'''
--------------------------趋势判断end---------------------------------
'''

#平仓的同时不反向开仓
df['开仓'] = np.where(df['平仓'].isnull(), df['开仓'], None)

dates = pd.DatetimeIndex(df.date)
df.index = dates
df = df.drop('date', axis=1)

df['bk总手数'] = 0
df['bkprice'] = 0
df['sk总手数'] = 0
df['skprice'] = 0
df['b保证金'] = 0  # 
df['s保证金'] = 0
df['b持仓均价'] = 0  # 
df['s持仓均价'] = 0  #
df['s保证金'] = 0
df['b合约金额'] = 0  # 比如3000点买的螺纹， 实际合约价值是10吨，3万元
df['s合约金额'] = 0
df['总金额'] = 0

def run1(df, zj_init):
    '''zj_init 初始资金
    简单跑， 每次遇到信号开一手，没有开仓止损，没有资金管理 平仓信号全平
    只根据信号开平仓
    '''
    arr = np.zeros(df.shape[0])
    arr[0] = zj_init  # 
    df['可用余额'] = arr # 初始化可用余额
    rows_index = range(df.shape[0])
    for i in rows_index:
        row = df.iloc[i]  # 判断用row， 赋值用df.ix
        last_row = df.iloc[i-1] if i > 0 else row
       
        # 多
        #if row['开仓'] == 'bk':
        #    df.ix[i, 'bk总手数'] = last_row['bk总手数'] + 1
        #    # 简单计算， 保证金比例就一比十， 既价格就是保证金额
        #    df.ix[i, 'bkprice'] = row.o if row.o>row.nhh2 else row.nhh2 # 前两天的高点作为开仓价,跳开用今天的开盘作为开仓价
        #    df.ix[i, 'b保证金'] = last_row['b保证金'] + df.ix[i, 'bkprice']  # 
        #    df.ix[i, 'b合约金额'] = df.ix[i, 'bkprice'] * df.ix[i, 'bk总手数'] * 10 # 螺纹一手10吨
        #    df.ix[i, '可用余额'] = last_row['可用余额'] - df.ix[i, 'bkprice'] # 
        #else: 
        #    df.ix[i, 'bk总手数'] = last_row['bk总手数']
        #    df.ix[i, 'b保证金'] = last_row['b保证金']
        #    df.ix[i, '可用余额'] = last_row['可用余额']
        #    df.ix[i, 'b合约金额'] = row.c * df.ix[i, 'bk总手数'] * 10 # 螺纹一手10吨
        #if row['平仓'] == 'bp':
        #    df.ix[i, 'bk总手数'] = 0
        #    df.ix[i, 'b保证金'] = 0
        #    #df.ix[i, '可用余额'] = last_row['可用余额'] + df.ix[i, 'b合约金额']/10
        #    df.ix[i, '可用余额'] = last_row['总金额']
        #    df.ix[i, 'b合约金额'] = 0
        ## 只跑多
        #df.ix[i, '总金额'] = df.ix[i, '可用余额'] + df.ix[i, 'b保证金'] + (df.ix[i, 'b合约金额']/ 10 - df.ix[i, 'b保证金'])*10


        ## 空
        if row['开仓'] == 'sk':
            df.ix[i, 'sk总手数'] = last_row['sk总手数'] + 1
            df.ix[i, 'skprice'] = row.o if row.o<row.nll2 else row.nll2 
            df.ix[i, 's保证金'] = last_row['s保证金'] + df.ix[i, 'skprice']
            df.ix[i, 's持仓均价'] = df.ix[i, 's保证金'] / df.ix[i, 'sk总手数']
            df.ix[i, 's合约金额'] = df.ix[i, 'skprice'] * df.ix[i, 'sk总手数'] * 10 # 螺纹一手10吨
            df.ix[i, '可用余额'] = last_row['可用余额'] - df.ix[i, 'skprice']
        else:
            df.ix[i, 'sk总手数'] = last_row['sk总手数']
            df.ix[i, 's保证金'] = last_row['s保证金']
            df.ix[i, '可用余额'] = last_row['可用余额']
            df.ix[i, 's合约金额'] = row.c * df.ix[i, 'sk总手数'] * 10 # 螺纹一手10吨
        if row['平仓'] == 'sp':
            df.ix[i, 'sk总手数'] = 0
            df.ix[i, 's保证金'] = 0
            df.ix[i, '可用余额'] = last_row['总金额']
            df.ix[i, 's合约金额'] = 0
        # 只跑空
        df.ix[i, '总金额'] = df.ix[i, '可用余额'] + df.ix[i, 's保证金'] + (df.ix[i, 's保证金'] - df.ix[i, 's合约金额']/ 10 )*10
        
        ## 多空一起跑
        #df.ix[i, '总金额'] = df.ix[i, '可用余额'] + df.ix[i, 'b保证金'] + (df.ix[i, 'b合约金额']/ 10 - df.ix[i, 'b保证金'])*10 \
        #                       + df.ix[i, 's保证金'] + (df.ix[i, 's保证金'] - df.ix[i, 's合约金额']/ 10  )*10  \
        ## 调整
        #if row['开仓'] == 'bk':
        #    df.ix[i, '总金额'] = df.ix[i, '总金额'] - row.l
    

    droplist = [ 'b', 'nhh2', 'nll2', 'DKXb方向',  '高于前两天高点', '低于前两天低点']
    df = df.drop(droplist, axis=1)
    df.to_csv('tmp.csv')
    plt.plot(df['总金额'])
    plt.title('run1')
    plt.show()
    
#run1(df, 100000)

def run2(df, zj_init, zs):
    '''zj_init 初始资金
    在run1的基础上有止损
    止损用前zs天最高最低点
    '''
    df = get_nhh(df, zs)  # 做空止损
    df = get_nll(df, zs)  # 做多止损
    df['b止损'] = df['nll{}'.format(zs)]
    df['s止损'] = df['nhh{}'.format(zs)]
    arr = np.zeros(df.shape[0])
    arr[0] = zj_init  # 
    df['可用余额'] = arr # 初始化可用余额
    rows_index = range(df.shape[0])
    for i in rows_index:
        row = df.iloc[i]  # 判断用row， 赋值用df.ix
        last_row = df.iloc[i-1] if i > 0 else row
        # 多
        if row['开仓'] == 'bk':
            df.ix[i, 'bk总手数'] = last_row['bk总手数'] + 1
            # 简单计算， 保证金比例就一比十， 既价格就是保证金额
            df.ix[i, 'bkprice'] = row.o if row.o>row.nhh2 else row.nhh2 # 前两天的高点作为开仓价,跳开用今天的开盘作为开仓价
            df.ix[i, 'b保证金'] = last_row['b保证金'] + df.ix[i, 'bkprice']  # 
            df.ix[i, 'b合约金额'] = df.ix[i, 'bkprice'] * df.ix[i, 'bk总手数'] * 10 # 螺纹一手10吨
            df.ix[i, '可用余额'] = last_row['可用余额'] - df.ix[i, 'bkprice'] # 
        else: 
            df.ix[i, 'bk总手数'] = last_row['bk总手数']
            df.ix[i, 'b保证金'] = last_row['b保证金']
            df.ix[i, '可用余额'] = last_row['可用余额']
            df.ix[i, 'b合约金额'] = row.c * df.ix[i, 'bk总手数'] * 10 # 螺纹一手10吨
        if (row['平仓'] == 'bp') or (row.l <= row['b止损']):
            df.ix[i, 'bk总手数'] = 0
            df.ix[i, 'b保证金'] = 0
            #df.ix[i, '可用余额'] = last_row['可用余额'] + df.ix[i, 'b合约金额']/10
            df.ix[i, '可用余额'] = last_row['总金额']
            df.ix[i, 'b合约金额'] = 0
        df.ix[i, '总金额'] = df.ix[i, '可用余额'] + df.ix[i, 'b保证金'] + (df.ix[i, 'b合约金额']/ 10 - df.ix[i, 'b保证金'])*10


        # 空
        #if row['开仓'] == 'sk':
        #    df.ix[i, 'sk总手数'] = last_row['sk总手数'] + 1
        #    df.ix[i, 'skprice'] = row.o if row.o<row.nll2 else row.nll2 
        #    df.ix[i, 's保证金'] = last_row['s保证金'] + df.ix[i, 'skprice']
        #    df.ix[i, 's合约金额'] = df.ix[i, 'skprice'] * df.ix[i, 'sk总手数'] * 10 # 螺纹一手10吨
        #    df.ix[i, '可用余额'] = last_row['可用余额'] - df.ix[i, 'skprice']
        #else:
        #    df.ix[i, 'sk总手数'] = last_row['sk总手数']
        #    df.ix[i, 's保证金'] = last_row['s保证金']
        #    df.ix[i, '可用余额'] = last_row['可用余额']
        #    df.ix[i, 's合约金额'] = row.c * df.ix[i, 'sk总手数'] * 10 # 螺纹一手10吨
        #if (row['平仓'] == 'sp') or (row.h >= row['s止损']):
        #    df.ix[i, 'sk总手数'] = 0
        #    df.ix[i, 's保证金'] = 0
        #    df.ix[i, '可用余额'] = last_row['总金额']
        #    df.ix[i, 's合约金额'] = 0
        #df.ix[i, '总金额'] = df.ix[i, '可用余额'] + df.ix[i, 's保证金'] + (df.ix[i, 's保证金'] - df.ix[i, 's合约金额']/ 10 )*10
        

        #df.ix[i, '总金额'] = df.ix[i, '可用余额'] + df.ix[i, 'b保证金'] + (df.ix[i, 'b合约金额']/ 10 - df.ix[i, 'b保证金'])*10 \
        #                       + df.ix[i, 's保证金'] + (df.ix[i, 's保证金'] - df.ix[i, 's合约金额']/ 10  )*10
        ## 调整
        #if row['开仓'] == 'bk':
        #    df.ix[i, '总金额'] = df.ix[i, '总金额'] - row.l

    droplist = ['b', 'nhh2', 'nll2', 'DKXb方向',  '高于前两天高点', '低于前两天低点']
    df = df.drop(droplist, axis=1)
    df.to_csv('tmp2.csv')
    plt.plot(df['总金额'])
    plt.title('run2')
    plt.show()
    
#run2(df, 100000, zs=4)


def run3(df, zj_init, zs, fangxiang):
    '''zj_init 初始资金
    在run2的基础上资金管理，简单考虑，用以下规则,真实情况还要考虑止损幅度
    总金额每有4万，开仓一手，即开仓手数=int(总金额/40000), 但最多开100手
    止损用前zs天最高最低点
    fangxiang  '多'   '空'
    '''
    df = get_nhh(df, zs)  # 做空止损
    df = get_nll(df, zs)  # 做多止损
    df['b止损'] = df['nll{}'.format(zs)] # 移动和开仓止损
    df['s止损'] = df['nhh{}'.format(zs)]
    df['一次开仓手数'] = 0
    arr = np.zeros(df.shape[0])
    arr[0] = zj_init  # 
    df['可用余额'] = arr # 初始化可用余额
    rows_index = range(df.shape[0])
    new_high = 0 # 多止损
    new_low = 0 # 空移动止损
    for i in rows_index:
        row = df.iloc[i]  # 判断用row， 赋值用df.ix
        last_row = df.iloc[i-1] if i > 0 else row
        # 多
        if fangxiang == '多':
            if row['开仓'] == 'bk':
                df.ix[i, '一次开仓手数'] = min(int(last_row['可用余额'] / 40000), 100)
                df.ix[i, 'bk总手数'] = last_row['bk总手数'] + df.ix[i, '一次开仓手数']
                # 简单计算， 保证金比例就一比十， 既价格就是保证金额
                df.ix[i, 'bkprice'] = row.o if row.o>row.nhh2 else row.nhh2 # 前两天的高点作为开仓价,跳开用今天的开盘作为开仓价
                df.ix[i, 'b保证金'] = last_row['b保证金'] + df.ix[i, 'bkprice']*df.ix[i, '一次开仓手数']   # 
                df.ix[i, 'b合约金额'] = df.ix[i, 'bkprice'] * df.ix[i, 'bk总手数'] * 10 # 螺纹一手10吨
                df.ix[i, '可用余额'] = last_row['可用余额'] - df.ix[i, 'bkprice'] *df.ix[i, '一次开仓手数'] # 
            else: 
                df.ix[i, 'bk总手数'] = last_row['bk总手数']
                df.ix[i, 'b保证金'] = last_row['b保证金']
                df.ix[i, '可用余额'] = last_row['可用余额']
                df.ix[i, 'b合约金额'] = row.c * df.ix[i, 'bk总手数'] * 10 # 螺纹一手10吨
            if row['平仓'] == 'bp':
                df.ix[i, 'bk总手数'] = 0
                df.ix[i, 'b保证金'] = 0
                #df.ix[i, '可用余额'] = last_row['可用余额'] + df.ix[i, 'b合约金额']/10
                df.ix[i, '可用余额'] = last_row['总金额']
                df.ix[i, 'b合约金额'] = 0
            if df.ix[i, 'bk总手数'] == 0:
                df.ix[i, 'b止损'] == 0
                new_high = 0
            else:
                new_high = max(df.ix[i, 'b止损'], new_high)
            #print(new_high)
            if row.l <= df.ix[i, 'b止损']:
                df.ix[i, 'bk总手数'] = 0
                df.ix[i, 'b保证金'] = 0
                #df.ix[i, '可用余额'] = last_row['可用余额'] + df.ix[i, 'b合约金额']/10
                df.ix[i, '可用余额'] = last_row['总金额']
                df.ix[i, 'b合约金额'] = 0

            df.ix[i, '总金额'] = df.ix[i, '可用余额'] + df.ix[i, 'b保证金'] + (df.ix[i, 'b合约金额']/ 10 - df.ix[i, 'b保证金'])*10
        
        # 空
        if fangxiang == '空':
            if row['开仓'] == 'sk':
                df.ix[i, '一次开仓手数'] = min(int(last_row['可用余额'] / 40000), 100)
                df.ix[i, 'sk总手数'] = last_row['sk总手数'] + df.ix[i, '一次开仓手数']
                df.ix[i, 'skprice'] = row.o if row.o<row.nll2 else row.nll2 
                df.ix[i, 's保证金'] = last_row['s保证金'] + df.ix[i, 'skprice'] * df.ix[i, '一次开仓手数']
                df.ix[i, 's合约金额'] = df.ix[i, 'skprice'] * df.ix[i, 'sk总手数'] * 10 # 螺纹一手10吨
                df.ix[i, '可用余额'] = last_row['可用余额'] - df.ix[i, 'skprice'] *df.ix[i, '一次开仓手数'] # 
            else:
                df.ix[i, 'sk总手数'] = last_row['sk总手数']
                df.ix[i, 's保证金'] = last_row['s保证金']
                df.ix[i, '可用余额'] = last_row['可用余额']
                df.ix[i, 's合约金额'] = row.c * df.ix[i, 'sk总手数'] * 10 # 螺纹一手10吨
            if df.ix[i, 'sk总手数'] == 0:
                df.ix[i, 's止损'] == 0
                new_low = 99999
            else:
                new_low = min(df.ix[i, 's止损'], new_low)
            #print(new_low)
            if (row['平仓'] == 'sp') or (row.h >= new_low):
                df.ix[i, 'sk总手数'] = 0
                df.ix[i, 's保证金'] = 0
                df.ix[i, '可用余额'] = last_row['总金额']
                df.ix[i, 's合约金额'] = 0
            df.ix[i, '总金额'] = df.ix[i, '可用余额'] + df.ix[i, 's保证金'] + (df.ix[i, 's保证金'] - df.ix[i, 's合约金额']/ 10 )*10
        
        #df.ix[i, '总金额'] = df.ix[i, '可用余额'] + df.ix[i, 'b保证金'] + (df.ix[i, 'b合约金额']/ 10 - df.ix[i, 'b保证金'])*10 \
        #                       + df.ix[i, 's保证金'] + (df.ix[i, 's保证金'] - df.ix[i, 's合约金额']/ 10  )*10
        ## 调整
        #if row['开仓'] == 'bk':
        #    df.ix[i, '总金额'] = df.ix[i, '总金额'] - row.l * df.ix[i, '一次开仓手数']

    droplist = [ 'b', 'nhh2', 'nll2',  '高于前两天高点', '低于前两天低点']
    df = df.drop(droplist, axis=1)
    df.to_csv('tmp3.csv')
    plt.plot(df['总金额'])
    title = 'run3-zs:{}-fangxiang:{}'.format(zs, fangxiang)
    plt.title(title)
    plt.show()
    #plt.savefig('{}.png'.format(title))
    
#run3(df, 100000, zs=3, fangxiang='多')
run3(df, 100000, zs=3, fangxiang='空')