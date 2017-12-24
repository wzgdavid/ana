'''
分析自己的交易记录
时间段 20150331 到 20171220  共356次交易
无关策略，策略中间有小的变化

看是什么原因导致连续的亏损
1   交易密集时？
2   交易品种太多？
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("darkgrid")# darkgrid , whitegrid , dark , white ,和 ticks 

plt.rcParams['font.sans-serif'] = ['SimHei'] # 正常显示中文

df = pd.read_csv('trade_record.csv', encoding='gbk')
df = df.sort_values(by='开仓日期').reset_index().drop(['Unnamed: 0', 'index'],axis=1)

df['盈亏'] = df['逐笔平仓盈亏'].apply(lambda y:1 if y>0 else -1) # 盈利 1  亏损 -1
总盈亏 = df['逐笔平仓盈亏'].sum()
yk = df['盈亏'].value_counts()
盈利比例 = yk[1]/(yk[1]+yk[-1])
#print(盈利比例)
#print(总盈亏)  # 心累


'''
分品种看
'''
def heyue_name(heyue):
    '''
    提取品种名
    '''
    rtn = ''
    for c in heyue:
        if c.isalpha():
            rtn += c
        else:
            break
    #print(rtn)
    return rtn

df['品种'] = df['合约'].apply(heyue_name)

pzcnt = df['品种'].value_counts()
#print(pzcnt) # 每个品种的交易次数
#pzcnt.plot(kind='bar')
#plt.show()


pzyk = df.groupby('品种')['逐笔平仓盈亏'].sum()
pzyk.sort_values()
#print(pzyk.sort_values(ascending=False)) # 每个品种盈亏


def ykbl(df, hue):
    '''计算盈亏比例'''
    return df[hue][1]/(df[hue][1]+df[hue][-1])
# 每个品种盈利比例 （大于0盈利，反之亏损）
df1 = df.groupby(['品种', '盈亏']).sum()['手数']
#df1.to_csv('tmp.csv')

print(
    ykbl(df1, 'rb'),
    ykbl(df1, 'MA'),
    ykbl(df1, 'm'),
    ykbl(df1, 'c'),
    ykbl(df1, 'hc'),
    ykbl(df1, 'y'),

)
#yk_ma = df1.ix[['MA', 1], '手数']##/(df1['MA', 1]+df1['MA',-1])
#print(yk_ma)
# plot
#sns.countplot(x='品种',hue='盈亏',data=df)
#plt.show()


'''
交易次数最多的是rb 79次    总体盈利-5000                                               盈利比例    .34
    第二多      MA 60次            -260   （比想象中好）                                           .4
    第三多      m  42              -7700                (感觉走势不明显，最近没碰)                 .27

而 盈利做多     c 交易 25次   盈利  5650  （比想象中好）(感觉走势不明显，所以好久没碰)             .28
    第二多      hc     11次         1630  （比想象中好）                                           .27
    第三多      y      12           360   （比想象中好）(感觉走势不明显，所以好久没碰)             .41

可见盈利和交易次数完全没关系，所以要控制住自己的心，要适当地远离市场
          和比例的关系也不大，最终还是要看预期
          所以后面就看盈亏，不比较次数和比例
'''

df2 = df.groupby(['开仓方向', '盈亏']).sum()['手数']
print(ykbl(df2, 'buy'),  ykbl(df2, 'sell'))  # 可见做多盈利比例更高

df3 = df.groupby('开仓方向').sum()
print(df3)
'''
做多 243次   平仓盈亏 -4075
做空 136次            -36115   
看出做多比做空 结果好很多啊   （如果从一开始就没做空就好了）（但不能这样想，多空还是都要做，只是少做空，而且更要小心）

在交易次数最多的rb MA m  和 盈利次数多的c hc y 上看是否也是这样
交易次数少的不看
看下来只有c是多空都盈利的，  原来我做的最好的是c
'''
df1 = df.groupby(['品种', '开仓方向']).sum()
print(df1['逐笔平仓盈亏'])
print(df1['逐笔平仓盈亏'][['rb', 'MA', 'm','c', 'hc', 'y' ]])

'''基本上都是做多的情况好于做空'''
#df1.to_csv('tmp.csv')

#print(df.head(20))






