from copy import deepcopy
from typing import List
from direction import Direction
from entity import Entity
from neuron import Neuron
from neuron_type import NeuronType


output_neurons: List[Neuron] = []


def move_forward(entity: 'Entity'):
    grid = entity.grid
    if grid is None:
        raise Exception('Grid is None')
    grid.move_relative(entity, Direction.UP)
    
def move_backwards(entity: 'Entity'):
    grid = entity.grid
    if grid is None:
        raise Exception('Grid is None')
    grid.move_relative(entity, Direction.DOWN)
    
output_neurons.append(Neuron('MUD', NeuronType.OUTPUT, output_func_a=move_forward, output_func_b=move_backwards))

def move_right(entity: 'Entity'):
    grid = entity.grid
    if grid is None:
        raise Exception('Grid is None')
    grid.move_relative(entity, Direction.RIGHT)
    
def move_left(entity: 'Entity'):
    grid = entity.grid
    if grid is None:
        raise Exception('Grid is None')
    grid.move_relative(entity, Direction.LEFT)
    
output_neurons.append(Neuron('MRL', NeuronType.OUTPUT, output_func_a=move_right, output_func_b=move_left))

def move_north(entity: 'Entity'):
    grid = entity.grid
    if grid is None:
        raise Exception('Grid is None')
    grid.move(entity, Direction.UP)
    
def move_south(entity: 'Entity'):
    grid = entity.grid
    if grid is None:
        raise Exception('Grid is None')
    grid.move(entity, Direction.DOWN)
    
output_neurons.append(Neuron('MNS', NeuronType.OUTPUT, output_func_a=move_north, output_func_b=move_south))

def move_east(entity: 'Entity'):
    grid = entity.grid
    if grid is None:
        raise Exception('Grid is None')
    grid.move(entity, Direction.RIGHT)
    
def move_west(entity: 'Entity'):
    grid = entity.grid
    if grid is None:
        raise Exception('Grid is None')
    grid.move(entity, Direction.LEFT)
    
output_neurons.append(Neuron('MEW', NeuronType.OUTPUT, output_func_a=move_east, output_func_b=move_west))


def move_random(entity: 'Entity'):
    grid = entity.grid
    if grid is None:
        raise Exception('Grid is None')
    grid.move_relative(entity, Direction.random())
output_neurons.append(Neuron('MRD', NeuronType.OUTPUT, output_func_a=move_random))

def stay_still(entity: 'Entity'):
    pass
output_neurons.append(Neuron('STS', NeuronType.OUTPUT, output_func_a=stay_still))

def get_fresh_output_neurons() -> List[Neuron]:
    return deepcopy(output_neurons)