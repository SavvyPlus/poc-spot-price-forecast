"""
"""

import pandas as pd


def create_date_range(start, end, freq):
    date_range = pd.date_range(start=start, end=end, freq=freq)
    return date_range


def create_df_ts_blank(start, end, freq, value_cols, dt_col='dt', value=-999):
    date_ragnge = create_date_range(start, end, freq)
    df = pd.DataFrame(date_ragnge, columns=[dt_col])
    for col in value_cols:
        df[col] = value
    return df


def add_new_col_func(df, col_name, func, *args, **kwargs):
    df.loc[: col_name] = df.apply(lambda row:
                                  func(row, args, kwargs),
                                  axis=1)




