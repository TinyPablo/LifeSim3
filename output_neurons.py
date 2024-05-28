from copy import deepcopy
from typing import List
from direction import Direction
from entity import Entity
from neuron import Neuron
from neuron_type import NeuronType


def move_north(entity: 'Entity'):
    entity.grid.move(entity, Direction.UP)

def move_north_east(entity: 'Entity'):
    entity.grid.move(entity, Direction.UP_RIGHT)

def move_east(entity: 'Entity'):
    entity.grid.move(entity, Direction.RIGHT)

def move_south_east(entity: 'Entity'):
    entity.grid.move(entity, Direction.DOWN_RIGHT)

def move_south(entity: 'Entity'):
    entity.grid.move(entity, Direction.DOWN)

def move_south_west(entity: 'Entity'):
    entity.grid.move(entity, Direction.DOWN_LEFT)

def move_west(entity: 'Entity'):
    entity.grid.move(entity, Direction.LEFT)

def move_north_west(entity: 'Entity'):
    entity.grid.move(entity, Direction.UP_LEFT)

def move_forward(entity: 'Entity'):
    entity.grid.move(entity, entity.transform.direction)

def move_random(entity: 'Entity'):
    entity.grid.move(entity, Direction.random())

def stay_still(entity: 'Entity'):
    pass

output_neurons: List[Neuron] = [
    Neuron('MOVE NORTH', NeuronType.OUTPUT, output_func_a=move_north),
    Neuron('MOVE NORTH-EAST', NeuronType.OUTPUT, output_func_a=move_north_east),
    Neuron('MOVE EAST', NeuronType.OUTPUT, output_func_a=move_east),
    Neuron('MOVE SOUTH-EAST', NeuronType.OUTPUT, output_func_a=move_south_east),
    Neuron('MOVE SOUTH', NeuronType.OUTPUT, output_func_a=move_south),
    Neuron('MOVE SOUTH-WEST', NeuronType.OUTPUT, output_func_a=move_south_west),
    Neuron('MOVE WEST', NeuronType.OUTPUT, output_func_a=move_west),
    Neuron('MOVE NORTH-WEST', NeuronType.OUTPUT, output_func_a=move_north_west),
    Neuron('MOVE FORWARD', NeuronType.OUTPUT, output_func_a=move_forward),
    Neuron('MOVE RANDOM', NeuronType.OUTPUT, output_func_a=move_random),
    Neuron('STAY STILL', NeuronType.OUTPUT, output_func_a=stay_still)
]


def get_fresh_output_neurons() -> List[Neuron]:
    return deepcopy(output_neurons)