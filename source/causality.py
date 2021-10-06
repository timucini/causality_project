from typing import List, Tuple
from pandas import DataFrame
from sklearn.base import BaseEstimator

UNCHANGED_PREDICTION = 'unchanged prediction'
DIFFERENCE = 'difference'


def calculate_difference(model: BaseEstimator, unchanged_data: DataFrame, changed_data: DataFrame, kpi: str,
                         generic_features: List[str], cv: int = 5) -> DataFrame:
    """
    This method is used to estimate the causality between the change in a process and the change in the outcome.

    Parameters:
    ---
    model : sklearn.base.BaseEstimator
        A sklearn estimator, which is used to estimate the causality
    unchanged_data : pandas.DataFrame
        The data of the unchanged process structured as a case table
    changed_data : pandas.DataFrame
        The data of the changed process structured as a case table
    kpi : str
        A string representing the column of the kpi/outcome of the unchanged_data
    generic_features : List[str]
        A list of strings representing the columns of the features, which describe the base process.
        Most likely the features that have not changed; Ensure that both data match the features
    cv : int
        A integer representing the number of folds used for a prediction

    Returns
    ---
    pandas.DataFrame
        Returns the changed_data with two more columns 'unchanged prediction' and 'difference'
    """
    from sklearn.model_selection import cross_validate as validate
    estimators = validate(model, unchanged_data[generic_features], unchanged_data[kpi], return_estimator=True,
                          n_jobs=-1, cv=cv).pop('estimator')
    predictions = []
    for estimator in estimators:
        predictions.append(estimator.predict(unchanged_data[generic_features]))
    changed_data[UNCHANGED_PREDICTION] = DataFrame(predictions).mean()
    changed_data[DIFFERENCE] = changed_data[kpi] - changed_data[UNCHANGED_PREDICTION]
    return changed_data


def full_check(model: BaseEstimator, unchanged_data: DataFrame, changed_data: DataFrame, kpi: str,
               generic_features: List[str], changed_features: List[str], cv=5,
               scoring='neg_mean_squared_error') -> float:
    """
     This method is used to estimate the causality between the change in a process and the change in the outcome.

    Parameters:
    ---
    model : sklearn.base.BaseEstimator
        A sklearn estimator, which should be used to estimate the causality
    unchanged_data : pandas.DataFrame
        The data of the unchanged process structured as a case table
    changed_data : pandas.DataFrame
        The data of the changed process structured as a case table
    kpi : str
        A string representing the column of the kpi/outcome of the unchanged_data
    generic_features : List[str]
        A list of strings representing the columns of the features, which describe the base process.
        Most likely the features that have not changed; Ensure that both data match the features
    changed_features : List[str]
        A list of strings representing the columns of the features describing the changes in the changed_data frame.
    cv : int
        A integer representing the number of folds used for a prediction
    scoring : str
        A string representing the scoring method according to sklearn used for evaluation

    Returns
    ---
    float
        A value defined by the scoring; larger value is better
    """
    from sklearn.model_selection import cross_validate as validate
    changed_data = calculate_difference(model, unchanged_data, changed_data, kpi, generic_features, cv)
    return DataFrame(
        validate(model, changed_data[changed_features], changed_data[DIFFERENCE], n_jobs=-1, cv=cv, scoring=scoring))[
        'test_score'].mean()


def feature_tracing(model: BaseEstimator, data: DataFrame, features: List[str], target: str, cv: int = 5,
                    scoring: str = 'neg_mean_squared_error') -> DataFrame:
    """
    This method can be used to find out which features best describe the problem.

    Parameters:
    ---
    model : sklearn.base.BaseEstimator
        A sklearn estimator, which should be used to estimate the problem
    data : pandas.DataFrame
        The data of a problem
    features : List[str]
        A list of strings representing the columns of the features describing the problem in the data
    target : str
        A string representing the column of the outcome of the problem
    cv : int
        A integer representing the number of folds used for a prediction
    scoring : str
        A string representing the scoring method according to sklearn used for evaluation

    Returns
    ---
    pandas DataFrame
        A data frame with all sampled feature combinations and their result
    """
    from sklearn.model_selection import cross_validate as validate
    records = []
    bias = -2 ** 16
    used_features = []
    dim = 0

    def trace(bias: float, used_features: List[str]) -> Tuple[float, List[str]]:
        best_features = []
        for feature in features:
            if feature not in used_features:
                trace_features = used_features + [feature]
                score = \
                    DataFrame(validate(model, data[trace_features], data[target], n_jobs=-1, cv=cv, scoring=scoring))[
                        'test_score'].mean()
                records.append({'features': trace_features, 'dim':dim, 'score': score})
                if score > bias:
                    bias = score
                    best_features = trace_features
        return bias, best_features

    while True:
        pre_bias = bias
        bias, used_features = trace(bias, used_features)
        dim = dim+1
        if bias == pre_bias:
            break
    return DataFrame(records)
