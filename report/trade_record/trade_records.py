'''
分析自己的交易记录
时间段 20150331 到 20171220  共356次交易
无关策略，策略中间有小的变化


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
看一段时间内的盈亏是否和交易频率相关
                是否和交易的品种数量相关
以季度看下来和交易频率关系不大
'''
print('-------------------------------------')
def readyto_date(date):
    '''20170211 这种形式不能转成DatatimeIndex     2016/12/28  这种可以'''
    date = str(date)
    year = date[:4]
    month = date[4:6]
    day = date[6:]
    return '/'.join([year, month, day])

df_dateidx = df.copy()
df_dateidx['开仓日期'] = df_dateidx['开仓日期'].apply(readyto_date)
df_dateidx.index = pd.DatetimeIndex(df_dateidx['开仓日期'])
df_dateidx = df_dateidx.drop('开仓日期', axis=1)
#print(df_dateidx.index)
#df_dateidx.to_csv('df_dateidx.csv')
#print( df['逐笔平仓盈亏'].resample('B') )

zb = df_dateidx['逐笔平仓盈亏']
# 逐月盈亏
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
#kc = df_dateidx['开仓方向']
#kcq = kc.resample('Q').count()
#plt.subplot(212)
#plt.title('季度交易次数')
#kcq.plot(kind='bar')
#plt.show()


print('--------------收益共性------------------')
'''
分析收益最高的交易前13条，看看他们的共性（
  比如做多时是不是都是DKX b线在d线上
   也拿周线的比较，是不是日线和周线的DKX同向
'''
feature_data = df_dateidx.sort_values(by='逐笔平仓盈亏')[-12:]  # [-12:]表示盈利的前12个  [:12] 是最大亏的前12个
#print(feature_data)

rb_test = feature_data.iloc[-1]
#print(type(rb_test.name))
#print(rb_test)
def get_DKX(df, n=10):
    df['a'] = (df.c * 3 + df.l + df.o + df.h)/6
    sum_ = '+'.join(['{}*df.a.shift({})'.format(20-i, i) for i in range(0, 20)]) 
    eval_str = '({})/210'.format(sum_)
    df['b'] = eval(eval_str)
    df['d'] = df.b.rolling(n).mean()
    return df.drop(['a'], axis=1)
print('-----------------for loop----------------------')

feature_results = []
for i in range(feature_data.shape[0]):
    row = feature_data.iloc[i]
    name = row['品种'].lower()
    kdata = pd.read_csv(r'..\..\data\{}.csv'.format(name)) # 对应品种的数据
    kdata = get_DKX(kdata)
    kdata.index = pd.DatetimeIndex(kdata['date'])
    #print(kdata.tail())
    # 看DKX b 在 d 的上 还是 下
    #print(name,'---------------aa')
    thatk = kdata.loc[row.name]  # 那一天的日K线
    feature_results.append( (
             'b在d上' if thatk['b'] > thatk['d'] else 'b在d下',
             row['开仓方向'],
             row.name,    # 开仓日期
             row['品种']
        ) )
feature_results = pd.DataFrame(feature_results, columns=['DKX', '方向','开仓日期','品种'])


print(feature_results)



'''
盈利的前12个
     DKX    方向       开仓日期  品种    周线DKX方向（自己看的）  开仓方向和日周DKX    开仓和周DKX
                                        b在d
0   b在d下  sell 2015-06-04   c           下                        同                    同
1   b在d下   buy 2017-01-12  MA           上                                              同                         
2   b在d下   buy 2016-01-15  TA           下                                                                
3   b在d下   buy 2017-01-12   c           上                                               同                             
4   b在d下   buy 2015-11-23   y           下                                                              
5   b在d下   buy 2016-06-06  hc           上                                               同             
6   b在d上   buy 2016-01-26  rb           下                                                                
7   b在d下  sell 2015-05-27   c           下                        同                     同                                     
8   b在d上   buy 2017-07-31  rb           上                        同                     同                                    
9   b在d上   buy 2017-07-31  rb           上                        同                     同                                    
10  b在d上   buy 2016-05-25   m           上                        同                     同                                    
11  b在d上   buy 2016-10-14  rb           上                        同                     同                                      
'''
'''
最大亏的前12个
     DKX    方向       开仓日期  品种     周线DKX方向（自己看的）   开仓方向和日周DKX   开仓和周DKX
                                            b在d
0   b在d下  sell 2017-09-28  rb             上     
1   b在d上   buy 2017-09-04  rb             上                        同                 同
2   b在d下   buy 2015-11-12   i             下                        
3   b在d下   buy 2015-06-19  ag             上                                           同
4   b在d上   buy 2017-12-05  rb             上                         同                同
5   b在d下  sell 2015-12-22   y             上                         
6   b在d下   buy 2016-07-14   m             上                                           同
7   b在d下   buy 2015-06-18   y             上                                           同
8   b在d下   buy 2015-06-02  ag             上                                           同
9   b在d下  sell 2016-08-25  ag             下                         同                同
10  b在d下  sell 2017-10-12  MA             上                         
11  b在d上  sell 2015-05-04  TA             上                         


亏损中  同  的也很多 ， 说明开仓点位不好
'''




