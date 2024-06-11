import random
from typing import List
from genome import Genome
from simulation_settings import settings
from grid import Grid
from entity import Entity
from simulation_settings import settings
from functools import wraps



class Simulation:
    def __init__(self) -> None:
        self.grid: 'Grid' = Grid(settings.grid_width, settings.grid_height, self)
        self.current_generation: int = 0
        self.current_step: int = 0
        self.entities: List[Entity] = []
        self.simulation_ended: bool = False

        self.survival_rate: float = 0.0

    def print_info(self) -> None:
        generation: int = self.current_generation
        step: int = self.current_step
        safe_entities: float = len([e for e in self.entities if self.selection_condition(e)]) / len(self.entities) * 100
        survival_rate: float = self.survival_rate

        info: str = (
            f'GENERATION: {generation}\n'
            f'STEP: {step}\n'
            f'SAFE ENTITIES: {safe_entities:.2f}%\n'
            f'SURVIVAL RATE: {survival_rate:.2f}%\n\n'
        )

        print(info, end='', flush=True)

    def generation_loop(self) -> None:
        
        self.current_step = 1

        for entity in self.entities:
            entity.brain.init()

        pictures: List[List[List[tuple[int, int, int]]]] = []

        
        
        while settings.steps_per_generation >= self.current_step and not self.simulation_ended:
            self.print_info()
            
            for entity in self.entities:
                entity.brain.process()

            pictures.append(self.grid.get_picture())
            self.current_step += 1
    
        self.on_generation_end(pictures)

    def on_generation_end(self, pictures: List[List[tuple[int, int, int]]]) -> None:
        self.do_natural_selection()     
        self.reproduce()
        Grid.save_video(pictures, self.current_generation, self.survival_rate)
        self.place_new_generation_entities()

    def simulation_loop(self) -> None:
        self.current_generation = 1

        while not self.simulation_ended and self.current_generation < (settings.max_generations + 1):
            self.generation_loop()
            self.current_generation += 1

        print(f'simulation ended | SEED: {settings.seed}')

    def populate(self) -> None:
        self.entities = [Entity(Genome(settings.brain_size), self, self.grid) for _ in range(settings.max_entity_count)]
        for entity in self.entities:
            self.grid.deploy_entity_randomly(entity)
        

    def start(self) -> None:
        self.populate()
        self.simulation_loop()

    
    def selection_condition(self, entity: Entity) -> bool:
        x: int = entity.transform.position_x
        y: int = entity.transform.position_y
        w: int = settings.grid_width
        h: int = settings.grid_height

        return w/2 > x and h/2 > y

    def do_natural_selection(self) -> None:
        for entity in self.entities:
            if not self.selection_condition(entity):
                entity.die()


    def reproduce(self) -> None:
        parents: List[Entity] = [e for e in self.entities if not e.dead]
        new_entities: List[Entity] = []

        self.survival_rate = len(parents) / len(self.entities) * 100

        if len(parents) < 2:
            print("population went extinct")
            self.simulation_ended = True
            return
        
        while len(new_entities) <= settings.max_entity_count:
            parent_a, parent_b = random.sample(parents, 2)
            child_genome: Genome = Genome.crossover(parent_a.brain.genome, parent_b.brain.genome)
            entity: Entity = Entity(child_genome, self, self.grid)
            new_entities.append(entity)

        self.entities = new_entities

        for parent in parents:
            parent.die()

    def place_new_generation_entities(self) -> None:
        for entity in self.entities:
            self.grid.deploy_entity_randomly(entity)