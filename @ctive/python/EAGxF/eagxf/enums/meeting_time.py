from enum import Enum, auto


class MtgTime(Enum):
    FUTURE = auto()
    PAST = auto()

    def __str__(self):
        return self.name.lower()

    def __repr__(self):
        return self.name.lower()
    
    @property
    def low(self):
        return self.name.lower()