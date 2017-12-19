'''
做一张表 记录run的结果,记录到csv中

字段

0 品种名 name
1 初始资金 （zj_init）
2 止损方式 （zs）    根据函数不同可能意义不同，有可能高低点，有可能atr
3 风险系数（f）
4 开仓间隔（jg）
5 允许最大仓位（maxcw）

（结果）
6 资金增长倍数
7 做多次数 
8 做空次数
9 日收益标准差
'''

import numpy as np
import pandas as pd
from d import run2

def record_run2(pinzhong):
    '''用各个参数跑run2
       然后把结果记录在csv文件中
       跑这个函数的时候，注意到d.py文件中改一下品种名pinzhong
    '''
    columns=['品种', 'zj_init', 'zs', 'f', '开仓间隔', 'maxcw', '资金增长倍数','做多次数', '做空次数', '日收益标准差'
        ]
    
    #run()
    rows = []
    #from d import df
    rows.append( run2(pinzhong, 2, 100000, f=0.02, maxcw=0.3, jiange=0) )
    rows.append( run2(pinzhong, 3, 100000, f=0.02, maxcw=0.3, jiange=0) )
    rows.append( run2(pinzhong, 4, 100000, f=0.02, maxcw=0.3, jiange=0) )
    rows.append( run2(pinzhong, 2, 100000, f=0.02, maxcw=0.3, jiange=0) )
    rows.append( run2(pinzhong, 2, 100000, f=0.03, maxcw=0.3, jiange=0) )
    rows.append( run2(pinzhong, 2, 100000, f=0.04, maxcw=0.3, jiange=0) )
    rows.append( run2(pinzhong, 2, 100000, f=0.02, maxcw=0.3, jiange=0) )
    rows.append( run2(pinzhong, 2, 100000, f=0.02, maxcw=0.4, jiange=0) )
    rows.append( run2(pinzhong, 2, 100000, f=0.02, maxcw=0.5, jiange=0) )
    rows.append( run2(pinzhong, 2, 100000, f=0.02, maxcw=0.3, jiange=0) )
    rows.append( run2(pinzhong, 2, 100000, f=0.02, maxcw=0.3, jiange=1) )
    rows.append( run2(pinzhong, 2, 100000, f=0.02, maxcw=0.3, jiange=2) )
    rows.append( run2(pinzhong, 2, 100000, f=0.02, maxcw=0.3, jiange=3) )

    df_results = pd.DataFrame(rows, columns=columns)
    #df_results = pd.DataFrame(rows)
    df_results.to_csv('record_run2.csv', mode='a')


if __name__ == '__main__':
    lst = ['rb', 'dy', 'c', 'm', 'sr', 'a', 'ma', 'ta']
    for pz in lst:
        record_run2(pz)