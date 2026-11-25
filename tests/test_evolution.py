from random import Random

from creature_sim.creature import Creature
from creature_sim.evolution import (
    HEALTH_RANGE,
    LEGS_RANGE,
    PREY_POSITION_RANGE,
    STAMINA_RANGE,
    WINGS_RANGE,
    Evolver,
)
from creature_sim.movement_policy import GreedyMovementPolicy
from creature_sim.power import Claws, Teeth

SAMPLES = 300


def make_evolver() -> Evolver:
    return Evolver(Random(0), GreedyMovementPolicy())


def evolve_many(evolver: Evolver) -> list[Creature]:
    return [evolver.evolve_prey() for _ in range(SAMPLES)]


def test_predator_starts_at_zero() -> None:
    assert make_evolver().evolve_predator().position == 0


def test_stats_stay_inside_ranges() -> None:
    for creature in evolve_many(make_evolver()):
        assert HEALTH_RANGE[0] <= creature.health <= HEALTH_RANGE[1]
        assert STAMINA_RANGE[0] <= creature.stamina <= STAMINA_RANGE[1]
        assert LEGS_RANGE[0] <= creature.legs <= LEGS_RANGE[1]
        assert WINGS_RANGE[0] <= creature.wings <= WINGS_RANGE[1]


def test_pray_position_stays_inside_range() -> None:
    for creature in evolve_many(make_evolver()):
        low, high = PREY_POSITION_RANGE
        assert low <= creature.position <= high


def test_same_seed_gives_same_creature() -> None:
    first = make_evolver().evolve_prey()
    second = make_evolver().evolve_prey()
    assert first == second


def test_modifiers_are_optional_and_claws_come_first() -> None:
    sizes = set()
    for creature in evolve_many(make_evolver()):
        modifiers = creature.body.power_modifiers
        sizes.add(len(modifiers))
        kinds = [type(modifier) for modifier in modifiers]
        assert kinds in ([], [Claws], [Teeth], [Claws, Teeth])
    assert sizes == {0, 1, 2}
