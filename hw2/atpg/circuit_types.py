class node_type:
    input_node = 0
    output_node = 1
    internal_wire = 3

#class to represnt the value of each node
class node_value:
    high = 1
    low = 0
    undefined = -1

class gate_type:
    AND_gate = 0
    OR_gate = 1
    NOT_gate = 2
    NAND_gate = 3
    NOR_gate = 4
    XOR_gate = 5
    XNOR_gate = 6