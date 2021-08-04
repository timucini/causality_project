from typing import List
from pandas import DataFrame
"""
This module covers methods and procedures for conducting causality testing.
"""
def linearFullCheck(unchangedData:DataFrame, changedData:DataFrame, kpi:str, genericFeatures:List[str], changeFeatures:List[str], score:str='neg_mean_squared_error') -> int:
    from source.ml.linear_regression import getModel as linear
    from source.ml.linear_regression import implementation as model
    from sklearn.model_selection import cross_validate as validate
    UNCHANGED_PREDICTION = 'unchaged prediction'
    DIFFRENCE = 'diffrence'
    unchagedModel = linear(unchangedData[genericFeatures], unchangedData[kpi])
    changedData[UNCHANGED_PREDICTION] = unchagedModel.predict(changedData[genericFeatures])
    changedData[DIFFRENCE] = changedData[kpi]-changedData[UNCHANGED_PREDICTION]
    return DataFrame(validate(model, changedData[changeFeatures], changedData[DIFFRENCE], scoring=score, n_jobs=-1)).mean().to_dict()['test_score']