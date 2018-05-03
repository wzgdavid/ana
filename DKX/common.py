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

def get_nhh(df, n):
    '''前n天最高点（不包含当天）'''
    df['nhh{}'.format(n)] = df.h.shift(1).rolling(window=n, center=False).max() #- 2 # 提前几点
    return df

def get_nll(df, n):
    '''前n天最低点（不包含当天）'''
    df['nll{}'.format(n)] = df.l.shift(1).rolling(window=n, center=False).min() #+ 2 # 提前几点
    return df

def get_nhhzs(df, n):
    '''前n天最高点（不包含当天） 止损用'''
    df['nhh_zs'] = df.h.shift(1).rolling(window=n, center=False).max()
    return df

def get_nllzs(df, n):
    '''前n天最低点（不包含当天）止损用'''
    df['nll_zs'] = df.l.shift(1).rolling(window=n, center=False).min()
    return df
def get_nhhzs2(df, n):
    '''前n天最高点（不包含当天） 止损用'''
    df['nhh_zs2'] = df.h.shift(1).rolling(window=n, center=False).max()
    return df

def get_nllzs2(df, n):
    '''前n天最低点（不包含当天）止损用'''
    df['nll_zs2'] = df.l.shift(1).rolling(window=n, center=False).min()
    return df
    
def get_ma(df, n):
    df['ma{}'.format(n)] = df.c.rolling(window=n, center=False).mean()
    return df

def get_atr(df, n):
    '''TR : MAX( MAX( (HIGH-LOW),ABS(REF(CLOSE,1)-HIGH) ), ABS(REF(CLOSE,1)-LOW));文华的公式
    '''
    df['hl'] = df.h - df.l
    df['ch'] = abs(df.c.shift(1) - df.h)
    df['cl'] = abs(df.c.shift(1) - df.l)
    df['tr'] = df.loc[:, ['hl','ch', 'cl']].apply(lambda x: x.max(), axis=1)
    df['atr'] = df.tr.rolling(window=n, center=False).mean()
    df = df.drop(['hl', 'ch', 'cl', 'tr'], axis=1)
    return df

def result(df, params):
    '''
    df  run 处理后的df
    parms  run 函数 的参数
    '''
    #print(df['开仓'].value_counts())
    title = 'run2 zs={}  开仓间隔={} f={}  maxcw={}'.format(params['zs'], 
                                                            params['jiange'],
                                                            params['f'],
                                                            params['maxcw'])
    #plt.title(title)
    #plt.show()
    print('参数：', title)
    倍数 = round( (df.ix[-1, '总金额']/params['zj_init']),  1)
    print('资金增长倍数：{}'.format( 倍数 ))
    print('做多次数:{} 做空次数:{}'.format(params['做多次数'], params['做空次数']))
    
    df['returns'] = df['总金额'].pct_change() # 日收益变动
    df['ret_index'] = (1 + df['returns']).cumprod() # 资金曲线
    #df.ret_index.plot()
    # 最后700天的日收益标准差，越小表示越稳
    ret_std = round(df.returns[-700:].std(), 5)
    print('标准差：', ret_std)
    df['ret_index_log'] = np.log(df['ret_index'])

    # 定义顺序，参照totalrun.py的 文件起始的几行
    result_row = (
        params['pinzhong'],
        params['zj_init'], params['zs'], params['f'], params['jiange'],params['maxcw'],
        倍数, params['做多次数'], params['做空次数'], ret_std
        )
    # 显示曲线
    df.ret_index_log.plot()
    plt.title('收益倍数: '+title)
    #plt.show()
        
    #print(result_row)
    return result_row




#[(3542.0, 6)]
#[(3538, 6)]
#[(3105.0, 6)]
#[(3010.0, 6)]
#lst = [(3091.0, 6), (3221, 5)]
lst = [(3088.0, 6), (3192, 5), (3256.0, 5), (3295.0, 5), (3317.0, 4), (3377.0, 4), (3408.0, 3), (3393, 3), (3436.0, 3), (3553.0, 3), (3573.0, 2), (3619.0, 2), (3621.0, 2)]
#[(3512.0, 6), (3542.0, 5), (3558.0, 5), (3688.0, 5), (3702.0, 4), (3750.0, 4), (3843.0, 3)]
#[(3835.0, 6), (3875.0, 6), (3911.0, 5), (4000.0, 5)]
#[(3912.0, 6)]
#[(3927.0, 6), (4092.0, 5)]
def avg(lst):
    '''
    加权平均
    '''
    sum_ = 0
    quanzhong_sum = 0
    for price, quanzhong in lst:
        sum_ += price * quanzhong
        quanzhong_sum += quanzhong
    
    return int(sum_/quanzhong_sum)

if __name__ == '__main__':
    print(avg(lst))