from typing import Optional
from entity import Entity

class Cell:
    def __init__(self) -> None:
        self.object: Optional[Entity] = None

    def set_object(self, object: Optional[Entity]) -> None:
        self.object = object

    def reset(self) -> None:
        self.object = None

    @property
    def occupied(self) -> bool:
        return self.object is not None
    
    @property
    def is_entity(self) -> bool:
        return type(self.object) == Entity
    
    def __str__(self) -> str:
        return self.object.__str__()
    
    def __repr__(self) -> str:
        return self.__str__()