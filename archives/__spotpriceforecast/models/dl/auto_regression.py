import autokeras as ak



def train_ak_regression(X, y, **kwargs):
    """
    """
    regressor = ak.StructuredDataRegressor(**kwargs)
    regressor.fit(X, y)
    return regressor