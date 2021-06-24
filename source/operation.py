def to_case_table(event_frame, case_id='case:concept:name', activity_id='concept:name', timestamp='time:timestamp', aggregate={}, fillna=None, rename_count='Num of'):
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

def apply_scenario(event_frame, scenario, activity_id='concept:name'):
    for description, resource in scenario.items():
        if resource['apply_to']!=None:
            func = lambda x:resource['functions'][x[activity_id]](x[resource['apply_to']])
        else:
            func = lambda x:resource['functions'][x[activity_id]]()
        event_frame[description] = event_frame.apply(func, axis=1)
    return event_frame

def calculate_outcome(case_table, ruleset):
    from pandas import DataFrame
    case_records = case_table.reset_index().to_dict('records')

    def get_value(activity, record, rule):
        if isinstance(activity, tuple):
            values = []
            for paralell_activity in activity:
                values.append(get_value(paralell_activity, record, rule))
            return max(values)
        else:
            return record[rule+' '+activity]

    for rule in ruleset:
        for record in case_records:
            value = 0
            if ruleset[rule]:
                for activity in ruleset[rule]:
                    value = value+get_value(activity, record, rule)
            else:
                for acticity in record:
                    if rule in acticity:
                        value = value+record[acticity]
            record[rule] = value
    
    return DataFrame(case_records).sort_values(case_table.index.name)