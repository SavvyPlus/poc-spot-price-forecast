"""
"""

import os


class Config(object):
    pass


class DevConfig(Config):
    prediction_length = 140000
    test_data_length = 20000
    train_data_length = 280000
    pass


class ProdConfig(Config):
    pass


def get_config():
    env = os.getenv('env', 'dev')
    if env == 'prod':
        return ProdConfig()
    else:
        return DevConfig()
