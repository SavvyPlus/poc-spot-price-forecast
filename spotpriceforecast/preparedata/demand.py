"""
"""

import logging
import pandas as pd

from spotpriceforecast import settings


def to_csv_historical_demands(demand_pkls, final_demand_csv):
    """can use for demand and spot
    """
    # row = [dt, NSW1, QLD1, SA1, TAS1, VIC1]
    demands = []
    for demand_pkl in demand_pkls:
        demand_data = pd.read_pickle(demand_pkl)
        demand_day = []
        for dt in demand_data.keys():            
            demand_5min = []
            demand_5min.append(dt)
            for state in settings.STATES:
                try:
                    demand_5min.append(demand_data[dt][state])
                except KeyError as e:
                    logging.error(demand_data)
                    raise(e)
            demand_day.append(demand_5min)
        demands = demands + demand_day

    df = pd.DataFrame(demands, columns=[settings.DT_COL]+settings.STATES)
    df = df.sort_values(by=[settings.DT_COL])
    df.to_csv(final_demand_csv, index=False, header=True)


