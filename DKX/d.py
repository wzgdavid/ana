

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from common import *#get_DKX, get_nhh, get_nll, get_ma, avg,get_nhhzs,get_nllzs,get_atr


plt.rcParams['font.sans-serif'] = ['SimHei'] # 正常显示中文
#pinzhong = 'sr' # 跑的时候注意是不是要改一下这个变量

def ready(pinzhong):
    if pinzhong == 'rb':
        df = pd.read_csv(r'..\data\rb\zs.csv')
    else:
        df = pd.read_csv(r'..\data\{}.csv'.format(pinzhong))
    
    df = get_DKX(df)
    df = get_nhh(df, 2)
    df = get_nll(df, 2)
    df = get_ma(df, 20)
    
    '''
    --------------------------趋势判断1---------------------------------
    '''
    # 趋势判断，DKXb方向，1 向上   0向下  当天参照前两天
    #df['condition'] = np.where(df.b.shift(1)>df.b.shift(2), 1, 0) 
    # 趋势2   DKXb线在d线上做多，反之空
    df['condition'] = np.where(df.b.shift(1)>=df.d.shift(1), 1, 0) 
    
    
    
    # 开仓条件
    df = df.dropna(axis=0)
    df['高于前两天高点'] = np.where(df.h > df.nhh2, 1, None)   # 看当天 
    df['低于前两天低点'] = np.where(df.l < df.nll2, 1, None)
    # 开仓  bk开多  sk开空
    df['开仓'] = np.where((df['高于前两天高点'] == 1) & (df['condition']==1), 'bk', None)
    df['开仓'] = np.where((df['低于前两天低点'] == 1) & (df['condition']==0), 'sk', df['开仓'] )
    
    # 开仓  bk开多  sk开空
    # 多一个条件前一次开仓的止损移动过了，才能开仓(或者说，前一天低点比前两天低点高（做多）)
    # 这个开仓的次数少了，收益曲线的标准差小了
    # 起个名字，叫 渐进式开仓
    #df['开仓'] = np.where((df['高于前两天高点'] == 1) & (df['condition']==1) & (df.l.shift(1) > df.l.shift(2)), 'bk', None)
    #df['开仓'] = np.where((df['低于前两天低点'] == 1) & (df['condition']==0) & (df.h.shift(1) < df.h.shift(2)), 'sk', df['开仓'] )
    
    # 平仓 趋势反转 'bp' 平多  'sp' 平空
    #df['平仓'] = np.where((df.condition.shift(2) == 1) & (df.condition.shift(1) == 0), 'bp', None)
    #df['平仓'] = np.where((df.condition.shift(2) == 0) & (df.condition.shift(1) == 1), 'sp', df['平仓'])
    #df['平仓'] = None # 没有平仓信号， 只用止损平仓
    
    '''
    --------------------------趋势判断2---------------------------------
    '''
    # 趋势判断，K线在ma20上下，1 上   0下  当天参照前一天
    #df['condition'] = np.where(df.l.shift(1)>df.ma20.shift(1), 1, None) 
    #df['condition'] = np.where(df.h.shift(1)<df.ma20.shift(1), 0, df['condition']) 
    ## 开仓条件
    #df = df.dropna(axis=0)
    #df['高于前两天高点'] = np.where(df.h > df.nhh2, 1, None)   # 看当天 
    #df['低于前两天低点'] = np.where(df.l < df.nll2, 1, None)
    ## 开仓  bk开多  sk开空
    #df['开仓'] = np.where((df['高于前两天高点'] == 1) & (df['condition']==1), 'bk', None)
    #df['开仓'] = np.where((df['低于前两天低点'] == 1) & (df['condition']==0), 'sk', df['开仓'] )
    ## 平仓 趋势反转 'bp' 平多  'sp' 平空
    ##df['平仓'] = np.where((df['condition']==1, 'bp', None)
    ##df['平仓'] = np.where((df['低于前两天低点'] == 1) & (df['condition']==0), 'sp', df['平仓'])
    #df['平仓'] = None
    
    
    '''
    --------------------------趋势判断end---------------------------------
    '''
    
    #平仓的同时不反向开仓
    #df['开仓'] = np.where(df['平仓'].isnull(), df['开仓'], None)
    
    # 这个不能少
    dates = pd.DatetimeIndex(df.date)
    df.index = dates
    df = df.drop('date', axis=1)
    
    df['bk总手数'] = 0
    df['bkprice'] = 0
    #df['b持仓均价'] = 0  # 
    #df['b保证金'] = 0  #
    #df['b合约金额'] = 0  # 比如3000点买的螺纹， 实际合约价值是10吨，3万元
    df['是b止损'] = None
    df['sk总手数'] = 0
    df['skprice'] = 0 
    #df['s保证金'] = 0
    #df['s持仓均价'] = 0  #
    #df['s合约金额'] = 0
    df['是s止损'] = None
    df['余额占比'] = 0

    return df


