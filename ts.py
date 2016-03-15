# encoding: utf-8
import sys
from itertools import combinations
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tushare as ts
import util

# tushare 的数据不准 节假日会多一天多余的数据
'''
看n天后收益
'''

@util.display_func_name
def foo(daima, days=5, scope=0.05):
    '''没条件  买进 看n天后收益
    作为参考基准,结果比这个差的就不用看了
    '''
    df = pd.read_csv('data/%s.xls' % daima)
    util.strip_columns(df)
    df = df.loc[:, ['date', 'open', 'close', 'low']]

    df['earning'] = df.open.shift(days) - df.open
    df['stoploss_point'] = df.open * (1-scope)
    rolling_low = pd.rolling_min(df.low, days)
    df['stoploss'] = df.stoploss_point - df.open

    df['earning_with_stoploss'] = np.where(rolling_low > df.stoploss_point, df.earning, df.stoploss)
    
    func_name = sys._getframe().f_code.co_name
    df = df.loc[days: , :]  # 因为近期的看不到n天后的数据，所以没收益，因此不计算
    
    #df.to_csv('files_tmp/%s_%s.csv' % (func_name, daima))  # 以函数名作为文件名保存

    df = df.where(df.earning != 0) # for count
    summ = df.earning.sum()
    summ2 = df.earning_with_stoploss.sum()

    count = df.earning.count() # count is same
    #count2 = df.earning_with_stoploss.count()

    average_earnings =  summ / count
    average_earnings2 =  summ2 / count #
   
    print average_earnings, average_earnings2
    print summ, summ2
    print count
    
    #return summ, average_earnings, summ2, average_earnings2, count
    return summ2 / count



@util.display_func_name
def foo3(daima, ma='ma5', days=5, scope=0.05):
    '''只要前一天整K大于ma 买进 看n天后收益
    '''

    df = pd.read_csv('data/%s.xls' % daima)
    util.strip_columns(df)
    df = df.loc[:, ['date', 'open', 'close', 'low', 'ma5', 'ma10', 'ma20']]



    # yesterday greater than ma
    df['gt_ma'] = df.low.shift(-1) > df[ma].shift(-1)
    df['earning'] = np.where(df['gt_ma'], df.close.shift(days) - df.open, 0)
    #df['earning2'] = np.where(df.close < df[ma], df.close.shift(days) - df.close, 0)
    #print df['earning'].sum()
    df['stoploss_point'] = df.open * (1-scope)
    rolling_low = pd.rolling_min(df.low, days)
    df['stoploss'] = np.where(df['gt_ma'], df.stoploss_point - df.open , 0)

    df['earning_with_stoploss'] = np.where(rolling_low > df.stoploss_point, df.earning, df.stoploss)
    
    func_name = sys._getframe().f_code.co_name
    df = df.loc[days: , :]  # 因为近期的看不到n天后的数据，所以没收益，因此不计算
    
    df.to_csv('files_tmp/%s_%s.csv' % (func_name, daima))  # 以函数名作为文件名保存

    df = df.where(df.earning != 0) # for count
    summ = df.earning.sum()
    summ2 = df.earning_with_stoploss.sum()

    count = df.earning.count() # count is same
    count2 = df.earning_with_stoploss.count()

    average_earnings =  summ / count
    average_earnings2 =  summ2 / count #

    print average_earnings, average_earnings2
    print summ, summ2
    print count, count2
    
    return summ, average_earnings, summ2, average_earnings2, count
#print foo3('999999', ma='ma20', days=250, scope=0.05)



@util.display_func_name
def run_foo3(daima):
    '''
    nicest result
        hs300 ma20  0.14--0.17 days 250--330
        999999 ma20  0.11 -- 0.15  240--280

    foo3 params : the best ma is ma20
                  best days is about 300 

    '''
    scopes = np.arange(0.04, 0.2, 0.01)
    hold_days = range(150,350,10)
    mas = ['ma5', 'ma10', 'ma20']

    df_scope = []
    df_day = []
    df_ma = []

    df_sum = []
    df_sum2 = []
    df_count = []
    df_avge = []
    df_avge2 = []
    for scope in scopes:
        for day in hold_days:
            for ma in mas:
                #print scope
                rtn = foo3(daima, ma=ma, days=day, scope=scope)
                df_scope.append(scope)
                df_day.append(day)
                df_ma.append(ma)
                df_sum.append(rtn[0])
                df_avge.append(rtn[1])
                df_sum2.append(rtn[2])
                df_avge2.append(rtn[3])
                df_count.append(rtn[4])
    df = pd.DataFrame({
        'scope': df_scope,
        'days':df_day,
        'ma':df_ma,
        'sum':df_sum,
        'avge':df_avge,
        'sum2':df_sum2,
        'avge2':df_avge2,
        'count':df_count,


        })
    df.to_csv('files_tmp/run_foo3_%s.csv' % daima)
#run_foo3('999999')

@util.display_func_name
def foo3b(daima, ma='ma5', days=5):
    '''只要前一天整K小于ma 买进 看n天后收益
    想验证的结果是  收益应该是负的
    '''
    df = pd.read_csv('data/%s.xls' % daima)
    util.strip_columns(df)
    df = df.loc[:, ['date', 'open', 'close', 'high', 'ma5', 'ma10', 'ma20']]

    # yesterday less than ma
    df['lt_ma'] = df.high.shift(-1) < df[ma].shift(-1)
    df['earning'] = np.where(df['lt_ma'], df.close.shift(days) - df.open, 0)
    
    func_name = sys._getframe().f_code.co_name
    df = df.loc[days: , :]  # 因为近期的看不到n天后的数据，所以没收益，因此不计算
    df.to_csv('files_tmp/%s.csv' % func_name)  # 以函数名作为文件名保存

    df = df.where(df.earning != 0)
    summ = df.earning.sum()
    
    count = df.earning.count() # count is same

    average_earnings =  summ / count

    print average_earnings
    print summ
    print count
    
#print foo3('zxb', ma='ma10', days=99, scope=0.15)

#foo('hs300', days=150, scope=0.15)

#foo3('hs300', ma='ma20', days=150, scope=0.15)

#foo3b('zxb', ma='ma20', days=150)


@util.display_func_name
def maup(daima, ma='ma5', days=5, scope=0.05):
    '''昨天ma大于qian天ma 买进 看n天后收益
    '''
    df = pd.read_csv('data/%s.xls' % daima)
    util.strip_columns(df)
    df = df.loc[:, ['date', 'open', 'low', 'close', 'ma5', 'ma10', 'ma20']]

    df['maup'] = df[ma].shift(-1) > df[ma].shift(-2)
    df['earning'] = np.where(df['maup'], df.close.shift(days) - df.open, 0)

    df['stoploss_point'] = df.open * (1-scope)
    rolling_low = pd.rolling_min(df.low, days)
    df['stoploss'] = np.where(df['maup'], df.stoploss_point - df.open , 0)

    df['earning_with_stoploss'] = np.where(rolling_low > df.stoploss_point, df.earning, df.stoploss)
    
    func_name = sys._getframe().f_code.co_name
    df = df.loc[days: , :]  # 因为近期的看不到n天后的数据，所以没收益，因此不计算
    
    df.to_csv('files_tmp/%s_%s.csv' % (func_name, daima))  # 以函数名作为文件名保存

    df = df.where(df.earning != 0) # for count
    summ = df.earning.sum()
    summ2 = df.earning_with_stoploss.sum()

    count = df.earning.count() # count is same
    count2 = df.earning_with_stoploss.count()

    average_earnings =  summ / count
    average_earnings2 =  summ2 / count #

    print average_earnings, average_earnings2
    print summ, summ2
    print count, count2
    
    return summ, average_earnings, summ2, average_earnings2, count


