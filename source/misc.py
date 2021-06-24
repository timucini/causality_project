def read_bpmn(path, name=''):
    from pm4py import read_bpmn
    return read_bpmn(str(path/name))

def get_scenario(path, name='', scale=0.1, activity_id='concept:name'):
    from pandas import read_csv, to_timedelta
    from numpy.random import normal
    scenario_raw = read_csv(path/name)
    scenario_raw['Execution time'] = to_timedelta(scenario_raw['Execution time']).dt.total_seconds()/60/60
    scenario = {'time':{'apply_to':None,'functions':{}},'cost':{'apply_to':'time','functions':{}}}
    for record in scenario_raw.to_dict('records'):
        if record['Automated']:
            scenario['time']['functions'][record['Activity']] = lambda:record['Execution time']
        else:
            scenario['time']['functions'][record['Activity']] = lambda:normal(record['Execution time'],record['Execution time']*scale)
        scenario['cost']['functions'][record['Activity']] = lambda x:record['Execution costs']+x*record['Resources cost/hour']
    return scenario

def get_dummy_scenario(activities, scale=0.1, activity_id='concept:name'):
    from numpy.random import randint, normal, random_sample
    scenario = {'time':{'apply_to':None,'functions':{}},'cost':{'apply_to':'time','functions':{}}}
    for activity in activities:
        time = randint(5, 300)/60
        cost = randint(1, 100)
        factor = randint(5, 100)
        scenario['time']['functions'][activity] = lambda:normal(time,time*scale)
        scenario['cost']['functions'][activity] = lambda x:cost+x*factor
    return scenario

def get_dummy_ruleset(event_frame, case_id='case:concept:name', activity_id='concept:name', n_parallels=2, name='cost'):
    from numpy.random import randint
    case = event_frame[case_id].drop_duplicates().sample(1).iloc[0]
    activities = event_frame[event_frame[case_id]==case][activity_id]
    parallels = activities.sample(n_parallels)
    ruleset = activities.drop(parallels.index).to_list()
    for parallel in parallels:
        pos = randint(0, len(ruleset))
        ruleset[pos] = (ruleset[pos], parallel)
    return {name:ruleset}