import json
import random
from typing import Dict, List
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
        self.generation_data: Dict[str, int | str] = {}

    def update_survival_rate(self, alive_entities_count: int) -> None:
        self.survival_rate = alive_entities_count / settings.max_entity_count * 100

    def log_info(self) -> None:
        generation: int = self.current_generation
        step: int = self.current_step
        safe_entities: float = len([e for e in self.entities if self.selection_condition(e.transform.position_x, e.transform.position_y)]) / settings.max_entity_count * 100
        survival_rate: float = self.survival_rate

        info: str = (
            f'GENERATION: {generation}\n'
            f'STEP: {step}\n'
            f'SAFE ENTITIES: {safe_entities:.2f}%\n'
            f'PREVIOUS SURVIVAL RATE: {survival_rate:.2f}%\n\n'
        )

        print(info, end='', flush=True)

    def update_genome_diversity(self) -> None:
        self.generation_data['genome_diversity'] = {}
        for entity in self.entities:
            for neuron in entity.brain.neurons:
                if neuron.disabled:
                    self.generation_data['genome_diversity'][neuron.name] = 0
                    continue

                if neuron.name not in self.generation_data['genome_diversity']:
                    self.generation_data['genome_diversity'][neuron.name] = 1
                    continue
                
                self.generation_data['genome_diversity'][neuron.name] += 1


    def generation_loop(self) -> None:
        
        self.current_step = 1

        for entity in self.entities:
            entity.brain.init()

        self.update_genome_diversity()
        pictures: List[List[List[tuple[int, int, int]]]] = []
        while settings.steps_per_generation >= self.current_step and not self.simulation_ended:
            if (self.current_step % (1 // settings.loging_rate) == 0) or \
            (self.current_step == 1) or (self.current_step == settings.steps_per_generation):
                self.log_info()
            
            for entity in self.entities:
                entity.brain.process()

            
            

            pictures.append(self.grid.get_picture())
            self.current_step += 1
    
        self.on_generation_end(pictures)

    def on_generation_end(self, pictures: List[List[tuple[int, int, int]]]) -> None:
        self.do_natural_selection()     
        self.reproduce()
        Grid.save_video(pictures, self.current_generation)
        self.update_simulation_data()
        self.place_new_generation_entities()


    @staticmethod
    def load_simulation_data() -> List:
        simulation_data_path = f"{settings.simulation_directory}/simulation_data.json"
        try:
            with open(simulation_data_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            with open(simulation_data_path, 'w+') as f:
                return []
        except json.JSONDecodeError:
            with open(simulation_data_path, 'w') as f:
                return []

    @staticmethod
    def write_simulation_data(generation_data: Dict) -> None:
        simulation_data_path = f"{settings.simulation_directory}/simulation_data.json"
        all_data: List[Dict] = Simulation.load_simulation_data()

        with open(simulation_data_path, 'w') as f:
            all_data.append(generation_data)
            json.dump(all_data, f)


    def update_simulation_data(self):
        self.generation_data["generation"] = self.current_generation
        self.generation_data["survival_rate"] = self.survival_rate

        Simulation.write_simulation_data(self.generation_data)



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

    
    def selection_condition(self, x: int, y: int) -> bool:
        w: int = settings.grid_width
        h: int = settings.grid_height

        return  w/2 > x and h/2 > y

    def do_natural_selection(self) -> None:
        alive_entities = []
        for entity in self.entities:
            if self.selection_condition(entity.transform.position_x, entity.transform.position_y):
                alive_entities.append(entity)
            else:
                entity.die()
        self.entities = alive_entities



    def reproduce(self) -> None:
        parents: List[Entity] = self.entities
        new_entities: List[Entity] = []
            
        self.update_survival_rate(len(parents))

        if len(parents) < 2:
            print("population went extinct")
            self.simulation_ended = True
            return
        self.generation_data['brains'] = str(parents[0].brain)
        
        while len(new_entities) < settings.max_entity_count:
            parent_a, parent_b = random.sample(parents, 2)
            child_genome: Genome = Genome.crossover(parent_a.brain.genome, parent_b.brain.genome)
            entity: Entity = Entity(child_genome, self, self.grid)
            new_entities.append(entity)

        for e in self.entities:
            e.die()

        self.entities = new_entities


    def place_new_generation_entities(self) -> None:
        for entity in self.entities:
            self.grid.deploy_entity_randomly(entity)