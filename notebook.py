
from pandas import set_option
set_option('display.expand_frame_repr', False)
from pm4py import read_xes
from pm4py import convert_to_dataframe as as_frame
from environment import *

case_id = 'case:concept:name'
activity_id = 'concept:name'

unchanged_basic_ruleset = [
    "Check stock availability",
    "Check raw materials availabilty",
    (
        [
            "Request raw materials from Supplier 1",
            "Obtain raw materials from Supplier 1"
        ],
        [
            "Request raw materials from Supplier 2",
            "Obtain raw materials from Supplier 2"
        ]
    ),
    "Manufacture product",
    "Retrieve product from warehouse",
    "Confirm order",
    (
        [
            "Get shipping address",
            "Ship product"
        ],
        [
            "Emit invoice",
            "Receive Payment"
        ]
    ),
    "Archieve order"
]
changed_basic_ruleset = [
    "Check stock availability",
    "Check raw materials availabilty",
    "Notify unavailability to customer",
    (
        "Start request raw materials from Supplier 1",
        "Start request raw materials from Supplier 2"
    ),
    (
        "Obtain raw materials from Supplier 1",
        "Obtain raw materials from Supplier 2"
    ),
    "Manufacture product",
    "Retrieve product from warehouse",
    "Confirm order",
    "Get shipping address",
    (
        "Ship product",
        [
            "Emit invoice",
            "Receive Payment"
        ]
    ),
    "Archieve order"
]
print(unchanged_basic_ruleset)
print(changed_basic_ruleset)

from source.misc import read_bpmn
from source.simulation import basic_bpmn_petri_net

unchanged_bpmn = read_bpmn(BPMN_DIR_PATH,'Order-to-Cash-Model-1.bpmn')
changed_bpmn = read_bpmn(BPMN_DIR_PATH,'Order-to-Cash-Model-2.bpmn')

unchanged_eventlog = basic_bpmn_petri_net(unchanged_bpmn)
changed_eventlog = basic_bpmn_petri_net(changed_bpmn)

print(unchanged_eventlog)
print(changed_eventlog)

from source.misc import get_scenario

unchanged_scenario = get_scenario(SIMULATION_DATA_DIR_PATH, 'Order-to-Cash_unchanged.csv')
changed_scenario = get_scenario(SIMULATION_DATA_DIR_PATH, 'Order-to-Cash_changed.csv')

print(unchanged_scenario)
print(changed_scenario)

from source.operation import apply_scenario

unchanged_eventlog = apply_scenario(unchanged_eventlog, unchanged_scenario, activity_id)
changed_eventlog = apply_scenario(changed_eventlog, changed_scenario, activity_id)
print(unchanged_eventlog)
print(changed_eventlog)

from source.operation import to_case_table

unchanged_case_table = to_case_table(unchanged_eventlog, case_id, activity_id, fillna=0, aggregate={'cost':'sum','time':'sum'})
changed_case_table = to_case_table(changed_eventlog, case_id, activity_id, fillna=0, aggregate={'cost':'sum','time':'sum'})

print(unchanged_case_table)
print(changed_case_table)

from source.operation import calculate_outcome

unchanged_ruleset = {'time':unchanged_basic_ruleset,'cost':None}
changed_ruleset = {'time':changed_basic_ruleset,'cost':None}

unchanged_case_table = calculate_outcome(unchanged_case_table, unchanged_ruleset)
changed_case_table = calculate_outcome(changed_case_table, changed_ruleset)

print(unchanged_case_table)
print(changed_case_table)

unchanged_case_table.to_csv(CASE_TABLE_DIR_PATH/'unchanged.csv', index=False)
changed_case_table.to_csv(CASE_TABLE_DIR_PATH/'changed.csv', index=False)


