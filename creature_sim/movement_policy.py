"""which Movement the Mover chooses"""

from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass

from creature_sim.movement import Movement, Mover


class MovementPolicy(ABC):
    @abstractmethod
    def choose(
        self, mover: Mover, movements: Sequence[Movement]
    ) -> Movement | None: ...


@dataclass(frozen=True)
class GreedyMovementPolicy(MovementPolicy):
    def choose(self, mover: Mover, movements: Sequence[Movement]) -> Movement | None:
        movs_list = [m for m in movements if m.can_be_used_by(mover)]
        return max(movs_list, key=lambda m: m.speed, default=None)