'''
然后  同样的  看下 DKX的斜率
'''
print('---------------------DKX的斜率------------------------')
print(feature_data)
feature_results2 = []
for i in range(feature_data.shape[0]):
    row = feature_data.iloc[i]
    #print(row)
    name = row['品种'].lower()
    kdata = pd.read_csv(r'..\..\data\{}.csv'.format(name)) # 对应品种的数据
    kdata = get_DKX(kdata)
    kdata.index = pd.DatetimeIndex(kdata['date'])
    # 求KDX斜率
    #kdata['last_b'] = kdata.d.shift(1)
    kdata['斜率'] = (kdata.b / kdata.d.shift(1))
    #print(kdata) 

    #print(name,'---------------aa')
    thatk = kdata.loc[row.name]  # 那一天的日K线
    feature_results2.append( (
             kdata.ix[row.name, '斜率'] if kdata.ix[row.name, '斜率'] else None,

             row['开仓方向'],
             row.name,    # 开仓日期
             row['品种']
        ) )
    
feature_results2 = pd.DataFrame(feature_results2, columns=['DKX', '方向','开仓日期','品种'])


print(feature_results2)



'''
由此可见  最赚钱的几次交易有一个共同特征， 就是日线和周线都是顺势的仓位

接着用这个思路到我的历史交易记录里去区分顺势的和非顺势的，看看这两者的结果是否有明显差异 
'''
print('-------------------5675----------------')
#print(df.head())
# 分品种看   
name = 'rb' # name换一个可看其他品种
dff = df_dateidx[df_dateidx['品种'] == name].copy()   # 对应品种的交易记录

kdata = pd.read_csv(r'..\..\data\{}.csv'.format(name)) # 对应品种的数据
kdata = get_DKX(kdata)
kdata.index = pd.DatetimeIndex(kdata['date'])
kdata['斜率'] = (kdata.b / kdata.d.shift(1))  # 斜率指DKX的斜率
kdata = kdata.dropna(axis=0)
# 开仓当天的斜率

dff['斜率'] = kdata.loc[dff.index,:]['斜率']

dff['斜率上下'] = np.where(dff['斜率']>1, 'up', 'down')
# 斜率向上买， 向下卖是顺势
dff['顺势'] = np.where( (dff['斜率']>1) & (dff['开仓方向'] == 'buy' ), True, False)
dff['顺势'] = np.where( (dff['斜率']<1) & (dff['开仓方向'] == 'sell' ), True, dff['顺势'])
#print(dff.head(30))
print(dff[['开仓方向','斜率','顺势','逐笔平仓盈亏']] )
syk = dff.groupby('顺势').sum()['逐笔平仓盈亏']  #  顺势和逆势的盈亏
ccs = dff['顺势'].value_counts()           #  顺势和逆势交易次数
print(syk)
print(ccs)  #

print('--------------------顺势平均单次盈亏------------')
print(syk[True]/ccs[True])  
print('--------------------逆势平均单次盈亏------------')   
print(syk[False]/ccs[False]) 
'''
看下来也是顺势比逆势要好， 但这里还没看周线的DKX是否顺势， 这个不太好弄，
但数据好在不多，我看了2017年下半年的交易，周线DKX都是向上的，也就是说下半年不能做空
如果过滤掉那些做空的单子，也要好很多啊
而且这段时间螺纹开仓有点多啊，特别是11月，和刚开始的几个月没区别，不应该
2017-07-12   buy  1.045487   True     -20
2017-07-17   buy  1.046790   True    -740
2017-07-19   buy  1.045078   True    -790
2017-07-31   buy  1.015143   True    4570
2017-07-31   buy  1.015143   True    3620
2017-08-10   buy  1.044014   True    -950
2017-08-17   buy  1.026456   True    -480
2017-09-04   buy  1.011099   True   -1920
2017-09-20  sell  0.987730   True    -430
2017-09-28  sell  0.968292   True   -2080
2017-10-11  sell  0.969961   True    -360
2017-10-19  sell  0.993141   True    -720
2017-10-19  sell  0.993141   True     350
2017-10-24   buy  1.001397   True    -370
2017-10-30  sell  0.999227   True    -540
2017-11-01   buy  0.996555  False    -580
2017-11-02   buy  0.996296  False     -10
2017-11-03   buy  0.996018  False    -570
2017-11-09   buy  1.004089   True    -590
2017-11-10   buy  1.006797   True    -760
2017-11-17  sell  1.012169  False    -720
2017-11-23   buy  1.013196   True    -700
2017-11-27   buy  1.014959   True    1830
2017-11-29   buy  1.019361   True     610
2017-12-05   buy  1.028482   True   -1610
2017-12-07   buy  1.022841   True    -430
2017-12-08   buy  1.019055   True     -40
2017-12-11   buy  1.016326   True    -870
2017-12-12   buy  1.013517   True    -980
2017-12-20  sell  0.993370   True   -1020
以上是部分数据，以周线来说应该是只能buy的，sell是逆势
sell的单子亏了5520  一共8单   平均一次亏690  
buy的单子亏了1780  一共22单  平均一次亏81  也不好，因为做的太频繁了， 但还是比sell的好多了


然后用其他品种看下来也是顺势比逆势好多了，所以以后一定要坚定
（也不是说我不坚定，之前方法不完善，没有好的方法来对趋势做判断，开仓点位也不好吧，）

结论就是以后一定要用和里的方法去判断趋势，要顺大势，具体用什么指标，我也试过，
不管用均线，MACD，JDK，不管是趋势指标还是震荡指标，只要按照一定的规则去做。效果差不多。
'''