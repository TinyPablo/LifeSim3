import random
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from grid import Grid
    from genome import Genome

class Entity:
    def __init__(self, genome: 'Genome') -> None:
        from brain import Brain
        from neurons import get_neuron_set

        self.brain: Brain = Brain(genome, *get_neuron_set())
        self.dead = False
        self.x: Optional[int] = None
        self.y: Optional[int] = None
        self.grid: Optional['Grid'] = None

    def die(self) -> None:
        self.dead = True
        if self.grid:
            self.grid.remove_entity(self.x, self.y)
        self.x, self.y, self.grid = None, None, None

    def try_mutate(self, percent_chance: float) -> None:
        if random.uniform(0.0, 100.0) < percent_chance:
            self.mutate()

    def mutate(self) -> None:
        self.brain.mutate()

    def set_position(self, x: Optional[int], y: Optional[int], grid: Optional['Grid'] = None) -> None:
        self.x = x
        self.y = y
        if grid is not None:
            self.grid = grid
