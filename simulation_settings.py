import os
import random

class SimulationSettings:
    def __init__(self):
        self.simulation_directory = './simulations'

        self.grid_width = 256
        self.grid_height = 256

        self.gene_mutation_chance = .01

        self.random_seed = True
        self.seed = 2673244385

        self.steps_per_generation = 300

        self.max_entity_count = 6000

        self.brain_size = 24
        self.max_internal_neurons = 6

        self.initialize_seed()
        self.save_settings()

    def initialize_seed(self):
        if self.random_seed:
            self.seed = random.getrandbits(32)
        random.seed(self.seed)

        print('SEED:', self.seed)

    def save_settings(self):
        path: str = f'./{self.simulation_directory}/{self.seed}/settings/'
        os.makedirs(path, exist_ok=True)
        file_path = os.path.join(path, 'settings.txt')
        with open(file_path, 'w+') as file:
            file.write(f'{self.simulation_directory = }\n')
            file.write(f'{self.max_internal_neurons = }\n')
            file.write(f'{self.grid_width = }\n')
            file.write(f'{self.grid_height = }\n')
            file.write(f'{self.gene_mutation_chance = }\n')
            file.write(f'{self.random_seed = }\n')
            file.write(f'{self.seed = }\n')
            file.write(f'{self.steps_per_generation = }\n')
            file.write(f'{self.max_entity_count = }\n')
            file.write(f'{self.brain_size = }\n')

settings = SimulationSettings()
