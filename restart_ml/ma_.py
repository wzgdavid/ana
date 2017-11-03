'''
训练集   当天的四个价格
结果集    程序生成，
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
#df = pd.read_csv(r'..\data\ta.csv')
df = df.ix[:, ['o', 'h', 'l', 'c']] 

df = df.fillna(0) # 把手动输入的do的空行补满
n = 20
df['ma'] = df.c.rolling(window=n, center=False).mean()

df = df.dropna()  # 去掉没有ma的行

######
#用程序生成结果集，规则自定
###########
## 后三天低点和高点都是一天比一天高，做多
#l_higher = (df.l.shift(-1) > df.l) & (df.l.shift(-2) > df.l.shift(-1))
#h_higher = (df.h.shift(-1) > df.h) & (df.h.shift(-2) > df.h.shift(-1))
#df['do'] = np.where(h_higher & l_higher, 1, np.nan)
## 反之 做空
#l_lower = (df.l.shift(-1) < df.l) & (df.l.shift(-2) < df.l.shift(-1))
#h_lower = (df.h.shift(-1) < df.h) & (df.h.shift(-2) < df.h.shift(-1))
#df['do'] = np.where(l_lower & h_lower, 2, df['do'])
# 后一天低点和高点都是一天比一天高，做多
l_higher = (df.l.shift(-1) > df.l)
h_higher = (df.h.shift(-1) > df.h)
df['do'] = np.where(h_higher & l_higher, 1, np.nan)
# 反之 做空
l_lower = (df.l.shift(-1) < df.l)
h_lower = (df.h.shift(-1) < df.h)
df['do'] = np.where(l_lower & h_lower, 2, df['do'])
# 其他情况不操作， 
df.do = df.do.fillna(0)


df['higherthanma'] = np.where(df.c>df.ma, 1, 0)
df['lowerthanma'] = np.where(df.c<df.ma, 1, 0)


#df = df.ix[n:, ['oma', 'cma' ,'hma', 'lma','oma2', 'cma2' ,'hma2', 'lma2','do']] 
#df = df.ix[n:, ['oma', 'cma' ,'hma', 'lma', 'do']] 
df = df.ix[:, ['higherthanma', 'lowerthanma', 'do']] 
#df.drop('do', axis=1).to_csv('tmp.csv')
#df.to_csv('tmp.csv')
X = df.drop('do', axis=1)

#x = StandardScaler().fit_transform(x)

#print(x)
#classle = LabelEncoder()
y = df['do']

#print(y[y==2].sum())
#print(X, y)
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, test_size=0.3)
#print(y_test.shape)
model = GaussianNB() # 
model = MLPClassifier(hidden_layer_sizes=(133,133,133),max_iter=999)  # 
#model = DTC() #
#model = KNeighborsClassifier(n_neighbors=5, p=2, metric='minkowski')
model = LogisticRegression(C=1000, random_state=0)                 
# 以下都有UndefinedMetricWarning
#model = MultinomialNB() 
#model = SVC(kernel='linear', C=1.0, random_state=1) # ma20  76左右
#model = SVC(kernel='rbf', C=1.0, random_state=0, gamma=0.1) # ma20 67左右

model.fit(X_train, y_train)
print(model.score(X_train, y_train))

predicted = model.predict(X_test)
expected = y_test
report = metrics.classification_report(predicted, expected)
print(report)


# 混淆矩阵
cm = metrics.confusion_matrix(predicted, expected)
print(cm)
