from direction import Direction


class Transform:
    def __init__(self) -> None:
        self.position_x: int = None
        self.position_y: int = None

        self.direction: Direction = Direction.random()

    @property
    def next_x(self) -> tuple[int, int]:
        return self.position_x + self.direction.value[0]
    
    @property
    def next_y(self) -> tuple[int, int]:
        return self.position_y + self.direction.value[1]

    def __str__(self) -> str:
        return f'[x: {self.position_x} y: {self.position_y}] {self.direction.name}'

    
