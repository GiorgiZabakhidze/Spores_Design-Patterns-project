from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass
from enum import IntEnum


class PowerModifier(ABC):
    @abstractmethod
    def apply(self, power: int) -> int: ...

    @abstractmethod
    def __str__(self) -> str: ...


class ClawSize(IntEnum):
    SMALL = 2
    MEDIUM = 3
    BIG = 4


class TeethSharpness(IntEnum):
    SHARP = 3
    SHARPER = 6
    SHARPEST = 9


@dataclass(frozen=True)
class Claws(PowerModifier):
    size: ClawSize

    def apply(self, power: int) -> int:
        return power * self.size

    def __str__(self) -> str:
        return f"{self.size.name.lower()} claws"


@dataclass(frozen=True)
class Teeth(PowerModifier):
    sharpness: TeethSharpness

    def apply(self, power: int) -> int:
        return power + self.sharpness

    def __str__(self) -> str:
        return f"{self.sharpness.name.lower()} teeth"


def apply_modifiers(power: int, modifiers: Sequence[PowerModifier]) -> int:
    for modifier in modifiers:
        power = modifier.apply(power)
    return power
