'''
训练集   当天的四个价格和DKX的b线的比值
         当天b线和昨天b线的比值
结果集    后n天收盘价
'''
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.naive_bayes import GaussianNB,MultinomialNB
from sklearn.tree import DecisionTreeClassifier as DTC
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler, StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression

df = pd.read_csv(r'..\data\rb.csv')

df['ma'] = df.c.rolling(window=20, center=False).mean()
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

#df.b.plot()
#df.c.plot()
#plt.show()


df['ob'] = df.o / df.b
df['cb'] = df.c / df.b
df['hb'] = df.h / df.b
df['lb'] = df.l / df.b
df['ob2'] = df.o.shift(1) / df.b.shift(1)
df['cb2'] = df.c.shift(1) / df.b.shift(1)
df['hb2'] = df.h.shift(1) / df.b.shift(1)
df['lb2'] = df.l.shift(1) / df.b.shift(1)

df['bb'] = df.ma / df.ma.shift(1)# b比值

df['label'] = df.c.shift(-10) / df.o.shift(-1) # 后n天收盘价除明天开盘价
#df['label'] = np.round(df.label, 1)  # 改变小数点保留位数
df.label = np.where(df.label>1, 1, 0)
le = LabelEncoder()
df['label'] = le.fit_transform(df.label.values)
#print(df.label)

df = df.dropna(axis=0)
#df.to_csv('tmp.csv')
X = df.loc[:,['ob','cb','hb','lb','bb','ob2','cb2','hb2','lb2']]
#X = df.loc[:,['bb']]
X = X * 100
ss = StandardScaler()
#X = ss.fit_transform(X)

y = df['label']


X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, test_size=0.3)

#model = GaussianNB() # 4.8372
#model = MLPClassifier(hidden_layer_sizes=(3,3,3),max_iter=999)  # 2.3606 2.3968
#model = DTC() # 0 ?那么好？？？因为没有交叉验证
#model = KNeighborsClassifier(n_neighbors=5, p=2, metric='minkowski') # 3.9818
#model = LogisticRegression(C=1000, random_state=0)      # 2.5912  ob2等 2.6194
#model = MultinomialNB()  # 2.3429
#model = SVC(kernel='linear', C=3.0, random_state=1) # 2.322  ob2等 2.397
model = SVC(kernel='rbf', C=3.0, random_state=0, gamma=0.2) # 2.2951    ob2等 2.0717

model.fit(X_train, y_train)
#model.fit(X, y)
y_pred = model.predict(X_test)
#y_true = le.inverse_transform(y)
#y_pred = le.inverse_transform(y_pred)
result = {'y_true': y_test, 'y_pred': y_pred}
dfr = pd.DataFrame(result)
dfr.to_csv('tmp.csv')
#dfr = dfr.dropna(axis=0)
cost = ((dfr.y_true - dfr.y_pred)**2).sum()
print(cost)