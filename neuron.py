import copy
from math import tanh
from typing import Callable, Dict, List, Set
from neuron_type import NeuronType


class Neuron:
    def __init__(self, name: str, type: NeuronType, *, input_func: Callable = None, output_func_a: Callable = None, output_func_b: Callable = None) -> None:
        self.name: str = name
        self.type: NeuronType = type
        
        if self.type == NeuronType.INPUT and input_func is None:
            raise TypeError('INPUT NEURON requires input function')
        self.input_func: Callable = input_func
        
        if self.type == NeuronType.OUTPUT and output_func_a is None:
            raise TypeError('OUTPUT NEURON requires output function a')
        self.output_func_a: Callable = output_func_a
        self.output_func_b: Callable = output_func_b

        self.input_neurons: List['Neuron'] = []
        self.output_neurons: List['Neuron'] = []

        self.weight: float = None
        self.output: float = None 

    def __str__(self) -> str:
        input_names: List[str] = [neuron.name for neuron in self.input_neurons]
        output_names: List[str] = [neuron.name for neuron in self.output_neurons]
        return f'{self.name} {input_names} {output_names}'

    def __repr__(self) -> str:
        return self.__str__()
    
    def execute(self) -> None:
        if self.type == NeuronType.INPUT:
            neuron_output = self.input_func()
            self.output = neuron_output
            print(self, self.output)


        elif self.type == NeuronType.INTERNAL:
            input_neurons_sum: float = sum([input_neuron.output * input_neuron.weight for input_neuron in self.input_neurons])
            print([(input_neuron.output, input_neuron.weight) for input_neuron in self.input_neurons])
            print(f'{input_neurons_sum = }')
            neuron_output = tanh(input_neurons_sum)
            self.output = neuron_output
            print(f'{tanh(input_neurons_sum) = }')
            print(self, neuron_output)
            

        elif self.type == NeuronType.OUTPUT:
            input_neurons_sum: float = sum([input_neuron.output * input_neuron.weight for input_neuron in self.input_neurons])
            print([(input_neuron.output, input_neuron.weight) for input_neuron in self.input_neurons])
            print(f'{input_neurons_sum = }')
            neuron_output = tanh(input_neurons_sum)
            print(f'{tanh(input_neurons_sum) = }')
            print(self, neuron_output)

            if neuron_output > 0:
                self.output_func_a()
            elif self.output_func_b is not None:
                self.output_func_b()

    @staticmethod
    def connect_neurons(input_neuron: 'Neuron', output_neuron: 'Neuron', connection_weight: float) -> None:
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
        
        if Neuron.detect_cycle(input_neuron):
            input_neuron.output_neurons.remove(output_neuron)
            output_neuron.input_neurons.remove(input_neuron)
            raise ValueError("Adding this connection creates a cycle")
        
        input_neuron.weight = connection_weight 

    @staticmethod
    def detect_cycle(start: 'Neuron') -> bool:
        def visit(neuron: 'Neuron', visited: Set['Neuron'], rec_stack: Set['Neuron']) -> bool:
            if neuron not in visited:
                visited.add(neuron)
                rec_stack.add(neuron)

                for neighbor in neuron.output_neurons:
                    if neighbor not in visited and visit(neighbor, visited, rec_stack):
                        return True
                    elif neighbor in rec_stack:
                        return True

                rec_stack.remove(neuron)
            return False

        visited: Set[Neuron] = set()
        rec_stack: Set[Neuron] = set()
        return visit(start, visited, rec_stack)

    @staticmethod
    def sort(neurons: List['Neuron']) -> List['Neuron']:
        neurons_copy = copy.deepcopy(neurons)
        
        sorted_neurons: List['Neuron'] = []
        no_incoming: List['Neuron'] = [n for n in neurons_copy if len(n.input_neurons) == 0]

        while no_incoming:
            n: Neuron = no_incoming.pop()
            sorted_neurons.append(n)

            for m in n.output_neurons:
                m.input_neurons.remove(n)
                if len(m.input_neurons) == 0:
                    no_incoming.append(m)

        if len(sorted_neurons) != len(neurons_copy):
            raise ValueError("Graph has at least one cycle, sorting is not possible")
        
        sorted_map = {neuron.name: index for index, neuron in enumerate(sorted_neurons)}
        
        neurons.sort(key=lambda neuron: sorted_map.get(neuron.name, float('inf')))
        
        return neurons
    
    @staticmethod
    def filter(neurons: List['Neuron']) -> List['Neuron']:
        return [n for n in neurons if n.input_neurons or n.output_neurons]
    
    @staticmethod
    def create_neurons(num_input: int, num_internal: int, num_output: int) -> List['Neuron']:
        neurons: List['Neuron'] = []

        for i in range(1, num_input + 1):
            neurons.append(Neuron(f'S{i}', NeuronType.INPUT))

        for i in range(1, num_internal + 1):
            neurons.append(Neuron(f'I{i}', NeuronType.INTERNAL))

        for i in range(1, num_output + 1):
            neurons.append(Neuron(f'A{i}', NeuronType.OUTPUT))

        return neurons