def run1(df,zs, zj_init):
    '''
    每次遇到开仓信号都开仓
    每次只开一手， 三天低点开仓止损和移动止损（先统一止损点跑，简单）
    
    '''
    arr = np.zeros(df.shape[0])
    arr[0] = zj_init  # 
    df['可用余额'] = arr # 初始化可用余额
    df['总金额'] = arr
    df = get_nhhzs(df, zs)  # 做空止损
    df = get_nllzs(df, zs)  # 做多止损

    feiyong = 3 # 每次两个滑点， 再用一个滑点代替费用，共3点
    new_high = 0
    new_low = 99999
    rows_index = range(df.shape[0])
    for i in rows_index:
        row = df.iloc[i]  # 不变动的值判断用row， 赋值用df.ix
        last_row = df.iloc[i-1] if i > 0 else row
        if i == 0:
            continue
        ss = 1 # 每次新开仓手数
        if df.ix[i, 'sk总手数'] == 0: # 多空只能做一个方向
            if row['开仓'] == 'bk':
                df.ix[i, 'bkprice'] = bkprice = row.o + feiyong if row.o>row.nhh2 else row.nhh2 + feiyong
                df.ix[i, 'bk总手数'] = df.ix[i-1, 'bk总手数'] + ss  # 等于上一日的bk总手数加1
                df.ix[i, 'b止损'] = row.nll_zs
                df.ix[i, '可用余额'] = df.ix[i-1, '可用余额'] - bkprice * ss
                #df.ix[i, 'b保证金'] = df.ix[i-1, 'b保证金'] + bkprice * ss
                new_change = (row.c - bkprice) * ss * 10 # 新开仓价格变化
                old_change = (row.c - last_row.c) * df.ix[i-1, 'bk总手数'] *10# 旧开仓价格变化
                #print(new_change, old_change)
                df.ix[i, '总金额'] = df.ix[i-1, '总金额'] + new_change + old_change
            else: 
                df.ix[i, 'bk总手数'] = df.ix[i-1, 'bk总手数'] 
                df.ix[i, '可用余额'] = df.ix[i-1, '可用余额']
                #df.ix[i, 'b保证金'] = df.ix[i-1, 'b保证金']
                if df.ix[i, 'bk总手数'] == 0:
                    df.ix[i, 'b止损'] = new_high = 0
                else:
                    df.ix[i, 'b止损'] = new_high = max(df.ix[i, 'nll_zs'],  new_high)
                old_change = (row.c - last_row.c) * df.ix[i-1, 'bk总手数']*10# 旧开仓价格变化
                df.ix[i, '总金额'] = df.ix[i-1, '总金额'] + old_change

        if df.ix[i, 'bk总手数'] == 0: # 多空只能做一个方向
            if row['开仓'] == 'sk':
                df.ix[i, 'skprice'] = skprice = row.o -feiyong if row.o<row.nll2 else row.nll2 - feiyong
                df.ix[i, 'sk总手数'] = df.ix[i-1, 'sk总手数'] + ss  # 等于上一日的sk总手数加1
                df.ix[i, 's止损'] = row.nhh_zs
                df.ix[i, '可用余额'] = df.ix[i-1, '可用余额'] - skprice * ss
                #df.ix[i, 's保证金'] = df.ix[i-1, 's保证金'] + skprice * ss
                new_change = (skprice - row.c) * ss * 10 # 新开仓价格变化
                old_change = (last_row.c - row.c) * df.ix[i-1, 'sk总手数'] *10# 旧开仓价格变化
                #print(new_change, old_change)
                df.ix[i, '总金额'] = df.ix[i-1, '总金额'] + new_change + old_change
            else: 
                df.ix[i, 'sk总手数'] = df.ix[i-1, 'sk总手数'] 
                df.ix[i, '可用余额'] = df.ix[i-1, '可用余额']
                #df.ix[i, 's保证金'] = df.ix[i-1, 's保证金']
                if df.ix[i, 'sk总手数'] == 0:
                    df.ix[i, 's止损'] = new_low = 999999
                else:
                    df.ix[i, 's止损'] = new_low = min(df.ix[i, 'nhh_zs'],  new_low)
                    #print(df.ix[i, 's止损'],  i)
                old_change = (last_row.c - row.c) * df.ix[i-1, 'sk总手数'] *10# 旧开仓价格变化
                df.ix[i, '总金额'] = df.ix[i-1, '总金额'] + old_change

        # 处理止损
        if df.ix[i, 'bk总手数'] != 0: 
            if row.l <= df.ix[i, 'b止损'] and df.ix[i, 'bk总手数'] !=0:
                df.ix[i, '是b止损'] = 1
                change = (df.ix[i, 'b止损'] - last_row.c - feiyong)  * df.ix[i-1, 'bk总手数']* 10
                df.ix[i, '总金额'] = df.ix[i-1, '总金额'] + change
                df.ix[i, 'bk总手数'] = 0
                #df.ix[i, 'b保证金'] = 0
                df.ix[i, '可用余额'] = df.ix[i, '总金额']
        if df.ix[i, 'sk总手数'] != 0: 
            if row.h >= df.ix[i, 's止损'] and df.ix[i, 'sk总手数'] !=0:
                df.ix[i, '是s止损'] = 1
                change = (last_row.c - df.ix[i, 's止损'] - feiyong)  * df.ix[i-1, 'sk总手数']* 10
                df.ix[i, '总金额'] = df.ix[i-1, '总金额'] + change
                df.ix[i, 'sk总手数'] = 0
                #df.ix[i, 's保证金'] = 0
                df.ix[i, '可用余额'] = df.ix[i, '总金额']

        #df.ix[i,'余额占比'] = df.ix[i, '可用余额'] / df.ix[i, '总金额']

    df.to_csv('tmp1.csv')
    plt.plot(df['总金额'])
    plt.plot(df['可用余额'])
    plt.legend()
    title = 'run1'
    plt.title(title)
    plt.show()

