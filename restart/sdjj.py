# encoding: utf-8
import sys
sys.path.append("..")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from general_index import General, GeneralIndex
from copy import deepcopy


class Sdjj(GeneralIndex):
    def __init__(self, daima):
        super(Sdjj, self).__init__(daima)
        #self.get_ma(5,10,20)
        self.get_sdjj()

    def foo(self):
        print self.df['o']
        pass

    def tupo_sdhsdl(self, n=10):
        '''四点均线突破前n天最高开多，突破前n天最低开空，
        
        暂时还想不出移动止损怎么写，先写不带移动止损的，用信号平仓的策略
        # 暂时结果 rb 11(28008), 12(28080.25) 天最好
        '''
        self.get_nsdl(n)
        self.get_nsdh(n)
        df = deepcopy(self.df) 
        #df['tupo_sdh'] = df.sdjj.shift(1) < df.nsdh.shift(1) & df.sdjj > df.nsdh 
        df['tmp1'] = df.sdjj.shift(1) < df.nsdh.shift(1)
        df['tmp2'] = df.sdjj > df.nsdh
        df['tupo_sdh'] = df.tmp1 & df.tmp2  #今天的四点均价突破前n天的四点均价高点
        df['bksk'] = np.where(df['tupo_sdh'], 'bk' , None)
        #df.loc[: ,'bkcnt'] = 0
        #df['bkcnt'] = np.where(df['tupo_sdh'], df.bkcnt.shift(1)+1 , df.bkcnt.shift(2))

        df['tmp1'] = df.sdjj.shift(1) > df.nsdl.shift(1)
        df['tmp2'] = df.sdjj < df.nsdl
        df['tupo_sdl'] = df.tmp1 & df.tmp2
        # bk表示买开仓或买平仓，sk相反
        df['bksk'] = np.where(df['tupo_sdl'], 'sk' , df['bksk'])

        self.run(df)

    def qian_n_ri(self, n=10):
        '''比前n日高，买开仓，反之 (连着几天取这几天的第一天)'''
        df = deepcopy(self.df) 
        df['tmp1'] = df.sdjj > df.sdjj.shift(n)
        df['tmp2'] = df.sdjj.shift(1) < df.sdjj.shift(n+1)
        df['higher'] = df.tmp1 & df.tmp2 # 第一次比前第n天高
        df['tmp1'] = df.sdjj < df.sdjj.shift(n)
        df['tmp2'] = df.sdjj.shift(1) > df.sdjj.shift(n+1)
        df['lower'] = df.tmp1 & df.tmp2 # 第一次比前第n天低
          
        df['bksk'] = np.where(df['higher'], 'bk' , None)
        # bk表示买开仓或买平仓，sk相反
        df['bksk'] = np.where(df['lower'], 'sk' , df['bksk'])
        df.to_csv('tmp.csv')
        #print df.loc[:, ['date','sdjj', 'higher']]
        self.run(df)


  

if __name__ == '__main__':
    s = Sdjj('rb')
    #s.foo()
    
    s.tupo_sdhsdl(12) # rb 11(28008), 12(28080.25) 天最好
    #s.qian_n_ri()
    #print s.df.index
    #print s.df.loc[:, ['date','sdjj', 'tupo_sdl', 'tupo_sdh']]
    #s.df.to_csv('tmp.csv')  
    #df = pd.read_csv('../data/%s.xls' % 'RBL9')
    #print df