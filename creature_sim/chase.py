from collections.abc import Sequence

from creature_sim.creature import Creature
from creature_sim.movement import Movement


class ChasePhase:
    def __init__(self, movements: Sequence[Movement]) -> None:
        self._movements = movements

    def run(self, predator: Creature, prey: Creature) -> bool:
        """returns true if predator catches prey"""
        while predator.try_move(self._movements):
            prey.try_move(self._movements)
            if predator.position >= prey.position:
                return True
        return False
