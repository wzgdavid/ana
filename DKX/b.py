'''
20171110
python36
基于report/DKX_MA_趋势概率.ipynb策略
规则说明以多为例，空则反之
0 趋势定义：DKXb线方向向上
1 开仓止损：前一天最低点
2 平仓：趋势反转
3 资金管理：单次允许最大亏损f%
4 开仓方式：
5 想到再写


先写出测试的资金曲线
再根据不同参数，画曲线，看最优参数
'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from common import get_DKX, get_nhh, get_nll

df = pd.read_csv(r'..\data\rb\zs.csv')

df = get_DKX(df)
df = get_nhh(df, 2)
df = get_nll(df, 2)
print(df.tail())
# 趋势判断，DKXb方向，1 向上   0向下  当天参照前两天
df['DKXb方向'] = np.where(df.b.shift(1)>df.b.shift(2), 1, 0) 
# 开仓条件
df['高于前两天高点'] = np.where(df.h > df.nhh, 1, None)   # 看当天 
df['低于前两天低点'] = np.where(df.l < df.nll, 1, None)
# 开仓  bk开多  sk开空
df['开仓'] = np.where((df['高于前两天高点'] == 1) & (df['DKXb方向']==1), 'bk', None)
df['开仓'] = np.where((df['低于前两天低点'] == 1) & (df['DKXb方向']==0), 'sk', df['开仓'] )

df['多开仓止损'] = np.where(df.开仓=='bk', df.l.shift(1),None)
df['空开仓止损'] = np.where(df.开仓=='sk', df.h.shift(1),None)
# 平仓 趋势反转 'bp' 平多  'sp' 平空
df['平仓'] = np.where((df.DKXb方向.shift(2) == 1) & (df.DKXb方向.shift(1) == 0), 'bp', None)
df['平仓'] = np.where((df.DKXb方向.shift(2) == 0) & (df.DKXb方向.shift(1) == 1), 'sp', df['平仓'])
'''
删选出一部分试验 ，否则太慢， 注意以后要去掉
'''
#df = df.head(200) # 删选出一部分试验 ，否则太慢， 注意以后要去掉
for idx in range(df.shape[0]): # 
    pass
df.to_csv('tmpb.csv')