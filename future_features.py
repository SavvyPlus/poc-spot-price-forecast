import numpy as np
import pandas as pd

from sklearn.tree import DecisionTreeRegressor
# from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

from spotpriceforecast import settings, config
from spotpriceforecast.utils import panda

from matplotlib import pyplot as plt

import seaborn as sns
sns.set(style="whitegrid")

conf = config.get_config()

merged_path = './dataset/historical/merged/'              
labled_suffix = '_labeled.csv'

forecast_path = './dataset/forecast/demand/'

np.random.seed(28)


def forcast_demand():
    for state in ['NSW1']:
        shift_len = 14
        df = pd.read_csv(merged_path+state+labled_suffix, header=0)
        df = df[[settings.DT_COL, 'demand']]
        df_test = df.tail(conf.test_data_length+1)
        start_future = df.at[len(df)-conf.test_data_length-1, settings.DT_COL]

        df = df[:-conf.test_data_length]           
        
        X_cols = []
        for i in range(1, shift_len+1):
            col = 'd'+str(i)
            df[col] = df['demand'].shift(i)
            X_cols.append(col)
        df = df[shift_len:]

        X_train = df[X_cols].values.tolist()
        y_train = df['demand'].values.flatten()
        print("start training")
        
        m = DecisionTreeRegressor(criterion='friedman_mse', max_depth=9999,
                                  min_samples_split=2, min_samples_leaf=1, 
                                  min_weight_fraction_leaf=0.000000000000001)
        
        m.fit(X_train, y_train)
        print("finish training")
        future_ts = panda.create_date_range(start_future,
                                            '2023-12-31 23:55:00',
                                            '5min')
        future_ts = [str(ts) for ts in future_ts]
        x_pred_set = list(df.iloc[-1,:][X_cols])        
        future_data = []
        for ts in future_ts:
            future = []            
            y = m.predict([x_pred_set])[0]            
            if y >= 10000:
                if x_pred_set[1] < 8000:
                    y = y*0.6
                else:
                    y = 10000

            future.append(ts)
            future.append(y)
            future_data.append(future)
            x_pred_set.insert(0, y)
            x_pred_set = x_pred_set[:shift_len]
            print(y)
        df_future = pd.DataFrame(data=future_data, columns=['dt', 'demand'])

        dict_y = {'actual': list(df_test['demand']), 'predicted': list(df_future.head(conf.test_data_length+1)['demand'])}
        df_y = pd.DataFrame(dict_y)  
        sns_line = sns.lineplot(data=df_y[['actual', 'predicted']][:8000])
        sns_line.figure.savefig(f'play_demand_f{state}.png')
        plt.clf()    

        
        print("mean_absolute_error: ", mean_absolute_error(df_test['demand'], df_future.head(conf.test_data_length+1)['demand']))
        df_future.to_csv(forecast_path+state+'_demand.csv', index=False)

        # print(f'done: {state}')
        
       


        

def main():
    forcast_demand()
    # forcast_pv()


if __name__ == '__main__':
    main()
    
        



