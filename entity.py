import random
from typing import List, Optional, TYPE_CHECKING

from transform import Transform


if TYPE_CHECKING:
    from grid import Grid
    from genome import Genome

class Entity:
    def __init__(self, genome: 'Genome') -> None:
        from brain import Brain

        self.brain: Brain = Brain(genome, self)
        self.transform: Transform = Transform()

        self.dead: bool = False

        self.grid: Optional['Grid'] = None

    def __str__(self) -> str:
        return 'E'

    def __repr__(self) -> str:
        return self.__str__()

    def die(self) -> None:
        self.dead = True

        self.transform = Transform()
        self.grid = None

    def try_mutate(self, percent_chance: float) -> None:
        if random.uniform(0.0, 100.0) < percent_chance:
            self.mutate()

    def mutate(self) -> None:
        self.brain.mutate()

    def set_position(self, x: Optional[int], y: Optional[int], grid: 'Grid') -> None:
        if any([self.transform.position_x, self.transform.position_y, self.grid]):
            raise Exception('Enemy has already been deployed')
        
        self.transform.position_x = x
        self.transform.position_y = y
        self.grid = grid