@util.display_func_name
def foo3_maup(daima, ma='ma5', days=5, scope=0.05):
    '''前一天整K大于ma,and 今天ma大于昨天ma  买进 看n天后收益
    '''
    df = pd.read_csv('data/%s.xls' % daima)
    util.strip_columns(df)
    df = df.loc[:, ['date', 'open', 'close', 'low', 'ma5', 'ma10', 'ma20']]

    # yesterday greater than ma
    df['gt_ma'] = df.low.shift(-1) > df[ma].shift(-1)
    df['maup'] = df[ma].shift(-1) > df[ma].shift(-2)
    df['gtma_and_maup'] = df.gt_ma & df.maup
    df['earning'] = np.where(df['gtma_and_maup'], df.close.shift(days) - df.open, 0)

    df['stoploss_point'] = df.open * (1-scope)
    rolling_low = pd.rolling_min(df.low, days)
    df['stoploss'] = np.where(df['gtma_and_maup'], df.stoploss_point - df.open , 0)

    df['earning_with_stoploss'] = np.where(rolling_low > df.stoploss_point, df.earning, df.stoploss)
    
    func_name = sys._getframe().f_code.co_name
    df = df.loc[days: , :]  # 因为近期的看不到n天后的数据，所以没收益，因此不计算
    
    df.to_csv('files_tmp/%s_%s.csv' % (func_name, daima))  # 以函数名作为文件名保存

    df = df.where(df.earning != 0) # for count
    summ = df.earning.sum()
    summ2 = df.earning_with_stoploss.sum()

    count = df.earning.count() # count is same
    count2 = df.earning_with_stoploss.count()

    average_earnings =  summ / count
    average_earnings2 =  summ2 / count #

    print average_earnings, average_earnings2
    print summ, summ2
    print count, count2
    
    return summ, average_earnings, summ2, average_earnings2, count
#ma='ma20'
#days=300
#scope=0.1
#foo3('hs300', ma=ma, days=days, scope=scope)
#foo3_maup('hs300', ma=ma, days=days, scope=scope)
#maup('hs300', ma=ma, days=days, scope=scope)


@util.display_func_name
def foo3_madown(daima, ma='ma5', days=5, scope=0.05):
    df = pd.read_csv('data/%s.xls' % daima)
    util.strip_columns(df)
    df = df.loc[:, ['date', 'open', 'close', 'low', 'ma5', 'ma10', 'ma20']]

    # yesterday greater than ma
    df['gt_ma'] = df.low.shift(-1) > df[ma].shift(-1)
    df['madown'] = df[ma].shift(-1) < df[ma].shift(-2)
    df['both'] = df.gt_ma & df.madown
    df['earning'] = np.where(df['both'], df.close.shift(days) - df.open, 0)

    df['stoploss_point'] = df.open * (1-scope)
    rolling_low = pd.rolling_min(df.low, days)
    df['stoploss'] = np.where(df['both'], df.stoploss_point - df.open , 0)

    df['earning_with_stoploss'] = np.where(rolling_low > df.stoploss_point, df.earning, df.stoploss)
    
    func_name = sys._getframe().f_code.co_name
    df = df.loc[days: , :]  # 因为近期的看不到n天后的数据，所以没收益，因此不计算
    
    df.to_csv('files_tmp/%s_%s.csv' % (func_name, daima))  # 以函数名作为文件名保存

    df = df.where(df.earning != 0) # for count
    summ = df.earning.sum()
    summ2 = df.earning_with_stoploss.sum()

    count = df.earning.count() # count is same
    count2 = df.earning_with_stoploss.count()

    average_earnings =  summ / count
    average_earnings2 =  summ2 / count #

    print average_earnings, average_earnings2
    print summ, summ2
    print count, count2
    
    return summ, average_earnings, summ2, average_earnings2, count



@util.display_func_name
def foo3b_maup(daima, ma='ma5', days=5, scope=0.05):
    '''前一天整K小于ma,and 昨天ma大于前天ma  买进 看n天后收益
    '''
    df = pd.read_csv('data/%s.xls' % daima)
    util.strip_columns(df)
    df = df.loc[:, ['date', 'open', 'close','low', 'high', 'ma5', 'ma10', 'ma20']]

    # yesterday less than ma
    df['lt_ma'] = df.high.shift(-1) < df[ma].shift(-1)
    df['maup'] = df[ma].shift(-1) > df[ma].shift(-2)
    df['ltma_and_maup'] = df.lt_ma & df.maup
    df['earning'] = np.where(df['ltma_and_maup'], df.close.shift(days) - df.open, 0)

    df['stoploss_point'] = df.open * (1-scope)
    rolling_low = pd.rolling_min(df.low, days)
    df['stoploss'] = np.where(df['ltma_and_maup'], df.stoploss_point - df.open , 0)

    df['earning_with_stoploss'] = np.where(rolling_low > df.stoploss_point, df.earning, df.stoploss)
    
    func_name = sys._getframe().f_code.co_name
    df = df.loc[days: , :]  # 因为近期的看不到n天后的数据，所以没收益，因此不计算
    
    df.to_csv('files_tmp/%s_%s.csv' % (func_name, daima))  # 以函数名作为文件名保存

    df = df.where(df.earning != 0) # for count
    summ = df.earning.sum()
    summ2 = df.earning_with_stoploss.sum()

    count = df.earning.count() # count is same
    count2 = df.earning_with_stoploss.count()

    average_earnings =  summ / count
    average_earnings2 =  summ2 / count #

    print average_earnings, average_earnings2
    print summ, summ2
    print count, count2
    
    #return summ, average_earnings, summ2, average_earnings2, count
#ma='ma20'
#days=300
#scope=0.1
#foo3('hs300', ma=ma, days=days, scope=scope)
#foo3b_maup('hs300', ma=ma, days=days, scope=scope)
#foo3_maup('hs300', ma=ma, days=days, scope=scope)
#maup('hs300', ma=ma, days=days, scope=scope)


@util.display_func_name
def ma_crossup(daima, scope=0.05, days=5, ma1='ma5', ma2='ma10'):
    df = pd.read_csv('data/%s.xls' % daima)
    util.strip_columns(df)
    df = df.loc[:, ['date', 'open', 'close','low', 'ma5', 'ma10', 'ma20']]

    df['ma_crossup'] = (df[ma1].shift(-2) < df[ma2].shift(-2)) & (df[ma1].shift(-1) > df[ma2].shift(-1))
    
    df['earning'] = np.where(df.ma_crossup, df.close.shift(days) - df.open, 0)

    df['stoploss_point'] = df.open * (1-scope)
    rolling_low = pd.rolling_min(df.low, days)
    df['stoploss'] = np.where(df['ma_crossup'], df.stoploss_point - df.open , 0)

    df['earning_with_stoploss'] = np.where(rolling_low > df.stoploss_point, df.earning, df.stoploss)
    
    func_name = sys._getframe().f_code.co_name
    df = df.loc[days: , :]  # 因为近期的看不到n天后的数据，所以没收益，因此不计算
    
    df.to_csv('files_tmp/%s_%s.csv' % (func_name, daima))  # 以函数名作为文件名保存

    df = df.where(df.earning != 0) # for count
    summ = df.earning.sum()
    summ2 = df.earning_with_stoploss.sum()

    count = df.earning.count() # count is same
    count2 = df.earning_with_stoploss.count()

    average_earnings =  summ / count
    average_earnings2 =  summ2 / count #

    print average_earnings, average_earnings2
    print summ, summ2
    print count, count2
    
    #return summ, average_earnings, summ2, average_earnings2, count


#days=200
#scope=0.1
#ma_crossup('999999', scope=scope, days=days, ma1='ma5', ma2='ma10')
#foo3_maup('999999', ma='ma20', days=days, scope=scope)


@util.display_func_name
def foo5(daima, scope=0.05, hold_days=5, ma1='ma5', ma2='ma10'):
    '''
    ma cross up
    old version 
    '''
    df = pd.read_csv('data/%s.xls' % daima)
    util.strip_columns(df)
    df = df.loc[ :, ['date', 'open', 'close', 'high', 'low', 'ma5', 'ma10', 'ma20'] ]
    df['rolling_low'] = pd.rolling_min(df.low, hold_days)
    df['stop_loss'] = df.open * (1- scope)
    # df['earnings'] = if rolling_low > stop_loss   ?  open.shift(hold_days) - df.open : df.stop_loss - df.open
    # df['logic'] = np.where(df['AAA'] > 5,'high','low')
    df['earnings'] = np.where(df.rolling_low > df.stop_loss , df.close.shift(hold_days) - df.open ,df.stop_loss - df.open)
   
    ma5_crossup_10 = (df[ma1].shift(-2) < df[ma2].shift(-2)) & (df[ma1].shift(-1) > df[ma2].shift(-1))
    #ma5_crossdown_10 = (df.ma5.shift(-2) > df.ma10.shift(-2)) & (df.ma5.shift(-1) < df.ma10.shift(-1))
    
    df['ma5_up_10'] = np.where(ma5_crossup_10, True, None)
    df['ma_cross_earnings'] = df.earnings * df.ma5_up_10
    df.to_csv('files_tmp/foo5.csv')
    #summ = df.ma_cross_earnings.shift(hold_days * -1 + 1).sum() # 不计算没有rolling_low的行
    #count = df.ma_cross_earnings.shift(hold_days * -1 + 1).count()
    summ = df.ma_cross_earnings.shift(hold_days).sum() # 不计算没有rolling_low的行
    count = df.ma_cross_earnings.shift(hold_days).count()
    average_earnings =  summ / count 
    print average_earnings
    print summ 
    print count
    print 'en-----------------d--------------------'
    return summ, count, average_earnings


