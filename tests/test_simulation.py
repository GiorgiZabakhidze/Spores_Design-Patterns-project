from random import Random

from creature_sim.chase import ChasePhase
from creature_sim.creature import Body, Creature
from creature_sim.evolution import Evolver
from creature_sim.fight import FightPhase
from creature_sim.movement import DEFAULT_MOVEMENTS
from creature_sim.movement_policy import GreedyMovementPolicy
from creature_sim.outcome import Outcome
from creature_sim.reporting import SimulationReporter
from creature_sim.simulation import Simulation


def make_creature(stamina: int, health: int, power: int, position: int = 0) -> Creature:
    return Creature(
        body=Body(),
        health=health,
        stamina=stamina,
        base_power=power,
        movement_policy=GreedyMovementPolicy(),
        position=position,
    )


class FixedEvolver(Evolver):
    """Hands out the creatures it was given instead of random ones."""

    def __init__(self, predator: Creature, prey: Creature) -> None:
        super().__init__(Random(0), GreedyMovementPolicy())
        self._predator = predator
        self._prey = prey

    def evolve_predator(self) -> Creature:
        return self._predator

    def evolve_prey(self) -> Creature:
        return self._prey


class FakeReporter(SimulationReporter):
    def __init__(self) -> None:
        self.calls: list[tuple[str, int | Outcome]] = []

    def report_start(self, number: int, predator: Creature, prey: Creature) -> None:
        self.calls.append(("start", predator.position))
        self.calls.append(("prey_start", prey.position))

    def report_outcome(self, outcome: Outcome) -> None:
        self.calls.append(("outcome", outcome))


def run_simulation(predator: Creature, prey: Creature) -> tuple[Outcome, FakeReporter]:
    reporter = FakeReporter()
    simulation = Simulation(
        FixedEvolver(predator, prey),
        ChasePhase(DEFAULT_MOVEMENTS),
        FightPhase(),
        reporter,
    )
    return simulation.run(1), reporter


def test_tired_predator_means_prey_escaped() -> None:
    predator = make_creature(stamina=0, health=10, power=5)
    prey = make_creature(stamina=0, health=10, power=1, position=50)
    outcome, _ = run_simulation(predator, prey)
    assert outcome is Outcome.PREY_ESCAPED


def test_caught_and_killed_prey() -> None:
    predator = make_creature(stamina=5, health=10, power=5)
    prey = make_creature(stamina=0, health=5, power=1, position=1)
    outcome, _ = run_simulation(predator, prey)
    assert outcome is Outcome.PREY_KILLED


def test_caught_but_predator_loses_fight() -> None:
    predator = make_creature(stamina=5, health=5, power=1)
    prey = make_creature(stamina=0, health=50, power=5, position=1)
    outcome, _ = run_simulation(predator, prey)
    assert outcome is Outcome.PREY_ESCAPED


def test_start_is_reported_before_the_chase() -> None:
    predator = make_creature(stamina=5, health=10, power=5)
    prey = make_creature(stamina=0, health=5, power=1, position=1)
    _, reporter = run_simulation(predator, prey)
    assert reporter.calls[0] == ("start", 0)  # predator had not moved yet
    assert reporter.calls[1] == ("prey_start", 1)


def test_reported_outcome_matches_returned_outcome() -> None:
    predator = make_creature(stamina=0, health=10, power=5)
    prey = make_creature(stamina=0, health=10, power=1, position=9)
    outcome, reporter = run_simulation(predator, prey)
    assert reporter.calls[-1] == ("outcome", outcome)
