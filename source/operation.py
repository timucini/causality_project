"""
This module is used to do operational activities with process data.
"""
from pandas import DataFrame

def to_case_table(event_frame:DataFrame, case_id:str='case:concept:name', activity_id:str='concept:name', timestamp:str='time:timestamp', aggregate:dict={}, fillna=None, rename_count:str='Num of') -> DataFrame:
    """
    This method is used to transform an evnetl-log to a case table.

    Parameters
    ---
    event_frame : pandas.DataFrame
        The dataframe representing the event-log
    case_id : str
        The column in the dataframe representing the case_ids
    activity_id : str
        The column in the dataframe representing the activity_ids
    timestamp : str
        The column in the dataframe representing the timestamp
    aggregate : dict
        A dict used to aggregate values by a given function. At least it will be used:
            'timestamp':count
    fillna : Any
        A value used to fill na values
    rename_count : str
        A string used to rename the counted columns
            Num of <Activity>

    Returns
    ---
    pandas.DataFrame
    """
    if rename_count:
        event_frame = event_frame.rename(columns={timestamp:rename_count})
        timestamp = rename_count
    aggregate.update({timestamp:'count'})
    event_frame = event_frame.groupby([case_id,activity_id]).agg(aggregate)
    event_frame = event_frame.reset_index()
    case_table = event_frame.pivot(index=case_id, columns=activity_id)
    case_table.columns = [" ".join(col) for col in case_table.columns.to_flat_index()]
    case_table = case_table.fillna(fillna).sort_index()
    return case_table

def apply_scenario(event_frame:DataFrame, scenario:dict, activity_id:str='concept:name') -> DataFrame:
    """
    This method is used to apply a scenario to an event-log.

    Parameters
    ---
    event_frame : pandas.DataFrame
        The dataframe representing the event-log
    scenario : dict
        The scenario wich should be applied
    activity_id : str
        The column in the dataframe representing the activity_ids

    Returns
    ---
    pandas.DataFrame:
        The eventframe with added columns for each scenario entry
    """
    for description, resource in scenario.items():
        if resource['apply_to']!=None:
            func = lambda x:resource['functions'][x[activity_id]](x[resource['apply_to']])
        else:
            func = lambda x:resource['functions'][x[activity_id]]()
        event_frame[description] = event_frame.apply(func, axis=1)
    return event_frame

def calculate_outcome(case_table:DataFrame, ruleset:dict) -> DataFrame:
    """
    This method is used to calculate the outcome of a process for each given ruleset.

    Parameters
    ---
    case_table : pandas.DataFrame
        The dataframe representing the case_table
    ruleset : dict
        Inhabitates the rules wich are applied

    Returns
    ---
    pandas.DataFrame:
        The case table with added columns for each applied rule
    """
    case_records = case_table.reset_index().to_dict('records')

    def get_value(activity:'str|tuple|list', record:dict, rule:str):
        if not isinstance(activity, str):
            values = []
            for paralell_activity in activity:
                values.append(get_value(paralell_activity, record, rule))
            if isinstance(activity, tuple):
                return max(values)
            elif isinstance(activity, list):
                return sum(values)
        else:
            return record[rule+' '+activity]

    for rule in ruleset:
        for record in case_records:
            value = 0
            if ruleset[rule]:
                value = value+get_value(ruleset[rule], record, rule)
            else:
                for acticity in record:
                    if rule in acticity:
                        value = value+record[acticity]
            record[rule] = value    
    return DataFrame(case_records).sort_values(case_table.index.name)