#run1(df, 3, 100000)



def run2(pinzhong,zs, zj_init, f=0.01, maxcw=0.3, jiange=0):
    '''
    有资金管理
    zs 指前 zs 天的最低（高）点
    每次开仓允许的损失，f（当前总金额的百分比）
    maxcw, 允许最大仓位（当前总金额的百分比）
    '''
    df = ready(pinzhong)
    arr = np.zeros(df.shape[0])
    arr[0] = zj_init  # 
    df['可用余额'] = arr # 初始化可用余额
    df['总金额'] = arr
    df = get_nhhzs(df, zs)  # 做空止损
    df = get_nllzs(df, zs)  # 做多止损
    yue = 1 - maxcw # 反过来就是余额允许的最小比例
    feiyong = 3 # 每次两个滑点， 再用一个滑点代替费用，共3点
    new_high = 0
    new_low = 99999
    rows_index = range(df.shape[0])
    bk_idx = sk_idx = 0 # 每次开仓时的index
    b间隔 = s间隔 = jiange
    做多次数 = 做空次数 = 0
    for i in rows_index:
        row = df.iloc[i]  # 不变动的值判断用row， 赋值用df.ix
        last_row = df.iloc[i-1] if i > 0 else row
        if i == 0:
            continue
        if df.ix[i, 'sk总手数'] == 0: # 多空只能做一个方向
            bk_conditions = [
                row['开仓'] == 'bk',
                (df.ix[i-1, '可用余额'] / df.ix[i-1, '总金额']) > yue,
                i > (bk_idx + b间隔),
            ]
            #print('bk_idx',bk_idx, i)
            if all(bk_conditions):
            #if row['开仓'] == 'bk' and (df.ix[i-1, '可用余额'] / df.ix[i-1, '总金额']) > yue and i > bk_idx+b间隔:
                # 根据f算开几手
                bk_idx = i
                loss  = df.ix[i-1, '总金额'] * f
                zsrange = row.nhh2 - row.nll2
                ss = int(loss / (zsrange * 10))
                #print(loss,zsrange,ss)

                df.ix[i, 'bkprice'] = bkprice = row.o + feiyong if row.o>row.nhh2 else row.nhh2 + feiyong
                df.ix[i, 'bk总手数'] = df.ix[i-1, 'bk总手数'] + ss  # 等于上一日的bk总手数加1
                df.ix[i, 'b止损'] = row.nll_zs  ##############################-10
                df.ix[i, '可用余额'] = df.ix[i-1, '可用余额'] - bkprice * ss
                #df.ix[i, 'b保证金'] = df.ix[i-1, 'b保证金'] + bkprice * ss
                new_change = (row.c - bkprice) * ss * 10 # 新开仓价格变化
                old_change = (row.c - last_row.c) * df.ix[i-1, 'bk总手数'] *10# 旧开仓价格变化
                #print(new_change, old_change)
                df.ix[i, '总金额'] = df.ix[i-1, '总金额'] + new_change + old_change
                做多次数 += 1
            else: 
                df.ix[i, 'bk总手数'] = df.ix[i-1, 'bk总手数'] 
                df.ix[i, '可用余额'] = df.ix[i-1, '可用余额']
                #df.ix[i, 'b保证金'] = df.ix[i-1, 'b保证金']
                if df.ix[i, 'bk总手数'] == 0:
                    df.ix[i, 'b止损'] = new_high = 0
                else:
                    df.ix[i, 'b止损'] = new_high = max(df.ix[i, 'nll_zs'],  new_high)
                old_change = (row.c - last_row.c) * df.ix[i-1, 'bk总手数']*10# 旧开仓价格变化
                df.ix[i, '总金额'] = df.ix[i-1, '总金额'] + old_change

        if df.ix[i, 'bk总手数'] == 0: # 多空只能做一个方向
            sk_conditions = [
                row['开仓'] == 'sk',
                (df.ix[i-1, '可用余额'] / df.ix[i-1, '总金额']) > yue,
                i > (sk_idx + s间隔),
            ]
            if all(sk_conditions):
            #if row['开仓'] == 'sk'and (df.ix[i-1, '可用余额'] / df.ix[i-1, '总金额']) > yue:
                # 根据f算开几手
                sk_idx = i
                loss  = df.ix[i-1, '总金额'] * f
                zsrange = row.nhh2 - row.nll2
                ss = int(loss / (zsrange * 10))
                #print(loss,zsrange,ss)
                df.ix[i, 'skprice'] = skprice = row.o -feiyong if row.o<row.nll2 else row.nll2 - feiyong
                df.ix[i, 'sk总手数'] = df.ix[i-1, 'sk总手数'] + ss  # 等于上一日的sk总手数加1
                df.ix[i, 's止损'] = row.nhh_zs ################################+ 10
                df.ix[i, '可用余额'] = df.ix[i-1, '可用余额'] - skprice * ss
                #df.ix[i, 's保证金'] = df.ix[i-1, 's保证金'] + skprice * ss
                new_change = (skprice - row.c) * ss * 10 # 新开仓价格变化
                old_change = (last_row.c - row.c) * df.ix[i-1, 'sk总手数'] *10# 旧开仓价格变化
                #print(new_change, old_change)
                df.ix[i, '总金额'] = df.ix[i-1, '总金额'] + new_change + old_change
                做空次数 += 1
            else: 
                df.ix[i, 'sk总手数'] = df.ix[i-1, 'sk总手数'] 
                df.ix[i, '可用余额'] = df.ix[i-1, '可用余额']
                #df.ix[i, 's保证金'] = df.ix[i-1, 's保证金']
                if df.ix[i, 'sk总手数'] == 0:
                    df.ix[i, 's止损'] = new_low = 999999
                else:
                    df.ix[i, 's止损'] = new_low = min(df.ix[i, 'nhh_zs'],  new_low)
                    #print(df.ix[i, 's止损'],  i)
                old_change = (last_row.c - row.c) * df.ix[i-1, 'sk总手数'] *10# 旧开仓价格变化
                df.ix[i, '总金额'] = df.ix[i-1, '总金额'] + old_change

        # 处理止损
        if df.ix[i, 'bk总手数'] != 0: 
            if row.l <= df.ix[i, 'b止损']:
                df.ix[i, '是b止损'] = 1
                zsprice = df.ix[i, 'b止损'] if row.o >= df.ix[i, 'b止损'] else row.o
                change = (zsprice - last_row.c - feiyong)  * df.ix[i-1, 'bk总手数']* 10
                df.ix[i, '总金额'] = df.ix[i-1, '总金额'] + change
                df.ix[i, 'bk总手数'] = 0
                #df.ix[i, 'b保证金'] = 0
                df.ix[i, '可用余额'] = df.ix[i, '总金额']
        if df.ix[i, 'sk总手数'] != 0: 
            if row.h >= df.ix[i, 's止损']:
                df.ix[i, '是s止损'] = 1
                zsprice = df.ix[i, 's止损'] if row.o <= df.ix[i, 's止损'] else row.o
                change = (last_row.c - zsprice - feiyong)  * df.ix[i-1, 'sk总手数']* 10
                df.ix[i, '总金额'] = df.ix[i-1, '总金额'] + change
                df.ix[i, 'sk总手数'] = 0
                #df.ix[i, 's保证金'] = 0
                df.ix[i, '可用余额'] = df.ix[i, '总金额']

        #df.ix[i,'余额占比'] = df.ix[i, '可用余额'] / df.ix[i, '总金额']
        #if i > 100:
        #    break
    #df.to_csv('tmp2.csv')
    #plt.plot(df['总金额'])
    ##plt.plot(df['可用余额'])
    #plt.legend()
    params = {
        'pinzhong': pinzhong,
        'zj_init': zj_init,
        'zs': zs,
        'f': f,
        'maxcw': maxcw,
        'jiange': jiange,
        '做多次数': 做多次数,
        '做空次数': 做空次数,
        
    }
    result_row = result(df, params)
    return result_row


