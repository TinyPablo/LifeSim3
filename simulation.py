import math
import os
import random
import threading
import time
from typing import List, Optional, Union
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

        self.survival_rate: float = 0.0
        self.mutations: int = 0
        self.render: bool = True

    def on_generation_end(self) -> None:
        self.do_natural_selection()
        self.reproduce()
        self.place_new_generation_entities()
        
        self.rename_generation_dir()

    def rename_generation_dir(self) -> None:
        if self.render:
            os.rename(f'{settings.simulation_directory}/{settings.seed}/{self.current_generation}', \
            f'{settings.simulation_directory}/{settings.seed}/{self.current_generation}-{self.survival_rate}')

    def print_info(self) -> None:
        gen: int = self.current_generation
        step: int = self.current_step
        sr: Union[int, float] = round(self.survival_rate if self.survival_rate is not None else 0, 2)
        safe: float = len([e for e in self.entities if self.selection_condition(e)]) / len(self.entities) * 100
        safe = round(safe if safe is not None else 0, 2)
        mutations: int = self.mutations
        
        print(f'\rGEN: {gen}|STEP: {step}|SAFE: {safe}%|SR: {sr}%|MUT: {mutations}|REND: {self.render}' \
                  , end='', flush=True)

    def generation_loop(self) -> None:
        self.current_step = 1
        
        for entity in self.entities:
            entity.brain.init()

        while settings.steps_per_generation >= self.current_step and not self.simulation_ended:

            self.print_info()
            
            for entity in self.entities:
                entity.brain.process()

            if self.render:
                self.grid.render(self.current_generation, self.current_step)
                pass
            self.current_step += 1
    
        self.on_generation_end()

    def simulation_loop(self) -> None:
        self.current_generation = 1

        while settings.max_generation_count >= self.current_generation and not self.simulation_ended:
            self.generation_loop()
            self.current_generation += 1

        print(f'simulation ended | SEED: {settings.seed}')


    def populate(self) -> None:
        self.entities = [Entity(Genome(settings.brain_size), self, self.grid) for _ in range(settings.max_entity_count)]
        for entity in self.entities:
            self.grid.deploy_entity_randomly(entity)

    def prompt_manager(self) -> None:
        def prompt_thread() -> None:
            while True:
                input()
                self.render = not self.render

        threading.Thread(target=prompt_thread).start()
        

        

    def start(self) -> None:
        self.prompt_manager()
        self.populate()

        self.simulation_loop()

    
    def selection_condition(self, entity: Entity) -> bool:
        x: int = entity.transform.position_x
        y: int = entity.transform.position_y


        # return ((settings.grid_width * 1/3) > x or x > (settings.grid_width * 2/3)) and \
        # ((settings.grid_height * 1/3) > y or y > (settings.grid_height * 2/3))

        return settings.grid_height // 3 > y 

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
        
        while len(new_entities) <= settings.max_entity_count:
            parent_a, parent_b = random.sample(parents, 2)
            child_genome: Genome = Genome.crossover(parent_a.brain.genome, parent_b.brain.genome)
            entity: Entity = Entity(child_genome, self, self.grid)

            mutated = entity.try_mutate(settings.mutation_chance)
            
            if mutated:
                self.mutations += 1

            new_entities.append(entity)

        self.entities = new_entities

        for parent in parents:
            parent.die()

    def place_new_generation_entities(self) -> None:
        for entity in self.entities:
            self.grid.deploy_entity_randomly(entity)

    



