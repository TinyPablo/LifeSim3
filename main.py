from enum import Enum
from typing import List, Self
from collections import deque


class NeuronType(Enum):
    SENSORY = 0
    INTERNAL = 1
    ACTION = 2


class Neuron:
    def __init__(self, name: str, type: NeuronType) -> None:
        self.name: str = name
        self.type: NeuronType = type
        self.input_neurons: List[Self] = []
        self.output_neurons: List[Self] = []

    def __str__(self) -> str:
        input_names = [neuron.name for neuron in self.input_neurons]
        output_names = [neuron.name for neuron in self.output_neurons]
        return f'{self.name} ({self.type.name}) -> Inputs: {input_names} Outputs: {output_names}'
    
    def __repr__(self) -> str:
        return self.__str__()

    @staticmethod
    def connect_neurons(input_neuron: 'Neuron', output_neuron: 'Neuron') -> None:
        if input_neuron.type == NeuronType.ACTION:
            raise ValueError("INPUT neuron cannot be ACTION NEURON")
        elif output_neuron.type == NeuronType.SENSORY:
            raise ValueError("OUTPUT neuron cannot be SENSORY NEURON")
        
        input_neuron.output_neurons.append(output_neuron)
        output_neuron.input_neurons.append(input_neuron)
    
    @staticmethod
    def sort(neurons: List['Neuron']) -> List['Neuron']:
        in_degree = {neuron: len(neuron.input_neurons) for neuron in neurons}
        
        queue = deque([neuron for neuron in neurons if in_degree[neuron] == 0])
        
        sorted_neurons = []
        
        while queue:
            neuron = queue.popleft()
            sorted_neurons.append(neuron)
            
            for output_neuron in neuron.output_neurons:
                in_degree[output_neuron] -= 1
                if in_degree[output_neuron] == 0:
                    queue.append(output_neuron)
        
        if len(sorted_neurons) != len(neurons):
            raise ValueError("Cycle detected in the neural network")
        
        return sorted_neurons



i1 = Neuron('I1', NeuronType.INTERNAL)
i2 = Neuron('I2', NeuronType.INTERNAL)
i3 = Neuron('I3', NeuronType.INTERNAL)
i4 = Neuron('I4', NeuronType.INTERNAL)

neurons: List[Neuron] = [i1, i2, i3, i4]

Neuron.connect_neurons(i1, i2)
Neuron.connect_neurons(i2, i3)
Neuron.connect_neurons(i3, i4)
Neuron.connect_neurons(i4, i1)

sorted_neurons = Neuron.sort(neurons)

for n in sorted_neurons:
    print(n)
    