#foo5('zxb', scope=0.06, hold_days=250, ma1='ma5', ma2='ma10')  # 
#print foo5('hs300', scope=0.15, hold_days=300, ma1='ma5', ma2='ma10')  # 

#foo5('hs300', scope=0.05, hold_days=250, ma1='ma5', ma2='ma10') 
#ma_crossup('hs300', scope=0.05, days=250, ma1='ma5', ma2='ma10')

def run_foo5(daima):
    scopes = np.arange(0.05, 0.2, 0.01)
    hold_days = [100,150,200,250,280,290,300]
    mas = [
        ('ma5', 'ma10'), 
        ('ma5', 'ma20'),
        ('ma10', 'ma20'),
    ]

    df_scope = []
    df_day = []
    df_ma = []
    df_sum = []
    df_count = []
    df_avge = []
    for scope in scopes:
        for day in hold_days:
            for ma in mas:
                #print scope
                rtn = foo5(daima, scope=scope, hold_days=day, ma1=ma[0], ma2=ma[1])
    
                df_scope.append(scope)
                df_day.append(day)
                df_ma.append(ma)
                df_sum.append(rtn[0])
                df_count.append(rtn[1])
                df_avge.append(rtn[2])
    df = pd.DataFrame({
        'scope': df_scope,
        'days':df_day,
        'ma':df_ma,
        'sum':df_sum,
        'count':df_count,
        'avge':df_avge

        })
    df.to_csv('files_tmp/run_foo5_%s.csv' % daima)
    

#run_foo5('cyb')


@util.display_func_name
def move_stop_loss(daima, scope=0.05, hold_days=100):
    '''not completed'''

    df = pd.read_csv('data/%s.xls' % daima)
    df = df.loc[ :, ['date','open', 'close', 'high', 'low', 'ma5', 'ma10', 'ma20'] ]
    df['rolling_high'] = pd.rolling_max(df.high, hold_days)
    df['new_highest'] = np.where(df.high > df.high.shift(-1), True ,False)
    df['move_stop_loss'] = df.open * (1- scope)
    #df['move_stop_loss'] = 
    print df
    #df['earnings'] = np.where(df.rolling_low > df.stop_loss , df.open.shift(hold_days) - df.open ,df.stop_loss - df.open)
    df.to_csv('files_tmp/move_stop_loss.csv')
    #summ = df.ma_cross_earnings.shift(hold_days * -1 + 1).sum() # 不计算没有rolling_low的行
    #count = df.ma_cross_earnings.shift(hold_days * -1 + 1).count()
    #average_earnings =  summ / count 
    #print average_earnings
    #print summ 
    #print count
    
    #return summ, count, average_earnings

#move_stop_loss('hs300', 0.05)

@util.display_func_name
def cross_bs(daima, ma1, ma2):
    '''ma1 crossup ma2 buy  ma1 crossdown ma2 sell 
       open buy   close sell

       result is   not OK
    '''
    df = pd.read_csv('data/%s.xls' % daima)
    df = df.loc[ :, ['date','open', 'close', 'high', 'low', 'ma5', 'ma10', 'ma20', 'ma60'] ]
    ma1_crossup_2 = (df[ma1].shift(-2) < df[ma2].shift(-2)) & (df[ma1].shift(-1) > df[ma2].shift(-1))
    ma1_crossdown_2 = (df[ma1].shift(-2) > df[ma2].shift(-2)) & (df[ma1].shift(-1) < df[ma2].shift(-1))
    
    df['ma1_crossup_2'] = np.where(ma1_crossup_2, df.open, 0)
    df['ma1_crossdown_2'] = np.where(ma1_crossdown_2, df.close, 0)
    #has_signal = df.ma1_crossup_2 + df.ma1_crossdown_2 ==1
    #df['has_signal'] = np.where(has_signal==1, True, None)
    df = df[(df.ma1_crossup_2 != 0) | (df.ma1_crossdown_2 != 0) ]
    df.to_csv('files_tmp/cross_bs.csv')
    print df.ma1_crossdown_2.sum() - df.ma1_crossup_2.sum(), df.ma1_crossup_2.count()

#cross_bs('hs300', 'ma5', 'ma10')


@util.display_func_name
def kdjcross_bs(daima):
    '''k crossup d buy  k crossdown d sell 
       open buy   close sell

       result is   not OK
    '''
    df = pd.read_csv('data/%s.xls' % daima)
    #df = df.loc[ :, ['datetime','open', 'close', 'high', 'low', 'KDJ.K', 'KDJ.D'] ]
    #print df.columns
    #df.columns = [col.strip() for col in df.columns]
    util.strip_columns(df)
    df = df.loc[ :, ['date','open', 'close', 'high', 'low', 'KDJ.K', 'KDJ.D'] ]
    k_crossup_d = (df['KDJ.K'].shift(-2) < df['KDJ.D'].shift(-2)) & (df['KDJ.K'].shift(-1) > df['KDJ.D'].shift(-1))
    d_crossdown_d = (df['KDJ.K'].shift(-2) > df['KDJ.D'].shift(-2)) & (df['KDJ.K'].shift(-1) < df['KDJ.D'].shift(-1))
    
    df['k_crossup_d'] = np.where(k_crossup_d, df.open, 0)
    df['k_crossdown_d'] = np.where(d_crossdown_d, df.close, 0)
    
    df['earnings_cumsum'] = df.k_crossdown_d.cumsum() - df.k_crossup_d.cumsum()
    
    df.to_csv('files_tmp/kdjcross_bs.csv')
    

#kdjcross_bs('999999')


#maup('zxb', ma='ma10', days=111, scope=0.15)
#foo3_maup('zxb', ma='ma20', days=111, scope=0.15)

@util.display_func_name
def maup_kdjup(daima, ma='ma20', kdj='KDJ.J', days=200, scope=0.15):
    df = pd.read_csv('data/%s.xls' % daima)
    util.strip_columns(df)
    df = df.loc[:, ['date', 'open', 'close', 'low', 'ma5', 'ma10', 'ma20','KDJ.K', 'KDJ.D', 'KDJ.J']]


    df['kdjup'] = df[kdj].shift(-1) > df[kdj].shift(-2)
    df['maup'] = df[ma].shift(-1) > df[ma].shift(-2)
    df['bothup'] = df.kdjup & df.maup
    df['earning'] = np.where(df['bothup'], df.close.shift(days) - df.open, 0)

    df['stoploss_point'] = df.open * (1-scope)
    rolling_low = pd.rolling_min(df.low, days)
    df['stoploss'] = np.where(df['bothup'], df.stoploss_point - df.open , 0)

    df['earning_with_stoploss'] = np.where(rolling_low > df.stoploss_point, df.earning, df.stoploss)
    
    func_name = sys._getframe().f_code.co_name
    df = df.loc[days: , :]  # 因为近期的看不到n天后的数据，所以没收益，因此不计算
    
    df.to_csv('files_tmp/%s_%s.csv' % (func_name, daima))  # 以函数名作为文件名保存

    df = df.where(df.earning != 0) # for count
    summ = df.earning.sum()
    summ2 = df.earning_with_stoploss.sum()

    count = df.earning.count() # count is same
    count2 = df.earning_with_stoploss.count()

    average_earnings =  summ / count
    average_earnings2 =  summ2 / count #

    print average_earnings, average_earnings2
    print summ, summ2
    print count, count2
    
    #return summ, average_earnings, summ2, average_earnings2, count



