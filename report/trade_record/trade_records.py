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

df['盈亏'] = df['逐笔平仓盈亏'].apply(lambda y:1 if y>0 else -1) # 盈利 1  亏损 -1 （平仓大于0盈利，反之亏损）
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
print(pzcnt) # 每个品种的交易次数
#pzcnt.plot(kind='bar')
#plt.show()


#pzyk = df.groupby('品种')['逐笔平仓盈亏'].sum()
#pzyk = pzyk.sort_values(ascending=False)
#print(pzyk) # 每个品种盈亏
#pzyk.plot(kind='bar')
#plt.show()


def ykbl(df, hue):
    '''计算盈亏比例'''
    ratio = df[hue][1]/(df[hue][1]+df[hue][-1])
    return '{} : {}%'.format( hue, round(ratio*100, 1) )

# 每个品种盈利比例 
df1 = df.groupby(['品种', '盈亏']).sum()['手数']

print(ykbl(df1, 'rb'))
print(ykbl(df1, 'MA'))
print(ykbl(df1, 'm' ))
print(ykbl(df1, 'c' ))
print(ykbl(df1, 'hc'))
print(ykbl(df1, 'y' ))


#yk_ma = df1.ix[['MA', 1], '手数']##/(df1['MA', 1]+df1['MA',-1])
#print(yk_ma)
# plot
#sns.countplot(x='品种',hue='盈亏',data=df)
#plt.show()


'''
交易次数最多的是rb 79次    总体盈利-5000                                                盈利比例    .34

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
print(df3['逐笔平仓盈亏'])
'''
做多 243次   平仓盈亏 -4075    平均单次 -16.8

做空 136次            -36115             -265

看出做多比做空 结果好很多啊   
'''


'''
做多更好？是不是因为这个时间段总体是偏多

那把所有数据分成三个时间段，再看看是不是也是做多比做空好

一共356条记录 分成  120条左右一段
'''

print('--------------分三个时间段----------------')
df_s1 = df.iloc[:119, :]
df_s2 = df.iloc[119:238, :]
df_s3 = df.iloc[238:, :]

print(df_s1.groupby('开仓方向').sum()['逐笔平仓盈亏'])
print(df_s2.groupby('开仓方向').sum()['逐笔平仓盈亏'])
print(df_s3.groupby('开仓方向').sum()['逐笔平仓盈亏'])

'''
可见也是做多好于做空， 说明做空确实是比较难，（或者说我的操作方式不适合做空）

在交易次数最多的几个品种 rb MA m  jd 上看是否也是这样。交易次数少的不看
'''
df1 = df.groupby(['品种', '开仓方向']).sum()
#print(df1)
#print(df1['逐笔平仓盈亏'])
print(df1['逐笔平仓盈亏'][['rb', 'MA', 'm','jd']])

print('''---------------这样看不明显，应该要看平均每次的平仓盈亏---------''')
print('rb', df1['逐笔平仓盈亏']['rb']/df1['手数']['rb'])
print('MA', df1['逐笔平仓盈亏']['MA']/df1['手数']['MA'])
print('m', df1['逐笔平仓盈亏']['m']/df1['手数']['m'])
print('jd', df1['逐笔平仓盈亏']['jd']/df1['手数']['jd'])
print('c', df1['逐笔平仓盈亏']['c']/df1['手数']['c'])
#可见做多比做空好多啦（但不能这样想，多空还是都要做，空少做，而且更要小心,要么说明我的做法不适合做空，做空用别的方法）
#df1.to_csv('tmp.csv')

#print(df.head(20))




'''
看一段时间内的盈亏是否和交易频繁相关

以季度看下来关系应该不大，交易还是要看时机
'''
print('-------------------------------------')
def readyto_date(date):
    '''20170211 这种形式不能转成DatatimeIndex     2016/12/28  这种可以'''
    date = str(date)
    year = date[:4]
    month = date[4:6]
    day = date[6:]
    return '/'.join([year, month, day])

df_alldate = df.copy()
df_alldate['开仓日期'] = df_alldate['开仓日期'].apply(readyto_date)
df_alldate.index = pd.DatetimeIndex(df_alldate['开仓日期'])
df_alldate = df_alldate.drop('开仓日期', axis=1)
#print(df_alldate.index)
#df_alldate.to_csv('df_alldate.csv')
#print( df['逐笔平仓盈亏'].resample('B') )

# 逐月盈亏
zb = df_alldate['逐笔平仓盈亏']
#yk = zb.resample('M').sum()
#yk.plot(kind='bar')
#plt.show()    

# 逐季度作图
# 逐季度盈亏   
#plt.subplot(211)
#plt.title('季度盈亏')
#yk = zb.resample('Q').sum()
#yk.plot(kind='bar')
#'''
#注意， 现在的资金比初期多, 如果按百分比算的话，应该是比初期要好的
#'''
## 逐季度交易次数
#kc = df_alldate['开仓方向']
#kcq = kc.resample('Q').count()
#plt.subplot(212)
#plt.title('季度交易次数')
#kcq.plot(kind='bar')
#plt.show()  





