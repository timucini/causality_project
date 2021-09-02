from typing import Tuple
from pandas import DataFrame
"""
This module covers methods and procedures for filtering features from case_tables.
"""
def variance_dropout(case_table: DataFrame, round=3) -> DataFrame:
    """
    This method is used to drop features/columns with a variance of zero.

    Parameters:
    ---
    case_table : pandas.DataFrame
        The data wich should be used

    Returns
    ---
    pandas.DataFrame
    """
    variance = case_table.var().round(round)
    return case_table.drop(columns=variance[variance==0].index.to_list())

def scale_comparison_dropout(case_table: DataFrame) -> DataFrame:
    """
    This method is used to drop features/columns which carry identical information on an aligned scale.

    Parameters:
    ---
    case_table : pandas.DataFrame
        The data wich should be used

    Returns
    ---
    pandas.DataFrame
    """
    from source.misc import min_max_scale
    scaled = min_max_scale(case_table)
    duped = []
    for column in scaled.columns:
        for other in scaled.columns:
            if column!=other:
                diff = scaled[column]==scaled[other]
                if diff.sum()==len(diff):
                    if (column in duped) or (other in duped):
                        break
                    else:
                        duped.append(column)
    return case_table.drop(columns=duped)

def prepare_features(unchanged_case_table: DataFrame, changed_case_table: DataFrame) -> Tuple[DataFrame,DataFrame]:
    """
    This method is used to drop unnecessary features/columns based on variance and scale. In addition, missing features are added if necessary.

    Parameters:
    ---
    unchanged_case_table : pandas.DataFrame

    changed_case_table : pandas.DataFrame

    Returns
    ---
    Tuple of pandas.DataFrame
    """
    from pandas import Series
    prepared_unchanged = scale_comparison_dropout(variance_dropout(unchanged_case_table))
    prepared_changed = scale_comparison_dropout(variance_dropout(changed_case_table))
    unchanged_features = Series(prepared_unchanged.columns)
    changed_features = Series(prepared_changed.columns)
    missing_changed = unchanged_features[~unchanged_features.isin(changed_features)]
    for feature in missing_changed:
        if feature in changed_case_table:
            prepared_changed[feature] = changed_case_table[feature]
        else:
            prepared_changed[feature] = 0
    return prepared_unchanged, prepared_changed