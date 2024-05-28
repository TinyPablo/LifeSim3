from copy import deepcopy
import random
from typing import List
from entity import Entity
from neuron import Neuron
from neuron_type import NeuronType

input_neurons: List[Neuron] = []


def get_distance_to_north(entity: Entity):
    return entity.distance_to_north
input_neurons.append(Neuron('DTN', NeuronType.INPUT, input_func=get_distance_to_north))

def get_distance_to_east(entity: Entity):
    return entity.distance_to_east
input_neurons.append(Neuron('DTE', NeuronType.INPUT, input_func=get_distance_to_east))

def get_distance_to_south(entity: Entity):
    return entity.distance_to_south
input_neurons.append(Neuron('DTS', NeuronType.INPUT, input_func=get_distance_to_south))

def get_distance_to_west(entity: Entity):
    return entity.distance_to_west
input_neurons.append(Neuron('DTW', NeuronType.INPUT, input_func=get_distance_to_west))

def get_age(entity: Entity):
    return entity.age
input_neurons.append(Neuron('AGE', NeuronType.INPUT, input_func=get_age))

def random_input(entity: Entity):
    return random.random()
input_neurons.append(Neuron('RND', NeuronType.INPUT, input_func=random_input))


def get_fresh_input_neurons() -> List[Neuron]:
    return deepcopy(input_neurons)