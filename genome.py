import random
from typing import List, Optional
from gene import Gene


class Genome:
    def __init__(self, size: Optional[int] = None, genes: Optional[list[Gene]] = None) -> None:
        self.genes: Optional[List[Gene]] = None
        self.size: Optional[int] = size
        if genes is None:
            self.randomize()
        else:
            self.genes = genes

    def randomize(self) -> None:
        if self.size is None:
            raise Exception('None exception')
        self.genes = [Gene() for _ in range(self.size)]

    def __str__(self) -> str:
        if self.genes is None:
            raise Exception('None exception')
        return '\n'.join([str(gene) for gene in self.genes])
    
    def __iter__(self):
        return iter(self.genes)
    
    def mutate(self) -> None:
        if self.genes is None:
            raise Exception('None exception')
        random.choice(self.genes).flip_random_bit()

    def crossover(genome_a: 'Genome', genome_b: 'Genome') -> 'Genome':
        if genome_a.genes is None or genome_b.genes is None:
            raise Exception('None exeption')
        half_len_a = len(genome_a.genes) // 2
        half_len_b = len(genome_b.genes) // 2

        use_first_half_a = bool(random.randint(0, 1))
        use_first_half_b = bool(random.randint(0, 1))

        half_a = genome_a.genes[:half_len_a] if use_first_half_a else genome_a.genes[half_len_a:]
        half_b = genome_b.genes[:half_len_b] if use_first_half_b else genome_b.genes[half_len_b:]

        return Genome(genes=half_a + half_b)


def main() -> None:
    from genome import Genome
    g1, g2 = Genome(2), Genome(2)
    print(g1, '\n')
    print(g2, '\n')

    g3 = Genome.crossover(g1, g2)
    print(g3, '\n')


if __name__ == '__main__':
    main()