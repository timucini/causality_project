from sklearn.linear_model import LinearRegression
import environment as E
from pandas import read_csv
from source.features import prepare_features
from source.causality import full_check, feature_tracing, calculate_diffrence
unchanged = read_csv(E.CASE_TABLE_DIR_PATH/'unchanged.csv')
changed = read_csv(E.CASE_TABLE_DIR_PATH/'changed.csv')
#d = unchanged.describe()
#for col in d.columns:
#    print(d[col])
unchanged, changed = prepare_features(unchanged, changed)
print("Unchanged data:")
print(unchanged)
print("Changed data:")
print(changed)
generic_features = unchanged.drop(columns=['case:concept:name','time','cost']).columns.to_list()
change_features = changed.drop(columns=['case:concept:name','time','cost']+generic_features).columns.to_list()
print("Changed features:")
for feature in change_features:
    print(feature)
#print(full_check(LinearRegression(), unchanged, changed, 'cost', generic_features, change_features))
generic_features = feature_tracing(LinearRegression(), unchanged, generic_features, 'cost').sort_values('score', ascending=False).iloc[0]['features']
print(generic_features)
changed = calculate_diffrence(LinearRegression(), unchanged, changed, 'cost', generic_features)
print(changed)
change_features = changed.drop(columns=['case:concept:name','time','cost','diffrence','unchaged prediction']).columns.to_list()
print(feature_tracing(LinearRegression(), changed, change_features, 'cost').sort_values('score', ascending=False).iloc[0]['features'])
#print()
#for feature in change_features:
#    from sklearn.linear_model import LinearRegression
#    print("Prediction of " + feature + ": " + str(full_check(LinearRegression(), unchanged, changed, 'cost', generic_features, [feature])))