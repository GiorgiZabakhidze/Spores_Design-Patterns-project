"""The possible results of one simulation, and their log messages"""

from enum import Enum


class Outcome(Enum):
    PREY_ESCAPED = "Pray ran into infinity"
    PREY_KILLED = "Some R-rated things have happened"