@util.display_func_name
def maup_kdjdown(daima, ma='ma20', kdj='KDJ.J', days=200, scope=0.15):
    df = pd.read_csv('data/%s.xls' % daima)
    util.strip_columns(df)
    df = df.loc[:, ['date', 'open', 'close', 'low', 'ma5', 'ma10', 'ma20','KDJ.K', 'KDJ.D', 'KDJ.J']]


    df['kdjdown'] = df[kdj].shift(-1) < df[kdj].shift(-2)
    df['maup'] = df[ma].shift(-1) > df[ma].shift(-2)
    df['both'] = df.kdjdown & df.maup
    df['earning'] = np.where(df['both'], df.close.shift(days) - df.open, 0)

    df['stoploss_point'] = df.open * (1-scope)
    rolling_low = pd.rolling_min(df.low, days)
    df['stoploss'] = np.where(df['both'], df.stoploss_point - df.open , 0)

    df['earning_with_stoploss'] = np.where(rolling_low > df.stoploss_point, df.earning, df.stoploss)
    
    func_name = sys._getframe().f_code.co_name
    df = df.loc[days: , :]  # 因为近期的看不到n天后的数据，所以没收益，因此不计算
    
    df.to_csv('files_tmp/%s_%s.csv' % (func_name, daima))  # 以函数名作为文件名保存

    df = df.where(df.earning != 0) # for count
    summ = df.earning.sum()
    summ2 = df.earning_with_stoploss.sum()

    count = df.earning.count() # count is same
    count2 = df.earning_with_stoploss.count()

    average_earnings =  summ / count
    average_earnings2 =  summ2 / count #

    print average_earnings, average_earnings2
    print summ, summ2
    print count, count2
    
    #return summ, average_earnings, summ2, average_earnings2, count

#maup_kdjup('hs300', ma='ma20', kdj='KDJ.J', days=200, scope=0.15)
#maup_kdjdown('hs300', ma='ma20', kdj='KDJ.J', days=200, scope=0.15)

@util.display_func_name
def foo3_kdjup(daima, ma='ma20', kdj='KDJ.J', days=200, scope=0.15):
    df = pd.read_csv('data/%s.xls' % daima)
    util.strip_columns(df)
    df = df.loc[:, ['date', 'open', 'close', 'low', 'ma5', 'ma10', 'ma20','KDJ.K', 'KDJ.D', 'KDJ.J']]

    df['kdjup'] = df[kdj].shift(-1) > df[kdj].shift(-2)
    # yesterday greater than ma
    df['gt_ma'] = df.low.shift(-1) > df[ma].shift(-1)
    df['both'] = df.kdjup & df.gt_ma
    df['earning'] = np.where(df['both'], df.close.shift(days) - df.open, 0)

    df['stoploss_point'] = df.open * (1-scope)
    rolling_low = pd.rolling_min(df.low, days)
    df['stoploss'] = np.where(df['both'], df.stoploss_point - df.open , 0)

    df['earning_with_stoploss'] = np.where(rolling_low > df.stoploss_point, df.earning, df.stoploss)
    
    func_name = sys._getframe().f_code.co_name
    df = df.loc[days: , :]  # 因为近期的看不到n天后的数据，所以没收益，因此不计算
    
    df.to_csv('files_tmp/%s_%s.csv' % (func_name, daima))  # 以函数名作为文件名保存

    df = df.where(df.earning != 0) # for count
    summ = df.earning.sum()
    summ2 = df.earning_with_stoploss.sum()

    count = df.earning.count() # count is same
    count2 = df.earning_with_stoploss.count()

    average_earnings =  summ / count
    average_earnings2 =  summ2 / count #

    print average_earnings, average_earnings2
    print summ, summ2
    print count, count2
    #return summ, average_earnings, summ2, average_earnings2, count

@util.display_func_name
def foo3_kdjdown(daima, ma='ma20', kdj='KDJ.J', days=200, scope=0.15):
    df = pd.read_csv('data/%s.xls' % daima)
    util.strip_columns(df)
    df = df.loc[:, ['date', 'open', 'close', 'low', 'ma5', 'ma10', 'ma20','KDJ.K', 'KDJ.D', 'KDJ.J']]

    df['kdjdown'] = df[kdj].shift(-1) < df[kdj].shift(-2)
    # yesterday greater than ma
    df['gt_ma'] = df.low.shift(-1) > df[ma].shift(-1)
    df['both'] = df.kdjdown & df.gt_ma
    df['earning'] = np.where(df['both'], df.close.shift(days) - df.open, 0)

    df['stoploss_point'] = df.open * (1-scope)
    rolling_low = pd.rolling_min(df.low, days)
    df['stoploss'] = np.where(df['both'], df.stoploss_point - df.open , 0)

    df['earning_with_stoploss'] = np.where(rolling_low > df.stoploss_point, df.earning, df.stoploss)
    
    func_name = sys._getframe().f_code.co_name
    df = df.loc[days: , :]  # 因为近期的看不到n天后的数据，所以没收益，因此不计算
    
    df.to_csv('files_tmp/%s_%s.csv' % (func_name, daima))  # 以函数名作为文件名保存

    df = df.where(df.earning != 0) # for count
    summ = df.earning.sum()
    summ2 = df.earning_with_stoploss.sum()

    count = df.earning.count() # count is same
    count2 = df.earning_with_stoploss.count()

    average_earnings =  summ / count
    average_earnings2 =  summ2 / count #

    print average_earnings, average_earnings2
    print summ, summ2
    print count, count2
    
    #return summ, average_earnings, summ2, average_earnings2, count


@util.display_func_name
def foo3_maup_kdjdown(daima, ma='ma20', kdj='KDJ.J', days=200, scope=0.15):
    df = pd.read_csv('data/%s.xls' % daima)
    util.strip_columns(df)
    df = df.loc[:, ['date', 'open', 'close', 'low', 'ma5', 'ma10', 'ma20','KDJ.K', 'KDJ.D', 'KDJ.J']]
    
    df['gt_ma'] = df.low.shift(-1) > df[ma].shift(-1)
    df['maup'] = df[ma].shift(-1) > df[ma].shift(-2)
    df['kdjdown'] = df[kdj].shift(-1) < df[kdj].shift(-2)
    # yesterday greater than ma
    
    df['all'] = df.kdjdown & df.gt_ma & df.maup
    df['earning'] = np.where(df['all'], df.close.shift(days) - df.open, 0)

    df['stoploss_point'] = df.open * (1-scope)
    rolling_low = pd.rolling_min(df.low, days)
    df['stoploss'] = np.where(df['all'], df.stoploss_point - df.open , 0)

    df['earning_with_stoploss'] = np.where(rolling_low > df.stoploss_point, df.earning, df.stoploss)
    
    func_name = sys._getframe().f_code.co_name
    df = df.loc[days: , :]  # 因为近期的看不到n天后的数据，所以没收益，因此不计算
    
    df.to_csv('files_tmp/%s_%s.csv' % (func_name, daima))  # 以函数名作为文件名保存

    df = df.where(df.earning != 0) # for count
    summ = df.earning.sum()
    summ2 = df.earning_with_stoploss.sum()

    count = df.earning.count() # count is same
    count2 = df.earning_with_stoploss.count()

    average_earnings =  summ / count
    average_earnings2 =  summ2 / count #

    print average_earnings, average_earnings2
    print summ, summ2
    print count, count2
    
    #return summ, average_earnings, summ2, average_earnings2, count


@util.display_func_name
def foo3_maup_kdjup(daima, ma='ma20', kdj='KDJ.J', days=200, scope=0.15):
    df = pd.read_csv('data/%s.xls' % daima)
    util.strip_columns(df)
    df = df.loc[:, ['date', 'open', 'close', 'low', 'ma5', 'ma10', 'ma20','KDJ.K', 'KDJ.D', 'KDJ.J']]
    
    df['gt_ma'] = df.low.shift(-1) > df[ma].shift(-1)
    df['maup'] = df[ma].shift(-1) > df[ma].shift(-2)
    df['kdjup'] = df[kdj].shift(-1) > df[kdj].shift(-2)
    # yesterday greater than ma
    
    df['all'] = df.kdjup & df.gt_ma & df.maup
    df['earning'] = np.where(df['all'], df.close.shift(days) - df.open, 0)

    df['stoploss_point'] = df.open * (1-scope)
    rolling_low = pd.rolling_min(df.low, days)
    df['stoploss'] = np.where(df['all'], df.stoploss_point - df.open , 0)

    df['earning_with_stoploss'] = np.where(rolling_low > df.stoploss_point, df.earning, df.stoploss)
    
    func_name = sys._getframe().f_code.co_name
    df = df.loc[days: , :]  # 因为近期的看不到n天后的数据，所以没收益，因此不计算
    
    df.to_csv('files_tmp/%s_%s.csv' % (func_name, daima))  # 以函数名作为文件名保存

    df = df.where(df.earning != 0) # for count
    summ = df.earning.sum()
    summ2 = df.earning_with_stoploss.sum()

    count = df.earning.count() # count is same
    count2 = df.earning_with_stoploss.count()

    average_earnings =  summ / count
    average_earnings2 =  summ2 / count #

    print average_earnings, average_earnings2
    print summ, summ2
    print count, count2
    
    #return summ, average_earnings, summ2, average_earnings2, count

