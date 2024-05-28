from copy import deepcopy
import random
from typing import List
from direction import Direction
from entity import Entity
from neuron import Neuron
from neuron_type import NeuronType


def get_distance_to_north(entity: 'Entity'):
    return entity.distance_to_north

def get_distance_to_east(entity: 'Entity'):
    return entity.distance_to_east

def get_distance_to_south(entity: 'Entity'):
    return entity.distance_to_south

def get_distance_to_west(entity: 'Entity'):
    return entity.distance_to_west

def get_age(entity: 'Entity'):
    return entity.age

def random_input(entity: 'Entity'):
    return random.random()

def blockage_in_direction(entity, direction):
    return entity.grid.blockage_in_direction(entity, direction)

def blockage_up(entity: 'Entity'):
    return blockage_in_direction(entity, Direction.UP)

def blockage_down(entity: 'Entity'):
    return blockage_in_direction(entity, Direction.DOWN)

def blockage_left(entity: 'Entity'):
    return blockage_in_direction(entity, Direction.LEFT)

def blockage_right(entity: 'Entity'):
    return blockage_in_direction(entity, Direction.RIGHT)

def blockage_up_left(entity: 'Entity'):
    return blockage_in_direction(entity, Direction.UP_LEFT)

def blockage_up_right(entity: 'Entity'):
    return blockage_in_direction(entity, Direction.UP_RIGHT)

def blockage_down_left(entity: 'Entity'):
    return blockage_in_direction(entity, Direction.DOWN_LEFT)

def blockage_down_right(entity: 'Entity'):
    return blockage_in_direction(entity, Direction.DOWN_RIGHT)


input_neurons: List[Neuron] = [
    Neuron('DISTANCE TO NORTH', NeuronType.INPUT, input_func=get_distance_to_north),
    Neuron('DISTANCE TO EAST', NeuronType.INPUT, input_func=get_distance_to_east),
    Neuron('DISTANCE TO SOUTH', NeuronType.INPUT, input_func=get_distance_to_south),
    Neuron('DISTANCE TO WEST', NeuronType.INPUT, input_func=get_distance_to_west),
    Neuron('AGE', NeuronType.INPUT, input_func=get_age),
    Neuron('RANDOM INPUT', NeuronType.INPUT, input_func=random_input),
    Neuron('BLOCKAGE UP', NeuronType.INPUT, input_func=blockage_up),
    Neuron('BLOCKAGE DOWN', NeuronType.INPUT, input_func=blockage_down),
    Neuron('BLOCKAGE LEFT', NeuronType.INPUT, input_func=blockage_left),
    Neuron('BLOCKAGE RIGHT', NeuronType.INPUT, input_func=blockage_right),
    Neuron('BLOCKAGE UP LEFT', NeuronType.INPUT, input_func=blockage_up_left),
    Neuron('BLOCKAGE UP RIGHT', NeuronType.INPUT, input_func=blockage_up_right),
    Neuron('BLOCKAGE DOWN LEFT', NeuronType.INPUT, input_func=blockage_down_left),
    Neuron('BLOCKAGE DOWN RIGHT', NeuronType.INPUT, input_func=blockage_down_right)
]


def get_fresh_input_neurons() -> List[Neuron]:
    return deepcopy(input_neurons)
