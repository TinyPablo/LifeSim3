from direction import Direction


class Transform:
    def __init__(self) -> None:
        self.position_x: int = None
        self.position_y: int = None

        self.direction: Direction = Direction.random()

    def __str__(self) -> str:
        return f'[x: {self.position_x} y: {self.position_y}] {self.direction.name}'

    
