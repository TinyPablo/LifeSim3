from copy import deepcopy
from typing import List
from input_neurons import input_neurons
from neuron import Neuron
from output_neurons import output_neurons
from internal_neurons import internal_neurons

def get_neuron_set() -> tuple[List[Neuron], List[Neuron], List[Neuron]]:
    return deepcopy(input_neurons), deepcopy(output_neurons), deepcopy(internal_neurons)