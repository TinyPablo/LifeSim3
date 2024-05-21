from enum import Enum
from typing import Dict, List, Self


class NeuronType(Enum):
    INPUT = 0
    INTERNAL = 1
    OUTPUT = 2


class Neuron:
    def __init__(self, name: str, type: NeuronType) -> None:
        self.name: str = name
        self.type: NeuronType = type
        self.input_neurons: List[Self] = []
        self.output_neurons: List[Self] = []

    def __str__(self) -> str:
        input_names = [neuron.name for neuron in self.input_neurons]
        output_names = [neuron.name for neuron in self.output_neurons]
        return f'{self.name} {input_names} {output_names}'
    
    def __repr__(self) -> str:
        return self.__str__()

    @staticmethod
    def connect_neurons(input_neuron: 'Neuron', output_neuron: 'Neuron') -> None:
        if input_neuron.type == NeuronType.OUTPUT:
            raise ValueError("INPUT neuron cannot be OUTPUT NEURON")
        if output_neuron.type == NeuronType.INPUT:
            raise ValueError("OUTPUT neuron cannot be INPUT NEURON")
        if input_neuron == output_neuron:
            raise ValueError("INPUT NEURON cannot be OUTPUT NEURON")
        if output_neuron in input_neuron.input_neurons or input_neuron in output_neuron.output_neurons:
            raise ValueError("Reverse connection is not allowed")
        if output_neuron in input_neuron.output_neurons or input_neuron in output_neuron.input_neurons:
            raise ValueError("Connection duplicate not allowed")

        input_neuron.output_neurons.append(output_neuron)
        output_neuron.input_neurons.append(input_neuron)

    
    @staticmethod
    def sort(neurons: List['Neuron']) -> List['Neuron']:
        sorted_neurons: List['Neuron'] = []
        no_incoming: List['Neuron'] = [n for n in neurons if len(n.input_neurons) == 0]
        print(no_incoming)
        while no_incoming:
            n = no_incoming.pop()
            sorted_neurons.append(n)
            
            for m in n.output_neurons:
                m.input_neurons.remove(n)
                if len(m.input_neurons) == 0:
                    no_incoming.append(m)

        if len(sorted_neurons) != len(neurons):
            raise ValueError("Graph has at least one cycle, sorting is not possible")

        return sorted_neurons
    
    @staticmethod
    def create_neurons(num_input: int, num_internal: int, num_output: int) -> Dict[str, 'Neuron']:
        neurons: Dict[str, Neuron] = {}

        for i in range(1, num_input + 1):
            name = f'S{i}'
            neurons[name] = Neuron(name, NeuronType.INPUT)

        for i in range(1, num_internal + 1):
            name = f'I{i}'
            neurons[name] = Neuron(name, NeuronType.INTERNAL)
            
        for i in range(1, num_output + 1):
            name = f'A{i}'
            neurons[name] = Neuron(name, NeuronType.OUTPUT)

        return neurons
    
    
ns = Neuron.create_neurons(2,4,1)

Neuron.connect_neurons(ns['S1'], ns['I1'])
Neuron.connect_neurons(ns['I1'], ns['I3'])
Neuron.connect_neurons(ns['I4'], ns['I3'])
Neuron.connect_neurons(ns['S1'], ns['I4'])
Neuron.connect_neurons(ns['I1'], ns['I2'])
Neuron.connect_neurons(ns['I3'], ns['I2'])
Neuron.connect_neurons(ns['I4'], ns['I2'])
Neuron.connect_neurons(ns['I2'], ns['A1'])
Neuron.connect_neurons(ns['S2'], ns['I2'])
Neuron.connect_neurons(ns['S2'], ns['A1'])

ns = list(ns.values())

sorted_neurons = Neuron.sort(ns)

for i, n in enumerate(sorted_neurons):
    print(i+1, n)
