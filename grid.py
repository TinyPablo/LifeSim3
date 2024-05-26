import random
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from entity import Entity

class Grid:
    def __init__(self, width: int, height: int) -> None:
        self.width: int = width
        self.height: int = height
        self.grid: List[List[Optional['Entity']]] = [[None for _ in range(self.height)] for _ in range(self.width)]

    def __str__(self) -> str:
        return str(self.grid)

    def __repr__(self) -> str:
        return self.__str__()

    def is_cell_empty(self, x: int, y: int) -> bool:
        return self.grid[x][y] is None

    def deploy_enemy_randomly(self, entity: 'Entity') -> None:
        all_coords = [(x, y) for x in range(self.width) for y in range(self.height)]
        random.shuffle(all_coords)

        for x, y in all_coords:
            if self.is_cell_empty(x, y):
                self.place_entity(entity, x, y)
                return
        raise Exception('All cells are taken')

    def place_entity(self, entity: 'Entity', x: int, y: int) -> None:
        self.grid[x][y] = entity
        entity.set_position(x, y, self)

    def remove_entity(self, x: int, y: int) -> None:
        entity = self.grid[x][y]
        if entity:
            entity.set_position(None, None)
            self.grid[x][y] = None


def main() -> None:
    from entity import Entity
    from genome import Genome

    g = Grid(2, 2)
    e = Entity(Genome(4))
    print(g)
    g.deploy_enemy_randomly(e)
    print(g)


if __name__ == '__main__':
    main()
