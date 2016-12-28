# encoding: utf-8
import sys
sys.path.append("..")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from general_index import General, GeneralIndex

'''
四点均价  开收盘价，最高价，最低价
'''

class Sdjj(GeneralIndex):
    def __init__(self, daima):
        super(Sdjj, self).__init__(daima)
        self.sdjj()

    def foo(self):
        print self.df['o']
        pass


if __name__ == '__main__':
    s = Sdjj('rb')
    #s.foo()
    print s.df['sdjj']
    #df = pd.read_csv('../data/%s.xls' % 'RBL9')
    #print df