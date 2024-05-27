import os
import random
from typing import Optional, List, TYPE_CHECKING
from cell import Cell
from simulation_settings import settings
from PIL import Image

if TYPE_CHECKING:
    from entity import Entity

class Grid:
    def __init__(self, width: int, height: int) -> None:
        self.width: int = width
        self.height: int = height
        self.grid: List[List[Cell]] = [[Cell() for _ in range(self.height)] for _ in range(self.width)]

    def __str__(self) -> str:
        grid_str = ''
        for row in self.grid:
            row_str = ' '.join([str(cell) if cell is not None else '.' for cell in row])
            grid_str += row_str + '\n'
        return grid_str.strip()

    def __repr__(self) -> str:
        return self.__str__()

    def __repr__(self) -> str:
        return self.__str__()

    def deploy_enemy_randomly(self, entity: 'Entity') -> None:
        all_coords = [(x, y) for x in range(self.width) for y in range(self.height)]
        random.shuffle(all_coords)

        for x, y in all_coords:
            if not self.grid[x][y].occupied:
                self.place_object(entity, x, y)
                return
        raise Exception('All cells are taken')
    
    def try_set_position(self, object: Optional['Entity'], x: int, y: int) -> bool:
        if 0 > x or x > self.width:
            return False
        if 0 > y or y > self.height:
            return False
        if self.grid[x][y].occupied:
            return False
        
        self.place_object(object, x, y)

    def place_object(self, object: Optional['Entity'], x: int, y: int) -> None:
        self.grid[x][y].set_object(object)
        object.set_position(x, y, self)

    def remove_entity(self, x: int, y: int) -> None:
        cell = self.grid[x][y]
        if cell.is_entity:
            cell.object.die()
            self.grid[x][y].reset()

    def render(self) -> None:
        GEN = 1
        STEP = 1
        path = f'./{settings.SEED}/{GEN}'
        os.makedirs(path, exist_ok=True)
        
        full_path = f'{path}/{STEP}.png'
        
        height = len(self.grid)
        width = len(self.grid[0])
        
        img = Image.new('RGB', (width, height), "white")
        pixels = img.load()
        
        for y in range(height):
            for x in range(width):
                cell = self.grid[y][x]
                if cell.is_entity:
                    pixels[x, y] = (0, 0, 255)
                elif not cell.occupied:
                    pixels[x, y] = (255, 255, 255)
        
        img.save(full_path)