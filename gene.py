import random
from typing import Optional
from connection import ConnectionTipType, ConnectionEndType


class Gene:
    def __init__(self, gene: Optional[int] = None) -> None:
        self._gene: Optional[int] = None
        if gene is None:
            self.randomize()
        else:
            self._gene = gene

    @property
    def gene(self) -> int:
        if self._gene is None:
            raise Exception('Gene is None')
        return self._gene & 0xFFFF_FFFF
    
    @gene.setter
    def gene(self, value: int) -> None:
        self._gene = value

    def randomize(self) -> None:
        self.gene: int = random.randint(0, 0xFFFF_FFFF)

    def __int__(self) -> int:
        return self.gene

    def __str__(self) -> str:
        return \
            f'{self.conn_tip_neuron_type.name} ' \
            f'{self.conn_tip_neuron_id} ' \
            f'{self.conn_end_neuron_type.name} ' \
            f'{self.conn_end_neuron_id} ' \
            f'{self.conn_weight} ' \
            f'{self.gene}'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    @property
    def conn_tip_neuron_type(self) -> ConnectionTipType:
        if (self.gene >> 31) & 1:
            return ConnectionTipType.INPUT
        return ConnectionTipType.INTERNAL
    
    @property
    def conn_tip_neuron_id(self) -> int:
        return (self.gene >> 24) & 0b111_1111
    
    @property
    def conn_end_neuron_type(self) -> ConnectionEndType:
        if (self.gene >> 23) & 1:
            return ConnectionEndType.OUTPUT
        return ConnectionEndType.INTERNAL
    
    @property
    def conn_end_neuron_id(self) -> int:
        return (self.gene >> 16) & 0b111_1111
    
    @property
    def conn_weight(self) -> float:
        n: int = self.gene & 0xFFFF
        return n / 8192 - 4
    
    def try_mutate(self, percent_chance: float):
        if random.uniform(0.0, 100.0) < percent_chance:
            print('mutated')
            self.flip_random_bit()

    def flip_random_bit(self) -> None:
        bit_position = random.randint(0, 31)
        mask = 1 << bit_position
        self.gene ^= mask
    
def main() -> None:
    g: Gene = Gene()

    print(g.gene)
    print(g.conn_tip_neuron_type)
    print(g.conn_tip_neuron_id)
    print(g.conn_end_neuron_type)
    print(g.conn_end_neuron_id)
    print(g.conn_weight)

    g.flip_random_bit()
 
 
    print(g.gene)
    print(g.conn_tip_neuron_type)
    print(g.conn_tip_neuron_id)
    print(g.conn_end_neuron_type)
    print(g.conn_end_neuron_id)
    print(g.conn_weight)

if __name__ == '__main__':
    main()