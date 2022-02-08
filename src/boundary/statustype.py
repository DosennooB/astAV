from enum import Enum

class StatusTyp(Enum):
    WAITING = 1
    PROCESSING = 2
    DONE = 3
    ERROR = 4
    CANCELD = 5