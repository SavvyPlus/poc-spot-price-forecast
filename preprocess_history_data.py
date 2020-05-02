"""
"""
import os

import pandas as pd

from spotpriceforecast import settings 
from spotpriceforecast.utils import labelday
from spotpriceforecast.preparedata import demand, spot, pv




def handle_demand():
    demand_pkl_folder = './data/raw/demand/pkl/'
    final_demand_csv = './dataset/historical/demand/actual_demand_5mins.csv'
    _, _, demand_pkl_filenames = [f for f in os.walk(demand_pkl_folder)][0]
    demand_pkls = [demand_pkl_folder+demand_pkl for demand_pkl
                   in demand_pkl_filenames]
    demand.to_csv_historical_demands(demand_pkls, final_demand_csv)


def handle_spot():
    demand_pkl_folder = './data/raw/spot/pkl/'
    final_demand_csv = './dataset/historical/spot/actual_spot_5mins.csv'
    _, _, demand_pkl_filenames = [f for f in os.walk(demand_pkl_folder)][0]
    demand_pkls = [demand_pkl_folder+demand_pkl for demand_pkl
                   in demand_pkl_filenames]
    spot.to_csv_history_spot(demand_pkls, final_demand_csv)


def handle_pv():
    pv_pkl_folder = './data/raw/pv/pkl/'
    final_pv_csv = './dataset/historical/pv/actual_pv_5mins.csv'
    _, _, pv_pkl_filenames = [f for f in os.walk(pv_pkl_folder)][0]    
    pv_pkls = [pv_pkl_folder+pkl for pkl
               in pv_pkl_filenames]
    
    pv.to_csv_historical_pv(pv_pkls[0], final_pv_csv)


def replace_outlier_spot():
    spot_csv = './dataset/historical/spot/actual_spot_5mins.csv'
    replaced_spot_csv = './dataset/historical/spot/actual_spot_5mins_final.csv'

    df = pd.read_csv(spot_csv, header=0)    
    df.fillna(method='ffill', inplace=True)
    df.fillna(method='bfill', inplace=True)

    # for index, row in df.iterrows():
    #     if row.isnull().any():
    #         print(row)
        
    min_spot = 0
            
    for state in settings.STATES:
        max_spot = df[state].quantile(0.998)
        for i in range(len(df)):            
            value = df.at[i, state]
            if value < min_spot:
                df.at[i, state] = min_spot
            if value > max_spot:
                df.at[i, state] = max_spot
        
                
    print(df.describe())
    print(df.isnull().values.any())
    df.to_csv(replaced_spot_csv, index=False)


def replace_outlier_demand():
    demand_csv = './dataset/historical/demand/actual_demand_5mins.csv'
    replaced_demand_csv = './dataset/historical/demand/actual_demand_5mins_final.csv'

    df = pd.read_csv(demand_csv, header=0)    
    df.fillna(method='ffill', inplace=True)
    df.fillna(method='bfill', inplace=True)

    # for index, row in df.iterrows():
    #     if row.isnull().any():
    #         print(row)
        
    min_spot = 0
    print(df.quantile(0.998))
            
    # for state in settings.STATES:
    #     max_spot = df[state].quantile(0.998)
    #     for i in range(len(df)):            
    #         value = df.at[i, state]
    #         if value < min_spot:
    #             df.at[i, state] = min_spot
    #         if value > max_spot:
    #             df.at[i, state] = max_spot
        
                
    print(df.describe())
    print(df.isnull().values.any())
    # df.to_csv(replaced_spot_csv, index=False)


def replace_outlier_pv():
    pv_csv = './dataset/historical/pv/actual_pv_5mins.csv'
    replaced_pv_csv = './dataset/historical/pv/actual_pv_5mins_final.csv'

    df = pd.read_csv(pv_csv, header=0)    
    df.fillna(method='ffill', inplace=True)
    df.fillna(method='bfill', inplace=True)

    # for index, row in df.iterrows():
    #     if row.isnull().any():
    #         print(row)
        
    min_spot = 0
    print(df.quantile(0.9))
            
    # for state in settings.STATES:
    #     max_spot = df[state].quantile(0.998)
    #     for i in range(len(df)):            
    #         value = df.at[i, state]
    #         if value < min_spot:
    #             df.at[i, state] = min_spot
    #         if value > max_spot:
    #             df.at[i, state] = max_spot
        
                
    print(df.describe())
    print(df.isnull().values.any())
    # df.to_csv(replaced_spot_csv, index=False) 


def join_features():
    spot_csv = './dataset/historical/spot/actual_spot_5mins_final.csv'
    demand_csv = './dataset/historical/demand/actual_demand_5mins_final.csv'
    pv_csv = './dataset/historical/pv/actual_pv_5mins_final.csv'

    final_path = './dataset/historical/merged/'

    df_spot = pd.read_csv(spot_csv, header=0)
    df_demand = pd.read_csv(demand_csv, header=0)
    df_pv = pd.read_csv(pv_csv, header=0)

    for state in settings.STATES:
        df_spot_state = df_spot[[settings.DT_COL, state]]
        df_demand_state = df_demand[[settings.DT_COL, state]]
        df_pv_state = df_pv[[settings.DT_COL, state]]
                
        df = df_spot_state.merge(df_demand_state, on=settings.DT_COL, 
                                 how='inner')
        
        df.columns = [settings.DT_COL, 'spot', 'demand']        
        df = df.join(df_pv_state.set_index(settings.DT_COL), 
                     on=settings.DT_COL, how='inner')
        df.columns = [settings.DT_COL, 'spot', 'demand', 'pv']       

        # df = labelday.add_daytype_to_df(df, settings.DT_COL, state=state[:-1])
        # df = labelday.add_time_df(df, settings.DT_COL)
        # df = labelday.add_season_au_df(df, settings.DT_COL)
        
        print(df.head())
        df.to_csv(final_path+state+'.csv', index=False)

        
def add_lable_features():
    final_path = './dataset/historical/merged/'
    for state in settings.STATES:
        df = pd.read_csv(final_path+state+'.csv', header=0)
        df = labelday.add_season_au_df(df, settings.DT_COL)
        df = labelday.add_daytype_to_df(df, settings.DT_COL, state=state[:-1])
        df = labelday.add_time_df(df, settings.DT_COL)
        print(df.head())
        df.to_csv(final_path+state+'_labeled.csv', index=False)



def main():
    # handle_demand()
    # handle_spot()
    # handle_pv()
    # replace_outlier_spot()
    # replace_outlier_demand()
    # replace_outlier_pv()
    # join_features()
    add_lable_features()


if __name__ == '__main__':
    main()


