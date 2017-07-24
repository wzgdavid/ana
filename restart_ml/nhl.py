'''
训练集   当天的四个价格，和前n天最高最低点
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
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler, StandardScaler
df = pd.read_csv(r'..\data\rb_ml_ma.csv')
df = df.fillna(0)
n = 20
#df['ma'] = df.c.rolling(window=n, center=False).mean()
df['nhh'] = df.h.shift(1).rolling(window=n, center=False).max()  # 前n天最高点
df['nll'] = df.l.shift(1).rolling(window=n, center=False).min()  # 前n天最低点

df['cnhh'] = df.c / df.nhh
df['cnll'] = df.c / df.nll


#df = df.ix[n:, ['oma', 'cma' ,'hma', 'lma','oma2', 'cma2' ,'hma2', 'lma2','do']] 
#df = df.ix[n:, ['oma', 'cma' ,'hma', 'lma', 'do']] 
df = df.ix[n:, ['cnhh', 'cnll', 'do']] 
df = df.dropna()
x = df.drop('do', axis=1)

x = StandardScaler().fit_transform(x)

#print(x)
#classle = LabelEncoder()
y = df['do']

#print(x, y)
x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.7, test_size=0.3)

#model = GaussianNB() # 60左右
#model = MLPClassifier(hidden_layer_sizes=(13,13,13),max_iter=999)  # ma20 67左右
model = DTC() #
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
