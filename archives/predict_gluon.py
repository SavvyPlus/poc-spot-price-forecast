import pandas as pd
from matplotlib import pyplot as plt

from gluonts.dataset import common
from gluonts.model import deepar
from gluonts.trainer import Trainer

from spotpriceforecast.gluon import createdata


train_csv = './data/csv/date_spot_demand_pv_train.csv'
test_csv = './data/csv/date_spot_demand_pv_test.csv'


freq = "5min"
prediction_length = 800
context_length = prediction_length

start_train_idx = 0
end_train_idx = 100000

def plot_series(op, yhat, truth=False,
                truth_data=None, truth_label='Truth', prediction_length=prediction_length):
    x = range(0, prediction_length)
    plt.gcf().clear()
    mean_label,   = plt.plot(x, yhat, label='predicted')
    # q1_label,     = plt.plot(x, yhat_lower, label='yhat_lower')
    # q2_label,     = plt.plot(x, yhat_upper, label='yhat_upper')

    if truth:
        ground_truth, = plt.plot(x, truth_data, label=truth_label)
        plt.legend(handles=[ground_truth, mean_label])
        # plt.legend(handles=[ground_truth, mean_label])
    else:
        plt.legend(handles=[mean_label])
    # plt.yticks(np.arange(5.0, 12.0, 0.5))
    plt.savefig(op)

train_obj, test_obj = createdata.create_json_deepar_train_test(train_csv,
                                                               prediction_length,
                                                               start_train_idx,
                                                               end_train_idx)

training_data = common.ListDataset([train_obj], freq=freq)
validation_data = common.ListDataset([test_obj], freq=freq)

trainer = Trainer(epochs=1, learning_rate=0.0000001, hybridize=False)
estimator = deepar.DeepAREstimator(freq=freq, 
                                   prediction_length=prediction_length, 
                                   context_length=context_length,
                                   trainer=trainer, 
                                   use_feat_dynamic_real=True)
predictor = estimator.train(training_data=training_data, 
                            validation_data=validation_data)                                   


# predict

start_pred_idx = 0
end_pred_idx = 10000


test_pred_obj, target_truth = createdata.create_test_predict_data(test_csv,
                                                                  prediction_length,
                                                                  start_pred_idx,
                                                                  end_pred_idx)

test_pred_data = common.ListDataset([test_pred_obj], freq=freq)

prediction = next(predictor.predict(test_pred_data))

                                                      

target_predicted = prediction.quantile(0.7)

assert len(target_truth) == len(target_predicted)

for i in range(len(target_truth)):
    print(f'Truth: {target_truth[i]} - Predicted: {target_predicted[i]}')


op = './data/plots/deepar/800_1.png'

plot_series(op, target_predicted, truth=True, truth_data=target_truth)

# end predict


# predict

start_pred_idx = 1000
end_pred_idx = 11000


test_pred_obj, target_truth = createdata.create_test_predict_data(test_csv,
                                                                  prediction_length,
                                                                  start_pred_idx,
                                                                  end_pred_idx)

test_pred_data = common.ListDataset([test_pred_obj], freq=freq)

prediction = next(predictor.predict(test_pred_data))

                                                      

target_predicted = prediction.quantile(0.7)

assert len(target_truth) == len(target_predicted)

for i in range(len(target_truth)):
    print(f'Truth: {target_truth[i]} - Predicted: {target_predicted[i]}')


op = './data/plots/deepar/800_2.png'

plot_series(op, target_predicted, truth=True, truth_data=target_truth)

# end predict

# predict

start_pred_idx = 14000
end_pred_idx = 15000


test_pred_obj, target_truth = createdata.create_test_predict_data(test_csv,
                                                                  prediction_length,
                                                                  start_pred_idx,
                                                                  end_pred_idx)

test_pred_data = common.ListDataset([test_pred_obj], freq=freq)

prediction = next(predictor.predict(test_pred_data))

                                                      

target_predicted = prediction.quantile(0.7)

assert len(target_truth) == len(target_predicted)

for i in range(len(target_truth)):
    print(f'Truth: {target_truth[i]} - Predicted: {target_predicted[i]}')


op = './data/plots/deepar/800_3.png'

plot_series(op, target_predicted, truth=True, truth_data=target_truth)

# end predict


# predict

start_pred_idx = 14000
end_pred_idx = 90000


test_pred_obj, target_truth = createdata.create_test_predict_data(test_csv,
                                                                  prediction_length,
                                                                  start_pred_idx,
                                                                  end_pred_idx)

test_pred_data = common.ListDataset([test_pred_obj], freq=freq)

prediction = next(predictor.predict(test_pred_data))

                                                      

target_predicted = prediction.quantile(0.7)

assert len(target_truth) == len(target_predicted)

for i in range(len(target_truth)):
    print(f'Truth: {target_truth[i]} - Predicted: {target_predicted[i]}')


op = './data/plots/deepar/800_4.png'

plot_series(op, target_predicted, truth=True, truth_data=target_truth)

# end predict