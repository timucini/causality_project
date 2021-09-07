from pandas import read_csv
from environment import *
time = read_csv(CAUSALITY_FEATURE_TABLES_PATH/'time_explanation.csv')
print(time)