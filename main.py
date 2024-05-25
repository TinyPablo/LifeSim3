
import random
from entity import Entity
from brain import Brain
from genome import Genome
from input_neurons import input_neurons
from output_neurons import output_neurons
from internal_neurons import internal_neurons
from copy import deepcopy
random.seed(20222)
genome = Genome(10)
brain = Brain(genome, deepcopy(input_neurons), deepcopy(output_neurons), deepcopy(internal_neurons))
entity = Entity(brain)
print(brain.genome)
entity.try_mutate(100)
print()
print(brain.genome)

# brain.connect_neurons()
# brain.process_brain()