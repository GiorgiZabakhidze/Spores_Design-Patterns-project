"""fight class between predator and prey that met"""

from creature_sim.creature import Creature
from creature_sim.outcome import Outcome


class FightPhase:
    def run(self, predator: Creature, prey: Creature) -> Outcome:
        while predator.is_alive and prey.is_alive:
            predator.attack(prey)
            prey.attack(predator)
        return Outcome.PREY_ESCAPED if prey.is_alive else Outcome.PREY_KILLED
