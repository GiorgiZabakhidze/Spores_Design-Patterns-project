"""Ways a creature can move along the world ray"""

from abc import ABC, abstractmethod
from typing import Protocol


class Mover(Protocol):
    @property
    def legs(self) -> int: ...

    @property
    def wings(self) -> int: ...

    @property
    def stamina(self) -> int: ...


class Movement(ABC):
    name: str
    required_stamina: int
    cost: int
    speed: int

    def can_be_used_by(self, mover: Mover) -> bool:
        return self._has_stamina(mover) and self._has_body_for(mover)

    def _has_stamina(self, mover: Mover) -> bool:
        return mover.stamina >= max(self.required_stamina, self.cost)

    @abstractmethod
    def _has_body_for(self, mover: Mover) -> bool: ...


class Crawling(Movement):
    name = "Crawling"
    required_stamina = 0
    cost = 1
    speed = 1

    def _has_body_for(self, mover: Mover) -> bool:
        return True


class LeggedMovement(Movement):
    required_legs: int

    def _has_body_for(self, mover: Mover) -> bool:
        return mover.legs >= self.required_legs


class WingedMovement(Movement):
    required_wings: int

    def _has_body_for(self, mover: Mover) -> bool:
        return mover.wings >= self.required_wings


class Hopping(LeggedMovement):
    name = "Hopping"
    required_stamina = 20
    cost = 2
    speed = 3
    required_legs = 1


class Walking(LeggedMovement):
    name = "Walking"
    required_stamina = 40
    cost = 2
    speed = 4
    required_legs = 2


class Running(LeggedMovement):
    name = "Running"
    required_stamina = 60
    cost = 4
    speed = 6
    required_legs = 2


class Flying(WingedMovement):
    name = "Flying"
    required_stamina = 80
    cost = 4
    speed = 8
    required_wings = 2


DEFAULT_MOVEMENTS: tuple[Movement, ...] = (
    Crawling(),
    Hopping(),
    Walking(),
    Running(),
    Flying(),
)
