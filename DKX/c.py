'''
用tips中 的收益计算方式
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
df['returns'] = df.c.pct_change()
df['ret_index'] = (1 + df['returns']).cumprod()
#df['ret_index'][0] = 1  # 每日收益
df.loc[0,'ret_index'] = 1
# 趋势判断，DKXb方向，1 向上   0向下  当天参照前两天
df['DKXb方向'] = np.where(df.b.shift(1)>df.b.shift(2), 1, 0) 
# 开仓条件
df = df.dropna(axis=0)
df['高于前两天高点'] = np.where(df.h > df.nhh, 1, None)   # 看当天 
df['低于前两天低点'] = np.where(df.l < df.nll, 1, None)
# 开仓  bk开多  sk开空
df['开仓'] = np.where((df['高于前两天高点'] == 1) & (df['DKXb方向']==1), 'bk', None)
df['开仓'] = np.where((df['低于前两天低点'] == 1) & (df['DKXb方向']==0), 'sk', df['开仓'] )
# 平仓 趋势反转 'bp' 平多  'sp' 平空
df['平仓'] = np.where((df.DKXb方向.shift(2) == 1) & (df.DKXb方向.shift(1) == 0), 'bp', None)
df['平仓'] = np.where((df.DKXb方向.shift(2) == 0) & (df.DKXb方向.shift(1) == 1), 'sp', df['平仓'])

#平仓的同时不反向开仓
df['开仓'] = np.where(df['平仓'].isnull(), df['开仓'], None)

# 多空持仓总手数
df['bk总手数'] = 0
df['sk总手数'] = 0

df['开仓手数'] = 1  # 目前简单处理，固定手数  后面加入资金管理

df['未持仓金额'] = 0
df.loc[0,'未持仓金额'] = 200000  # 初始化
df['b持仓金额'] = 0
df['s持仓金额'] = 0
bk_cnt = 0 # 多仓开仓总数量
sk_cnt = 0 # 开空仓开仓总数量


dates = pd.DatetimeIndex(df.date)
df.index = dates
df = df.drop('date', axis=1)
# 计算收益

droplist = ['vol', 'b', 'nhh', 'nll', 'returns', 'DKXb方向',  '高于前两天高点', '低于前两天低点']
df = df.drop(droplist, axis=1)
df.to_csv('tmp.csv')