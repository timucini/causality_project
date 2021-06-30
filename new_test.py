from os import name
from pathlib import Path
from source.misc import read_bpmn, get_dummy_scenario, get_dummy_ruleset, get_scenario
from source.simulation import basic_bpmn_petri_net
from source.operation import to_case_table, apply_scenario, calculate_outcome

path = Path(__file__).parent
bpmn = read_bpmn(path/'resources'/'bpmns', name='Order-to-Cash-Model-1.bpmn')
event_frame = basic_bpmn_petri_net(bpmn)
#scenario = get_dummy_scenario(event_frame['concept:name'].unique().tolist())
scenario = get_scenario(path/'resources'/'simulation_data', name='Order-to-Cash_unchanged.csv')
print(event_frame['concept:name'].drop_duplicates())
event_frame = apply_scenario(event_frame, scenario)
print(event_frame)
case_table = to_case_table(event_frame, fillna=0, aggregate={'cost':'sum','time':'sum'})
print(case_table)
ruleset = get_dummy_ruleset(event_frame)
print(ruleset)
#ruleset = {'time':None,'cost':None}
#case_table = calculate_outcome(case_table, ruleset)
#print(case_table)
#case_table.to_csv(path/'test_ct2.csv', sep=';', index=False, decimal=',', quoting=2)

activities = {'changed_process': ["Check stock availability", "Check raw materials availabilty", "Notify unavailability to customer",
                                    ("Request raw materials from Supplier 1", "Request raw materials from Supplier 2"),
                                    ("Obtain raw materials from Supplier 1", "Obtain raw materials from Supplier 2"),
                                    "Manufacture product", "Retrieve product from warehouse", "Confirm order", "Get shipping address",
                                    ("Ship product", "Emit invoice"), "Receive Payment", "Archieve order"],

            'unchanged_process': ["Check stock availability", "Check raw materials availabilty", ("Request raw materials from Supplier 1",
                                    "Request raw materials from Supplier 2", "Obtain raw materials from Supplier 1",
                                    "Obtain raw materials from Supplier 2"), "Manufacture product", "Retrieve product from warehouse",
                                    "Confirm order", ("Get shipping address", "Ship product", "Emit invoice", "Receive Payment"),
                                    "Archieve order"]}