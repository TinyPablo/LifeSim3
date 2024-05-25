from typing import List
from neuron import Neuron
from neuron_type import NeuronType


MAX_INTERNAL_NEURONS = 3

internal_neurons: List[Neuron] = [Neuron(f'I{i+1}', NeuronType.INTERNAL) for i in range(MAX_INTERNAL_NEURONS)]