'''
训练集   当天的四个价格，和ma（用pandas算不同的ma来学习）
结果集    自己看k线决定做多1  做空2 或不操作0 ，输入进csv
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

df = pd.read_csv(r'..\data\rb_ml_ma.csv')
df = df.fillna(0)
n = 20
df['ma'] = df.c.rolling(window=n, center=False).mean()


df['oma'] = df.o / df.ma
df['cma'] = df.c / df.ma
df['hma'] = df.h / df.ma
df['lma'] = df.l / df.ma
df['oma2'] = df.o.shift(1) / df.ma
df['cma2'] = df.c.shift(1) / df.ma
df['hma2'] = df.h.shift(1) / df.ma
df['lma2'] = df.l.shift(1) / df.ma

#df = df.ix[n:, ['oma', 'cma' ,'hma', 'lma','oma2', 'cma2' ,'hma2', 'lma2','do']] 
#df = df.ix[n:, ['oma', 'cma' ,'hma', 'lma', 'do']] 
#df = df.ix[n:, ['oma', 'cma' ,'hma', 'lma', 'do']] 
df['higherthanma'] = np.where(df.c>df.ma, 1, 0)
df['lowerthanma'] = np.where(df.c<df.ma, 1, 0)


#df = df.ix[n:, ['oma', 'cma' ,'hma', 'lma','oma2', 'cma2' ,'hma2', 'lma2','do']] 
#df = df.ix[n:, ['oma', 'cma' ,'hma', 'lma', 'do']] 
df = df.ix[:, ['higherthanma', 'lowerthanma', 'do']] 
#df.drop('do', axis=1).to_csv('tmp.csv')
#df.to_csv('tmp.csv')
x = df.drop('do', axis=1)

#print(x)
#classle = LabelEncoder()
y = df['do']

#print(x, y)
x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.7, test_size=0.3)

#model = GaussianNB() # 60左右
model = MLPClassifier(hidden_layer_sizes=(13,13,13),max_iter=999)  # ma20 67左右
#model = DTC() #
#model = KNeighborsClassifier(n_neighbors=5, p=2, metric='minkowski')
model = LogisticRegression(C=1000, random_state=0)                 # 太差
# 以下都有UndefinedMetricWarning
#model = MultinomialNB() 
#model = SVC(kernel='linear', C=1.0, random_state=1) # ma20  76左右
#model = SVC(kernel='rbf', C=1.0, random_state=0, gamma=0.1) # ma20 67左右

model.fit(x_train, y_train)


predicted = model.predict(x_test)
expected = y_test
report = metrics.classification_report(predicted, expected)
print(report)


# 混淆矩阵
cm = metrics.confusion_matrix(predicted, expected)
print(cm)
