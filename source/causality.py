from typing import List
from pandas import DataFrame
"""
This module covers methods and procedures for conducting causality testing.
"""
def linear_full_check(unchanged_data:DataFrame, changed_data:DataFrame, kpi:str, generic_features:List[str], change_features:List[str]) -> int:
    from sklearn.linear_model import LinearRegression as linear
    from sklearn.model_selection import cross_validate as validate
    UNCHANGED_PREDICTION = 'unchaged prediction'
    DIFFRENCE = 'diffrence'
    unchagedModel = linear().fit(unchanged_data[generic_features], unchanged_data[kpi])
    changed_data[UNCHANGED_PREDICTION] = unchagedModel.predict(changed_data[generic_features])
    changed_data[DIFFRENCE] = changed_data[kpi]-changed_data[UNCHANGED_PREDICTION]
    print(changed_data[[UNCHANGED_PREDICTION,kpi,DIFFRENCE]])
    return DataFrame(validate(linear(), changed_data[change_features], changed_data[DIFFRENCE], n_jobs=-1)).mean()['test_score']