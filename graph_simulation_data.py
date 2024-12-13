import sys
import json
from typing import Any, Dict, List

if len(sys.argv) < 1:
    raise Exception('Incorrect path!')


with open(f'{sys.argv[1]}/settings.json', 'r') as f:
    simulation_settings: List[Dict] = json.load(f)

with open(f'{sys.argv[1]}/simulation_data.json', 'r') as f:
    simulation_data: List[Dict] = json.load(f)
simulation_data = [simulation_data[0]]

max_entity_count: int = simulation_settings['max_entity_count']

for i, gen in enumerate(simulation_data):
    print(f'============== GENERATION {i} ==============')
    for neuron_name, occurence_count in sorted(gen['genome_diversity'].items(), key=lambda x: x[1], reverse=True):
        if occurence_count:
            print(neuron_name, occurence_count / max_entity_count * 100)
    
