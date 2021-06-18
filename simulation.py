import pm4py


def basic_simulate_bpmn_petri_net(bpmn, n=1000):
    from pm4py import convert_to_petri_net as convert
    from pm4py.algo.simulation.playout.petri_net.variants.basic_playout import apply_playout as simulate
    from pm4py import convert_to_dataframe as as_frame
    net, im, fm = convert(bpmn)
    return as_frame(simulate(net, im, n, final_marking=fm))

def extensive_simulate_bpmn_petri_net(bpmn, n=1000, traces=5):
    from pm4py import convert_to_petri_net as convert
    from pm4py.algo.simulation.playout.petri_net.variants import extensive
    from pm4py.algo.simulation.playout.petri_net.algorithm import Variants
    from pm4py import convert_to_dataframe as as_frame
    net, im, fm = convert(bpmn)
    #return as_frame(extensive.apply(net, im, fm, parameters={Variants.EXTENSIVE.value.Parameters.}))
