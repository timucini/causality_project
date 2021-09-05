"""
This module is used for all required none operational and simulating functions. The module and the containing functions
can be deprecated in further versions of the project.
"""
from pathlib import Path
from typing import List
from pandas import DataFrame
from pm4py.objects.bpmn.obj import BPMN


def read_bpmn(path: Path, name: str = '') -> BPMN:
    """
    This method is used to read bpmn/xml files.

    Parameters:
    ---
    path : pathlib.Path
        The path of the bpmn file
    name : str
        The name of the bpmn file, if the path is a directory

    Returns
    ---
    pm4py.objects.bpmn.obj.BPMN
    """
    from pm4py import read_bpmn
    return read_bpmn(str(path / name))


def get_scenario(path: Path, name: str = '', scale: float = 0.1) -> dict:
    """
    This method is used to read a CSV file representing a scenario. The file should contain columns with headers like:

    column | type
    --- | ---
    'Activity' | str
    'Execution time' | timedelta
    'Execution costs' | numerical
    'Automated' | boolean
    'Resources cost/hour' | numerical

    Parameters
    ---
    path : pathlib.Path
        The path of the CSV file
    name : str
        The name of the CSV file, if the path is a directory
    scale : float
        The scale which the output should variate if the activity is not automated
    
    Returns
    ---
    dict:
        A dictionary representing a scenario
        'time':dict
            'apply_to': str | None
            'functions': dict
                '<Activity>': lambda function
        'cost':dict
            'apply_to': str | None
            'functions': dict
                '<Activity>': lambda function
    """
    from pandas import read_csv, to_timedelta
    from numpy.random import normal
    scenario_raw = read_csv(path / name)
    scenario_raw['Execution time'] = to_timedelta(scenario_raw['Execution time']).dt.total_seconds() / 60 / 60
    scenario = {'time': {'apply_to': None, 'functions': {}}, 'cost': {'apply_to': 'time', 'functions': {}}}
    for record in scenario_raw.to_dict('records'):
        if record['Automated']:
            scenario['time']['functions'][record['Activity']] = lambda: record['Execution time']
        else:
            scenario['time']['functions'][record['Activity']] = lambda: normal(record['Execution time'],
                                                                               record['Execution time'] * scale)
        scenario['cost']['functions'][record['Activity']] = lambda x: record['Execution costs'] + x * record[
            'Resources cost/hour']
    return scenario


def get_dummy_scenario(activities: List[str], scale: float = 0.1) -> dict:
    """
    This method generates a dummy scenario from scratch by using the given activities.

    Parameters
    ---
    activities : list of str
        The activities used to create the dummy scenario
    scale : float
        The scale which the output should variate
    
    Returns
    ---
    dict:
        A dictionary representing a scenario
        'time':dict
            'apply_to': None
            'functions': dict
                '<Activity>': lambda function
        'cost':dict
            'apply_to': 'time'
            'functions': dict
                '<Activity>': lambda function
    """
    from numpy.random import randint, normal
    scenario = {'time': {'apply_to': None, 'functions': {}}, 'cost': {'apply_to': 'time', 'functions': {}}}
    for activity in activities:
        time = randint(5, 300) / 60
        cost = randint(1, 100)
        factor = randint(5, 100)
        scenario['time']['functions'][activity] = lambda: normal(time, time * scale)
        scenario['cost']['functions'][activity] = lambda x: cost + x * factor
    return scenario


def get_dummy_ruleset(event_frame: DataFrame, case_id: str = 'case:concept:name', activity_id: str = 'concept:name',
                      n_parallels: int = 2, name: str = 'cost') -> dict:
    """
    This method generates a dummy ruleset from scratch by using the event-log.

    Parameters
    ---
    event_frame : pandas.DataFrame
        The dataframe representing the event-log
    case_id : str
        The column in the dataframe representing the case_ids
    activity_id : str
        The column in the dataframe representing the activity_ids
    n_parallels : int
        Number of parallel performed activities
    name : str
        Name of the ruleset
    
    Returns
    ---
    dict:
        A dictionary representing a ruleset
        'name': list
            [<activity>,(<activity>,<activity>),...]
    """
    from numpy.random import randint
    case = event_frame[case_id].drop_duplicates().sample(1).iloc[0]
    activities = event_frame[event_frame[case_id] == case][activity_id]
    parallels = activities.sample(n_parallels)
    ruleset = activities.drop(parallels.index).to_list()
    for parallel in parallels:
        pos = randint(0, len(ruleset))
        ruleset[pos] = (ruleset[pos], parallel)
    return {name: ruleset}


def min_max_scale(frame: DataFrame, scale_min: int = 0, scale_max: int = 1) -> DataFrame:
    return_frame = frame.copy()
    numerics = frame.select_dtypes(include='number').columns
    for column in numerics:
        column_min = frame[column].min()
        column_max = frame[column].max()
        if column_min == scale_min and column_max == scale_max:
            continue
        if column_min == column_max:
            scale = 0
        else:
            scale = (scale_max - scale_min) / (column_max - column_min)
        return_frame[column] = scale * frame[column] - frame[column].min() * scale
    return return_frame
