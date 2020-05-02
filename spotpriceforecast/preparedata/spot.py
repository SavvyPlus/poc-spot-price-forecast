"""
"""

import numpy as np
import pandas as pd

from spotpriceforecast import settings


def to_csv_history_spot(spot_pkls, final_spot_csv):
    """can use for spot and spot
    """
    # row = [dt, NSW1, QLD1, SA1, TAS1, VIC1]
    spots = []
    for spot_pkl in spot_pkls:
        spot_data = pd.read_pickle(spot_pkl)
        spot_day = []
        for dt in spot_data.keys():
            # dt = str(dt)
            spot_5min = []
            spot_5min.append(dt)
            for state in settings.STATES:
                try:
                    spot_5min.append(spot_data[dt][state])
                except KeyError:
                    spot_5min.append(np.nan)
            spot_day.append(spot_5min)
        spots = spots + spot_day

    df = pd.DataFrame(spots, columns=[settings.DT_COL]+settings.STATES)
    df = df.sort_values(by=[settings.DT_COL])
    df.to_csv(final_spot_csv, index=False, header=True)