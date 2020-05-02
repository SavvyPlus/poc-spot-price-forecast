import pandas as pd

from spotpriceforecast import settings 
from spotpriceforecast.utils import labelday
from spotpriceforecast.preparedata import demand, spot, pv


demand_path = './dataset/forecast/demand/'
pv_path = './dataset/forecast/pv/'

merge_path = './dataset/forecast/merged/'


def main():
    for state in settings.STATES:
        demand_file = demand_path+state+'_demand.csv'
        pv_file = pv_path+state+'_pv.csv'

        df_demand = pd.read_csv(demand_file, header=0)
        df_pv = pd.read_csv(pv_file, header=0)

        df = df_demand.merge(df_pv, on=settings.DT_COL, 
                             how='inner')
        df = labelday.add_season_au_df(df, settings.DT_COL)
        df = labelday.add_daytype_to_df(df, settings.DT_COL, state=state[:-1])
        df = labelday.add_time_df(df, settings.DT_COL)
        
        df.to_csv(merge_path+state+'.csv', index=False)


if __name__ == "__main__":
    main()