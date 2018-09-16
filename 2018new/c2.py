
'''
这个和c.py相反，是做空
'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from common import *#get_DKX, get_nhh, get_nll, get_ma, avg,get_nhhzs,get_nllzs,get_atr

#pinzhong = 'pp'
pinzhong_lst = ['rb','sr','c','ma','pp','ta','m','a','rm','y']
#pinzhong_lst = ['rb','sr']

#pinzhong_lst = ['rbl91h','srl91h','ml91h','oil91h','ppl91h']
for pinzhong in pinzhong_lst:
    print(pinzhong, '-------------------------------')
    plt.rcParams['font.sans-serif'] = ['SimHei'] # 正常显示中文
    df = pd.read_csv(r'..\data\{}.csv'.format(pinzhong))
    df = get_DKX(df)
    
    df = get_ma(df, 20)
    
    df = get_atr(df, 50)
    df = df.dropna()   
    
    '''
    过滤  start
    '''
    df = df.iloc[-500:,  :]  #选择部分
    df['condition'] = 1  # 不过滤
    #df['condition'] = np.where(df.c.shift(1)>df.ma.shift(1), 1, 0) #  df.c.shift(1)>df.ma.shift(1)  在ma下
    #df['condition'] = np.where(df.c.shift(1)<df.c.shift(2), 1, 0) #  df.c.shift(1)>df.ma.shift(1)  # 前一次浮盈

    
    #df['condition'] = np.where(   (df.c.shift(1)<df.ma.shift(1)) & (df.c.shift(1)>df.c.shift(2)), 1, 0) ##在ma上 且 前一次浮盈
    #df['condition'] = np.where(df.ma.shift(1)>df.ma.shift(2), 1, 0) # df.ma.shift(1)>df.ma.shift(2)  ma斜率向上
    
    
    rows_index = range(df.shape[0])
    
    '''先写出只做多的程序'''
    持仓期 = 20 #
       
    n = 1 # 止损几个ATR
    m = 2 # 移动止损几个ATR
    y = 4 # 止盈几个ATR
    盈利额 = 0
    亏损额 = 0
    盈利次数 = 0 
    亏损次数 = 0
    跳开滑点 = 3  # 3
    一般滑点 = 1  # 1
    for i in rows_index:
        
        row = df.iloc[i] 
        #print(list(row))
        #if row.condition == 1 and i%2 == 0: # 每两天开一次仓
        if row.condition == 1:
            skprice = row['c']
            止损 = skprice + (int(row['atr'])+1) * n
            止盈 = skprice - (int(row['atr'])+1) * y
            for j in range(i+1, i+持仓期+1): # 从开仓日开始和后面 持仓期 的天数 逐一作比较
                row2last = df.iloc[j-1] # 移动止损前一天的参照
                try:
                    row2 = df.iloc[j]
                except Exception:
                    print(i,j)
                    print(list(row2))
                
        
                
                '''在持仓期内打到止损'''
                '''移动止损的写法  '''
                if 1: # 移动止损开关
                    移动止损 = row2last.l + (int(row2last['atr'])+1) * m
                    止损 = max(止损,移动止损)
                #if 1: # 止损开关
                #    if row2['h'] >= 止损:
                #        if row2.o > 止损:   # 处理跳开直接越过止损
                #            pcprice = row2.o - skprice + 跳开滑点 
                #        else:
                #            pcprice = 止损 - skprice + 一般滑点
                #
                #        if pcprice > 0:
                #            亏损额 += pcprice
                #            亏损次数 += 1
                #        else :
                #            盈利额 += abs(pcprice)
                #            盈利次数 += 1    
                #        break
        
                
        
                '''没移动止损的写法  更简单'''
                if 1: # 止损开关
                    if row2['h'] >= 止损:
                        if row2.o > 止损:   # 处理跳开直接越过止损
                            亏损额 += row2.o - skprice + 跳开滑点
                        else:
                            亏损额 += 止损 - skprice + 一般滑点
                        亏损次数 += 1
                        break
    
    
                '''在持仓期内打到止盈'''
                if 0: # 止盈开关    总体来说还是不主动止盈好一点
                    if row2['h'] >= 止盈:
                        盈利次数 += 1
                        if row2.o > 止盈:   # 处理跳开直接越过止盈
                            盈利额 += skprice - row2.o - 一般滑点 
                        else:
                            盈利额 += skprice - 止盈 - 一般滑点
                        break
                '''在持仓期内没有止损， 到持仓时间，自然平仓''' 
                if j == i+持仓期:
                    pcprice = row.c -  (row2.c + 一般滑点)
                    if pcprice > 0:
                        盈利额 += pcprice
                        盈利次数 += 1
                    else:
                        亏损额 += abs(pcprice)
                        亏损次数 += 1
                #print(skprice, 止损)
        #if i ==10:break # 测试用
    
        #print(i)
        if i ==df.shape[0]-持仓期-1:
            #print(df.shape[0], 持仓期, i)
            break
    df.to_csv('tmp.csv')
    
    print(盈利额, 亏损额, )
    print('盈亏比',盈利额/亏损额)
    print('胜率', 盈利次数/(盈利次数+亏损次数))
    