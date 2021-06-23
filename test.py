from networkx.algorithms import similarity
import pm4py as pm
import pandas as pd
from path import path
#from pm4py.algo.simulation.playout.process_tree import algorithm as sim
from pm4py.algo.simulation.playout.petri_net.variants import basic_playout as sim
from pm4py.algo.simulation.playout.petri_net.variants import extensive 

bpmn = pm.read_bpmn(str(path/"resources"/"bpmns"/"Order-to-Cash-Model-2.bpmn"))
#pm.view_bpmn(bpmn)
net, im, fm = pm.convert_to_petri_net(bpmn)
evl = sim.apply_playout(net, im, no_traces=1000, max_trace_length=10, final_marking=fm)
frame = pm.convert_to_dataframe(evl)

case_id = 'case:concept:name'
activity_names = 'concept:name'

cases = frame[case_id].unique().tolist()
activities = frame[activity_names].drop_duplicates()

def to_case_table(cases, activities, frame):
    case_table = []
    for case in cases:
        case_log = frame[frame[case_id]==case]
        time = (case_log['time:timestamp'].max()-case_log['time:timestamp'].min()).total_seconds()
        keys = activities.to_list()
        values = activities.isin(case_log[activity_names]).to_list()
        for key in pd.Series(keys)[values]:
            values[keys.index(key)] = len(case_log[case_log[activity_names]==key])
        for i in range(0,len(values)):
            values[i] = int(values[i])
        case_entry = dict(zip(['case_id']+keys+['time'],[case]+values+[time]))
        case_table.append(case_entry)
    return pd.DataFrame(case_table)
to_case_table(cases, activities, frame).to_csv(path/"test2.csv", index=False)