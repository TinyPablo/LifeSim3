import random
from brain import Brain


class Entity:
    def __init__(self, brain: Brain) -> None:
        self.brain: Brain = brain

    def try_mutate(self, percent_chance: float) -> None:
        if random.uniform(0.0, 100.0) < percent_chance:
            self.mutate()

    def mutate(self) -> None:
        self.brain.mutate()