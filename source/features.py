from os import dup
from typing import Tuple
from pandas import DataFrame

def variance_dropout(case_table: DataFrame) -> DataFrame:
    variance = case_table.var()
    return case_table.drop(columns=variance[variance==0].index.to_list())

def scale_comparison_dropout(case_table: DataFrame) -> DataFrame:
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

#def add_changed_features(changed_case_table: DataFrame) -> DataFrame:
#    import numpy as np
#    #Notify unavailability to customer features
#    changed_case_table['Is notify customer automated'] = changed_case_table['cost Notify unavailability to customer']>0, 0, 0)
#    case_table_changed['Changed parallelism step notify customer'] = np.where(case_table_changed['cost Notify unavailability to customer'] > 0, 0, 0)
#    case_table_changed['Changed containment step notify customer'] = np.where(case_table_changed['cost Notify unavailability to customer'] > 0, 1, 0)
#    #Request raw materials from Suppliers features
#    case_table_changed['Changed automation step request materials'] = np.where(case_table_changed['cost Start request raw materials from Supplier 1'] > 0, 1, 0)
#    case_table_changed['Changed parallelism step request materials'] = np.where(case_table_changed['cost Start request raw materials from Supplier 1'] > 0, 0, 0)
#    case_table_changed['Changed containment step request materials'] = np.where(case_table_changed['cost Start request raw materials from Supplier 1'] > 0, 0, 0)
#    #Get shipping address features
#    case_table_changed['Changed automation step shipping address'] = np.where(case_table_changed['cost Get shipping address'] > 0, 0, 0)
#    case_table_changed['Changed parallelism step shipping address'] = np.where(case_table_changed['cost Get shipping address'] > 0, 0, 0)
#    case_table_changed['Changed containment step shipping address'] = np.where(case_table_changed['cost Get shipping address'] > 0, 1, 0)
#    return case_table_changed


#def get_generic_feature_list() -> List[str]:
#    return generic_feature_list
#
#
#def get_changed_feature_list() -> List[str]:
#    return changed_feature_list
#
#