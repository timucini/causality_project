import pandas as pd

def getSimulationDataUnchangedProcess():
    data_dict = pd.read_csv('../resources/simulation_data/Order-to-Cash_unchanged.csv').to_dict('record')
    return data_dict

def getSimulationDataChangedProcess():
    data_dict = pd.read_csv('../resources/simulation_data/Order-to-Cash_changed.csv').to_dict('record')
    return data_dict
    