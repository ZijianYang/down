from enum import Enum, unique


@unique
class RuleType(Enum):
    page = 1
    regex = 2
