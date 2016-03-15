# encoding: utf-8
import sys
from itertools import combinations
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import util



class MoveStopLoss():
    def __init__(self, daima):
        df = pd.read_csv('data/%s.xls' % daima)
        util.strip_columns(df)
        self.df = df.loc[:, ['date', 'open', 'high', 'close', 'low', 'ma5', 'ma10', 'ma20', 'ma40', 'KDJ.K', 'KDJ.D', 'KDJ.J']]
        self.daima = daima


    @util.display_func_name
    def foo(self, days=5):
    	'''

    	'''
        df = self.df
        daima = self.daima
        df['low_pct'] = (pd.rolling_min(df.low, days) - df.open) / df.open
        df['high_pct'] = (pd.rolling_max(df.high, days) - df.open) / df.open

        func_name = sys._getframe().f_code.co_name
        self._to_result(df, days, func_name)        