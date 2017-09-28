def get_atr(df, n):
    '''TR : MAX( MAX( (HIGH-LOW),ABS(REF(CLOSE,1)-HIGH) ), ABS(REF(CLOSE,1)-LOW));文华的公式
    '''
    df['hl'] = df.h - df.l
    df['ch'] = abs(df.c.shift(1) - df.h)
    df['cl'] = abs(df.c.shift(1) - df.l)
    df['tr'] = df.loc[:, ['hl','ch', 'cl']].apply(lambda x: x.max(), axis=1)
    df['atr'] = df.tr.rolling(window=n, center=False).mean()
    #df = df.drop(['hl', 'ch','cl','tr'], axis=1)
    return df['atr']

def get_ma(df, n):
    df['ma'] = df.c.rolling(window=n, center=False).mean()

    return df['ma']

def get_nhh(df, n):
    df['nhh'] =df.h.rolling(window=n, center=False).max()
    return df['nhh']

def get_nhhst(df, n):
    df['nhhst'] =df.st_h.rolling(window=n, center=False).max()
    return df['nhhst']

def get_nll(df, n):
    df['nll'] =df.l.rolling(window=n, center=False).min()
    return df['nhh']

def get_nllst(df, n):
    df['nllst'] =df.st_l.rolling(window=n, center=False).min()
    return df['nllst']