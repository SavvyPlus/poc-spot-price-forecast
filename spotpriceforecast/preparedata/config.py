simulation_tag = 'Run_126'

bucket_inputs = "007-spot-price-forecast-physical"

train_state = 'NSW1'

actual_spot_5_mins_path = 'nem-pricing-v2/actual_spot_price_5_mins/{}.pickle'  # date
actual_total_demand_5_mins_path = 'nem-pricing-v2/actual_total_demand_5_mins/{}.pickle'  # date
pv_data_s3_pickle_path = 'cache/{}/pv.pickle'    # assumptions version

prediction_length = 400