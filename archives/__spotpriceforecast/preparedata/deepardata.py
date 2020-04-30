"""
"""

import json
import logging

import pandas as pd
from dateutil.parser import parse

from spotpriceforecast import utils


def create_date_spot_demand(spot_path, demand_path, state, 
                            start_date, max_days, out_path):
    """
    """
    data = []

    for i in range(0, max_days):
        date = utils.future_date_from_str(start_date, i)
        spot_file = spot_path.format(date)
        demand_file = demand_path.format(date)

        spot_data = pd.read_pickle(spot_file)
        demand_data = pd.read_pickle(demand_file)

        for day_key in spot_data:
            try:
                spot = spot_data[day_key][state]
                demand = demand_data[day_key][state]
                row = [day_key, spot, demand]
                data.append(row)
            except KeyError:
                break
    
    df = pd.DataFrame(data, columns=['date', 'spot', 'demand'])
    df = df.sort_values(by=['date'])
    df.to_csv(out_path, index=False, header=False)


def create_date_spot_demand_pv(spot_demand_csv, pv_path, state, out_path):
    """
    """
    df = pd.read_csv(spot_demand_csv)
    data = df.values.tolist()
    pv_values = pd.read_pickle(pv_path)    

    for row in data:
        date = row[0]
        day, time_str = date.split()
        day_key = parse(day).date()
        pv_index = utils.get_index_pv(time_str)
        pv_value = pv_values[state][day_key][pv_index]
        row.append(pv_value)
    
    df = pd.DataFrame(data, 
                      columns=['date', 'spot', 'demand', 'pv'])    
    df = df.sort_values(by=['date'])
    df.to_csv(out_path, index=False, header=False)


def split_date_spot_demand_pv(csv_path, year, train_csv, test_csv):
    """
    """
    df = pd.read_csv(csv_path, parse_dates=[0])    
    df.columns = ['date', 'spot', 'demand', 'pv']
    

    df_train = df[df['date'].dt.year < year]
    df_test = df[df['date'].dt.year == year]

    df_train.to_csv(train_csv, index=False, header=False)
    df_test.to_csv(test_csv, index=False, header=False)


def get_deepar_format(csv_path, target_idx=1, features_idx=[]):
    """
    """
    df = pd.read_csv(csv_path)
    data = df.values.tolist()
    
    target = []
    dynamic_feat = [[] for i in range(len(features_idx))]  

    for row in data:
        target.append(row[target_idx])
        for j in range(len(features_idx)):
            dynamic_feat[j].append(row[features_idx[j]])
    
    for k in range(len(dynamic_feat)):
        assert len(target) == len(dynamic_feat[k])
    
    return target, dynamic_feat


def create_json_deepar_train_test(csv_path, prediction_length, 
                                  train_json, test_json,
                                  start, target_idx=1, features_idx=[],                                  
                                  encoding = "utf-8"):
    """
    """
    target, dynamic_feat = get_deepar_format(csv_path, target_idx,
                                             features_idx)
    
    test_obj = {"start": start, "target": target, "dynamic_feat": dynamic_feat}
    
    dynamic_feat_train = [f[:-prediction_length] for f in dynamic_feat]
    train_obj = {"start": start, "target": target[:-prediction_length],
                "dynamic_feat": dynamic_feat_train}

    with open(train_json, 'wb') as f:
        f.write(json.dumps(train_obj).encode(encoding))
        f.write('\n'.encode(encoding))
    
    with open(test_json, 'wb') as f:
        f.write(json.dumps(test_obj).encode(encoding))
        f.write('\n'.encode(encoding))
    




