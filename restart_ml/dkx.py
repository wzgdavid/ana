'''
训练集   当天的四个价格和DKX的b线的比值
         当天b线和昨天b线的比值
结果集    
'''

import numpy as np
import pandas as pd



df = pd.read_csv(r'..\data\rb\zl.csv')

# 构建指标
def get_DKX(df, n=10):
    df['a'] = (df.c * 3 + df.l + df.o + df.h)/6
    df['b'] = (20*df.a + 19*df.a.shift(1) + 18*df.a.shift(2) + 17*df.a.shift(3) + 
        16*df.a.shift(4) + 15*df.a.shift(5) + 14*df.a.shift(6) + 
        13*df.a.shift(7) + 12*df.a.shift(8) + 11*df.a.shift(9) + 
        10*df.a.shift(10) + 9*df.a.shift(11) + 8*df.a.shift(12) + 7*df.a.shift(13) + 
        6*df.a.shift(14) + 5*df.a.shift(15) + 4*df.a.shift(16) + 
        3*df.a.shift(17) + 2*df.a.shift(18) + 1*df.a.shift(19))/210
    df['d'] = df.b.rolling(n).mean()
    return df.drop(['a'], axis=1)

df = get_DKX(df) 
df['ma'] = df.c.rolling(window=10, center=False).mean()


df['ob'] = df.o / df.b
df['cb'] = df.c / df.b
df['hb'] = df.h / df.b
df['lb'] = df.l / df.b
#df['ob2'] = df.o.shift(1) / df.b.shift(1)
#df['cb2'] = df.c.shift(1) / df.b.shift(1)
#df['hb2'] = df.h.shift(1) / df.b.shift(1)
#df['lb2'] = df.l.shift(1) / df.b.shift(1)

df['bb'] = df.b / df.b.shift(1)# b比值
#df['bshift1'] = df.b.shift(1)

# 标签规则
n = 1
# label 1
df['label'] = df.c.shift(-1 * n) / df.c # 后n天收盘价除今天收盘价
df.label = np.where(df.label>1, 1, 0)
# label 2
#df['label'] = np.where(df.bb>1, 1, 0)

#print(df.label)

#过滤数据
df['DKX_b_up'] = np.where(df.b > df.b.shift(1), 1, 0)
#df = df.ix[df.DKX_b_up==1,:]  # 过滤出DKXb 向上的数据

df['higher_DKX'] = np.where(df.h<df.b, 1, 0)
#df = df.ix[df.higher_DKX==1,:]  # 过滤出k线比DKXb 高的数据

# 过滤出ma向上的数据
df['ma_up'] = np.where(df.ma > df.ma.shift(1), 1, 0)
#df = df.ix[df.ma_up==1, :]
# k线在ma上的数据
df['ma_up'] = np.where(df.l > df.ma, 1, 0)
df = df.ix[df.ma_up==1, :]

# 过滤条件后的结果
def result(df):
    '''df is dataframe'''
    df['c_up'] = np.where( df.c/df.c.shift(1)>1, 1, 0 )
    gailv = np.round(df.c_up.sum()/df.shape[0], 3) * 100
    gailv = str(gailv)[:4]
    print( 'c比前一天高的概率 {}% '.format(gailv)) # 某条件下   c比前一天高的概率
    
    df['l_up'] = np.where( df.l/df.l.shift(1)>1, 1, 0 )
    gailv = round(df.l_up.sum()/df.shape[0], 3) * 100
    gailv = str(gailv)[:4]
    print('low比前一天高的概率 {}%'.format(gailv)) # 某条件下   low比前一天高的概率
result(df)

df.to_csv('tmp.csv')
df = df.dropna(axis=0)

'''
#print(df.head(30))

X = df.loc[:, ['ob','cb','hb','lb']]
#print(X)
#X = df.loc[:,['bb']]
#X = X * 100

#ss = StandardScaler()
ss = MinMaxScaler()
#X = ss.fit_transform(X)

X = ss.fit_transform(X)
y = df.label

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, test_size=0.3)


# 构建数据完毕
# 开始学习
'''

'''
model = GaussianNB()
#model = MLPClassifier(hidden_layer_sizes=(3,3,3),max_iter=999) 
#model = DTC()  # 100% ?
#model = KNeighborsClassifier(n_neighbors=5, p=2, metric='minkowski')
#model = LogisticRegression(C=1000, random_state=0)
#model = MultinomialNB() 
#model = SVC(kernel='linear', C=3.0, random_state=1)
#model = SVC(kernel='rbf', C=3.0, random_state=0, gamma=0.2) 
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

dff = pd.DataFrame()  # 结果比较的dataframe
dff['y_true'] = y_test
dff['y_pred'] = y_pred
dff['right pred'] = np.where(dff.y_true==dff.y_pred, 1, None)
print(dff['right pred'].sum()/dff.shape[0])
dff.to_csv('tmp.csv')
'''
