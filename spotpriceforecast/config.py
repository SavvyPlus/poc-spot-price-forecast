"""
"""

import os


class Config(object):
    pass


class DevConfig(Config):
    pass


class ProdConfig(Config):
    pass


def get_config():
    env = os.getenv('env', 'dev')
    if env == 'prod':
        return ProdConfig()
    else:
        return DevConfig()
