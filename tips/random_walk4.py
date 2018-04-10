'''
随机的数列是否也符合顺势
'''
import numpy as np
import pandas as pd

draws = np.random.randint(0,2,99999)
steps = np.where(draws>0, 1, -1)
walk = steps.cumsum() # 

df = pd.DataFrame(walk, columns=['a']) # 代表价格

df['DKX'] = (20*df.a + 19*df.a.shift(1) + 18*df.a.shift(2) + 17*df.a.shift(3) + 
    16*df.a.shift(4) + 15*df.a.shift(5) + 14*df.a.shift(6) + 
    13*df.a.shift(7) + 12*df.a.shift(8) + 11*df.a.shift(9) + 
    10*df.a.shift(10) + 9*df.a.shift(11) + 8*df.a.shift(12) + 7*df.a.shift(13) + 
    6*df.a.shift(14) + 5*df.a.shift(15) + 4*df.a.shift(16) + 
    3*df.a.shift(17) + 2*df.a.shift(18) + 1*df.a.shift(19))/210

df['DKX方向'] = np.where(df.DKX.shift(1)>df.DKX.shift(2), '向上', '向下')
df['DKX方向'] = np.where(df.a.shift(1)>df.DKX.shift(1), '向上', '向下')
df = df.dropna(axis=0)


#df['损益'] = df.a.shift(3) - df.a
df['损益'] = np.where(df['DKX方向'] == '向上', df.a.shift(3) - df.a, 0)
print(df['损益'].sum())
print(df)