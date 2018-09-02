
'''
算盈亏比
用循环逐个比较
可有有移动止损
因为b.py算不了移动止损
'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from common import *#get_DKX, get_nhh, get_nll, get_ma, avg,get_nhhzs,get_nllzs,get_atr

pinzhong = 'rm'
plt.rcParams['font.sans-serif'] = ['SimHei'] # 正常显示中文
df = pd.read_csv(r'..\data\{}.csv'.format(pinzhong))
df = get_DKX(df)



df = get_ma(df, 17)

df = get_atr(df, 50)
df = df.dropna()   

'''
过滤  start
'''
#df = df.iloc[2500:3000,  :]  #选择部分
#df['condition'] = 1  # 不过滤
df['condition'] = np.where(df.l.shift(1)>df.ma.shift(1), 1, 0) #  df.c.shift(1)>df.ma.shift(1)  在ma上
#df['condition'] = np.where(df.ma.shift(1)>df.ma.shift(2), 1, 0) # df.ma.shift(1)>df.ma.shift(2)  ma斜率向上


rows_index = range(df.shape[0])

'''先写出只做多的程序'''
持仓期 = 3  #
   
n = 1 # 止损几个ATR
m = 1 # 移动止损几个ATR
y = 2 # 止盈几个ATR
盈利额 = 0
亏损额 = 0
盈利次数 = 0 
亏损次数 = 0
跳开滑点 = 3  # 3
一般滑点 = 1  # 1
for i in rows_index:
    
    row = df.iloc[i] 
    if row.condition == 0:continue
    bkprice = row['c']
    止损 = bkprice - (int(row['atr'])+1) * n
    止盈 = bkprice + (int(row['atr'])+1) * y
    for j in range(i+1, i+持仓期+1): # 从开仓日开始和后面 持仓期 的天数 逐一作比较
        row2last = df.iloc[j-1] # 移动止损前一天的参照
        row2 = df.iloc[j]
        '''在持仓期内打到止损'''
        if 0: # 移动止损开关
            移动止损 = row2last.h - (int(row2last['atr'])+1) * m
            止损 = max(止损,移动止损)
        if 1: # 止损开关
            if row2['l'] <= 止损:
                亏损次数 += 1
                if row2.o < 止损:   # 处理跳开直接越过止损
                    亏损额 += bkprice-row2.o + 跳开滑点
                    #亏损 += bkprice-止损  
                else:
                    亏损额 += bkprice-止损 + 一般滑点
                break
        '''在持仓期内打到止盈'''
        if 0: # 止盈开关
            if row2['h'] >= 止盈:
                盈利次数 += 1
                if row2.o > 止盈:   # 处理跳开直接越过止盈
                    盈利额 += row2.o - bkprice - 一般滑点
                    #亏损 += bkprice-止损  
                else:
                    盈利额 += 止盈 - bkprice - 一般滑点
                break
        '''在持仓期内没有止损， 到持仓时间，自然平仓''' 
        if j == i+持仓期:
            pcprice = row2.c - (row.c + 一般滑点)
            if pcprice > 0:
                盈利额 += pcprice
                盈利次数 += 1
            else:
                亏损额 += abs(pcprice)
                亏损次数 += 1
        #print(bkprice, 止损)
    #if i ==10:break # 测试用
    if i ==df.shape[0]-持仓期-1:break
df.to_csv('tmp.csv')

#print(盈利, 亏损, )
print('盈亏比',盈利额/亏损额)
print('胜率', 盈利次数/(盈利次数+亏损次数))
    