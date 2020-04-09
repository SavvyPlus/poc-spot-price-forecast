"""
"""

import pandas as pd



def get_deepar_format(csv_path, time_idx = 0, target_idx=1, features_idx=[]):
    """
    """
    df = pd.read_csv(csv_path)    
    data = df.values.tolist()
    
    ts = []
    target = []
    dynamic_feat = [[] for i in range(len(features_idx))]  

    for row in data:
        ts.append(row[time_idx])
        target.append(row[target_idx])
        for j in range(len(features_idx)):
            dynamic_feat[j].append(row[features_idx[j]])
    
    for k in range(len(dynamic_feat)):
        assert len(target) == len(dynamic_feat[k])
    
    return ts, target, dynamic_feat


def create_json_deepar_train_test(csv_path, prediction_length,                                   
                                  start_idx, end_idx,
                                  time_idx=0,
                                  target_idx=1, features_idx=[2, 3]):
    """
    """
    idxes, target, dynamic_feat = get_deepar_format(csv_path, time_idx,
                                                    target_idx,
                                                    features_idx)
    
    dynamic_feat_test = [f[start_idx:end_idx] 
                          for f in dynamic_feat]
    test_obj = {"start": idxes[start_idx], 
                "target": target[start_idx:end_idx], 
                "feat_dynamic_real": dynamic_feat_test}
    
    dynamic_feat_train = [f[start_idx:end_idx-prediction_length] 
                          for f in dynamic_feat]
    train_obj = {"start": idxes[start_idx], 
                "target": target[start_idx:end_idx-prediction_length], 
                "feat_dynamic_real": dynamic_feat_train}

    return train_obj, test_obj
    
    

def create_test_predict_data(csv_path, prediction_length,                                   
                             start_idx, end_idx,
                             time_idx=0,
                             target_idx=1, features_idx=[2, 3]):
    """
    """
    idxes, target, dynamic_feat = get_deepar_format(csv_path, time_idx,
                                                    target_idx,
                                                    features_idx)
    
    target_test = target[start_idx:end_idx]
    target_truth = target[end_idx:end_idx+prediction_length]

    dynamic_feat_test = [f[start_idx:end_idx+prediction_length] 
                           for f in dynamic_feat]
    
    test_obj = {"start": idxes[start_idx], 
                "target": target_test, 
                "feat_dynamic_real": dynamic_feat_test}
    
    return test_obj, target_truth