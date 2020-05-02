"""
"""

import pandas as pd
from spotpriceforecast import settings
from spotpriceforecast.utils import helpers, panda


def to_csv_historical_pv(pv_pkl, final_pv_csv):
    """
    """
    pv_data = {}    
    pv_values = pd.read_pickle(pv_pkl)
    for state in settings.STATES:
        pv_state = pv_values[state]
        pv_data_state = []
        for date in pv_state.keys():
            date_idexs = panda.create_date_range(str(date)+' 00:00:00',
                                                 str(date)+' 23:55:00', '5min')
            for date_idx in date_idexs:
                pv_index = helpers.get_index_pv(str(date_idx).split()[-1])
                pv_value = pv_values[state][date][pv_index]
                pv_data_state.append([str(date_idx), pv_value])
        pv_data[state] = pv_data_state
    
    dt = [row[0] for row in pv_data[settings.STATES[0]]]

    df = pd.DataFrame(dt, columns=[settings.DT_COL])

    for state in settings.STATES:
        df[state] = [row[1] for row in pv_data[state]]
    
    df = df.sort_values(by=[settings.DT_COL])
    df.to_csv(final_pv_csv, index=False, header=True)






