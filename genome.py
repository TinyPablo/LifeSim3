import random
from gene import Gene


class Genome:
    def __init__(self, size: int, genes: list[Gene] = None) -> None:
        self.genes: list[Gene] = None
        self.size: int = size
        if genes is None:
            self.randomize()
        else:
            self.genes = genes

    def randomize(self) -> None:
        self.genes: list[Gene] = [Gene() for _ in range(self.size)]

    def __str__(self) -> str:
        return '\n'.join([str(gene) for gene in self.genes])
    
    def __iter__(self):
        return iter(self.genes)
    
    def mutate(self) -> None:
        random.choice(self.genes).flip_random_bit()
    
    
    

def main() -> None:
    g: Genome = Genome(4)
    print(g)

if __name__ == '__main__':
    main() 