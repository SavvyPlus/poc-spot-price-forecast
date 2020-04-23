import logging
import datetime
import ujson as json
import pandas as pd
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


def convert_pkl_json(in_path, out_path):
    data = pd.read_pickle(in_path)
    if type(data) == list:
        data = {'data': data}         
    try:
        with open(out_path, 'w') as fp:
            json.dump(data, fp, indent=8)            
    except Exception as e:
        logging.error(e)



def create_csv(vals, header=None, delimiter=",", byte=False):
    """
    file_path + csv ex: abc/ef.csv
    if file_path is not none -> save to file
    else return bytes
    header is an array
    vals is an array of array
    *Note all header and vals are string type
    """
    # list of string val with comma
    def join_val(val):
        val = [str(v) for v in val]
        return delimiter.join(val)

    vals_comma = [join_val(val) for val in vals]
    # string full  vals with newline
    full_content = "\n".join(vals_comma)

    if header is not None:
        header = delimiter.join(header)
        full_content = header + "\n" + full_content

    if byte:
        full_content = full_content.encode()
        return full_content
    else:
        return full_content
        