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

    def on_generation_end(self) -> None:
        self.do_natural_selection()
        self.reproduce()
        self.perform_mutations()
        self.place_new_generation_entities()

    def generation_loop(self) -> None:
        self.current_step = 1

        while settings.steps_per_generation >= self.current_step and not self.simulation_ended:
            print(f'gen: {self.current_generation} | step: {self.current_step}')
            for entity in self.entities:
                entity.brain.init_and_process()

            self.grid.render(self.current_generation, self.current_step)
            self.current_step += 1

        self.on_generation_end()

    def simulation_loop(self) -> None:
        self.current_generation = 1

        for entity in self.entities:
            self.grid.deploy_entity_randomly(entity)

        while settings.max_generation_count >= self.current_generation and not self.simulation_ended:
            self.generation_loop()
            self.current_generation += 1

        print(f'simulation ended | SEED: {settings.seed}')


    def populate(self) -> None:
        self.entities = [Entity(Genome(settings.brain_size)) for _ in range(settings.max_entity_count)]

    def start(self) -> None:
        self.populate()
        self.simulation_loop()

    def do_natural_selection(self) -> None:
        for entity in self.entities:
            
            entity_entered_safe_zone = \
                entity.transform.position_x > (settings.grid_width - (settings.grid_width // 2)) and \
                entity.transform.position_y < (settings.grid_height - (settings.grid_height // 2))
            if not entity_entered_safe_zone:
                entity.die()

    def reproduce(self) -> None:
        parents: List[Entity] = [e for e in self.entities if not e.dead]
        print(len(parents))
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

    



