from typing import List
from neuron import Neuron
from neuron_type import NeuronType


output_neurons: List[Neuron] = []


def move_forward():
    return print('moved forward')
output_neurons.append(Neuron('MFW', NeuronType.OUTPUT, output_func_a=move_forward))

def move_up():
    return print('moved up')
def move_down():
    return print('moved down')
output_neurons.append(Neuron('MUD', NeuronType.OUTPUT, output_func_a=move_up, output_func_b=move_down))

def move_right():
    return print('moved right')
def move_left():
    return print('moved left')
output_neurons.append(Neuron('MRL', NeuronType.OUTPUT, output_func_a=move_right, output_func_b=move_left))

def move_north():
    return print('moved north')
def move_south():
    return print('moved south')
output_neurons.append(Neuron('MNS', NeuronType.OUTPUT, output_func_a=move_north, output_func_b=move_south))

def move_east():
    return print('moved east')
def move_west():
    return print('moved west')
output_neurons.append(Neuron('MEW', NeuronType.OUTPUT, output_func_a=move_east, output_func_b=move_west))
