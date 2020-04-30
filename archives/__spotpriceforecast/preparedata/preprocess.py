import pandas as pd

def convert_inter_conector_to_list(d_dict, date_str, freq='5min'):        
    obj_keys = list(d_dict.keys())
    periods = len(obj_keys)
    idxes_time = pd.date_range(date_str, periods=periods, freq=freq)            
    header = list(d_dict[obj_keys[0]].keys())
    results = []

    for i, dt in enumerate(idxes_time):
        current_obj = d_dict[i]
        row = []
        row.append(str(dt))
        for h in header:
            row.append(current_obj[h])
        results.append(row)

    header = ['date'] + header

    return header, results
    