'''
参数： run2 zs=2  开仓间隔=0 f=0.02  maxcw=0.3
资金增长倍数：105
做多次数:281 做空次数:279
标准差： 0.02722

参数： run3 zs=2  f=0.02  maxcw=0.3
总金额增长间隔：0   总金额减少间隔：0
总金额增长f：0.03   总金额减少f：0.02
资金增长倍数：155
做多次数:269 做空次数:260
标准差： 0.02893

参数： run2 zs=2  开仓间隔=1 f=0.02  maxcw=0.3   11
资金增长倍数：74
做多次数:213 做空次数:212
标准差： 0.02075

参数： run2 zs=2  开仓间隔=0 f=0.02  maxcw=0.4
资金增长倍数：169
做多次数:317 做空次数:314
标准差： 0.02974



参数： run2 zs=3  开仓间隔=0 f=0.02  maxcw=0.3
资金增长倍数：123
做多次数:239 做空次数:244
标准差： 0.02964

参数： run2 zs=2  开仓间隔=0 f=0.03  maxcw=0.3
资金增长倍数：299
做多次数:231 做空次数:233
标准差： 0.03315



渐进式开仓
参数： run2 zs=2  开仓间隔=0 f=0.02  maxcw=0.3
资金增长倍数：41
做多次数:224 做空次数:224
标准差： 0.02199
'''



