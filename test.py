import environment as E
from pandas import read_csv
from source.features import prepare_features
from source.causality import linear_full_check
unchanged = read_csv(E.CASE_TABLE_DIR_PATH/'unchanged.csv')
changed = read_csv(E.CASE_TABLE_DIR_PATH/'changed.csv')
unchanged, changed = prepare_features(unchanged, changed)
print(unchanged)
print(changed)
generic_features = unchanged.drop(columns=['case:concept:name','time','cost']).columns.to_list()
change_features = changed.drop(columns=['case:concept:name','time','cost']+generic_features).columns.to_list()
print(change_features)
print(linear_full_check(unchanged, changed, 'time', generic_features, change_features))