# encoding: utf-8
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tushare as ts
import util

# tushare 的数据不准 节假日会多一天多余的数据

def foo(daima, days=5, scope=0.05):
    '''没条件  买进 看n天后收益'''
    df = pd.read_csv('data/%s.xls' % daima)
    util.strip_columns(df)
    df = df.loc[:, ['date', 'open', 'close', 'low']]

    df['earning'] = df.close.shift(days) - df.open
    df['stoploss_point'] = df.open * (1-scope)
    rolling_low = pd.rolling_min(df.low, days)
    df['stoploss'] = df.stoploss_point - df.open

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
#print '--------------------'
#foo3('hs300', ma='ma20', days=150, scope=0.15)
#print '--------------------'
#foo3b('zxb', ma='ma20', days=150)

def maup(daima, ma='ma5', days=5, scope=0.05):
    '''今天ma大于昨天ma 买进 看n天后收益
    '''
    df = pd.read_csv('data/%s.xls' % daima)
    util.strip_columns(df)
    df = df.loc[:, ['date', 'open', 'low', 'close', 'ma5', 'ma10', 'ma20']]

    # today ma larger than yesterday ma
    df['maup'] = df[ma] > df[ma].shift(-1)
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
#maup('zxb', ma='ma5', days=111, scope=0.15)
#foo3('zxb', ma='ma10', days=111, scope=0.15)


def foo3_maup(daima, ma='ma5', days=5, scope=0.05):
    '''前一天整K大于ma,and 今天ma大于昨天ma  买进 看n天后收益
    '''
    df = pd.read_csv('data/%s.xls' % daima)
    util.strip_columns(df)
    df = df.loc[:, ['date', 'open', 'close', 'low', 'ma5', 'ma10', 'ma20']]

    # yesterday greater than ma
    df['gt_ma'] = df.low.shift(-1) > df[ma].shift(-1)
    df['earning'] = np.where(df['gt_ma'], df.close.shift(days) - df.open, 0)
    
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


def foo4(daima, scope=0.05, hold_days=5):
    '''stop loss

    '''

    df = ts.get_hist_data(daima,)
    df = df.loc[ :, ['open', 'close', 'high', 'low'] ]
    df['rolling_low'] = pd.rolling_min(df.low, hold_days)
    df['stop_loss'] = df.open * (1- scope)
    # df['earnings'] = if rolling_low > stop_loss   ?  open.shift(hold_days) - df.open : df.stop_loss - df.open
    # df['logic'] = np.where(df['AAA'] > 5,'high','low')
    df['earnings'] = np.where(df.rolling_low > df.stop_loss , df.open.shift(hold_days) - df.open ,df.stop_loss - df.open)
    #print df
    df.to_csv('files_tmp/foo4.csv')
    #return df[''].sum()

#foo4('hs300', hold_days=30)


def foo5(daima, scope=0.05, hold_days=5, ma1='ma5', ma2='ma10'):
    '''
    ma cross up 
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
    #print average_earnings
    print summ 
    print count
    print 'en-----------------d--------------------'
    return summ, count, average_earnings


#foo5('zxb', scope=0.06, hold_days=250, ma1='ma5', ma2='ma10')  # 
#print foo5('hs300', scope=0.15, hold_days=300, ma1='ma5', ma2='ma10')  # 

#foo5('cyb', scope=0.05, hold_days=250, ma1='ma5', ma2='ma10')  
#foo2('cyb', scope=0.05, days=250, ma1='ma5', ma2='ma10')  

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
    #print 'en-----------------d--------------------'
    #return summ, count, average_earnings

#move_stop_loss('hs300', 0.05)


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