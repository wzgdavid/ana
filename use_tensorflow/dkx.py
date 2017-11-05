'''
训练集   当天的四个价格和DKX的b线的比值
         当天b线和昨天b线的比值
结果集    后n天收盘价，与当天的比值
'''
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler, LabelEncoder
import tensorflow as tf
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2' 



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
#df['ob2'] = df.o.shift(1) / df.b.shift(1)
#df['cb2'] = df.c.shift(1) / df.b.shift(1)
#df['hb2'] = df.h.shift(1) / df.b.shift(1)
#df['lb2'] = df.l.shift(1) / df.b.shift(1)

df['bb'] = df.ma / df.ma.shift(1)# b比值

df['label'] = df.c.shift(-20) / df.o.shift(-1) # 后n天收盘价除明天开盘价
df['label'] = np.round(df.label, 2)  # 改变小数点保留位数
print(df.label[0])
#y_labels = df.label.dropna().unique()
#print(y_labels)
#y_labels = sorted(np.int8(y_labels*100))
#print(y_labels)
#df.label = np.where(df.label>1, 1, 0)
#print(df.label)
#le = LabelEncoder()
#df['label'] = le.fit_transform(df.label.values)
#print(df.label)

df = df.dropna(axis=0)
#df.to_csv('tmp.csv')
X = df.loc[:,['ob','cb','hb','lb','bb']]
#print(X)
#X = df.loc[:,['bb']]
#X = X * 100
ss = StandardScaler()
#X = ss.fit_transform(X)



xs = ss.fit_transform(X)
dummies_label = pd.get_dummies(df.label)
y_labels = dummies_label.columns
#print(y_labels)
ys = dummies_label.values
#print(pd.concat([y, ys], axis=1))

#print(xs)
#print(ys)

outs = ys.shape[1]



# 构建数据完毕
# 开始深度学习




x = tf.placeholder(tf.float32, shape=(None, 5) )
W = tf.Variable( tf.zeros([5, 10 ]) )  # [10, 4]其实就是shape
b = tf.Variable( tf.zeros([10]) )

# 中间层1
x1 = tf.nn.sigmoid(tf.matmul(x,W) + b)
W1 = tf.Variable( tf.zeros([10, 10]) )
b1 = tf.Variable( tf.zeros([10]) )


# 中间层2
x2 = tf.nn.sigmoid(tf.matmul(x1,W1) + b1)
W2 = tf.Variable( tf.zeros([10, outs]) )
b2 = tf.Variable( tf.zeros([outs]) )

# 激励函数可用 sigmoid softmax 
#y = tf.matmul(x, W) + b  # 是不是没有用激励函数
y = tf.nn.sigmoid(tf.matmul(x2,W2) + b2)  # 
y_ = tf.placeholder(tf.float32, shape=[None, outs])

#cost = tf.reduce_mean( tf.pow((y_-y), 2) )  
cost = -tf.reduce_sum(y_*tf.log(y)) 
train_step = tf.train.GradientDescentOptimizer(1).minimize(cost)

init = tf.global_variables_initializer()



with tf.Session() as sess:
    sess.run(init)

    for i in range(999):
        idx = np.random.randint(10)  # 随机获取一个index
        feed_dict = {x: [xs[idx, :]],
                     y_: [ys[idx, :]]}
        sess.run( train_step, feed_dict=feed_dict )
    W_, b_ = sess.run([W,b])
    
#print(type(df.label))
#print(df.label)

with tf.Session() as sess:

    #a = np.arange(10)
    #np.random.shuffle(a)
    dff = pd.DataFrame(np.zeros([0,2]), columns=['y_true','y_pred'])
    #print(dff)
    for n in range(30,400):
        print(n)  
        y = tf.nn.softmax(tf.matmul(x, W_) + b_)
        feed_dict = {x: [xs[n, :]]}
        y_pred = sess.run(y, feed_dict=feed_dict)
        #print('n {}: '.format(n), y_pred.argmax())
        y_pred_value = y_labels[y_pred.argmax()]
        #print('n {}: '.format(df.label[n]), y_pred_value)

        y_true_value = df.label[n]
        y_pred_value = y_labels[y_pred.argmax()]
        dff.loc[n] = [y_true_value, y_pred_value]
        #print(type(y_pred), y_pred.shape, y_pred.argmax())
    # 这个检验方式是针对输出结果是哑变量的
    #correct_prediction = tf.equal(tf.argmax(y_pred,1), tf.argmax(y,1))
    #accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    #print(sess.run(accuracy, feed_dict=feed_dict))
#dff['y_true>1'] = dff.y_true > 1
#dff['y_true<1'] = dff.y_true < 1
#dff['y_pred>1'] = dff.y_pred > 1
#dff['y_pred<1'] = dff.y_pred < 1

dff['both>1'] = (dff.y_true > 1) & (dff.y_pred > 1)
dff['both<1'] = (dff.y_true < 1) & (dff.y_pred < 1)
dff['right'] =  dff['both>1'] | dff['both<1'] # 预测方向正确 
print(dff.right.sum()/ dff.shape[0], '预测方向正确率')
