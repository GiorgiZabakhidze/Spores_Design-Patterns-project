"""tests for fight after they met with GreedyPolicy"""

from creature_sim.creature import Body, Creature
from creature_sim.fight import FightPhase
from creature_sim.movement_policy import GreedyMovementPolicy
from creature_sim.outcome import Outcome


def make_creature(health: int, power: int) -> Creature:
    return Creature(
        body=Body(),
        health=health,
        stamina=0,
        base_power=power,
        movement_policy=GreedyMovementPolicy(),
    )


def fight(predator: Creature, prey: Creature) -> Outcome:
    return FightPhase().run(predator, prey)


def test_stronger_predator_kills_prey() -> None:
    assert fight(make_creature(10, 5), make_creature(10, 1)) is Outcome.PREY_KILLED


def test_stronger_prey_wins() -> None:
    assert fight(make_creature(10, 1), make_creature(10, 5)) is Outcome.PREY_ESCAPED


def test_both_die_in_same_round_counts_as_predator_win() -> None:
    predator, prey = make_creature(5, 5), make_creature(5, 5)
    assert fight(predator, prey) is Outcome.PREY_KILLED
    assert not predator.is_alive
    assert not prey.is_alive


def test_dying_creature_still_hits_back() -> None:
    predator, prey = make_creature(10, 3), make_creature(1, 3)
    fight(predator, prey)
    assert predator.health == 7


def test_fight_lasts_several_rounds() -> None:
    predator, prey = make_creature(10, 2), make_creature(7, 1)
    assert fight(predator, prey) is Outcome.PREY_KILLED
    assert predator.health == 6
