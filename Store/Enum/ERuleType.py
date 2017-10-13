from enum import Enum, unique


@unique
class ERuleType(Enum):
    page = 1
    regex = 2
