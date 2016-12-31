# encoding: utf-8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from general_index import General, GeneralIndex, rangerun, rangerun3
from copy import deepcopy

class Tongji(GeneralIndex):
    def __init__(self, daima):
        super(Tongji, self).__init__(daima)
        
        self.get_sdjj()


    def ma_updown_yinyangxian(self, n):
        self.get_ma(n)
        df = deepcopy(self.df)
        ma = 'ma%s' % n
        #df['maup'] = df[ma].shift(1) > df[ma].shift(2) # 看昨天和前天，然后统计今天
        #上面的只能写true false， 下面这句能自己制定
        df['maup'] = np.where(df[ma].shift(1) > df[ma].shift(2), 1 , None)
        df['maupsum'] = df.maup.sum()
        df['madown'] = np.where(df[ma].shift(1) < df[ma].shift(2), 1 , None)
        df['madownsum'] = df.madown.sum()
        df['yang'] = np.where(df.c > df.o, 1 , None)                   # 统计今天
        df['yin'] = np.where(df.c < df.o, 1 , None) 
        df['maup_yang'] = np.where(df.maup & df.yang, 1 , None)
        df['maup_yang_sum'] = df.maup_yang.sum()
        df['madown_yin'] = np.where(df.madown & df.yin,1 ,None)
        df['madown_yin_sum'] = df.madown_yin.sum()

        df.to_csv('tmp.csv')

if __name__ == '__main__':
    t = Tongji('rb')
    t.ma_updown_yinyangxian(5)