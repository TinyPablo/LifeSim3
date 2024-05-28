import os
import random
from typing import Optional, List, TYPE_CHECKING
from cell import Cell
from direction import Direction
from simulation_settings import settings
from PIL import Image

if TYPE_CHECKING:
    from entity import Entity
    from simulation import Simulation

class Grid:
    def __init__(self, width: int, height: int, simulation: 'Simulation') -> None:
        self.width: int = width
        self.height: int = height
        self.simulation: 'Simulation' = simulation
        self.grid: List[List[Cell]] = [[Cell() for _ in range(self.height)] for _ in range(self.width)]

    def __str__(self) -> str:
        grid_str = '\n'.join(
            ' '.join(str(self.grid[x][y]) for x in range(self.width))
            for y in range(self.height)
        )
        return grid_str


    def __repr__(self) -> str:
        return self.__str__()

    def deploy_entity_randomly(self, entity: 'Entity') -> None:
        all_coords = [(x, y) for x in range(self.width) for y in range(self.height)]
        random.shuffle(all_coords)

        for x, y in all_coords:
            placed = self.try_set_position(entity, x, y)
            if placed:
                entity.grid = self
                return
        raise Exception('All cells are taken')
    
    def try_set_position(self, object: Optional['Entity'], x: int, y: int) -> bool:
        if 0 > x or x >= self.width:
            return False
        if 0 > y or y >= self.height:
            return False
        if self.grid[x][y].is_occupied:
            return False
        self.place_object(object, x, y)
        return True

    def place_object(self, object: Optional['Entity'], x: int, y: int) -> None:
        self.grid[x][y].set_object(object)
        object.set_position(x, y)

    def remove_entity(self, x: int, y: int) -> None:
        cell = self.grid[x][y]
        if cell.is_entity:
            self.grid[x][y].reset()

    def render(self, GEN: int, STEP: int) -> None:
        path = f'{settings.simulation_directory}/{settings.seed}/{GEN}'
        os.makedirs(path, exist_ok=True)
        
        full_path = f'{path}/{STEP}.png'
        
        img = Image.new('RGB', (self.width, self.height), "white")
        pixels = img.load()
        
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[x][y]
                if cell.is_entity:
                    pixels[x, y] = (0, 0, 255)
                elif not cell.is_occupied:
                    pixels[x, y] = (255, 255, 255)
        
        img.save(full_path)

    def move_entity_in_direction(self, entity: 'Entity', direction: Direction, absolute_direction: Optional[Direction] = None) -> None:
        x: int = entity.transform.position_x
        y: int = entity.transform.position_y
        new_x: int = x + direction.value[0]
        new_y: int = y + direction.value[1]
        if self.try_set_position(entity, new_x, new_y):
            self.remove_entity(x, y)
            entity.set_position(new_x, new_y)
            entity.transform.direction = absolute_direction if absolute_direction is not None else direction

    def move_entity_in_relative_direction(self, entity: 'Entity', direction: Direction) -> None:
        current_direction = entity.transform.direction
        relative_direction = self.get_relative_direction(current_direction, direction)
        self.move_entity_in_direction(entity, relative_direction, direction)

    
    def get_relative_direction(self, current_direction: Direction, relative_direction: Direction) -> Direction:
        direction_mapping = {
            (Direction.UP, Direction.UP): Direction.UP,
            (Direction.UP, Direction.DOWN): Direction.DOWN,
            (Direction.UP, Direction.LEFT): Direction.LEFT,
            (Direction.UP, Direction.RIGHT): Direction.RIGHT,
            (Direction.UP, Direction.UP_LEFT): Direction.UP_LEFT,
            (Direction.UP, Direction.UP_RIGHT): Direction.UP_RIGHT,
            (Direction.UP, Direction.DOWN_LEFT): Direction.DOWN_LEFT,
            (Direction.UP, Direction.DOWN_RIGHT): Direction.DOWN_RIGHT,
            (Direction.DOWN, Direction.UP): Direction.DOWN,
            (Direction.DOWN, Direction.DOWN): Direction.UP,
            (Direction.DOWN, Direction.LEFT): Direction.RIGHT,
            (Direction.DOWN, Direction.RIGHT): Direction.LEFT,
            (Direction.DOWN, Direction.UP_LEFT): Direction.DOWN_RIGHT,
            (Direction.DOWN, Direction.UP_RIGHT): Direction.DOWN_LEFT,
            (Direction.DOWN, Direction.DOWN_LEFT): Direction.UP_RIGHT,
            (Direction.DOWN, Direction.DOWN_RIGHT): Direction.UP_LEFT,
            (Direction.LEFT, Direction.UP): Direction.LEFT,
            (Direction.LEFT, Direction.DOWN): Direction.RIGHT,
            (Direction.LEFT, Direction.LEFT): Direction.DOWN,
            (Direction.LEFT, Direction.RIGHT): Direction.UP,
            (Direction.LEFT, Direction.UP_LEFT): Direction.DOWN_LEFT,
            (Direction.LEFT, Direction.UP_RIGHT): Direction.UP_RIGHT,
            (Direction.LEFT, Direction.DOWN_LEFT): Direction.UP_LEFT,
            (Direction.LEFT, Direction.DOWN_RIGHT): Direction.DOWN_RIGHT,
            (Direction.RIGHT, Direction.UP): Direction.RIGHT,
            (Direction.RIGHT, Direction.DOWN): Direction.LEFT,
            (Direction.RIGHT, Direction.LEFT): Direction.UP,
            (Direction.RIGHT, Direction.RIGHT): Direction.DOWN,
            (Direction.RIGHT, Direction.UP_LEFT): Direction.UP_RIGHT,
            (Direction.RIGHT, Direction.UP_RIGHT): Direction.DOWN_LEFT,
            (Direction.RIGHT, Direction.DOWN_LEFT): Direction.DOWN_RIGHT,
            (Direction.RIGHT, Direction.DOWN_RIGHT): Direction.UP_LEFT,
            (Direction.UP_LEFT, Direction.UP): Direction.UP_LEFT,
            (Direction.UP_LEFT, Direction.DOWN): Direction.DOWN_RIGHT,
            (Direction.UP_LEFT, Direction.LEFT): Direction.UP,
            (Direction.UP_LEFT, Direction.RIGHT): Direction.DOWN,
            (Direction.UP_LEFT, Direction.UP_LEFT): Direction.LEFT,
            (Direction.UP_LEFT, Direction.UP_RIGHT): Direction.DOWN_LEFT,
            (Direction.UP_LEFT, Direction.DOWN_LEFT): Direction.UP_RIGHT,
            (Direction.UP_LEFT, Direction.DOWN_RIGHT): Direction.RIGHT,
            (Direction.UP_RIGHT, Direction.UP): Direction.UP_RIGHT,
            (Direction.UP_RIGHT, Direction.DOWN): Direction.DOWN_LEFT,
            (Direction.UP_RIGHT, Direction.LEFT): Direction.DOWN,
            (Direction.UP_RIGHT, Direction.RIGHT): Direction.UP,
            (Direction.UP_RIGHT, Direction.UP_LEFT): Direction.DOWN_RIGHT,
            (Direction.UP_RIGHT, Direction.UP_RIGHT): Direction.RIGHT,
            (Direction.UP_RIGHT, Direction.DOWN_LEFT): Direction.LEFT,
            (Direction.UP_RIGHT, Direction.DOWN_RIGHT): Direction.UP_LEFT,
            (Direction.DOWN_LEFT, Direction.UP): Direction.DOWN_LEFT,
            (Direction.DOWN_LEFT, Direction.DOWN): Direction.UP_RIGHT,
            (Direction.DOWN_LEFT, Direction.LEFT): Direction.UP,
            (Direction.DOWN_LEFT, Direction.RIGHT): Direction.DOWN,
            (Direction.DOWN_LEFT, Direction.UP_LEFT): Direction.RIGHT,
            (Direction.DOWN_LEFT, Direction.UP_RIGHT): Direction.UP_LEFT,
            (Direction.DOWN_LEFT, Direction.DOWN_LEFT): Direction.LEFT,
            (Direction.DOWN_LEFT, Direction.DOWN_RIGHT): Direction.DOWN_RIGHT,
            (Direction.DOWN_RIGHT, Direction.UP): Direction.DOWN_RIGHT,
            (Direction.DOWN_RIGHT, Direction.DOWN): Direction.UP_LEFT,
            (Direction.DOWN_RIGHT, Direction.LEFT): Direction.DOWN,
            (Direction.DOWN_RIGHT, Direction.RIGHT): Direction.UP,
            (Direction.DOWN_RIGHT, Direction.UP_LEFT): Direction.LEFT,
            (Direction.DOWN_RIGHT, Direction.UP_RIGHT): Direction.RIGHT,
            (Direction.DOWN_RIGHT, Direction.DOWN_LEFT): Direction.DOWN_LEFT,
            (Direction.DOWN_RIGHT, Direction.DOWN_RIGHT): Direction.UP_RIGHT,
        }
        return direction_mapping[(current_direction, relative_direction)]

