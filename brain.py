import time
from typing import Callable, List, TYPE_CHECKING, Optional
from connection import ConnectionEndType, ConnectionTipType
from gene import Gene
from genome import Genome
from neuron import Neuron
from neuron_type import NeuronType
from input_neurons import get_fresh_input_neurons
from output_neurons import get_fresh_output_neurons
from internal_neurons import get_fresh_internal_neurons

if TYPE_CHECKING:
    from entity import Entity

class Brain:
    def __init__(self, genome: Genome, entity: 'Entity') -> None:
        self.genome: Genome = genome
        self.entity: 'Entity' = entity

        self.input_neurons: list[Neuron] = get_fresh_input_neurons()
        self.output_neurons: list[Neuron] = get_fresh_output_neurons()
        self.internal_neurons: list[Neuron] = get_fresh_internal_neurons()

    def refresh_neurons(self) -> None:
        for neuron in self.input_neurons + self.output_neurons + self.internal_neurons:
            neuron.refresh()

    def connect_neurons(self) -> None:
        if self.genome.genes is None:
            raise Exception('Genes is None')
        genes: List[Gene] = self.genome.genes

        for gene in genes:
            input_neuron_list: Optional[List[Neuron]] = None
            output_neuron_list: Optional[List[Neuron]] = None

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
        neurons: List[Neuron] = self.input_neurons + self.output_neurons + self.internal_neurons
        neurons = Neuron.sort(neurons)
        Neuron.filter(neurons)

        final_action: Optional[Callable] = None
        final_action_chance: float = float('-inf')

        for n in neurons:
            if n.disabled:
                continue

            if n.type == NeuronType.INPUT:
                n.execute(self.entity)

            elif n.type == NeuronType.OUTPUT:
                neuron_action, action_chance = n.execute()
                if action_chance > final_action_chance and neuron_action is not None:
                    final_action = neuron_action
                    final_action_chance = action_chance
                    
            elif n.type == NeuronType.INTERNAL:
                n.execute()
                
        if final_action is not None:
            final_action(self.entity)

    def init_and_process(self) -> None:

        self.refresh_neurons()
        self.connect_neurons()
        self.process_brain()
    
    def mutate(self) -> None:
        self.genome.mutate()