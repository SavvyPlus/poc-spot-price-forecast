"""
"""

from spotpriceforecast import s3_process, utils
from spotpriceforecast.preparedata import config


def download_spot_price(output_path, max_days):
    """
    """    
    start_spot_date = '2017-01-01'
    for i in range(0, max_days):
        date = utils.future_date_from_str(start_spot_date, i)
        s3_spot_path = config.actual_spot_5_mins_path.format(date)
        file_name = s3_spot_path.split('/')[-1]

        pkl_bytes = s3_process.get_object_byte(config.bucket_inputs, 
                                               s3_spot_path)
        
        with open(output_path.format(file_name), 'wb') as f:
            f.write(pkl_bytes)
        
        