@util.display_func_name
def foo3_kdjdown_kdjgt(daima, ma='ma20', kdj='KDJ.J', days=200, scope=0.15, kdjvalue=0):
    df = pd.read_csv('data/%s.xls' % daima)
    util.strip_columns(df)
    df = df.loc[:, ['date', 'open', 'close', 'low', 'ma5', 'ma10', 'ma20','KDJ.K', 'KDJ.D', 'KDJ.J']]

    df['kdjdown'] = df[kdj].shift(-1) < df[kdj].shift(-2)
    df['gt_ma'] = df.low.shift(-1) > df[ma].shift(-1)
    df['kdjgt'] = df[kdj].shift(-1) > kdjvalue

    df['all'] = df.kdjdown & df.gt_ma & df.kdjgt
    df['earning'] = np.where(df['all'], df.close.shift(days) - df.open, 0)

    df['stoploss_point'] = df.open * (1-scope)
    rolling_low = pd.rolling_min(df.low, days)
    df['stoploss'] = np.where(df['all'], df.stoploss_point - df.open , 0)

    df['earning_with_stoploss'] = np.where(rolling_low > df.stoploss_point, df.earning, df.stoploss)
    
    func_name = sys._getframe().f_code.co_name
    df = df.loc[days: , :]  # 因为近期的看不到n天后的数据，所以没收益，因此不计算
    
    df.to_csv('files_tmp/%s_%s.csv' % (func_name, daima))  # 以函数名作为文件名保存

    df = df.where(df.earning != 0) # for count
    summ = df.earning.sum()
    summ2 = df.earning_with_stoploss.sum()

    count = df.earning.count() # count is same
    count2 = df.earning_with_stoploss.count()

    average_earnings =  summ / count
    average_earnings2 =  summ2 / count #

    print average_earnings, average_earnings2
    print summ, summ2
    print count, count2
    
    #return summ, average_earnings, summ2, average_earnings2, count



@util.display_func_name
def kdjup(daima, kdj='KDJ.D', days=5, scope=0.05):
    '''
    '''
    df = pd.read_csv('data/%s.xls' % daima)
    util.strip_columns(df)
    df = df.loc[:, ['date', 'open', 'close', 'low', 'KDJ.K', 'KDJ.D', 'KDJ.J']]

    df['kdjup'] = df[kdj].shift(-1) > df[kdj].shift(-2)
    df['earning'] = np.where(df['kdjup'], df.close.shift(days) - df.open, 0)

    df['stoploss_point'] = df.open * (1-scope)
    rolling_low = pd.rolling_min(df.low, days)
    df['stoploss'] = np.where(df['kdjup'], df.stoploss_point - df.open , 0)

    df['earning_with_stoploss'] = np.where(rolling_low > df.stoploss_point, df.earning, df.stoploss)
    
    func_name = sys._getframe().f_code.co_name
    df = df.loc[days: , :]  # 因为近期的看不到n天后的数据，所以没收益，因此不计算
    
    df.to_csv('files_tmp/%s_%s.csv' % (func_name, daima))  # 以函数名作为文件名保存

    df = df.where(df.earning != 0) # for count
    summ = df.earning.sum()
    summ2 = df.earning_with_stoploss.sum()

    count = df.earning.count() # count is same
    count2 = df.earning_with_stoploss.count()

    average_earnings =  summ / count
    average_earnings2 =  summ2 / count #

    print average_earnings, average_earnings2
    print summ, summ2
    print count, count2
    
    return summ, average_earnings, summ2, average_earnings2, count


@util.display_func_name
def kdjdown(daima, kdj='KDJ.D', days=5, scope=0.05):
    '''
    '''
    df = pd.read_csv('data/%s.xls' % daima)
    util.strip_columns(df)
    df = df.loc[:, ['date', 'open', 'close', 'low', 'KDJ.K', 'KDJ.D', 'KDJ.J']]

    df['kdjdown'] = df[kdj].shift(-1) < df[kdj].shift(-2)
    df['earning'] = np.where(df['kdjdown'], df.close.shift(days) - df.open, 0)

    df['stoploss_point'] = df.open * (1-scope)
    rolling_low = pd.rolling_min(df.low, days)
    df['stoploss'] = np.where(df['kdjdown'], df.stoploss_point - df.open , 0)

    df['earning_with_stoploss'] = np.where(rolling_low > df.stoploss_point, df.earning, df.stoploss)
    
    func_name = sys._getframe().f_code.co_name
    df = df.loc[days: , :]  # 因为近期的看不到n天后的数据，所以没收益，因此不计算
    
    df.to_csv('files_tmp/%s_%s.csv' % (func_name, daima))  # 以函数名作为文件名保存

    df = df.where(df.earning != 0) # for count
    summ = df.earning.sum()
    summ2 = df.earning_with_stoploss.sum()

    count = df.earning.count() # count is same
    count2 = df.earning_with_stoploss.count()

    average_earnings =  summ / count
    average_earnings2 =  summ2 / count #

    print average_earnings, average_earnings2
    print summ, summ2
    print count, count2
    
    return summ, average_earnings, summ2, average_earnings2, count


@util.display_func_name
def kdjlt(daima, kdj='KDJ.D', value=0, days=5, scope=0.05):
    '''
    '''
    df = pd.read_csv('data/%s.xls' % daima)
    util.strip_columns(df)
    df = df.loc[:, ['date', 'open', 'close', 'low', 'KDJ.K', 'KDJ.D', 'KDJ.J']]

    df['kdjlt'] = df[kdj].shift(-1) < value
    df['earning'] = np.where(df['kdjlt'], df.close.shift(days) - df.open, 0)

    df['stoploss_point'] = df.open * (1-scope)
    rolling_low = pd.rolling_min(df.low, days)
    df['stoploss'] = np.where(df['kdjlt'], df.stoploss_point - df.open , 0)

    df['earning_with_stoploss'] = np.where(rolling_low > df.stoploss_point, df.earning, df.stoploss)
    
    func_name = sys._getframe().f_code.co_name
    df = df.loc[days: , :]  # 因为近期的看不到n天后的数据，所以没收益，因此不计算
    
    df.to_csv('files_tmp/%s_%s.csv' % (func_name, daima))  # 以函数名作为文件名保存

    df = df.where(df.earning != 0) # for count
    summ = df.earning.sum()
    summ2 = df.earning_with_stoploss.sum()

    count = df.earning.count() # count is same
    count2 = df.earning_with_stoploss.count()

    average_earnings =  summ / count
    average_earnings2 =  summ2 / count #

    print average_earnings, average_earnings2
    print summ, summ2
    print count, count2
    
    return summ, average_earnings, summ2, average_earnings2, count

