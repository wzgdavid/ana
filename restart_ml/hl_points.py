'''找出高低点'''

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from tool import get_atr, get_ma

plt.rcParams['font.sans-serif'] = ['SimHei'] # 正常显示中文
hy = 'rb' # rb ta m a ma c jd dy cs
df = pd.read_csv(r'..\data\{}.csv'.format(hy))

df['h shift 1'] = df.h.shift(1)
df['h shift -1'] = df.h.shift(-1)
df['h higher than last 1'] = np.where(df.h - df.h.shift(1) > 0, 1, None)
df['h higher than next 1'] = np.where(df.h - df.h.shift(-1) > 0, 1, None)
df['h lower than last 1'] = np.where(df.h - df.h.shift(1) < 0, 1, None)
df['h lower than next 1'] = np.where(df.h - df.h.shift(-1) < 0, 1, None)

df['l shift 1'] = df.l.shift(1)
df['l shift -1'] = df.l.shift(-1)
df['l higher than last 1'] = np.where(df.l - df['l shift 1'] > 0, 1, None)
df['l higher than next 1'] = np.where(df.l - df['l shift -1'] > 0, 1, None)
df['l lower than last 1'] = np.where(df.l - df['l shift 1'] < 0, 1, None)
df['l lower than next 1'] = np.where(df.l - df['l shift -1'] < 0, 1, None)

df['short_h_high'] = np.where(df['h higher than last 1'] & df['h higher than next 1'], 1, None)
df['short_l_high'] = np.where(df['l higher than last 1'] & df['l higher than next 1'], 1, None)
df['short_high'] = np.where( df.short_h_high & df.short_l_high ,1, None)

df['short_h_low'] = np.where(df['h lower than last 1'] & df['h lower than next 1'], 1, None)
df['short_l_low'] = np.where(df['l lower than last 1'] & df['l lower than next 1'], 1, None)
df['short_low'] = np.where( df.short_h_low & df.short_l_low ,1, None)
中间过程 = [
    'h shift 1', 'h shift -1', 'h higher than last 1',
    'h higher than next 1', 'l shift 1', 'l shift -1',
    'l higher than last 1', 'l higher than next 1',
    'h lower than last 1', 'h lower than next 1',
    'l lower than last 1', 'l lower than next 1',
    'short_h_high', 'short_l_high',
    'short_h_low', 'short_l_low',
]


df = df.drop(中间过程, axis=1)

df = df[(df.short_high==1) | (df.short_low==1)]
print(df.head(200))