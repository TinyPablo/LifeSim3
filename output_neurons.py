from copy import deepcopy
from typing import List
from direction import Direction
from entity import Entity
from grid import Grid
from neuron import Neuron
from neuron_type import NeuronType
from simulation import Simulation


def move_north(entity: Entity, grid: Grid, simulation: Simulation):
    grid.move(entity, Direction.UP)
    
def move_east(entity: Entity, grid: Grid, simulation: Simulation):
    grid.move(entity, Direction.RIGHT)

def move_south(entity: Entity, grid: Grid, simulation: Simulation):
    grid.move(entity, Direction.DOWN)

def move_west(entity: Entity, grid: Grid, simulation: Simulation):
    grid.move(entity, Direction.LEFT)

def move_forward(entity: Entity, grid: Grid, simulation: Simulation):
    grid.move_relative(entity, Direction.UP)

def reverse(entity: Entity, grid: Grid, simulation: Simulation):
    grid.move_relative(entity, Direction.DOWN)

def move_right(entity: Entity, grid: Grid, simulation: Simulation):
    grid.move_relative(entity, Direction.RIGHT)

def move_left(entity: Entity, grid: Grid, simulation: Simulation):
    grid.move_relative(entity, Direction.LEFT)

def move_random(entity: Entity, grid: Grid, simulation: Simulation):
    grid.move(entity, Direction.random())

def stay_still(entity: Entity, grid: Grid, simulation: Simulation):
    pass

def kill(entity: Entity, grid: Grid, simulation: Simulation):
    x: int = entity.transform.next_x
    y: int = entity.transform.next_y
    if grid.in_boundaries(x, y):
        if grid.grid[x][y].is_entity:
            grid.grid[x][y].object.die()


output_neurons: List[Neuron] = [
    Neuron('move vertically', NeuronType.OUTPUT, output_func_a=move_north, output_func_b=move_south),
    Neuron('move horizontally', NeuronType.OUTPUT, output_func_a=move_east, output_func_b=move_west),
    Neuron('move forward', NeuronType.OUTPUT, output_func_a=move_forward),
    Neuron('reverse', NeuronType.OUTPUT, output_func_a=reverse),
    Neuron('move right-left', NeuronType.OUTPUT, output_func_a=move_right, output_func_b=move_left),
    Neuron('move random', NeuronType.OUTPUT, output_func_a=move_random),
    Neuron('stay still', NeuronType.OUTPUT, output_func_a=stay_still),
    # Neuron('kill', NeuronType.OUTPUT, output_func_a=kill),
]

def get_fresh_output_neurons() -> List[Neuron]:
    return deepcopy(output_neurons)