@util.display_func_name
def kdjgt(daima, kdj='KDJ.D', value=0, days=5, scope=0.05):
    '''
    '''
    df = pd.read_csv('data/%s.xls' % daima)
    util.strip_columns(df)
    df = df.loc[:, ['date', 'open', 'close', 'low', 'KDJ.K', 'KDJ.D', 'KDJ.J']]

    df['kdjgt'] = df[kdj].shift(-1) > value
    df['earning'] = np.where(df['kdjgt'], df.close.shift(days) - df.open, 0)

    df['stoploss_point'] = df.open * (1-scope)
    rolling_low = pd.rolling_min(df.low, days)
    df['stoploss'] = np.where(df['kdjgt'], df.stoploss_point - df.open , 0)

    df['earning_with_stoploss'] = np.where(rolling_low > df.stoploss_point, df.earning, df.stoploss)
    
    func_name = sys._getframe().f_code.co_name
    df = df.loc[days: , :]  # 因为近期的看不到n天后的数据，所以没收益，因此不计算
    
    df.to_csv('files_tmp/%s_%s.csv' % (func_name, daima))  # 以函数名作为文件名保存

    df = df.where(df.earning != 0) # for count
    summ = df.earning.sum()
    summ2 = df.earning_with_stoploss.sum()

    count = df.earning.count() # count is same
    count2 = df.earning_with_stoploss.count()

    average_earnings =  summ / count
    average_earnings2 =  summ2 / count #

    print average_earnings, average_earnings2
    print summ, summ2
    print count, count2
    
    return summ, average_earnings, summ2, average_earnings2, count


@util.display_func_name
def kdjlt_up(daima, kdj='KDJ.D', value=0, days=5, scope=0.05):
    df = pd.read_csv('data/%s.xls' % daima)
    util.strip_columns(df)
    df = df.loc[:, ['date', 'open', 'close', 'low', 'ma5', 'ma10', 'ma20','KDJ.K', 'KDJ.D', 'KDJ.J']]

    df['kdjlt'] = df[kdj].shift(-1) < value
    df['kdjup'] = df[kdj].shift(-1) > df[kdj].shift(-2)
    df['both'] = df.kdjlt & df.kdjup
    df['earning'] = np.where(df['both'], df.close.shift(days) - df.open, 0)

    df['stoploss_point'] = df.open * (1-scope)
    rolling_low = pd.rolling_min(df.low, days)
    df['stoploss'] = np.where(df['both'], df.stoploss_point - df.open , 0)

    df['earning_with_stoploss'] = np.where(rolling_low > df.stoploss_point, df.earning, df.stoploss)
    
    func_name = sys._getframe().f_code.co_name
    df = df.loc[days: , :]  # 因为近期的看不到n天后的数据，所以没收益，因此不计算
    
    df.to_csv('files_tmp/%s_%s.csv' % (func_name, daima))  # 以函数名作为文件名保存

    df = df.where(df.earning != 0) # for count
    summ = df.earning.sum()
    summ2 = df.earning_with_stoploss.sum()

    count = df.earning.count() # count is same
    count2 = df.earning_with_stoploss.count()

    average_earnings =  summ / count
    average_earnings2 =  summ2 / count #

    print average_earnings, average_earnings2
    print summ, summ2
    print count, count2
    
    #return summ, average_earnings, summ2, average_earnings2, count


@util.display_func_name
def kdjgt_up(daima, kdj='KDJ.D', value=0, days=5, scope=0.05):
    df = pd.read_csv('data/%s.xls' % daima)
    util.strip_columns(df)
    df = df.loc[:, ['date', 'open', 'close', 'low', 'ma5', 'ma10', 'ma20','KDJ.K', 'KDJ.D', 'KDJ.J']]

    df['kdjgt'] = df[kdj].shift(-1) > value
    df['kdjup'] = df[kdj].shift(-1) > df[kdj].shift(-2)
    df['both'] = df.kdjgt & df.kdjup
    df['earning'] = np.where(df['both'], df.close.shift(days) - df.open, 0)

    df['stoploss_point'] = df.open * (1-scope)
    rolling_low = pd.rolling_min(df.low, days)
    df['stoploss'] = np.where(df['both'], df.stoploss_point - df.open , 0)

    df['earning_with_stoploss'] = np.where(rolling_low > df.stoploss_point, df.earning, df.stoploss)
    
    func_name = sys._getframe().f_code.co_name
    df = df.loc[days: , :]  # 因为近期的看不到n天后的数据，所以没收益，因此不计算
    
    df.to_csv('files_tmp/%s_%s.csv' % (func_name, daima))  # 以函数名作为文件名保存

    df = df.where(df.earning != 0) # for count
    summ = df.earning.sum()
    summ2 = df.earning_with_stoploss.sum()

    count = df.earning.count() # count is same
    count2 = df.earning_with_stoploss.count()

    average_earnings =  summ / count
    average_earnings2 =  summ2 / count #

    print average_earnings, average_earnings2
    print summ, summ2
    print count, count2
    
    #return summ, average_earnings, summ2, average_earnings2, count


@util.display_func_name
def D_down_J_up(daima, days=5, scope=0.05):
    df = pd.read_csv('data/%s.xls' % daima)
    util.strip_columns(df)
    df = df.loc[:, ['date', 'open', 'close', 'low', 'ma5', 'ma10', 'ma20','KDJ.K', 'KDJ.D', 'KDJ.J']]

    df['ddown'] = df['KDJ.D'].shift(-1) < df['KDJ.D'].shift(-2)
    df['jup'] = df['KDJ.J'].shift(-1) > df['KDJ.J'].shift(-2)
    df['both'] = df.ddown & df.jup
    df['earning'] = np.where(df['both'], df.close.shift(days) - df.open, 0)

    df['stoploss_point'] = df.open * (1-scope)
    rolling_low = pd.rolling_min(df.low, days)
    df['stoploss'] = np.where(df['both'], df.stoploss_point - df.open , 0)

    df['earning_with_stoploss'] = np.where(rolling_low > df.stoploss_point, df.earning, df.stoploss)
    
    func_name = sys._getframe().f_code.co_name
    df = df.loc[days: , :]  # 因为近期的看不到n天后的数据，所以没收益，因此不计算
    
    df.to_csv('files_tmp/%s_%s.csv' % (func_name, daima))  # 以函数名作为文件名保存

    df = df.where(df.earning != 0) # for count
    summ = df.earning.sum()
    summ2 = df.earning_with_stoploss.sum()

    count = df.earning.count() # count is same
    count2 = df.earning_with_stoploss.count()

    average_earnings =  summ / count
    average_earnings2 =  summ2 / count #

    print average_earnings, average_earnings2
    print summ, summ2
    print count, count2
    
    #return summ, average_earnings, summ2, average_earnings2, count

@util.display_func_name
def foo4(daima, ma='ma5', offset=10,scale=0.1, days=5, scope=0.05):
    '''
    '''
    df = pd.read_csv('data/%s.xls' % daima)
    util.strip_columns(df)
    df = df.loc[:, ['date', 'open', 'close', 'low', 'ma5', 'ma10', 'ma20']]

    # ma gteater ma of n days earlier 
    df['magtma'] = (df[ma].shift(-1) - df[ma].shift(-1*offset)) >= df[ma].shift(-1) * scale
    

    df['earning'] = np.where(df['magtma'], df.close.shift(days) - df.open, 0)

    df['stoploss_point'] = df.open * (1-scope)
    rolling_low = pd.rolling_min(df.low, days)
    df['stoploss'] = np.where(df['magtma'], df.stoploss_point - df.open , 0)

    df['earning_with_stoploss'] = np.where(rolling_low > df.stoploss_point, df.earning, df.stoploss)
    
    func_name = sys._getframe().f_code.co_name
    df = df.loc[days: , :]  # 因为近期的看不到n天后的数据，所以没收益，因此不计算
    
    df.to_csv('files_tmp/%s_%s.csv' % (func_name, daima))  # 以函数名作为文件名保存

    df = df.where(df.earning != 0) # for count
    summ = df.earning.sum()
    summ2 = df.earning_with_stoploss.sum()

    count = df.earning.count() # count is same
    count2 = df.earning_with_stoploss.count()

    average_earnings =  summ / count
    average_earnings2 =  summ2 / count #

    print average_earnings, average_earnings2
    print summ, summ2
    print count, count2
    
    return summ, average_earnings, summ2, average_earnings2, count


