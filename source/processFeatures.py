from typing import List

from pandas import DataFrame
import numpy as np

from resources.features.List_features import generic_feature_list, changed_feature_list


def clean_dataframe(case_table: DataFrame) -> DataFrame:
    case_table.fillna(0, inplace=True)
    # get variance for dataframe
    variance = DataFrame([case_table.var()], index=['Variance'])
    # get activities that are always performed
    df_variance = variance.where(variance == 0).dropna(axis=1)
    columns_to_remove = df_variance.columns
    # remove num columns of activities that are always performed
    case_table.drop(columns_to_remove, inplace=True, axis=1)
    # get cost and time columns of activities that are always performed
    columns_to_removed_sliced = [sub[7:] for sub in columns_to_remove]
    cost_columns_to_remove = ["cost " + sub for sub in columns_to_removed_sliced]
    time_columns_to_remove = ["time " + sub for sub in columns_to_removed_sliced]
    # remove cost and time columns of these activities
    case_table.drop(cost_columns_to_remove, inplace=True, axis=1)
    case_table.drop(time_columns_to_remove, inplace=True, axis=1)
    # drop all num columns
    case_table.drop(list(case_table.filter(regex='Num')), axis=1, inplace=True)
    return case_table


def add_changed_features(case_table_changed: DataFrame) -> DataFrame:
    case_table_changed.fillna(0, inplace=True)
    #Notify unavailability to customer features
    case_table_changed['Changed automation step notify customer'] = np.where(
        case_table_changed['cost Notify unavailability to customer'] > 0, 0, 0)
    case_table_changed['Changed parallelism step notify customer'] = np.where(
        case_table_changed['cost Notify unavailability to customer'] > 0, 0, 0)
    case_table_changed['Changed containment step notify customer'] = np.where(
        case_table_changed['cost Notify unavailability to customer'] > 0, 1, 0)
    #Request raw materials from Suppliers features
    case_table_changed['Changed automation step request materials'] = np.where(
        case_table_changed['cost Start request raw materials from Supplier 1'] > 0, 1, 0)
    case_table_changed['Changed parallelism step request materials'] = np.where(
        case_table_changed['cost Start request raw materials from Supplier 1'] > 0, 0, 0)
    case_table_changed['Changed containment step request materials'] = np.where(
        case_table_changed['cost Start request raw materials from Supplier 1'] > 0, 0, 0)
    #Get shipping address features
    case_table_changed['Changed automation step shipping address'] = np.where(
        case_table_changed['cost Get shipping address'] > 0, 0, 0)
    case_table_changed['Changed parallelism step shipping address'] = np.where(
        case_table_changed['cost Get shipping address'] > 0, 0, 0)
    case_table_changed['Changed containment step shipping address'] = np.where(
        case_table_changed['cost Get shipping address'] > 0, 1, 0)
    return case_table_changed


def get_generic_feature_list() -> List[str]:
    return generic_feature_list


def get_changed_feature_list() -> List[str]:
    return changed_feature_list

