# encoding: utf-8
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tushare as ts
import zhibiao as zb
# tushare 的数据不准 节假日会多一天多余的数据

def foo():

    df = ts.get_hist_data('hs300', start='2016-01-01')
    df = df.loc[:, ['open', 'high', 'close', 'low', 'ma5', 'ma10', 'ma20']]
    df['k_crossup_ma5'] = df.open > df.ma5
    #df['open_shift_1'] = df['open'].shift(1)
    df.open
    print df

def foo2(daima, ma1='ma5', ma2='ma10', days=5):
    '''ma cross up'''
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
#run_foo2()
    






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

def run_foo4():
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
#run_foo4()



def foo5(daima, scope=0.05, hold_days=5, ma1='ma5', ma2='ma10'):
    '''
    ma cross up
    and
    stop loss

    '''

    #df = ts.get_hist_data(daima)
    df = pd.read_csv('data/%s.xls' % daima)
    df = df.loc[ :, ['open', 'close', 'high', 'low', 'ma5', 'ma10', 'ma20'] ]
    df['rolling_low'] = pd.rolling_min(df.low, hold_days)
    df['stop_loss'] = df.open * (1- scope)
    # df['earnings'] = if rolling_low > stop_loss   ?  open.shift(hold_days) - df.open : df.stop_loss - df.open
    # df['logic'] = np.where(df['AAA'] > 5,'high','low')
    df['earnings'] = np.where(df.rolling_low > df.stop_loss , df.open.shift(hold_days) - df.open ,df.stop_loss - df.open)
   
    ma5_crossup_10 = (df[ma1].shift(-2) < df[ma2].shift(-2)) & (df[ma1].shift(-1) > df[ma2].shift(-1))
    #ma5_crossdown_10 = (df.ma5.shift(-2) > df.ma10.shift(-2)) & (df.ma5.shift(-1) < df.ma10.shift(-1))
    
    df['ma5_up_10'] = np.where(ma5_crossup_10, True, None)
    df['ma_cross_earnings'] = df.earnings * df.ma5_up_10
    #df.to_csv('files_tmp/foo4.csv')
    summ = df.ma_cross_earnings.shift(hold_days * -1 + 1).sum() # 不计算没有rolling_low的行
    count = df.ma_cross_earnings.shift(hold_days * -1 + 1).count()
    average_earnings =  summ / count 
    #print average_earnings
    #print summ 
    #print count
    #print 'en-----------------d--------------------'
    return summ, count, average_earnings


#foo5('zxb', scope=0.06, hold_days=250, ma1='ma5', ma2='ma10')  # avg 1468   sum 38186   
#foo5('hs300', scope=0.05, hold_days=250, ma1='ma5', ma2='ma10')  #  795  23069
#foo5('hs300', scope=0.06, hold_days=250, ma1='ma5', ma2='ma10')
#foo5('cyb', scope=0.05, hold_days=250, ma1='ma5', ma2='ma10')  


def run_foo5(daima):
    scopes = np.arange(0.05, 0.3, 0.01)
    hold_days = [100,150,200,250,280,290,300,310,330, 350, 370]
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
    

#run_foo5('hs300')


def foo6(daima, scope=0.05, hold_days=5, ma='ma5'):
    '''
    open and close  > ma
    and
    stop loss

    '''
    df = ts.get_hist_data(daima,)
    df = df.loc[ :, ['open', 'close', 'high', 'low', 'ma5', 'ma10', 'ma20'] ]
    df['rolling_low'] = pd.rolling_min(df.low, hold_days)
    #df['has_rolling_low'] =np.where(df.rolling_low == None, False, True)
    df['stop_loss'] = df.open * (1- scope)

    df['earnings'] = np.where(df.rolling_low > df.stop_loss , df.open.shift(hold_days) - df.open ,df.stop_loss - df.open)
    
    openclose_gt_ma = (df.open > df[ma]) & (df.close > df[ma]) 
    
    df['openclose_gt_ma'] = np.where(openclose_gt_ma, True, None)
    df['gt_ma_earnings'] = df.earnings * df.openclose_gt_ma
    #df.to_csv('files_tmp/foo4.csv')
    summ = df.gt_ma_earnings.shift(hold_days * -1 + 1).sum()
    count = df.gt_ma_earnings.shift(hold_days * -1 + 1).count()
    average_earnings =  summ / count 
    #print summ
    #print count
    print average_earnings
    #return df[''].sum()

#foo6('cyb', scope=0.08, hold_days=200, ma='ma10')

def move_stop_loss(daima, scope=0.05, hold_days=100):


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

move_stop_loss('hs300', 0.05)