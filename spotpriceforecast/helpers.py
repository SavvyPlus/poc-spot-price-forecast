"""
"""

import pandas as pd
from dateutil.parser import parse

import holidays


def encode_day_type_df(df_row, dt_col, country='AU', state=None):
    """sunday/holiday = 2, startuday = 1, weekday = 0
    """
    code = 0
    dt_text = df_row[dt_col]
    date_text = dt_text.split()[0]
            
    au_holidays = holidays.CountryHoliday(country, prov=state)
    if date_text in au_holidays:
        code = 2
        return code
    
    dt = parse(dt_text)
    weekno = dt.weekday()
    # Saturday
    if weekno == 5:
        code = 1
    # Sunday
    if weekno == 6:
        code = 2
    return code


def encode_day_of_year_df(df_row, dt_col):
    """https://stackoverflow.com/questions/620305/convert-year-month-day-to-day-of-year-in-python
    """
    dt_text = df_row[dt_col]
    dt = parse(dt_text)
    day_of_year = dt.timetuple().tm_yday
    return day_of_year


def encode_week_number(df_row, dt_col):
    """
    """
    dt_text = df_row[dt_col]
    dt = parse(dt_text)
    week = dt.date().isocalendar()[1]
    return week


def encode_freq_index(df_row, dt_col, periods=289, freq='5min'):
    """
    """
    dt_text = df_row[dt_col]
    day_text = dt_text.split()[0]
    idxes_time = pd.date_range(day_text, periods=periods, freq=freq)
    idxes_time = [str(i) for i in idxes_time]
    period_id = idxes_time.index(dt_text)
    return period_id    


def encode_season_au_df(df_row, dt_col):
    """spring, summer, autumn, winter = 0, 1, 2, 3
    """
    season = 0
    dt_text = df_row[dt_col]
    dt = parse(dt_text)
    month = dt.month
    if month in [9, 10, 11]:
        season = 0
    if month in [12, 1, 2]:
        season = 1
    if month in [3, 4, 5]:
        season = 2
    if month in [6, 7, 8]:
        season = 3
    return season


def encode_time_df(df_row, dt_col):
    """0-6: 0
    6-9:1
    9-18:2
    18-21:3
    21-0:4
    """
    t = 0
    dt_text = df_row[dt_col]
    dt = parse(dt_text)
    h = dt.hour
    if h > 0 and h <= 6:
        t = 0
    if h > 6 and h <= 9:
        t = 1
    if h > 9 and h <= 18:
        t = 2
    if h > 18 and h <= 21:
        t = 3
    if h > 21:
        t = 4    
    return t



def add_daytype_to_df(df, dt_col, country='AU', state=None):
    """
    """
    df.loc[:, 'daytype'] = df.apply(lambda row:
                                    encode_day_type_df(row,
                                                       dt_col,
                                                       country,
                                                       state),
                                    axis=1)
    return df


def add_day_of_year_df(df, dt_col):
    """
    """
    df.loc[:, 'dayofyear'] = df.apply(lambda row:
                                      encode_day_of_year_df(row,
                                                       dt_col),
                                     axis=1)
    return df


def add_season_au_df(df, dt_col):
    """
    """
    df.loc[:, 'season'] = df.apply(lambda row:
                                    encode_season_au_df(row,
                                                        dt_col),
                                     axis=1)
    return df


def add_time_df(df, dt_col):
    """
    """
    df.loc[:, 'time'] = df.apply(lambda row:
                                 encode_time_df(row,
                                                dt_col),
                                 axis=1)
    return df


def add_week_df(df, dt_col):
    """
    """
    df.loc[:, 'week'] = df.apply(lambda row:
                                 encode_week_number(row,
                                                dt_col),
                                 axis=1)
    return df


def add_freq_index(df, dt_col, periods=289, freq='5min'):
    """
    """
    df.loc[:, 'period'] = df.apply(lambda row:
                                   encode_freq_index(row,
                                                     dt_col, 
                                                     periods=periods,
                                                     freq=freq),
                                   axis=1)
    return df