def run3(df,zs, zj_init, f=0.02, maxcw=0.3):
    '''
    有资金管理
    zs 指前 zs 天的最低（高）点
    每次开仓允许的损失，f（当前总金额的百分比）
    maxcw, 允许最大仓位（当前总金额的百分比）

    在run2的基础上，变动开仓间隔，
    总资金变多了，开仓间隔变小, 或者f变大
    总资金变少了，开仓间隔变大，或者f变小
    '''
    arr = np.zeros(df.shape[0])
    arr[0] = zj_init  # 
    df['可用余额'] = arr # 初始化可用余额
    df['总金额'] = arr
    df = get_nhhzs(df, zs)  # 做空止损
    df = get_nllzs(df, zs)  # 做多止损
    yue = 1 - maxcw # 反过来就是余额允许的最小比例
    feiyong = 3 # 每次两个滑点， 再用一个滑点代替费用，共3点
    new_high = 0
    new_low = 99999
    rows_index = range(df.shape[0])
    bk_idx = sk_idx = 0 # 每次开仓时的index
    做多次数 = 做空次数 = 0
    jiange = 0
    for i in rows_index:
        row = df.iloc[i]  # 不变动的值判断用row， 赋值用df.ix
        last_row = df.iloc[i-1] if i > 0 else row
        if i == 0:
            continue

        if df.ix[i, 'sk总手数'] == 0: # 多空只能做一个方向
            bk_conditions = [
                row['开仓'] == 'bk',
                (df.ix[i-1, '可用余额'] / df.ix[i-1, '总金额']) > yue,
                i > (bk_idx + jiange),
            ]
            #print('bk_idx',bk_idx, i)
            if all(bk_conditions):
            #if row['开仓'] == 'bk' and (df.ix[i-1, '可用余额'] / df.ix[i-1, '总金额']) > yue and i > bk_idx+b间隔:
                # 根据f算开几手
                bk_idx = i
                loss  = df.ix[i-1, '总金额'] * f
                zsrange = row.nhh2 - row.nll2
                ss = int(loss / (zsrange * 10))
                #print(loss,zsrange,ss)

                df.ix[i, 'bkprice'] = bkprice = row.o + feiyong if row.o>row.nhh2 else row.nhh2 + feiyong
                df.ix[i, 'bk总手数'] = df.ix[i-1, 'bk总手数'] + ss  # 等于上一日的bk总手数加1
                df.ix[i, 'b止损'] = row.nll_zs  ##############################-10
                df.ix[i, '可用余额'] = df.ix[i-1, '可用余额'] - bkprice * ss
                #df.ix[i, 'b保证金'] = df.ix[i-1, 'b保证金'] + bkprice * ss
                new_change = (row.c - bkprice) * ss * 10 # 新开仓价格变化
                old_change = (row.c - last_row.c) * df.ix[i-1, 'bk总手数'] *10# 旧开仓价格变化
                #print(new_change, old_change)
                df.ix[i, '总金额'] = df.ix[i-1, '总金额'] + new_change + old_change
                做多次数 += 1
            else: 
                df.ix[i, 'bk总手数'] = df.ix[i-1, 'bk总手数'] 
                df.ix[i, '可用余额'] = df.ix[i-1, '可用余额']
                #df.ix[i, 'b保证金'] = df.ix[i-1, 'b保证金']
                if df.ix[i, 'bk总手数'] == 0:
                    df.ix[i, 'b止损'] = new_high = 0
                else:
                    df.ix[i, 'b止损'] = new_high = max(df.ix[i, 'nll_zs'],  new_high)
                old_change = (row.c - last_row.c) * df.ix[i-1, 'bk总手数']*10# 旧开仓价格变化
                df.ix[i, '总金额'] = df.ix[i-1, '总金额'] + old_change

        if df.ix[i, 'bk总手数'] == 0: # 多空只能做一个方向
            sk_conditions = [
                row['开仓'] == 'sk',
                (df.ix[i-1, '可用余额'] / df.ix[i-1, '总金额']) > yue,
                i > (sk_idx + jiange),
            ]
            if all(sk_conditions):
            #if row['开仓'] == 'sk'and (df.ix[i-1, '可用余额'] / df.ix[i-1, '总金额']) > yue:
                # 根据f算开几手
                sk_idx = i
                loss  = df.ix[i-1, '总金额'] * f
                zsrange = row.nhh2 - row.nll2
                ss = int(loss / (zsrange * 10))
                #print(loss,zsrange,ss)
                df.ix[i, 'skprice'] = skprice = row.o -feiyong if row.o<row.nll2 else row.nll2 - feiyong
                df.ix[i, 'sk总手数'] = df.ix[i-1, 'sk总手数'] + ss  # 等于上一日的sk总手数加1
                df.ix[i, 's止损'] = row.nhh_zs ################################+ 10
                df.ix[i, '可用余额'] = df.ix[i-1, '可用余额'] - skprice * ss
                #df.ix[i, 's保证金'] = df.ix[i-1, 's保证金'] + skprice * ss
                new_change = (skprice - row.c) * ss * 10 # 新开仓价格变化
                old_change = (last_row.c - row.c) * df.ix[i-1, 'sk总手数'] *10# 旧开仓价格变化
                #print(new_change, old_change)
                df.ix[i, '总金额'] = df.ix[i-1, '总金额'] + new_change + old_change
                做空次数 += 1
            else: 
                df.ix[i, 'sk总手数'] = df.ix[i-1, 'sk总手数'] 
                df.ix[i, '可用余额'] = df.ix[i-1, '可用余额']
                #df.ix[i, 's保证金'] = df.ix[i-1, 's保证金']
                if df.ix[i, 'sk总手数'] == 0:
                    df.ix[i, 's止损'] = new_low = 999999
                else:
                    df.ix[i, 's止损'] = new_low = min(df.ix[i, 'nhh_zs'],  new_low)
                    #print(df.ix[i, 's止损'],  i)
                old_change = (last_row.c - row.c) * df.ix[i-1, 'sk总手数'] *10# 旧开仓价格变化
                df.ix[i, '总金额'] = df.ix[i-1, '总金额'] + old_change

        # 处理止损
        if df.ix[i, 'bk总手数'] != 0: 
            if row.l <= df.ix[i, 'b止损']:
                df.ix[i, '是b止损'] = 1
                zsprice = df.ix[i, 'b止损'] if row.o >= df.ix[i, 'b止损'] else row.o
                change = (zsprice - last_row.c - feiyong)  * df.ix[i-1, 'bk总手数']* 10
                df.ix[i, '总金额'] = df.ix[i-1, '总金额'] + change
                df.ix[i, 'bk总手数'] = 0
                #df.ix[i, 'b保证金'] = 0
                df.ix[i, '可用余额'] = df.ix[i, '总金额']
        if df.ix[i, 'sk总手数'] != 0: 
            if row.h >= df.ix[i, 's止损']:
                df.ix[i, '是s止损'] = 1
                zsprice = df.ix[i, 's止损'] if row.o <= df.ix[i, 's止损'] else row.o
                change = (last_row.c - zsprice - feiyong)  * df.ix[i-1, 'sk总手数']* 10
                df.ix[i, '总金额'] = df.ix[i-1, '总金额'] + change
                df.ix[i, 'sk总手数'] = 0
                #df.ix[i, 's保证金'] = 0
                df.ix[i, '可用余额'] = df.ix[i, '总金额']
        总金额增长间隔 = 0 # 收益增长时，多做，反之少做，通过间隔控制
        总金额减少间隔 = 0 # 看下来作用不明显
        总金额增长f = 0.03
        总金额减少f = f
        if df.ix[i, '总金额'] > df.ix[i-1, '总金额']:
            jiange = 总金额增长间隔
            f = 总金额增长f
        else:
            jiange = 总金额减少间隔
            f = 总金额减少f
        #df.ix[i,'余额占比'] = df.ix[i, '可用余额'] / df.ix[i, '总金额']
        #if i > 100:
        #    break
    #df.to_csv('tmp2.csv')
    #plt.plot(df['总金额'])
    ##plt.plot(df['可用余额'])
    #plt.legend()
    title = 'run3 zs={}  f={}  maxcw={}'.format(zs, f, maxcw)
    #plt.title(title)
    #plt.show()
    print('参数：', title)
    print('总金额增长间隔：{}   总金额减少间隔：{}'.format(总金额增长间隔,总金额减少间隔))
    print('总金额增长f：{}   总金额减少f：{}'.format(总金额增长f,总金额减少f))
    print('资金增长倍数：{}'.format( int(df.ix[-1, '总金额']/zj_init) ))
    print('做多次数:{} 做空次数:{}'.format(做多次数, 做空次数))
    result(df,title=title)

#run3(df, 2, 100000, maxcw=0.3)
'''
参数： run3 zs=2  f=0.02  maxcw=0.3
总金额增长间隔：0   总金额减少间隔：0
总金额增长f：0.01   总金额减少f：0.02
资金增长倍数：25
做多次数:243 做空次数:244
标准差： 0.01762

参数： run3 zs=2  f=0.01  maxcw=0.3
总金额增长间隔：0   总金额减少间隔：0
总金额增长f：0.02   总金额减少f：0.01
资金增长倍数：21
做多次数:246 做空次数:249
标准差： 0.0182

参数： run3 zs=2  f=0.02  maxcw=0.3
总金额增长间隔：0   总金额减少间隔：0
总金额增长f：0.03   总金额减少f：0.02
资金增长倍数：47
做多次数:211 做空次数:207
标准差： 0.0247
'''


if __name__ == '__main__':
    #run2(df, 2, 100000, f=0.02, maxcw=0.3)
    #run2(df, 2, 100000, f=0.02, maxcw=0.4)
    run2(df, 2, 100000, f=0.02, maxcw=0.3, jiange=0)
