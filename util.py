import sys


def strip_columns(df):
    df.columns = [col.strip() for col in df.columns]


def display_func_name(func):
    def _deco(*args, **kwargs):
        #print '-----------', func.__name__, '-----------'
        #print '-------------%s--------------' % func.__name__
        return func(*args, **kwargs)
    return _deco