@util.display_func_name
def foo3_foo4(daima, ma='ma5', offset=10,scale=0.1, days=5, scope=0.05):
    '''
    '''
    df = pd.read_csv('data/%s.xls' % daima)
    util.strip_columns(df)
    df = df.loc[:, ['date', 'open', 'close', 'low', 'ma5', 'ma10', 'ma20']]


    df['magtma'] = (df[ma].shift(-1) - df[ma].shift(-1*offset)) > df[ma].shift(-1) * scale
    df['gt_ma'] = df.low.shift(-1) > df[ma].shift(-1)
    df['all'] = df.magtma & df.gt_ma
    df['earning'] = np.where(df['all'], df.close.shift(days) - df.open, 0)

    df['stoploss_point'] = df.open * (1-scope)
    rolling_low = pd.rolling_min(df.low, days)
    df['stoploss'] = np.where(df['all'], df.stoploss_point - df.open , 0)

    df['earning_with_stoploss'] = np.where(rolling_low > df.stoploss_point, df.earning, df.stoploss)
    
    func_name = sys._getframe().f_code.co_name
    df = df.loc[days: , :]  # 因为近期的看不到n天后的数据，所以没收益，因此不计算
    
    df.to_csv('files_tmp/%s_%s.csv' % (func_name, daima))  # 以函数名作为文件名保存

    df = df.where(df.earning != 0) # for count
    summ = df.earning.sum()
    summ2 = df.earning_with_stoploss.sum()

    count = df.earning.count() # count is same
    count2 = df.earning_with_stoploss.count()

    average_earnings =  summ / count
    average_earnings2 =  summ2 / count #

    print average_earnings, average_earnings2
    print summ, summ2
    print count, count2
    
    return summ, average_earnings, summ2, average_earnings2, count


def ma_slope_gt(daima, ma, slope, days, scope, offset):
    '''
    slope 斜率
    昨天与offset天前斜率
    slop==0 offset==2时，和ma_up一样
    '''
    df = pd.read_csv('data/%s.xls' % daima)
    util.strip_columns(df)
    df = df.loc[:, ['date', 'open', 'close', 'low', 'ma5', 'ma10', 'ma20']]

    yesterday = df[ma].shift(-1)
    offsetday = df[ma].shift(-1*offset)
    real_slope = (yesterday - offsetday) / offsetday
    slope_key = 'ma_slope_gt_%s' % str(slope)
    df[slope_key] = real_slope > slope
    #df['gt_ma'] = df.low.shift(-1) > df[ma].shift(-1)
    #df['all'] = df.magtma & df.gt_ma
    df['earning'] = np.where(df[slope_key], df.close.shift(days) - df.open, 0)

    df['stoploss_point'] = df.open * (1-scope)
    rolling_low = pd.rolling_min(df.low, days)
    df['stoploss'] = np.where(df[slope_key], df.stoploss_point - df.open , 0)

    df['earning_with_stoploss'] = np.where(rolling_low > df.stoploss_point, df.earning, df.stoploss)
    
    func_name = sys._getframe().f_code.co_name
    df = df.loc[days: , :]  # 因为近期的看不到n天后的数据，所以没收益，因此不计算
    
    df.to_csv('files_tmp/%s_%s.csv' % (func_name, daima))  # 以函数名作为文件名保存

    df = df.where(df.earning != 0) # for count
    summ = df.earning.sum()
    summ2 = df.earning_with_stoploss.sum()

    count = df.earning.count() # count is same

    average_earnings =  summ / count
    average_earnings2 =  summ2 / count #

    print average_earnings, average_earnings2
    print summ, summ2
    print count
    
    return summ, average_earnings, summ2, average_earnings2, count

#ma_slope_gt('999999', 'ma5', 0.002, days=2, scope=0.1, offset=2)


@util.display_func_name
def ma_slope_range(daima, ma, slope, days, scope): #, offset):
    '''
    
    '''
    df = pd.read_csv('data/%s.xls' % daima)
    util.strip_columns(df)
    df = df.loc[:, ['date', 'open', 'close', 'low', 'ma5', 'ma10', 'ma20']]

    yesterday = df[ma].shift(-1)
    offsetday = df[ma].shift(-2)
    real_slope = (yesterday - offsetday) / offsetday
    df['ma_slope_range'] = (slope[0] <= real_slope) & (real_slope <= slope[1])
    df['earning'] = np.where(df['ma_slope_range'], df.close.shift(days) - df.open, 0)

    df['stoploss_point'] = df.open * (1-scope)
    rolling_low = pd.rolling_min(df.low, days)
    df['stoploss'] = np.where(df['ma_slope_range'], df.stoploss_point - df.open , 0)

    df['earning_with_stoploss'] = np.where(rolling_low > df.stoploss_point, df.earning, df.stoploss)
    
    func_name = sys._getframe().f_code.co_name
    df = df.loc[days: , :]  # 因为近期的看不到n天后的数据，所以没收益，因此不计算
    
    df.to_csv('files_tmp/%s_%s.csv' % (func_name, daima))  # 以函数名作为文件名保存

    df = df.where(df.earning != 0) # for count
    summ = df.earning.sum()
    summ2 = df.earning_with_stoploss.sum()

    count = df.earning.count() # count is same

    average_earnings =  summ / count
    average_earnings2 =  summ2 / count #

    print average_earnings, average_earnings2
    print summ, summ2
    print count
    
    return summ, average_earnings, summ2, average_earnings2, count

#ma_slope_range('zxb', 'ma20', slope = [0.0003, 0.0005], days=10, scope=0.1, offset=2)


#@util.display_func_name
def runall(daima, rlist, ma, ma2, kdj, offset=50,scale=0.11, days=220, scope=0.1, slope=0.001):
    '''
    '''
    df = pd.read_csv('data/%s.xls' % daima)
    util.strip_columns(df)
    df = df.loc[:, ['date', 'open', 'close', 'high', 'low', 'ma5', 'ma10', 'ma20', 'KDJ.K', 'KDJ.D', 'KDJ.J']]
    alltrues = np.array(np.ones( (len(df),26)), dtype=np.bool)

    tmpdf = pd.DataFrame(alltrues , columns=list('ABCDEFGHIJKLMNOPQRSTUVWXZY'))
    df['magtma'] = tmpdf.loc[:,['A']]
    df['gt_ma'] = tmpdf.loc[:,['B']]
    df['lt_ma'] = tmpdf.loc[:,['C']]
    df['ma_up'] = tmpdf.loc[:,['D']]
    df['ma_down'] = tmpdf.loc[:,['E']]
    df['ma_crossup'] = tmpdf.loc[:,['F']]
    df['kdj_up'] = tmpdf.loc[:,['G']]
    df['kdj_down'] = tmpdf.loc[:,['H']]
    df['ma_slope_gt'] = tmpdf.loc[:,['I']]
    #df['magtma'] = tmpdf.loc[:,['J']]
    #df['magtma'] = tmpdf.loc[:,['K']]
    #df['magtma'] = tmpdf.loc[:,['L']]
    #df['magtma'] = tmpdf.loc[:,['M']]
    #df['magtma'] = tmpdf.loc[:,['N']]
    #df['magtma'] = tmpdf.loc[:,['O']]

    # foo4
    if 'magtma' in rlist:
        df['magtma'] = (df[ma].shift(-1) - df[ma].shift(-1*offset)) > df[ma].shift(-1) * scale
    # foo3
    if 'gt_ma' in rlist:
        df['gt_ma'] = df.low.shift(-1) > df[ma].shift(-1)
    if 'lt_ma' in rlist:
        df['lt_ma'] = df.high.shift(-1) < df[ma].shift(-1)
    if 'ma_up' in rlist:
        df['ma_up'] = df[ma].shift(-1) > df[ma].shift(-2)
    if 'ma_down' in rlist:
        df['ma_down'] = df[ma].shift(-1) < df[ma].shift(-2)
    if 'ma_crossup'in rlist: # ma 金叉
       df['ma_crossup'] = (df[ma].shift(-2) < df[ma2].shift(-2)) & (df[ma].shift(-1) > df[ma2].shift(-1))
    if 'kdj_up'in rlist:
        df['kdj_up'] = df[kdj].shift(-1) > df[kdj].shift(-2)
    if 'kdj_down'in rlist:
        df['kdj_down'] = df[kdj].shift(-1) < df[kdj].shift(-2)
    if 'ma_slope_gt'in rlist:
        yesterday = df[ma].shift(-1)
        offsetday = df[ma].shift(-1*offset)
        real_slope = (yesterday - offsetday) / offsetday
        df['ma_slope_gt'] = real_slope > slope

    df['all'] = df.magtma & df.gt_ma & df.lt_ma & df.ma_up & df.ma_down & df.ma_crossup & df.kdj_up & df.kdj_down & df.ma_slope_gt
    #df['all'] = df.magtma * df.gt_ma * df.ma_up * df.ma_down * df.ma_crossup * df.kdj_up * df.kdj_down

    df['earning'] = np.where(df['all'], df.open.shift(days) - df.open, 0)

    df['stoploss_point'] = df.open * (1-scope)
    rolling_low = pd.rolling_min(df.low, days)
    df['stoploss'] = np.where(df['all'], df.stoploss_point - df.open , 0)

    df['earning_with_stoploss'] = np.where(rolling_low > df.stoploss_point, df.earning, df.stoploss)
    
    func_name = sys._getframe().f_code.co_name
    df = df.loc[days: , :]  # 因为近期的看不到n天后的数据，所以没收益，因此不计算
    
    df.to_csv('files_tmp/%s_%s.csv' % (func_name, daima))  # 以函数名作为文件名保存

    df = df.where(df.earning != 0) # for count
    summ = df.earning.sum()
    summ2 = df.earning_with_stoploss.sum()

    count = df.earning.count()
    #count2 = df.earning_with_stoploss.count()  # count is same
    if count==0:
        return
    average_earnings =  summ / count #if count else 0
    average_earnings2 =  summ2 / count #if count else 0 #

    #print rlist
    print average_earnings, average_earnings2
    #print summ, summ2
    print count
    
    return summ, average_earnings, summ2, average_earnings2, count

