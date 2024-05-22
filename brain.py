from connection import ConnectionEndType, ConnectionTipType
from gene import Gene
from genome import Genome
import random

from neuron import ActionNeuron, InternalNeuron, SensoryNeuron
random.seed(2)

class Brain:
    def __init__(self, genome: Genome, sensory_neurons: list[SensoryNeuron], action_neurons: list[ActionNeuron], internal_neurons: list[InternalNeuron]) -> None:
        self.genome: Genome = genome
        self.sensory_neurons: list[SensoryNeuron] = sensory_neurons
        self.action_neurons: list[ActionNeuron] = action_neurons
        self.internal_neurons: list[InternalNeuron] = internal_neurons

    @staticmethod
    def filter_genes(genes: list[Gene]) -> list[Gene]:
        filtered_genes: list[Gene] = []
        for gene in genes:
            print(gene, gene.self_connected)
            if gene.self_connected:
                continue
            
            if any(gene == f_gene for f_gene in filtered_genes):
                continue
            
            if any(gene.are_reverse_connected(gene, f_gene) for f_gene in filtered_genes):
                continue
            
            filtered_genes.append(gene)


        return filtered_genes


    def create_brain(self) -> None:
        genes = Brain.filter_genes(self.genome.genes)
        print(self.genome.genes)
        print(genes)

        for gene in genes:
        # for gene in self.genome.genes:

            if gene.conn_tip_neuron_type == ConnectionTipType.SENSORY:
                input_list = self.sensory_neurons
            elif gene.conn_tip_neuron_type == ConnectionTipType.INTERNAL:
                input_list = self.internal_neurons

            if gene.conn_end_neuron_type == ConnectionEndType.INTERNAL:
                output_list = self.internal_neurons
            elif gene.conn_end_neuron_type == ConnectionEndType.ACTION:
                output_list = self.action_neurons

            input_id = gene.conn_tip_neuron_id % len(input_list)
            output_id = gene.conn_end_neuron_id % len(output_list)

            input_list[input_id].output_neurons.append(output_list[output_id])
            output_list[output_id].input_neurons.append(input_list[input_id])




