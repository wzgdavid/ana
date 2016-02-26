# encoding: utf-8
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tushare as ts
import zhibiao as zb

# ts.set_token('390c325056c8c4524d0d7c048c5907e079e45f6e2f1f2b1b6dc5e9bc0f297136')
# fd = ts.Future()
# df = fd.Futu(exchangeCD='CCFX', field='secShortName,contractObject,minChgPriceNum,lastTradeDate,deliMethod')

def foo():

    df = ts.get_hist_data('hs300', start='2016-01-01')
    df = df.loc[:, ['open', 'high', 'close', 'low', 'ma5', 'ma10', 'ma20']]
    df['k_crossup_ma5'] = df.open > df.ma5
    #df['open_shift_1'] = df['open'].shift(1)
    df.open
    print df

def foo2(daima, ma1='ma5', ma2='ma10', days=5):

    df = ts.get_hist_data(daima)
    df = df.loc[:, ['open','close','ma5', 'ma10', 'ma20']]

    ma5_crossup_10 = (df[ma1].shift(-2) < df[ma2].shift(-2)) & (df[ma1].shift(-1) > df[ma2].shift(-1))
    #ma5_crossdown_10 = (df.ma5.shift(-2) > df.ma10.shift(-2)) & (df.ma5.shift(-1) < df.ma10.shift(-1))
    
    df['ma5_up_10'] = np.where(ma5_crossup_10, True, None)
    #df['ma5_down_10'] = np.where(ma5_crossdown_10, True, None)

    df['ma5_up_10_earning'] = np.where(df['ma5_up_10'], df.close.shift(days) - df.close, 0)
    #df['ma5_down_10_earning'] = np.where(df['ma5_down_10'], df.close - df.close.shift(2) , 0)

    #df.to_csv('files_tmp/foo2.csv')

    #print df['ma5_up_10_earning'].sum(), df['ma5_up_10'].count()
    #print df['ma5_down_10_earning'].sum(),  df['ma5_down_10'].count()
    return df['ma5_up_10_earning'].sum()

#print foo2('hs300', days=7)

def run_foo2():
    zhengshouyi_count = 0
    allcount = 0
    allrange = range(600000, 600999) + range(300000, 300555)

    for daima in allrange:
        #print  daima
        try:
            rtn = foo2(str(daima), ma1='ma10', ma2='ma20' , days=10)
        except AttributeError:
            continue
        if rtn > 0:
            zhengshouyi_count += 1
        allcount += 1
    print zhengshouyi_count, allcount, 'run_foo2 end'
run_foo2()
    






def qfq():
    ''''''
    df = ts.get_h_data('000584')  #
    #print hasattr(df, 'ma5')
    df = df.loc[:, ['open','close','ma5', 'ma10']]

    ma5_crossup_10 = (df.ma5.shift(-2) < df.ma10.shift(-2)) & (df.ma5.shift(-1) > df.ma10.shift(-1))
    ma5_crossdown_10 = (df.ma5.shift(-2) > df.ma10.shift(-2)) & (df.ma5.shift(-1) < df.ma10.shift(-1))
    df['ma5_up_10'] = np.where(ma5_crossup_10, 1, '')
    df['ma5_down_10'] = np.where(ma5_crossdown_10, 0, '')
    #df['open_shift_1'] = df['open'].shift(1)
    #df['test'] = np.where(df.open>df.close,'1','0')
    #df['test2'] = df.open>df.close
    df['ma5_up_10_earning'] = np.where(df['ma5_up_10']=='1', df.close.shift(20) - df.close, '')
    df['ma5_down_10_earning'] = np.where(df['ma5_down_10']=='0', df.close - df.close.shift(20) , '')
    #df['ma5_up_10_earning'] = df.close-df.close.shift(-10)

    df.to_csv('files_tmp/qfq.csv')
    #print df

#qfq()


def rand():

    df = ts.get_hist_data('200007')
    df = df.loc[:, ['open','close','high', 'low']]
    #print df.open.shift(-1) > df.close.shift(-1)
    #print df.open > df.close
    same_down = (df.open.shift(-1) > df.close.shift(-1)) & (df.open > df.close)
    same_up = (df.open.shift(-1) < df.close.shift(-1)) & (df.open < df.close)
    df['same_with_zuotian'] = np.where(same_down | same_up, True, None)
    #print df
    df.to_csv('files_tmp/rand.csv')
    diff_count = len(df) - df['same_with_zuotian'].count()
    diff_pct = diff_count / float(len(df))
    print diff_pct


# rand()

def foo3(daima, ma='ma5', days=5):
    '''只要大于ma 买进 看n天后收益'''
    df = ts.get_hist_data(daima)
    df = df.loc[:, ['close','ma5', 'ma10', 'ma20']]
    #df['gt_ma'] = df.close > df[ma]
    
    df['earning'] = np.where(df.close > df[ma], df.close.shift(days) - df.close, 0)
    #df['earning2'] = np.where(df.close < df[ma], df.close.shift(days) - df.close, 0)
    #print df['earning'].sum()
    return df['earning'].sum()
    #df.to_csv('files_tmp/foo3.csv')
#foo3('hs300')
#print foo3('hs300')
#foo3('002004')

def run_foo3():
    zhengshouyi_count = 0
    allcount = 0
    allrange = range(600000, 600999) + range(300000, 300555)

    for daima in allrange:
        print daima
        try:
            rtn = foo3(str(daima), ma='ma10', days=10)
        except AttributeError:
            continue
        if rtn > 0:
            zhengshouyi_count += 1
        allcount += 1
    print zhengshouyi_count, allcount, 'run_foo3 end'
#run_foo3()