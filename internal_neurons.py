from copy import deepcopy
from typing import List
from neuron import Neuron
from neuron_type import NeuronType
from simulation_settings import settings

internal_neurons: List[Neuron] = [Neuron(f'I{i+1}', NeuronType.INTERNAL) for i in range(settings.MAX_INTERNAL_NEURONS)]

def get_fresh_internal_neurons() -> List[Neuron]:
    return deepcopy(internal_neurons)