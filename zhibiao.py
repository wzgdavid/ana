import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tushare as ts

def kdj(df):
    rsv = (df['close'] - df['low'])
    df['rsv'] = rsv
    print df
