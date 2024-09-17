#custom errors to be used
class GateNotDefined(Exception):
    '''
    Error to be raised from the gate is not found in the the basic gates 
    '''
    def __init__(self, gate):
        self.message = f"{gate} not defined"
        super().__init__(self.message)

class GateReprError(Exception):
    '''
    Error to be raised for illegal gate declaration format 
    '''
    def __init__(self, gate_repr):
        self.message = f"{gate_repr} not valid"
        super().__init__(self.message)

#custom errors to be used
class FloatingOutput(Exception):
    '''
    Error to be raised from the gate is not found in the the basic gates 
    '''
    def __init__(self, node_name):
        self.message = f"{node_name} is floating, no driver for output node is defined"
        super().__init__(self.message)