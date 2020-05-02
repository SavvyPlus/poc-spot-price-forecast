import pandas as pd

from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

from spotpriceforecast import settings, config

from matplotlib import pyplot as plt
import seaborn as sns
sns.set(style="whitegrid")

conf = config.get_config()

historical_path = './dataset/historical/merged/'
future_path = './dataset/forecast/merged/'
results_path = './dataset/forecast/results/'

X_cols = ['demand', 'pv', 'season', 'daytype', 'time', 'prevspot']
y_col = ['spot']

op_line = './dataset/forecast/results/plots/{}_line.png'
op_box = './dataset/forecast/results/plots/{}_box.png'


def main():
    for state in settings.STATES[1:]:
        # init loading df
        df_hist = pd.read_csv(historical_path+state+'_labeled.csv', header=0)
        y_val = df_hist.tail(conf.test_data_length)['spot'].values.flatten()
        df_hist = df_hist[:-conf.test_data_length-1]
        # creata prevspot
        df_hist['prevspot'] = df_hist['spot'].shift(1)
        df_hist = df_hist[1:]        
        # train data from hist data
        X_train = df_hist[X_cols].values.tolist()
        y_train = df_hist[y_col].values.flatten()
        # print(df_hist.tail())

        # get future data
        df_futre = pd.read_csv(future_path+state+'.csv', header=0) 
        # print(df_futre.head())
        df_futre['prevspot'] = 0        
        X_future = df_futre[X_cols].values.tolist()
        
        print(f"start training {state}")
        m = DecisionTreeRegressor(criterion='friedman_mse',
                                  max_depth=140,
                                  min_samples_split=2,
                                  min_samples_leaf=1,
                                  min_weight_fraction_leaf=0.000000000000001)
        m.fit(X_train, y_train)

        # start forecasting
        y_pred = []
        curr_spot = y_train[-1]

        for i in range(len(X_future)):
            x = X_future[i]
            x[-1] = curr_spot
            y = m.predict([x])[0]
            y_pred.append(y)
            curr_spot = y
        
        df_futre['spot'] = y_pred
        df_futre = df_futre.drop(['prevspot'], axis=1)
        df_futre.to_csv(results_path+state+'.csv', index=False)
        
        y_val_pred = y_pred[:conf.test_data_length]
        

        print("mean_absolute_error: ", mean_absolute_error(y_val_pred, y_val))
        
        dict_validate = {'actual': y_val, 'predicted': y_val_pred}
        df_val = pd.DataFrame(dict_validate)

        sns_line = sns.lineplot(data=df_val[:8000])
        # sns_line = sns.scatterplot(data=df_y['error'][:4000])
        sns_line.figure.savefig(op_line.format(state))
        plt.clf()
        sns_box = sns.boxplot(data=df_val)
        sns_box.figure.savefig(op_box.format(state))



if __name__ == "__main__":
    main()
    