def to_frame(log, zfill):
    from pm4py import convert_to_dataframe as as_frame
    event_frame = as_frame(log)
    event_frame['case:concept:name'] = 'C'+event_frame['case:concept:name'].str.zfill(zfill)
    return event_frame

def basic_bpmn_petri_net(bpmn, n=1000):
    from pm4py import convert_to_petri_net as convert
    from pm4py.algo.simulation.playout.petri_net.variants.basic_playout import apply_playout as simulate
    net, im, fm = convert(bpmn)
    log = simulate(net, im, n, final_marking=fm)
    return to_frame(log, len(str(n)))

def basic_bpmn_tree(bpmn, n=1000):
    from pm4py import convert_to_process_tree as convert
    from pm4py.algo.simulation.playout.process_tree.variants.basic_playout import apply as simulate
    from pm4py.algo.simulation.playout.process_tree.variants.basic_playout import Parameters as params
    tree = convert(bpmn)
    log = simulate(tree, parameters={params.NO_TRACES:n})
    return to_frame(log, len(str(n)))