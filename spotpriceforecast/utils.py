import datetime
from dateutil.parser import parse

def future_date_from_str(ds, delta=0, format="%Y-%m-%d"):
    dt = parse(ds)
    next_dt = dt + datetime.timedelta(days=delta)
    if format is None:
        return dt
    return next_dt.strftime(format)


def get_index_pv(time_str):
    """pv data has 48 rows for one day
    we need data for every 5min
    """
    a = 0
    hour, minute, _ = time_str.split(':')
    hour = int(hour)
    minute = int(minute)

    if minute > 30:
        a = 1    
    index = hour*2 + a
    return index

# print(future_date_from_str('2017-12-31', 365*2))
# print(get_index_pv('2:35:00'))