"""print thigns for user"""

from abc import ABC, abstractmethod

from creature_sim.creature import Creature
from creature_sim.outcome import Outcome

PREDATOR_LABEL = "Predator"
PREY_LABEL = "Prey"


class SimulationReporter(ABC):
    @abstractmethod
    def report_start(self, number: int, predator: Creature, prey: Creature) -> None: ...

    @abstractmethod
    def report_outcome(self, outcome: Outcome) -> None: ...


def describe(label: str, creature: Creature) -> str:
    extras = ", ".join(str(modifier) for modifier in creature.body.power_modifiers)
    return (
        f"{label}: position={creature.position} health={creature.health} "
        f"stamina={creature.stamina} power={creature.base_power} "
        f"legs={creature.legs} wings={creature.wings} "
        f"extras=[{extras}] attack={creature.attack_power}"
    )


class ConsoleReporter:
    def report_start(self, sim_no: int, predator: Creature, prey: Creature) -> None:
        print(f"=== Simulation #{sim_no} ===")
        print(describe(PREDATOR_LABEL, predator))
        print(describe(PREY_LABEL, prey))

    def report_outcome(self, outcome: Outcome) -> None:
        print(outcome.value)
