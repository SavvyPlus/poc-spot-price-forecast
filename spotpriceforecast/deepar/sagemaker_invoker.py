"""
"""

import json
import random


def build_request_data(start, target, dynamic_feat, quantiles,
                       num_samples, output_types):
    """
    """    
    serie = {'start': start, 'target': target, 'dynamic_feat': dynamic_feat}

    series = [serie]

    configuration = {
        'output_types': output_types,
        'num_samples': num_samples,
        'quantiles': quantiles
    }
    http_data = {
        "instances": series,
        "configuration": configuration
    }
    request_data = json.dumps(http_data)
    return request_data


def get_predicted_series(result, num_samples, q1, q2):
    """
    Parse result from DeepAR JSON response.
    https://docs.aws.amazon.com/sagemaker/latest/dg/deepar-in-formats.html

    Parameters
    ----------
    result : dictionary
        Response from DeepAR.
    num_samples : int
        Number of sample paths that the model generates
        to estimate the mean and quantiles.
    q1 : string
        Lower quantile.
    q2 : string
        Upper quantile.

    Returns
    -------
    results : dict

    """
    json_result = json.loads(result)
    y_data = json_result['predictions'][0]
    y_mean = y_data['mean']
    y_q1 = y_data['quantiles'][q1]
    y_q2 = y_data['quantiles'][q2]
    y_sample = y_data['samples'][random.randint(0, num_samples)]

    results = {
        'y_mean': y_mean,
        'y_q1': y_q1,
        'y_q2': y_q2,
        'y_sample': y_sample
    }
    return results


def predict_single_timeseries(start, target, dynamic_feat, predictor,
                              quantiles=[0.2, 0.9],
                              num_samples=400,
                              output_types=["mean", "quantiles", "samples"]):
    """
    """
    request_data = build_request_data(start, target, dynamic_feat, quantiles,
                                      num_samples, output_types)
    
    predicted_response = predictor.predict(request_data).decode('utf-8')

    predicted_data = get_predicted_series(predicted_response, num_samples,
                                          quantiles[0], quantiles[1])
    return predicted_data