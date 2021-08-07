
from pandas import set_option

from source.processFeatures import *

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


from source.misc import get_scenario

unchanged_scenario = get_scenario(SIMULATION_DATA_DIR_PATH, 'Order-to-Cash_unchanged.csv')
changed_scenario = get_scenario(SIMULATION_DATA_DIR_PATH, 'Order-to-Cash_changed.csv')


from source.operation import apply_scenario

unchanged_eventlog = apply_scenario(unchanged_eventlog, unchanged_scenario, activity_id)
changed_eventlog = apply_scenario(changed_eventlog, changed_scenario, activity_id)


from source.operation import to_case_table

unchanged_case_table = to_case_table(unchanged_eventlog, case_id, activity_id, fillna=0, aggregate={'cost':'sum','time':'sum'})
changed_case_table = to_case_table(changed_eventlog, case_id, activity_id, fillna=0, aggregate={'cost':'sum','time':'sum'})

from source.operation import calculate_outcome

unchanged_ruleset = {'time':unchanged_basic_ruleset,'cost':None}
changed_ruleset = {'time':changed_basic_ruleset,'cost':None}

unchanged_case_table = calculate_outcome(unchanged_case_table, unchanged_ruleset)
changed_case_table = calculate_outcome(changed_case_table, changed_ruleset)


#ab hier :)

#kombrimieren Datensets
cleaned_unchanged_case_table = clean_dataframe(unchanged_case_table)
cleaned_changed_case_table = clean_dataframe(changed_case_table)

#anhängen veränderte Features
changed_dataset = add_changed_features(cleaned_changed_case_table)

#Erstellen der Feature Listen
generic_feature_list = get_generic_feature_list()
changed_feature_list = get_changed_feature_list()

# für causality.py um die Lineare Regression anzuwenden benötigt:
# Dataset unchanged -> cleaned_unchanged_case_table
# Dateset changed -> changed_dataset
# Liste generische Features -> generic_feature_list
# Liste geänderte Features -> changed_feature_list
