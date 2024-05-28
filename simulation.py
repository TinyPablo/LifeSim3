import random
from typing import List
from genome import Genome
from simulation_settings import settings
from grid import Grid
from entity import Entity
from simulation_settings import settings

class Simulation:
    def __init__(self) -> None:
        self.grid: 'Grid' = Grid(settings.grid_width, settings.grid_height, self)
        self.current_generation: int = 0
        self.current_step: int = 0
        self.entities: List[Entity] = []
        self.simulation_ended: bool = False

        self.survival_rate: int = None

    def on_generation_end(self) -> None:
        self.do_natural_selection()
        self.reproduce()
        self.perform_mutations()
        self.place_new_generation_entities()

    def print_info(self) -> None:
        gen: int = self.current_generation
        step: int = self.current_step
        sr: float = round(self.survival_rate if self.survival_rate is not None else 0, 2)
        safe: float = len([e for e in self.entities if self.selection_condition(e)]) / len(self.entities) * 100
        safe = round(safe if safe is not None else 0, 2)
        
        print(f'\rGEN: {gen} | STEP: {step} | SAFE: {safe}% | SR: {sr}%' \
                  , end='', flush=True)

    def generation_loop(self) -> None:
        self.current_step = 1
        while settings.steps_per_generation >= self.current_step and not self.simulation_ended:
            self.print_info()
            for entity in self.entities:
                entity.brain.init_and_process()

            self.grid.render(self.current_generation, self.current_step)
            self.current_step += 1

        self.on_generation_end()

    def simulation_loop(self) -> None:
        self.current_generation = 1

        while settings.max_generation_count >= self.current_generation and not self.simulation_ended:
            self.generation_loop()
            self.current_generation += 1

        print(f'simulation ended | SEED: {settings.seed}')


    def populate(self) -> None:
        self.entities = [Entity(Genome(settings.brain_size)) for _ in range(settings.max_entity_count)]

        for entity in self.entities:
            self.grid.deploy_entity_randomly(entity)

    def start(self) -> None:
        self.populate()
        self.simulation_loop()

    # def selection_condition(self, entity: Entity) -> bool:
    #     x: int = entity.transform.position_x
    #     y: int = entity.transform.position_y
    #     return \
    #         (settings.grid_width * .4) < x < (settings.grid_width * .6) and \
    #         (settings.grid_height * .4) < y < (settings.grid_height * .6)
    
    def selection_condition(self, entity: Entity) -> bool:
        x: int = entity.transform.position_x
        y: int = entity.transform.position_y
        return \
            (settings.grid_width * .5) < x

    def do_natural_selection(self) -> None:
        for entity in self.entities:
            if not self.selection_condition(entity):
                entity.die()

    def reproduce(self) -> None:
        parents: List[Entity] = [e for e in self.entities if not e.dead]

        self.survival_rate = len(parents) / settings.max_entity_count * 100

        new_entities: List[Entity] = []

        if len(parents) < 2:
            print("population went extinct")
            self.simulation_ended = True
            return
        
        while len(new_entities) < settings.max_entity_count:
            parent_a, parent_b = random.sample(parents, 2)
            child_genome: Genome = Genome.crossover(parent_a.brain.genome, parent_b.brain.genome)
            entity: Entity = Entity(child_genome)
            new_entities.append(entity)

        self.entities = new_entities

        for parent in parents:
            parent.die()

    def place_new_generation_entities(self) -> None:
        for entity in self.entities:
            self.grid.deploy_entity_randomly(entity)

    def perform_mutations(self) -> None:
        for entity in self.entities:
            entity.try_mutate(settings.mutation_chance)

    



