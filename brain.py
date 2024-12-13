import random
from typing import Callable, List
from connection import ConnectionEndType, ConnectionTipType
from gene import Gene
from genome import Genome
from neuron import Neuron
from neuron_type import NeuronType
from neurons import get_fresh_neurons
from entity import Entity

class Brain:
    def __init__(self, genome: Genome, entity: 'Entity') -> None:
        self.genome: Genome = genome
        self.entity: 'Entity' = entity

        self.neurons: list[Neuron] = get_fresh_neurons()


    def __str__(self) -> str:
        return '\n'.join([f'{n}' for n in self.neurons])

    @property
    def input_neurons(self) -> List[Neuron]:
        return [n for n in self.neurons if n.type == NeuronType.INPUT]
    
    @property
    def output_neurons(self) -> List[Neuron]:
        return [n for n in self.neurons if n.type == NeuronType.OUTPUT]
    
    @property
    def internal_neurons(self) -> List[Neuron]:
        return [n for n in self.neurons if n.type == NeuronType.INTERNAL]

    # def refresh_neurons(self) -> None:
    #     for neuron in self.neurons:
    #         neuron.refresh()

    def connect_neurons(self) -> None:
        genes: List[Gene] = self.genome.genes

        for gene in genes:
            input_neuron_list: List[Neuron] = list()
            output_neuron_list: List[Neuron] = list()

            if gene.conn_tip_neuron_type == ConnectionTipType.INPUT or not self.internal_neurons:
                input_neuron_list = self.input_neurons
            elif gene.conn_tip_neuron_type == ConnectionTipType.INTERNAL:
                input_neuron_list = self.internal_neurons

            if gene.conn_end_neuron_type == ConnectionEndType.OUTPUT or not self.internal_neurons:
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

    def init(self) -> None:
        self.connect_neurons()
        Neuron.sort(self.neurons)
        Neuron.filter(self.neurons)

    def process(self) -> None:
        final_action: Callable = lambda: None
        final_action_chance: float = float('-inf')

        for n in self.neurons:
            if n.disabled:
                continue

            if n.type == NeuronType.INPUT:
                n.execute_as_input_neuron(self.entity)

            elif n.type == NeuronType.OUTPUT:
                neuron_action, action_chance = n.execute_as_output_neuron()
                if action_chance > final_action_chance and neuron_action is not None:
                    final_action = neuron_action
                    final_action_chance = action_chance
                
                    if final_action is not None:
                        if random.uniform(0.0, 1.0) < action_chance:
                            final_action(self.entity, self.entity.grid, self.entity.simulation)
                    
            elif n.type == NeuronType.INTERNAL:
                n.execute_as_internal_neuron()