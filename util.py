def strip_columns(df):
    df.columns = [col.strip() for col in df.columns]