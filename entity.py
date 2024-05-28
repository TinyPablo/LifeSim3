import random
from typing import List, Optional, TYPE_CHECKING
from simulation_settings import settings
from transform import Transform
from genome import Genome


if TYPE_CHECKING:
    from grid import Grid

class Entity:
    def __init__(self, genome: 'Genome') -> None:
        from brain import Brain

        self.brain: 'Brain' = Brain(genome, self)

        self.transform: Transform = Transform()

        self.dead: bool = False

        self.grid: Optional['Grid'] = None

    def __str__(self) -> str:
        return 'E'

    def __repr__(self) -> str:
        return self.__str__()
    
    @property
    def age(self) -> float:
        if self.grid is None:
            raise Exception('None error')
        return self.grid.simulation.current_step / settings.steps_per_generation
    
    @property
    def distance_to_north(self) -> float:
        return self.transform.position_y / settings.grid_height
    
    @property
    def distance_to_south(self) -> float:
        return 1 - (self.transform.position_y / settings.grid_height)
    
    @property
    def distance_to_east(self) -> float:
        return self.transform.position_x / settings.grid_width
    
    @property
    def distance_to_west(self) -> float:
        return 1 - (self.transform.position_x / settings.grid_width)

    def die(self) -> None:
        if self.grid is None:
            raise Exception('None exception')
        self.grid.remove_entity(self.transform.position_x, self.transform.position_y)
        self.dead = True

        self.transform = Transform()
        self.grid = None

    def try_mutate(self, percent_chance: float) -> bool:
        if random.uniform(0.0, 100.0) < percent_chance:
            self.mutate()
            return True
        return False

    def mutate(self) -> None:
        self.brain.mutate()

    def set_position(self, x: int, y: int) -> None:        
        self.transform.position_x = x
        self.transform.position_y = y
