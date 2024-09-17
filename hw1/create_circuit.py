import re

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

#class to represent the type of each node in a circuit
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

class gate:
    '''
    This class is used to represent a gate

    Attributes:
    num_inputs: Number of inputs(int)
    type: Type of the gate(gate_type)
    input_nodes: Nodes that are fed in
    Output node: Output node of the gate
    '''

    def __init__(self, string_representation):
        '''
        This function creates a gate

        param[in] string_representation String representation of the gate
                                        The string after = in the circuit bench file
        '''
        self.input_nodes = []
        self.output_node = None
        self.type = None
        self.num_inputs = 0
        self.gate_string = ""

        self.__update_gate_type(string_representation)

    def __update_gate_type(self, string_representation: str):
        '''
        This function updates the gate type
        '''
        gate_dict = {"AND" : gate_type.AND_gate,
                     "OR"  : gate_type.OR_gate,
                     "NOT" : gate_type.NOT_gate,
                     "NOR" : gate_type.NOR_gate,
                     "NAND": gate_type.NAND_gate,
                     "XOR" : gate_type.XOR_gate,
                     "XNOR": gate_type.XNOR_gate}

        self.gate_string = re.match(r'^[^()]+', string_representation)

        if self.gate_string:
            self.gate_string = self.gate_string.group()
        else:
            raise GateReprError(string_representation)
        

        if self.gate_string not in gate_dict:
            raise GateNotDefined(self.gate_string)
        else:
            self.type = gate_dict[self.gate_string]
            self.input_nodes = re.findall(r'\((.*?)\)', string_representation)[0]
            self.input_nodes = self.input_nodes.split(",")
            self.num_inputs = len(self.input_nodes)

    def __repr__(self):
        '''
        Return a string representing the gate information
        '''
        str_repr = f"{self.num_inputs}-input {self.gate_string} gate | Input nodes: "
        for node in self.input_nodes:
            str_repr = str_repr + f"{node},"
        str_repr = str_repr[:-1] + " | "
        str_repr = f"{str_repr}Output node: {self.output_node.name}"
        return str_repr


#class to reprsent each node in a circuit
class node:
    '''
    This class represents a node in the circuit

    Attributes:
    name: Name of the node(string)
    type: Type of the node(node_type)
    value: Value of the node(node_value)
    gate_type: Type of gate(String)
    nodes_fed_in: List of nodes fed in(node)
    '''

    def __init__(self, circuit_bench_line: str):
        '''
        Initialize the object. 

        param[in] circuit_bench_line: A line in the circuit bench file
        '''
        self.name = None
        self.type = None
        self.value = node_value.undefined
        self.gate = None

        #check if it is an input node
        if ("INPUT" in circuit_bench_line.upper()):
            self.type = node_type.input_node
            self.name = re.findall(r'\((.*?)\)', circuit_bench_line)[0]
        elif ("OUTPUT" in circuit_bench_line.upper()):
            self.type = node_type.output_node
            self.name = re.findall(r'\((.*?)\)', circuit_bench_line)[0]
        else:
            #its an internal wire
            self.type = node_type.internal_wire
            self.name = circuit_bench_line.split("=")[0] #split at "=" symbol and the first element in the list
                                                         #is the node name
            self.name = self.name.rstrip() #remove any trailing white spaces
            self.__update_gate(circuit_bench_line)

    def __update_gate(self, circuit_bench_line):
        '''
        Updates the gate information of a node
        '''
        gate_string_representation = circuit_bench_line.split("=")[1]
        gate_string_representation = gate_string_representation.lstrip()
        self.gate = gate(gate_string_representation)
        self.gate.output_node = self

    def update(self, circuit_bench_file):
        '''
        This function updates the nodes properties based on the new circuit bench file
        '''
        if "OUTPUT" in circuit_bench_file.upper():
            #node is an output node
            self.type = node_type.output_node
        else:
            #an assignment done to the node, update the gate type
            self.__update_gate(circuit_bench_file)


class circuit:
    '''
    This class represents a circuit described in the circuit bench file

    Attributes:
    nodes: List of all the nodes(nodes)
    input_list: Index of input nodes in nodes list(int)
    output_list: Index of output nodes in nodes list(int)    
    '''
    
    def __init__(self, circuit_bench_file):
        '''
        Initializes the class

        param[in] circuit_bench_file: Path to the circuit bench file
        '''
        self.nodes = []
        self.input_list = []
        self.output_list = []
        self.node_index = {} #index of each node in the nodes list, key values for this dictionary are the node names
        
        lines = self.__parse_circuit_bench_file(circuit_bench_file)
        #create nodes
        self.__create_nodes(lines)
        #check if all outputs are defined
        self.__check_output_definition()

    def __parse_circuit_bench_file(self, circuit_bench_file):
        '''
        This function parses the circuit bench file and sends out a list
        '''
        lines = []

        with open(circuit_bench_file, "r") as f:
            for line in f:
                line = line.replace("\n", "")
                if len(line) == 0:
                    continue
                lines.append(line)

        return lines
    
    def __create_nodes(self, lines):
        '''
        This function creates nodes from the lines read from the circuit bench file
        '''
        for line in lines:
            #check if node is already created - Possible when output is declared after using a wire
            node_name = re.findall(r'\((.*?)\)', line)[0]

            if "=" in line:
                node_name = line.split("=")[0]
                node_name = node_name.rstrip()

            if node_name in self.node_index:
                #update the node properties
                self.nodes[self.node_index[node_name]].update(line)
            else:
                #new node in the circuit
                #create a node and add it to the node list
                self.nodes.append(node(line))
                if self.nodes[-1].type == node_type.input_node:
                    self.input_list.append(self.nodes[-1].name)
                elif self.nodes[-1].type == node_type.output_node:
                    self.output_list.append(self.nodes[-1].name)
                self.node_index[self.nodes[-1].name] = len(self.nodes) - 1

    
    def __check_output_definition(self):
        '''
        This function checks if all outputs are defined
        '''
        for node in self.nodes:
            if node.type == node_type.output_node:
                if node.gate == None:
                    raise FloatingOutput(node.name)
                
    def __repr__(self):
        '''
        This function returns the string representation of a circuit
        '''
        str_repr = "-------------------------------------------\n"
        str_repr = f"{str_repr}--------------Input Nodes------------------\n{self.input_list}\n"
        str_repr = f"{str_repr}-------------Output Nodes------------------\n{self.output_list}\n"
        str_repr = f"{str_repr}---------------Gate list-------------------\n"

        for node in self.nodes:
            if node.type != node_type.input_node:
                str_repr = f"{str_repr}{node.gate}\n"

        return str_repr
    
circuit_under_test = circuit("p1.txt")
print(circuit_under_test)