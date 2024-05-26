from typing import Callable, List
from connection import ConnectionEndType, ConnectionTipType
from gene import Gene
from genome import Genome
import random

from neuron import Neuron
from neuron_type import NeuronType


class Brain:
    def __init__(self, genome: Genome, input_neurons: list[Neuron], output_neurons: list[Neuron], internal_neurons: list[Neuron]) -> None:
        self.genome: Genome = genome
        self.input_neurons: list[Neuron] = input_neurons
        self.output_neurons: list[Neuron] = output_neurons
        self.internal_neurons: list[Neuron] = internal_neurons

    def connect_neurons(self) -> None:
        genes: List[Gene] = self.genome.genes

        for gene in genes:
            input_neuron_list: List[Gene] = None
            output_neuron_list: List[Gene] = None

            if gene.conn_tip_neuron_type == ConnectionTipType.INPUT:
                input_neuron_list = self.input_neurons
            elif gene.conn_tip_neuron_type == ConnectionTipType.INTERNAL:
                input_neuron_list = self.internal_neurons

            if gene.conn_end_neuron_type == ConnectionEndType.OUTPUT:
                output_neuron_list = self.output_neurons
            elif gene.conn_end_neuron_type == ConnectionEndType.INTERNAL:
                output_neuron_list = self.internal_neurons


            input_neuron: Neuron = input_neuron_list[gene.conn_tip_neuron_id % len(input_neuron_list)]
            output_neuron: Neuron = output_neuron_list[gene.conn_end_neuron_id % len(output_neuron_list)]

            try:
                Neuron.connect_neurons(input_neuron, output_neuron, gene.conn_weight)
                # print(input_neuron.type.name, input_neuron.name, output_neuron.type.name, output_neuron.name, gene.conn_weight)
            except ValueError as e:
                # print(f'Couldn\'t connect {input_neuron.name} to {output_neuron.name}')
                # print(f'Reason: {e}')
                pass

    def process_brain(self) -> None:

        neurons: Neuron = self.input_neurons + self.output_neurons + self.internal_neurons
        neurons: Neuron = Neuron.sort(neurons)
        neurons: Neuron = Neuron.filter(neurons)

        final_action: Callable = None
        final_action_chance: float = float('-inf')

        for n in neurons:
            if n.type == NeuronType.OUTPUT:
                neuron_action, action_chance = n.execute()
                if action_chance > final_action_chance and neuron_action is not None:
                    final_action = neuron_action
                    final_action_chance = action_chance
            else:
                n.execute()
                
        if final_action is not None:
            final_action()
    
    def mutate(self) -> None:
        self.genome.mutate()




