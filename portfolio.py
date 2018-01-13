'''
模拟组合对冲效果
同样的仓位两，没组合 对比 有组合
'''
import itertools
import random
import numpy as np
import pandas as pd

'''
实验模拟
单一品种每天有三种变化   +1   表示有比较大的正向（同持仓方向）变动
                         -1   表示有比较大的反向（逆持仓方向）变动
                         0    表示变动不大
每个品种都是这样变化

一天为一周期
'''
chg = 1,-1,0

'''
没组合
n份单一品种
'''
n = 10
# 每天的变动  +n  -n  0    就这三种
oneday_one = [a*n for a in chg]   # 单一品种持仓 一天的变化可能

df = pd.DataFrame(index=range(99999), columns=['init'])
df['one'] = df.init.apply(lambda a:random.choice(oneday_one)) # 生成一列1000天  每天变化的数列
print('单个品种的标准差')
print(df.one.std())
#print(df.one.sum()) 


'''
有组合
n种不同的品种各一份
'''
print(list(itertools.combinations(chg, 2)))
#oneday_n                      # 品种组合持仓 一天的变化可能

for x in range(n):
    df['n'+str(x)] = df.init.apply(lambda a:random.choice(chg))

# 计算n0加到  n几
bb = [] 
for x in range(n):
    bb.append('df.n' + str(x))

df['n'] = eval('+'.join(bb))

#df['n'] = df
print('n个品种的标准差')
print(df.n.std())
#print(df.n.sum())


'''
单个品种的标准差
8.16647355138
[(1, -1), (1, 0), (-1, 0)]
n个品种的标准差
2.58414063061

可看到同样的仓位，如果n个品种的话，波动比单个品种小很多
'''
