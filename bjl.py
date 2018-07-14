'''
揽法和押法


这次出一道百家乐的题目， 其答案就是不断的缆的基本形态。题目是这样的：
现有这样一靴百家乐的路，总数100手，中间只有庄和闲， 没有和。 庄也不抽水。已知庄闲各占不多不少50手，给你的本金只有153个基码，要求每一手都必须下注，你的注码法必须能通过所有的排列。所有的排列的意思，即穷尽100手内有50个庄50个闲的可能性，可以是先来50个庄，再来50个闲，也可以是先来50个闲，再来50个庄，也可以是单跳，也可以是两庄两闲等等。在最坏的情况之下，你要赢1个筹码，在最好的情况之下，你要赢50个筹码。你能皆开这道题吗?`
我相信我们的朋友们有这个能力解开。今天公布答案：
起步是2，输2买3， 再输还是买3，知道输赢手数相等，又从2开始。
赢2买1，再赢还是买1，知道直到输赢手数相等，又从2开始。
举例：+++--- ---+++，+2+1+1-1-1-1 -2-3-3+3+3+3这样就可以赢两个。
如果先输50手，就是-2-3-3-3……-3=-149 ，后面赢50手，就是+3+3…+3=150 赢一个筹码。
相反，如果先赢50手就是+2+1+1……+1=51， 后面连输50手， 就是-1-1-1。。。-1=-50 也赢一个码。
最好的情况是单跳：
+1+1+1+1……+1
+2-1+2-1……+1-2=+50
无论怎样的路，只要输赢手数相等，必定是正赢率。【转】

我改一下，每20次重来，既起步为二
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

draws = np.random.randint(0,2,1000000)
steps = np.where(draws>0, 1,0)
df = pd.DataFrame()

df['胜负'] = steps
# df['一注的量']
#df['下几注'] = 1
#df['下几注'] =np.where( df['胜负'].shift(1)==-1,df['下几注'].shift(1)+1,df['下几注'])
#df['下几注'] =np.where( df['胜负'].shift(1)==-1,df['下几注'].shift(1)+1,df['下几注'])
#df['下几注'] =np.where( df['胜负'].shift(1)==-1,df['下几注'].shift(1)+1,df['下几注'])
#df['下几注'] =np.where( df['胜负'].shift(1)==-1,df['下几注'].shift(1)+1,df['下几注'])
#df['下几注'] =np.where( df['胜负'].shift(1)==-1,df['下几注'].shift(1)+1,df['下几注'])
#df['下几注'] =np.where( df['胜负'].shift(1)==-1,df['下几注'].shift(1)+1,df['下几注'])
#df['下几注'] =np.where( df['胜负'].shift(1)==-1,df['下几注'].shift(1)+1,df['下几注'])
#df['下几注'] =np.where( df['胜负'].shift(1)==-1,df['下几注'].shift(1)+1,df['下几注'])
#df['下几注'] =np.where( df['胜负'].shift(1)==-1,df['下几注'].shift(1)+1,df['下几注'])
#df['下几注'] =np.where( df['胜负'].shift(1)==-1,df['下几注'].shift(1)+1,df['下几注'])
#df['下几注'] =np.where( df['胜负'].shift(1)==-1,df['下几注'].shift(1)+1,df['下几注'])
#df['下几注'] =np.where( df['胜负'].shift(1)==-1,df['下几注'].shift(1)+1,df['下几注'])
#df['下几注'] =np.where( df['胜负'].shift(1)==-1,df['下几注'].shift(1)+1,df['下几注'])
#df['下几注'] =np.where( df['胜负'].shift(1)==-1,df['下几注'].shift(1)+1,df['下几注'])
#df['下几注'] =np.where( df['胜负'].shift(1)==-1,df['下几注'].shift(1)+1,df['下几注'])
#df['下几注'] =np.where( df['胜负'].shift(1)==-1,df['下几注'].shift(1)+1,df['下几注'])
#df['下几注'] =np.where( df['胜负'].shift(1)==-1,df['下几注'].shift(1)+1,df['下几注'])
#df['下几注'] =np.where( df['胜负'].shift(1)==-1,df['下几注'].shift(1)+1,df['下几注'])
#df['下几注'] =np.where( df['胜负'].shift(1)==-1,df['下几注'].shift(1)+1,df['下几注'])
#df['下几注'] =np.where( df['胜负'].shift(1)==-1,df['下几注'].shift(1)+1,df['下几注'])
#df['盈亏'] = df['胜负'] *df['下几注']

#df['盈亏'] = np.where( (df['胜负'].shift(1)==1) , 1*df['胜负'], df['盈亏'])
#df['盈亏'] = np.where( (df['胜负'].shift(1)==-1) , 3*df['胜负'], df['盈亏'])

df['b'] = 0
rows_index = range(df.shape[0])


nums = range(1,50)
counter = dict.fromkeys(nums, 0)
cnt = 1
for i in rows_index:
    row_last = df.iloc[i-1]
    row = df.iloc[i]
    if row['胜负'] == row_last['胜负']:
        cnt +=1
    else:
        counter[cnt] += 1
        cnt =1

print(counter)

df.to_csv('tmp.csv')

#print(df['盈亏'].sum())








