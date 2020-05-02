"""
"""


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
