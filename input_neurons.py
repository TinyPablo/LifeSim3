from typing import List
from neuron import Neuron
from neuron_type import NeuronType


input_neurons: List[Neuron] = []


def get_distance_to_north(): 
    return .3
input_neurons.append(Neuron('DTN', NeuronType.INPUT, input_func=get_distance_to_north))

def get_distance_to_east():
    return .4
input_neurons.append(Neuron('DTE', NeuronType.INPUT, input_func=get_distance_to_east))

def get_distance_to_south():
    return .7
input_neurons.append(Neuron('DTS', NeuronType.INPUT, input_func=get_distance_to_south))

def get_distance_to_west():
    return .6
input_neurons.append(Neuron('DTW', NeuronType.INPUT, input_func=get_distance_to_west))

def get_age():
    return .2
input_neurons.append(Neuron('AGE', NeuronType.INPUT, input_func=get_age))