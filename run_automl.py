"""
"""
import os

import pandas as pd
import sklearn.metrics
import autosklearn.regression


from sklearn.metrics import mean_squared_error, r2_score

from matplotlib import pyplot as plt
import seaborn as sns
sns.set(style="whitegrid")
# sns.set_palette(sns.color_palette("husl", 8))
# savvy_theme = ["#079493", "#5bcec4ff", "#027f75ff"]
# sns.set_palette(sns.color_palette(savvy_theme))


# in_csv ='./data/csv/date_spot_demand_pv_daytype_doy_season_time_median.csv'
in_csv = './data/csv/spot_interconn.csv'
# header = ['date', 'spot', 'demand', 'pv', 'daytype', 'doy', 'season', 'time']

# X_cols = ['demand', 'pv', 'daytype', 'season', 'time', 'MWFLOW',	
#           'EXPORTLIMIT', 'IMPORTLIMIT',	'MARGINALLOSS', 'MaxFlowtoA',
#           'MaxFlowtoB', 'FlowtoB', 'FlowtoA', 'SparetoB', 'SparetoA']
# feature_types = ['numerical', 'numerical', 'categorical', 
#                  'categorical', 'categorical'] + (['numerical']*10)

X_cols = ['demand', 'pv', 'daytype', 'season',
          'EXPORTLIMIT', 'MaxFlowtoB', 'MARGINALLOSS']
feature_types = ['numerical', 'numerical', 'categorical', 'categorical', 
                'numerical', 'numerical', 'numerical']

# data_type = dict(zip(X_cols, feature_types))

y_col = ['spot']

test_case = 1

op_line = f'./data/plots/automl_inter/line_{test_case}.png'
op_box = f'./data/plots/automl_inter/box_{test_case}.png'


def main():
    df = pd.read_csv(in_csv, parse_dates=[0], header=0)
    # df.columns = header
       

    df_data = df[df['date'].dt.year == 2018]
    df_validate = df[df['date'].dt.year == 2019]
    
    X = df_data[X_cols].to_numpy()
    y = df_data[y_col].values.flatten()

    X_validate = df_validate[X_cols].to_numpy()
    y_validate = df_validate[y_col].values.flatten()

    automl = autosklearn.regression.AutoSklearnRegressor(
        time_left_for_this_task=440,
        per_run_time_limit=160,
        ensemble_size=1024,
        ensemble_nbest=1024,
        ensemble_memory_limit=2048,
        ml_memory_limit=6072,
        tmp_folder='/tmp/autosklearn_regression_example_tmp',
        output_folder='/tmp/autosklearn_regression_example_out',
    )

    automl.fit(X, y, dataset_name='spot_price',
               feat_type=feature_types)
    
    print(automl.show_models())
    y_pred = automl.predict(X_validate)
    
    
    print("Mean squared error: ", mean_squared_error(y_validate, y_pred))
    print("R2 score: ", r2_score(y_validate, y_pred))

    dict_y = {'actual': list(y_validate), 'predicted': list(y_pred)}
    df_y = pd.DataFrame(dict_y)  
        
    sns_line = sns.lineplot(data=df_y[0:1000])
    sns_line.figure.savefig(op_line)
    plt.clf()
    sns_box = sns.boxplot(data=df_y)
    sns_box.figure.savefig(op_box)

if __name__ == '__main__':
    main()