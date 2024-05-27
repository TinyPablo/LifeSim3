from direction import Direction


class Transform:
    def __init__(self) -> None:
        self.position_x: int = None
        self.position_y: int = None

        self.direction: Direction = Direction.random()

    def __str__(self) -> str:
        return \
            f'x: {self.position_x}\n' \
            f'y: {self.position_y}\n' \
            f'x: {self.direction.name} {self.direction.value}'

    
