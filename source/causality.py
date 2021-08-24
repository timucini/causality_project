from typing import List
from pandas import DataFrame
from sklearn.base import BaseEstimator
"""
This module covers methods and procedures for conducting causality testing.
"""
def linear_full_check(unchanged_data:DataFrame, changed_data:DataFrame, kpi:str, generic_features:List[str], changed_features:List[str]) -> float:
    """
    Depricated, this will be deleted soon.
    """
    from sklearn.linear_model import LinearRegression as linear
    from sklearn.model_selection import cross_validate as validate
    UNCHANGED_PREDICTION = 'unchaged prediction'
    DIFFRENCE = 'diffrence'
    unchagedModel = linear().fit(unchanged_data[generic_features], unchanged_data[kpi])
    changed_data[UNCHANGED_PREDICTION] = unchagedModel.predict(changed_data[generic_features])
    changed_data[DIFFRENCE] = changed_data[kpi]-changed_data[UNCHANGED_PREDICTION]
    print()
    print(changed_data[[UNCHANGED_PREDICTION,kpi,DIFFRENCE]])
    return DataFrame(validate(linear(), changed_data[changed_features], changed_data[DIFFRENCE], n_jobs=-1)).mean()['test_score']

def full_check(model:BaseEstimator, unchanged_data:DataFrame, changed_data:DataFrame, kpi:str, generic_features:List[str], changed_features:List[str]) -> float:
    """
    This method is used to estimate the causality of a change in a process an the change in the outcome.

    Parameters:
    ---
    model : sklearn.base.BaseEstimator
        A sklearn estimator, wich should be used to estimate the causality
    unchanged_data : pandas.DataFrame
        The data of the unchanged process organized as a case table
    changed_data : pandas.DataFrame
        The data of the changed process organized as a case table
    kpi : str
        A string representing the column of the kpi/outcome of the unchanged_data
    generic_features : List[str]
        A list of string representing the columns of the features describing the base process, most likely the features that have not changed; Ensure that both data inhabitates the features
    changed_features : List[str]
        A list of string representing the columns of the features describing the changes in the changed_data frame.

    Returns
    ---
    float
        A value between 0 and 1
    """
    from sklearn.model_selection import cross_validate as validate
    UNCHANGED_PREDICTION = 'unchaged prediction'
    DIFFRENCE = 'diffrence'
    estimators = validate(model, unchanged_data[generic_features], unchanged_data[kpi], return_estimator=True, n_jobs=-1).pop('estimator')
    predictions = []
    for estimator in estimators:
        predictions.append(estimator.predict(unchanged_data[generic_features]))
    changed_data[UNCHANGED_PREDICTION] = DataFrame(predictions).mean()
    changed_data[DIFFRENCE] = changed_data[kpi]-changed_data[UNCHANGED_PREDICTION]
    causality_model = model.__class__().set_params(**model.get_params())
    return DataFrame(validate(causality_model, changed_data[changed_features], changed_data[DIFFRENCE], n_jobs=-1))['test_score'].mean()