def read_bpmn(path, name=''):
    from pm4py import read_bpmn
    return read_bpmn(str(path/name))