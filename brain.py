from connection import ConnectionEndType, ConnectionTipType
from gene import Gene
from genome import Genome
import random

from neuron import Neuron

random.seed(2)

class Brain:
    def __init__(self, genome: Genome, sensory_neurons: list[Neuron], action_neurons: list[Neuron], internal_neurons: list[Neuron]) -> None:
        self.genome: Genome = genome
        self.input_neurons: list[Neuron] = sensory_neurons
        self.output_neurons: list[Neuron] = action_neurons
        self.internal_neurons: list[Neuron] = internal_neurons

    def create_brain(self) -> None:
        genes = self.genome.genes

        for gene in genes:
            print(gene)



