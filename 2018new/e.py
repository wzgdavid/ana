
'''
初始代码从c.py拷贝过来
研究相同间隔，同时移动止盈和止损
比如在3000点开仓，止损在2900点，止盈在3100点，过了一小时，价格达到3050，
这时同间隔移动止盈和止损，止盈位3150，止损位2950
'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from common import *#get_DKX, get_nhh, get_nll, get_ma, avg,get_nhhzs,get_nllzs,get_atr
plt.rcParams['font.sans-serif'] = ['SimHei'] # 正常显示中文


#pinzhong = 'pp'
#pinzhong_lst = ['rb','sr','c','ma','pp','ta','m','a','rm','y'] #'rb','sr','c','ma','pp','ta','m','a',
#pinzhong_lst = ['000004']
#pinzhong_lst = ['rbl91h','srl91h','ml91h','oil91h','ppl91h']
pinzhong_lst = ['rbl91h']
print('上一行盈亏比，下一行，胜率')
for pinzhong in pinzhong_lst:
    print(pinzhong, '---------------------------')
    
    df = pd.read_csv(r'..\data\{}.csv'.format(pinzhong))
    
    df = get_DKX(df)

    df = get_ma(df, 10)
    df['ma1'] = df.ma
    df = get_ma(df, 20)
    df['ma2'] = df.ma

    
    df = get_atr(df, 50)
    df = df.dropna()   
    
    '''
    过滤  start
    '''
    df = df.iloc[:,  :]  #选择部分  df.iloc[-1000:-500,  :] 这样选在同一时期的数据，才有比较意义，
    #df['condition'] = 1  # 不过滤

    #df['condition'] = np.where(df.c.shift(1)>df.ma.shift(1), 1, 0) #  df.c.shift(1)>df.ma.shift(1)  在ma上
    #df['condition'] = np.where(df.c.shift(1)>df.c.shift(2), 1, 0) #  df.c.shift(1)>df.ma.shift(1)  # 前一次浮盈
    #df['condition'] = np.where(df.ma1.shift(1)>df.ma2.shift(1), 1, 0)# 短期ma在长期ma上
    
    #df['condition'] = np.where(   (df.c.shift(1)>df.ma.shift(1)) & (df.c.shift(1)>df.c.shift(2)), 1, 0) ##在ma上 且 前一次浮盈
    #df['condition'] = np.where(df.ma.shift(1)>df.ma.shift(2), 1, 0) # df.ma.shift(1)>df.ma.shift(2)  ma斜率向上
    '''远离均线几个ATR'''
    df['condition'] = np.where(df.c.shift(1)>df.ma.shift(1)+df.atr.shift(1)*2, 1, 0) 
    rows_index = range(df.shape[0])
    
    '''先写出只做多的程序'''
    持仓期 = 99 #
       
    n = 4 # 止损几个ATR
    y = 2 # 止盈几个ATR
    盈利额 = 0
    亏损额 = 0
    盈利次数 = 0 
    亏损次数 = 0
    跳开滑点 = 3  # 3
    一般滑点 = 1  # 1
    zsccq = []  # 打到止损的单子的持仓期
    for i in rows_index:
        
        row = df.iloc[i] 
        #print(list(row))
        #if row.condition == 1 and i%2 == 0: # 每两天开一次仓
        if row.condition == 1:
            bkprice = row['c']
            bkindex = i
            止损 = bkprice - (int(row['atr'])+1) * n
            止盈 = bkprice + (int(row['atr'])+1) * y
            for j in range(i+1, i+持仓期+1): # 从开仓日开始和后面 持仓期 的天数 逐一作比较
                row2last = df.iloc[j-1] # 移动止损前一天的参照
                try:
                    row2 = df.iloc[j]
                except Exception:
                    print(i,j)
                    print(list(row2))
                

                
                if row2['l'] <= 止损:
                    if row2.o < 止损:   # 处理跳开直接越过止损
                        盈亏额 = row2.o - (bkprice + 跳开滑点)
                    else:
                        盈亏额 = 止损 - (bkprice + 一般滑点)

                    if 盈亏额 > 0:
                        盈利次数 += 1
                        盈利额 += 盈亏额
                    else:
                        亏损次数 += 1
                        亏损额+= abs(盈亏额)
                    break
                
                if row2['h'] >= 止盈:
                    
                    if row2.o > 止盈:   # 处理跳开直接越过止盈
                        盈亏额 = row2.o - bkprice - 跳开滑点 
                    else:
                        盈亏额 = 止盈 - bkprice - 一般滑点

                    if 盈亏额 > 0:
                        盈利次数 += 1
                        盈利额 += 盈亏额
                    else:
                        亏损次数 += 1
                        亏损额+= abs(盈亏额)
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


                止损 = row2last.c - (int(row2last['atr'])+1) * n
                止盈 = row2last.c + (int(row2last['atr'])+1) * y
                #print(bkprice, 止损)
        #if i ==10:break # 测试用
    
        #print(i)
        if i ==df.shape[0]-持仓期-1:
            #print(df.shape[0], 持仓期, i)
            break
    df.to_csv('tmp.csv')
    
    #print(盈利, 亏损, )
    
    print(盈利额/亏损额)
    print(盈利次数/(盈利次数+亏损次数))
    
    #print(zsccq)
    #print(max(zsccq))
    #print(sum(zsccq)/len(zsccq))
    