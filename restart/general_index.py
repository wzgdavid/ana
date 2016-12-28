# encoding: utf-8
import sys
sys.path.append("..")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class General(object):
    def __init__(self, daima):
        #df = pd.read_csv('../data/%s.xls' % daima) # windows excel 制表符\t 影响读取
        df = pd.read_csv('../data/%s.csv' % daima)
        self.df = df
        self.daima = daima

    def foo(self):
        print self.df['o']


class GeneralIndex(General):
    def __init__(self, daima):
        super(GeneralIndex, self).__init__(daima)
        #self.sdjj()
    #def __new__(self, daima):
    #    super(General, self).__init__(daima)

    #def ma5(self, n):
    #    self.ma5 = 

    def sdjj(self):
        self.df['sdjj'] = (self.df['o'] + self.df['c'] + self.df['h'] + self.df['l']) / 4

if __name__ == '__main__':

    #g = General('rb')
    #g.foo()
    gi = GeneralIndex('rb')
    print gi.df['sdjj']
    #gi.sdjj