import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# 构建指标
def get_DKX(df, n=10):
    df['a'] = (df.c * 3 + df.l + df.o + df.h)/6
    #df['b'] = (20*df.a + 19*df.a.shift(1) + 18*df.a.shift(2) + 17*df.a.shift(3) + 
    #    16*df.a.shift(4) + 15*df.a.shift(5) + 14*df.a.shift(6) + 
    #    13*df.a.shift(7) + 12*df.a.shift(8) + 11*df.a.shift(9) + 
    #    10*df.a.shift(10) + 9*df.a.shift(11) + 8*df.a.shift(12) + 7*df.a.shift(13) + 
    #    6*df.a.shift(14) + 5*df.a.shift(15) + 4*df.a.shift(16) + 
    #    3*df.a.shift(17) + 2*df.a.shift(18) + 1*df.a.shift(19))/210
    sum_ = '+'.join(['{}*df.a.shift({})'.format(20-i, i) for i in range(0, 20)]) 
    eval_str = '({})/210'.format(sum_)
    df['b'] = eval(eval_str)
    df['d'] = df.b.rolling(n).mean()
    return df.drop(['a'], axis=1)


def result(df,rates):
    #print('-----------------------------------')
    df = pd.DataFrame(rates, columns=['rates'])
    df['ret_index'] = (df['rates']).cumprod() # 曲线
    #print(df.describe())

    df['每次盈亏'] = np.where(df.rates>1, '盈利', '亏损')
    win_loss = df['每次盈亏'].value_counts()
    wl_pct = win_loss['盈利'] / df.shape[0]
    #print(win_loss)

    print('盈利比例{:.2f}'.format(wl_pct))
    final_return = df.ix[df.shape[0]-1, 'ret_index']
    print('最后收益{}'.format(final_return))
    max_loss = 1 - df.rates.min()
    print('单次最大亏损{}'.format(max_loss))
    print('交易次数{}'.format(len(rates)))
    df.to_csv('tmp.csv')