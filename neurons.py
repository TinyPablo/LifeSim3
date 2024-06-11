from copy import deepcopy
import math
import random
from typing import TYPE_CHECKING, List
from direction import Direction
from entity import Entity
from grid import Grid
from neuron import Neuron
from neuron_type import NeuronType
from simulation import Simulation
from simulation_settings import settings


if TYPE_CHECKING:
    from entity import Entity

# INPUT NEURON FUNCTIONS

def get_location_vertically(entity: Entity, grid: Grid, simulation: Simulation) -> float:
    return 1 - (entity.transform.position_y / settings.grid_height)

def get_location_horizontally(entity: Entity, grid: Grid, simulation: Simulation) -> float: 
    return 1 - (entity.transform.position_x / settings.grid_width)

def get_distance_north(entity: Entity, grid: Grid, simulation: Simulation) -> float: 
    return 1 - (entity.transform.position_y / settings.grid_height)

def get_distance_east(entity: Entity, grid: Grid, simulation: Simulation) -> float: 
    return entity.transform.position_x / settings.grid_width

def get_distance_south(entity: Entity, grid: Grid, simulation: Simulation) -> float: 
    return entity.transform.position_y / settings.grid_height

def get_distance_west(entity: Entity, grid: Grid, simulation: Simulation) -> float: 
    return 1 - (entity.transform.position_x / settings.grid_width)

def get_age(entity: Entity, grid: Grid, simulation: Simulation) -> float:
    return simulation.current_step / settings.steps_per_generation

def random_float(entity: Entity, grid: Grid, simulation: Simulation):
    return random.random()

def get_blockage_forward(entity: Entity, grid: Grid, simulation: Simulation) -> float:
    blockage_forward: bool = grid.blockage_in_direction(entity, entity.transform.direction)
    return 1.0 if blockage_forward else 0.0

def get_blockage_rightleft(entity: Entity, grid: Grid, simulation: Simulation) -> float:
    right_relative: Direction = grid.get_relative_direction(entity.transform.direction, Direction.RIGHT)
    left_relative: Direction = grid.get_relative_direction(entity.transform.direction, Direction.LEFT)

    blockage_right: bool = grid.blockage_in_direction(entity, right_relative)
    blockage_left: bool = grid.blockage_in_direction(entity, left_relative)

    if blockage_right and blockage_left:
        return 1.0
    elif blockage_right or blockage_left:
        return 0.5
    return 0.0

def oscilator_input(entity: Entity, grid: Grid, simulation: Simulation):
    return 0.5 * (math.sin((2 * math.pi * simulation.current_step) / settings.steps_per_generation) + 1)


def meets_condition_input(entity: Entity, grid: Grid, simulation: Simulation):
    if simulation.selection_condition(entity):
        return 1.0
    return 0.0
    
def get_entites_alive(entity: Entity, grid: Grid, simulation: Simulation):
    return len(simulation.entities) / settings.max_entity_count


# OUTPUT NEURON FUNCTIONS

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

def kys(entity: Entity, grid: Grid, simulation: Simulation):
    entity.die()

def kill(entity: Entity, grid: Grid, simulation: Simulation):
    x: int = entity.transform.next_x
    y: int = entity.transform.next_y
    if grid.in_boundaries(x, y):
        if type(grid.grid[x][y]) == Entity:
            grid.grid[x][y].object.die()





input_neurons: List[Neuron] = [
    Neuron('location vertically', NeuronType.INPUT, input_func=get_location_vertically),
    Neuron('location horizontally', NeuronType.INPUT, input_func=get_location_horizontally),
    Neuron('distance to north border', NeuronType.INPUT, input_func=get_distance_north),
    Neuron('distance to east border', NeuronType.INPUT, input_func=get_distance_east),
    Neuron('distance to south border', NeuronType.INPUT, input_func=get_distance_south),
    Neuron('distance to west border', NeuronType.INPUT, input_func=get_distance_west),
    Neuron('age', NeuronType.INPUT, input_func=get_age),
    Neuron('random float', NeuronType.INPUT, input_func=random_float),
    Neuron('blockage forward', NeuronType.INPUT, input_func=get_blockage_forward),
    Neuron('blockage right-left', NeuronType.INPUT, input_func=get_blockage_rightleft),
    Neuron('oscilator input', NeuronType.INPUT, input_func=oscilator_input),
    # Neuron('entities alive', NeuronType.INPUT, input_func=get_entites_alive),
    # Neuron('meets condition input', NeuronType.INPUT, input_func=meets_condition_input)

]

output_neurons: List[Neuron] = [
    Neuron('move vertically', NeuronType.OUTPUT, output_func_a=move_north, output_func_b=move_south),
    Neuron('move horizontally', NeuronType.OUTPUT, output_func_a=move_east, output_func_b=move_west),
    Neuron('move forward', NeuronType.OUTPUT, output_func_a=move_forward),
    Neuron('reverse', NeuronType.OUTPUT, output_func_a=reverse),
    Neuron('move right-left', NeuronType.OUTPUT, output_func_a=move_right, output_func_b=move_left),
    Neuron('move random', NeuronType.OUTPUT, output_func_a=move_random),
    Neuron('stay still', NeuronType.OUTPUT, output_func_a=stay_still),
    # Neuron('kys', NeuronType.OUTPUT, output_func_a=kys),
    # Neuron('kill', NeuronType.OUTPUT, output_func_a=kill),
]


internal_neurons: List[Neuron] = [Neuron(f'I{i+1}', NeuronType.INTERNAL) for i in range(settings.max_internal_neurons)]




neurons: List[Neuron] = [*input_neurons, *output_neurons, *internal_neurons]

def get_fresh_neurons() -> List[Neuron]:
    return deepcopy(neurons)
