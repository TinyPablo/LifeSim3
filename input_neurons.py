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



def get_location_vertically(entity: Entity, grid: Grid, simulation: Simulation) -> float: 
    return 1 - (entity.transform.position_x / settings.grid_height)

def get_location_horizontally(entity: Entity, grid: Grid, simulation: Simulation) -> float: 
    return 1 - (entity.transform.position_y / settings.grid_width)

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
    # Neuron('meets condition input', NeuronType.INPUT, input_func=meets_condition_input)

]


def get_fresh_input_neurons() -> List[Neuron]:
    return deepcopy(input_neurons)