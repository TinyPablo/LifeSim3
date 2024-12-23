import json
import os
import random
from typing import Dict

from utils import get_time_now

class SimulationSettings:
    def __init__(self):
        self.random_seed = False
        self.seed = 0
        self.initialize_seed()
        
        self.grid_width = 100
        self.grid_height = 100

        self.steps_per_generation = 300
        self.max_generations = 10000000

        self.max_entity_count = 1000
        self.brain_size = 16
        self.max_internal_neurons = 6
        self.gene_mutation_chance = 1/1000
        
        self.video_framerate = 30
        self.loging_rate = 1/15

        self.simulation_directory = f"./simulations/{self.seed} {get_time_now()}"
        self.save_settings()

    def initialize_seed(self):
        if self.random_seed:
            self.seed = random.getrandbits(32)
        random.seed(self.seed)

        print('SEED:', self.seed)

    def save_settings(self) -> None:
        os.makedirs(self.simulation_directory, exist_ok=True)
        with open(f"{self.simulation_directory}/settings.json", 'w+') as f:
            data: Dict = {
                'random_seed': self.random_seed,
                'seed': self.seed,
                'grid_width': self.grid_width,
                'grid_height': self.grid_height,
                'steps_per_generation': self.steps_per_generation,
                'max_generations': self.max_generations,
                'max_entity_count': self.max_entity_count,
                'brain_size': self.brain_size,
                'max_internal_neurons': self.max_internal_neurons,
                'gene_mutation_chance': self.gene_mutation_chance,
                'video_framerate': self.video_framerate,
                'loging_rate': self.loging_rate,
                'simulation_directory': self.simulation_directory
            }
            json.dump(data, f)
            
settings = SimulationSettings()