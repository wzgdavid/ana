'''
写到c就太复杂了，而且结果有不对，重写
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from common import get_DKX, get_nhh, get_nll, get_ma, avg,get_nhhzs,get_nllzs,get_atr
plt.rcParams['font.sans-serif'] = ['SimHei'] # 正常显示中文
df = pd.read_csv(r'..\data\rb\zs.csv')
#df = pd.read_csv(r'..\data\ma.csv')
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

# 这个不能少
dates = pd.DatetimeIndex(df.date)
df.index = dates
df = df.drop('date', axis=1)

df['bk总手数'] = 0
df['bkprice'] = 0
df['b持仓均价'] = 0  # 
df['b保证金'] = 0  #
df['b合约金额'] = 0  # 比如3000点买的螺纹， 实际合约价值是10吨，3万元
df['是b止损'] = None
df['sk总手数'] = 0
df['skprice'] = 0 
df['s保证金'] = 0
df['s持仓均价'] = 0  #
df['s合约金额'] = 0
df['是s止损'] = None
df['余额占比'] = 0

def run1(df,zs, zj_init):
    '''
    每次遇到开仓信号都开仓
    每次只开一手， 三天低点开仓止损和移动止损（先统一止损点跑，简单）
    
    '''
    arr = np.zeros(df.shape[0])
    arr[0] = zj_init  # 
    df['可用余额'] = arr # 初始化可用余额
    df['总金额'] = arr
    df = get_nhhzs(df, zs)  # 做空止损
    df = get_nllzs(df, zs)  # 做多止损

    feiyong = 3 # 每次两个滑点， 再用一个滑点代替费用，共3点
    new_high = 0
    new_low = 99999
    rows_index = range(df.shape[0])
    for i in rows_index:
        row = df.iloc[i]  # 不变动的值判断用row， 赋值用df.ix
        last_row = df.iloc[i-1] if i > 0 else row
        if i == 0:
            continue
        ss = 1 # 每次新开仓手数
        if df.ix[i, 'sk总手数'] == 0: # 多空只能做一个方向
            if row['开仓'] == 'bk':
                df.ix[i, 'bkprice'] = bkprice = row.o + feiyong if row.o>row.nhh2 else row.nhh2 + feiyong
                df.ix[i, 'bk总手数'] = df.ix[i-1, 'bk总手数'] + ss  # 等于上一日的bk总手数加1
                df.ix[i, 'b止损'] = row.nll_zs
                df.ix[i, '可用余额'] = df.ix[i-1, '可用余额'] - bkprice * ss
                #df.ix[i, 'b保证金'] = df.ix[i-1, 'b保证金'] + bkprice * ss
                new_change = (row.c - bkprice) * ss * 10 # 新开仓价格变化
                old_change = (row.c - last_row.c) * df.ix[i-1, 'bk总手数'] *10# 旧开仓价格变化
                #print(new_change, old_change)
                df.ix[i, '总金额'] = df.ix[i-1, '总金额'] + new_change + old_change
            else: 
                df.ix[i, 'bk总手数'] = df.ix[i-1, 'bk总手数'] 
                df.ix[i, '可用余额'] = df.ix[i-1, '可用余额']
                #df.ix[i, 'b保证金'] = df.ix[i-1, 'b保证金']
                if df.ix[i, 'bk总手数'] == 0:
                    df.ix[i, 'b止损'] = new_high = 0
                else:
                    df.ix[i, 'b止损'] = new_high = max(df.ix[i, 'nll_zs'],  new_high)
                old_change = (row.c - last_row.c) * df.ix[i-1, 'bk总手数']*10# 旧开仓价格变化
                df.ix[i, '总金额'] = df.ix[i-1, '总金额'] + old_change

        if df.ix[i, 'bk总手数'] == 0: # 多空只能做一个方向
            if row['开仓'] == 'sk':
                df.ix[i, 'skprice'] = skprice = row.o -feiyong if row.o<row.nll2 else row.nll2 - feiyong
                df.ix[i, 'sk总手数'] = df.ix[i-1, 'sk总手数'] + ss  # 等于上一日的sk总手数加1
                df.ix[i, 's止损'] = row.nhh_zs
                df.ix[i, '可用余额'] = df.ix[i-1, '可用余额'] - skprice * ss
                #df.ix[i, 's保证金'] = df.ix[i-1, 's保证金'] + skprice * ss
                new_change = (skprice - row.c) * ss * 10 # 新开仓价格变化
                old_change = (last_row.c - row.c) * df.ix[i-1, 'sk总手数'] *10# 旧开仓价格变化
                #print(new_change, old_change)
                df.ix[i, '总金额'] = df.ix[i-1, '总金额'] + new_change + old_change
            else: 
                df.ix[i, 'sk总手数'] = df.ix[i-1, 'sk总手数'] 
                df.ix[i, '可用余额'] = df.ix[i-1, '可用余额']
                #df.ix[i, 's保证金'] = df.ix[i-1, 's保证金']
                if df.ix[i, 'sk总手数'] == 0:
                    df.ix[i, 's止损'] = new_low = 999999
                else:
                    df.ix[i, 's止损'] = new_low = min(df.ix[i, 'nhh_zs'],  new_low)
                    #print(df.ix[i, 's止损'],  i)
                old_change = (last_row.c - row.c) * df.ix[i-1, 'sk总手数'] *10# 旧开仓价格变化
                df.ix[i, '总金额'] = df.ix[i-1, '总金额'] + old_change

        # 处理止损
        if df.ix[i, 'bk总手数'] != 0: 
            if row.l <= df.ix[i, 'b止损'] and df.ix[i, 'bk总手数'] !=0:
                df.ix[i, '是b止损'] = 1
                change = (df.ix[i, 'b止损'] - last_row.c - feiyong)  * df.ix[i-1, 'bk总手数']* 10
                df.ix[i, '总金额'] = df.ix[i-1, '总金额'] + change
                df.ix[i, 'bk总手数'] = 0
                #df.ix[i, 'b保证金'] = 0
                df.ix[i, '可用余额'] = df.ix[i, '总金额']
        if df.ix[i, 'sk总手数'] != 0: 
            if row.h >= df.ix[i, 's止损'] and df.ix[i, 'sk总手数'] !=0:
                df.ix[i, '是s止损'] = 1
                change = (last_row.c - df.ix[i, 's止损'] -feiyong)  * df.ix[i-1, 'sk总手数']* 10
                df.ix[i, '总金额'] = df.ix[i-1, '总金额'] + change
                df.ix[i, 'sk总手数'] = 0
                #df.ix[i, 's保证金'] = 0
                df.ix[i, '可用余额'] = df.ix[i, '总金额']

        #df.ix[i,'余额占比'] = df.ix[i, '可用余额'] / df.ix[i, '总金额']

    df.to_csv('tmp1.csv')
    plt.plot(df['总金额'])
    plt.plot(df['可用余额'])
    plt.legend()
    title = 'run1'
    plt.title(title)
    plt.show()

#run1(df, 3, 100000)



def run2(df,zs, zj_init, f=0.01, maxcw=0.3):
    '''
    有资金管理
    zs 指前 zs 天的最低（高）点
    每次开仓允许的损失，f（当前总金额的百分比）
    maxcw, 允许最大仓位（当前总金额的百分比）
    '''
    arr = np.zeros(df.shape[0])
    arr[0] = zj_init  # 
    df['可用余额'] = arr # 初始化可用余额
    df['总金额'] = arr
    df = get_nhhzs(df, zs)  # 做空止损
    df = get_nllzs(df, zs)  # 做多止损
    yue = 1 - maxcw # 反过来就是余额允许的最小比例
    feiyong = 3 # 每次两个滑点， 再用一个滑点代替费用，共3点
    new_high = 0
    new_low = 99999
    rows_index = range(df.shape[0])
    for i in rows_index:
        row = df.iloc[i]  # 不变动的值判断用row， 赋值用df.ix
        last_row = df.iloc[i-1] if i > 0 else row
        if i == 0:
            continue
        ss = 1 # 每次新开仓手数
        if df.ix[i, 'sk总手数'] == 0: # 多空只能做一个方向
            if row['开仓'] == 'bk' and (df.ix[i-1, '可用余额'] / df.ix[i-1, '总金额']) > yue:
                # 根据f算开几手
                loss  = df.ix[i-1, '总金额'] * f
                zsrange = row.nhh2 - row.nll2
                ss = int(loss / (zsrange * 10))
                #print(loss,zsrange,ss)

                df.ix[i, 'bkprice'] = bkprice = row.o + feiyong if row.o>row.nhh2 else row.nhh2 + feiyong
                df.ix[i, 'bk总手数'] = df.ix[i-1, 'bk总手数'] + ss  # 等于上一日的bk总手数加1
                df.ix[i, 'b止损'] = row.nll_zs  ##############################-10
                df.ix[i, '可用余额'] = df.ix[i-1, '可用余额'] - bkprice * ss
                #df.ix[i, 'b保证金'] = df.ix[i-1, 'b保证金'] + bkprice * ss
                new_change = (row.c - bkprice) * ss * 10 # 新开仓价格变化
                old_change = (row.c - last_row.c) * df.ix[i-1, 'bk总手数'] *10# 旧开仓价格变化
                #print(new_change, old_change)
                df.ix[i, '总金额'] = df.ix[i-1, '总金额'] + new_change + old_change
            else: 
                df.ix[i, 'bk总手数'] = df.ix[i-1, 'bk总手数'] 
                df.ix[i, '可用余额'] = df.ix[i-1, '可用余额']
                #df.ix[i, 'b保证金'] = df.ix[i-1, 'b保证金']
                if df.ix[i, 'bk总手数'] == 0:
                    df.ix[i, 'b止损'] = new_high = 0
                else:
                    df.ix[i, 'b止损'] = new_high = max(df.ix[i, 'nll_zs'],  new_high)
                old_change = (row.c - last_row.c) * df.ix[i-1, 'bk总手数']*10# 旧开仓价格变化
                df.ix[i, '总金额'] = df.ix[i-1, '总金额'] + old_change

        if df.ix[i, 'bk总手数'] == 0: # 多空只能做一个方向
            if row['开仓'] == 'sk'and (df.ix[i-1, '可用余额'] / df.ix[i-1, '总金额']) > yue:
                # 根据f算开几手
                loss  = df.ix[i-1, '总金额'] * f
                zsrange = row.nhh2 - row.nll2
                ss = int(loss / (zsrange * 10))
                #print(loss,zsrange,ss)
                df.ix[i, 'skprice'] = skprice = row.o -feiyong if row.o<row.nll2 else row.nll2 - feiyong
                df.ix[i, 'sk总手数'] = df.ix[i-1, 'sk总手数'] + ss  # 等于上一日的sk总手数加1
                df.ix[i, 's止损'] = row.nhh_zs ################################+ 10
                df.ix[i, '可用余额'] = df.ix[i-1, '可用余额'] - skprice * ss
                #df.ix[i, 's保证金'] = df.ix[i-1, 's保证金'] + skprice * ss
                new_change = (skprice - row.c) * ss * 10 # 新开仓价格变化
                old_change = (last_row.c - row.c) * df.ix[i-1, 'sk总手数'] *10# 旧开仓价格变化
                #print(new_change, old_change)
                df.ix[i, '总金额'] = df.ix[i-1, '总金额'] + new_change + old_change
            else: 
                df.ix[i, 'sk总手数'] = df.ix[i-1, 'sk总手数'] 
                df.ix[i, '可用余额'] = df.ix[i-1, '可用余额']
                #df.ix[i, 's保证金'] = df.ix[i-1, 's保证金']
                if df.ix[i, 'sk总手数'] == 0:
                    df.ix[i, 's止损'] = new_low = 999999
                else:
                    df.ix[i, 's止损'] = new_low = min(df.ix[i, 'nhh_zs'],  new_low)
                    #print(df.ix[i, 's止损'],  i)
                old_change = (last_row.c - row.c) * df.ix[i-1, 'sk总手数'] *10# 旧开仓价格变化
                df.ix[i, '总金额'] = df.ix[i-1, '总金额'] + old_change

        # 处理止损
        if df.ix[i, 'bk总手数'] != 0: 
            if row.l <= df.ix[i, 'b止损'] and df.ix[i, 'bk总手数'] !=0:
                df.ix[i, '是b止损'] = 1
                change = (df.ix[i, 'b止损'] - last_row.c - feiyong)  * df.ix[i-1, 'bk总手数']* 10
                df.ix[i, '总金额'] = df.ix[i-1, '总金额'] + change
                df.ix[i, 'bk总手数'] = 0
                #df.ix[i, 'b保证金'] = 0
                df.ix[i, '可用余额'] = df.ix[i, '总金额']
        if df.ix[i, 'sk总手数'] != 0: 
            if row.h >= df.ix[i, 's止损'] and df.ix[i, 'sk总手数'] !=0:
                df.ix[i, '是s止损'] = 1
                change = (last_row.c - df.ix[i, 's止损'] -feiyong)  * df.ix[i-1, 'sk总手数']* 10
                df.ix[i, '总金额'] = df.ix[i-1, '总金额'] + change
                df.ix[i, 'sk总手数'] = 0
                #df.ix[i, 's保证金'] = 0
                df.ix[i, '可用余额'] = df.ix[i, '总金额']

        #df.ix[i,'余额占比'] = df.ix[i, '可用余额'] / df.ix[i, '总金额']
        #if i > 100:
        #    break
    df.to_csv('tmp2.csv')
    plt.plot(df['总金额'])
    #plt.plot(df['可用余额'])
    plt.legend()
    title = 'run2 zs={}   f={}  maxcw={}'.format(zs, f,maxcw)
    plt.title(title)
    plt.show()

#run2(df, 2, 100000, f=0.02, maxcw=0.3)
#run2(df, 2, 100000, f=0.02, maxcw=0.4)
run2(df, 2, 100000, f=0.02, maxcw=0.5)


