"""
This module is used to simulate processes.
"""
from pm4py.objects.log.obj import EventLog
from pm4py.objects.bpmn.obj import BPMN
from pandas import DataFrame


def to_frame(log: EventLog, zfill: int) -> DataFrame:
    """
    This method is used to convert a pm4py event-log to a pandas dataframe.

    Parameters
    ---
    log : pm4py.objects.log.obj.EventLog
        The event-log which should be converted
    zfill : int
        The maximum number of zeros that lead the case id

    Returns
    ---
    pandas.DataFrame
    """
    from pm4py import convert_to_dataframe as as_frame
    event_frame = as_frame(log)
    event_frame['case:concept:name'] = 'C' + event_frame['case:concept:name'].str.zfill(zfill)
    return event_frame


def basic_bpmn_petri_net(bpmn: BPMN, n: int = 1000) -> DataFrame:
    """
    This method is used to simulate a bpmn with an according petri net.

    Parameters
    ---
    bpmn : pm4py.objects.log.obj.BPMN
        The bpmn which should be simulated
    n : int
        The amount of cases that should be simulated

    Returns
    ---
    pandas.DataFrame
    """
    from pm4py import convert_to_petri_net as convert
    from pm4py.algo.simulation.playout.petri_net.variants.basic_playout import apply_playout as simulate
    net, im, fm = convert(bpmn)
    log = simulate(net, im, n, final_marking=fm)
    return to_frame(log, len(str(n)))


def basic_bpmn_tree(bpmn: BPMN, n: int = 1000) -> DataFrame:
    """
    This method is used to simulate a bpmn with an according process tree.

    Parameters
    ---
    bpmn : pm4py.objects.log.obj.BPMN
        The bpmn which should be simulated
    n : int
        The amount of cases that should be simulated

    Returns
    ---
    pandas.DataFrame
    """
    from pm4py import convert_to_process_tree as convert
    from pm4py.algo.simulation.playout.process_tree.variants.basic_playout import apply as simulate
    from pm4py.algo.simulation.playout.process_tree.variants.basic_playout import Parameters as params
    tree = convert(bpmn)
    log = simulate(tree, parameters={params.NO_TRACES: n})
    return to_frame(log, len(str(n)))