def runn():
    daima = '999999'
    days = 2
    kdj='KDJ.D'
    ma='ma5'
    scope = 0.1
    kdjvalue=0
    foo(daima, days=days, scope=scope)
    foo3(daima, ma=ma, days=days, scope=scope)
    #foo3b(daima, ma=ma, days=days)
    foo3_kdjup(daima, ma=ma, kdj=kdj, days=days, scope=scope)
    #foo3_kdjdown(daima, ma=ma, kdj=kdj, days=days, scope=scope) # ma5 and 'KDJ.D' is best?
    foo3_maup(daima, ma=ma, days=days, scope=scope)
    #foo3_maup_kdjdown(daima, ma=ma, kdj=kdj, days=days, scope=scope)
    foo3_maup_kdjup(daima, ma=ma, kdj=kdj, days=days, scope=scope)
    #foo3b_maup(daima, ma=ma, days=days, scope=scope)
    maup(daima, ma=ma, days=days, scope=scope)
    maup_kdjup(daima, ma=ma, kdj=kdj, days=days, scope=scope)
    #maup_kdjdown(daima, ma=ma, kdj=kdj, days=days, scope=scope)
    kdjup(daima, kdj=kdj, days=days, scope=scope)
    #kdjdown(daima, kdj=kdj, days=days, scope=scope)
    #kdjlt(daima, kdj=kdj, value=kdjvalue, days=days, scope=scope)
    #kdjgt(daima, kdj=kdj, value=kdjvalue, days=days, scope=scope) # KDJ.D bigger the better ?! and no stoploss?
    #kdjlt_up(daima, kdj=kdj, value=kdjvalue, days=days, scope=scope)
    #kdjgt_up(daima, kdj=kdj, value=kdjvalue, days=days, scope=scope)
    #foo3_kdjdown_kdjgt(daima, ma=ma, kdj=kdj, days=days, scope=scope, kdjvalue=kdjvalue)
    #D_down_J_up(daima, days=days, scope=scope)
    foo4(daima, ma='ma5', offset=50,scale=0.11, days=days, scope=scope)
    #foo4(daima, ma='ma10', offset=50,scale=0.11, days=220, scope=scope)
    #foo4(daima, ma='ma20', offset=50,scale=0.11, days=220, scope=scope)
    foo3_foo4(daima, ma='ma10', offset=50,scale=0.11, days=days, scope=scope)
    ma_slope_range(daima, ma, slope = [0.0003, 0.001], days=days, scope=scope)
 

def test_runall():
    daima = 'hs300'
    rlist = ['magtma','gt_ma']
    days = 1
    kdj='KDJ.D'
    kdj2='KDJ.J'
    ma='ma5'
    ma2='ma20'
    scope = 0.1
    scale = 0.1
    offset=50
    foo(daima, days=days, scope=scope)
    runall(daima, rlist=rlist, ma=ma, ma2=ma2,kdj=kdj, kdj2=kdj, offset=offset,scale=scale, days=days, scope=scope)
    #maup(daima, ma=ma, days=days, scope=scope)
    #kdjdown(daima, kdj=kdj, days=days, scope=scope) 
    #maup_kdjdown(daima, ma=ma, kdj=kdj, days=days, scope=scope)  
    #foo3_maup(daima, ma=ma, days=days, scope=scope)
    #foo3_maup_kdjdown(daima, ma=ma, kdj=kdj, days=days, scope=scope)
    #foo3_maup_kdjup(daima, ma=ma, kdj=kdj, days=days, scope=scope)

def combinations_runall(daima, days, ma, scope):

    kdj='KDJ.D'
    
    ma2='ma10'
    scope = 0.1
    scale = 0.1
    slope = 0.001
    offset = 2
    rlist = [
        #'magtma',
        'gt_ma',
        #'lt_ma',
        'ma_up',
        #'ma_down',
        #'ma_crossup',
        'kdj_up',
        #'kdj_down',
        #'ma_slope_gt'

        ]
    df_rlist = []
    df_sum = []
    df_count = []
    df_avge = []
    df_sum2 = []
    df_avge2 = []

    frtn = foo(daima, days=days, scope=scope) # 参照
    for n in range(1, len(rlist)+1):
        for r in combinations(rlist, n):
            print r
            rtn = runall(daima, rlist=r, ma=ma, ma2=ma2,kdj=kdj, offset=offset,scale=scale, days=days, scope=scope, slope=slope)
            if rtn:
                df_rlist.append(r)
                df_sum.append(rtn[0])
                df_avge.append(rtn[1])
                df_sum2.append(rtn[2])
                df_avge2.append(rtn[3])
                df_count.append(rtn[4])

    df = pd.DataFrame({
        'rlist':df_rlist,
        'sum':df_sum,
        'sum2':df_sum2,
        'count':df_count,
        'avge':df_avge,
        'avge2':df_avge2,

        })
    df.to_csv('files_tmp/combinations_runall_%s.csv' % daima)




@util.display_func_name
def allmaup(daima, days=200, scope=0.15):
    df = pd.read_csv('data/%s.xls' % daima)
    util.strip_columns(df)
    df = df.loc[:, ['date', 'open', 'close', 'low', 'ma5', 'ma10', 'ma20', 'ma40','KDJ.K', 'KDJ.D', 'KDJ.J']]

    df['up1'] = df['ma5'].shift(-1) > df['ma5'].shift(-2)
    df['up2'] = df['ma10'].shift(-1) > df['ma10'].shift(-2)
    df['up3'] = df['ma20'].shift(-1) > df['ma20'].shift(-2)
    df['up4'] = df['ma40'].shift(-1) > df['ma40'].shift(-2)
    df['allup'] =  df.up1 & df.up2 & df.up3 & df.up4
    df['earning'] = np.where(df['allup'], df.close.shift(days) - df.open, 0)

    df['stoploss_point'] = df.open * (1-scope)
    rolling_low = pd.rolling_min(df.low, days)
    df['stoploss'] = np.where(df['allup'], df.stoploss_point - df.open , 0)

    df['earning_with_stoploss'] = np.where(rolling_low > df.stoploss_point, df.earning, df.stoploss)
    
    func_name = sys._getframe().f_code.co_name
    df = df.loc[days: , :]  # 因为近期的看不到n天后的数据，所以没收益，因此不计算
    
    df.to_csv('files_tmp/%s_%s.csv' % (func_name, daima))  # 以函数名作为文件名保存

    df = df.where(df.earning != 0) # for count
    summ = df.earning.sum()
    summ2 = df.earning_with_stoploss.sum()

    count = df.earning.count() # count is same
    count2 = df.earning_with_stoploss.count()

    average_earnings =  summ / count
    average_earnings2 =  summ2 / count #

    print average_earnings, average_earnings2
    print summ, summ2
    print count, count2
    
    #return summ, average_earnings, summ2, average_earnings2, count


if __name__ == '__main__':

    #runn()
    #test_runall()
    daima = '000002'
    days = 200
    ma = 'ma20'
    scope = 0.3
    combinations_runall(daima, days=days, ma=ma, scope=scope)
    allmaup(daima, days=days, scope=scope)

    #foo('999999', days=3, scope=0.05)



    pass