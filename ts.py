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

def foo2():

    df = ts.get_hist_data('hs300')
    df = df.loc[:, ['open','close','ma5', 'ma10']]

    ma5_crossup_10 = (df.ma5.shift(-2) < df.ma10.shift(-2)) & (df.ma5.shift(-1) > df.ma10.shift(-1))
    ma5_crossdown_10 = (df.ma5.shift(-2) > df.ma10.shift(-2)) & (df.ma5.shift(-1) < df.ma10.shift(-1))
    df['ma5_up_10'] = np.where(ma5_crossup_10, True, None)
    df['ma5_down_10'] = np.where(ma5_crossdown_10, True, None)

    df['ma5_up_10_earning'] = np.where(df['ma5_up_10'], df.close.shift(2) - df.close, 0)
    df['ma5_down_10_earning'] = np.where(df['ma5_down_10'], df.close - df.close.shift(2) , 0)

    df.to_csv('files_tmp/foo2.csv')
    print df
    print '--------------------';
    print df['ma5_up_10_earning'].sum(), df['ma5_up_10'].count()
    print df['ma5_down_10_earning'].sum(),  df['ma5_down_10'].count()
    #dc = set(df['ma5_down_10_earning'].cumsum())
    #for n in dc:
    #    print n


    


#foo2()



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

    df.to_csv('files_tmp/tmp.csv')
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
    df.to_csv('files_tmp/tmp.csv')
    diff_count = len(df) - df['same_with_zuotian'].count()
    diff_pct = diff_count / float(len(df))
    print diff_pct


# rand()