from creature_sim.chase import ChasePhase
from creature_sim.creature import Body, Creature
from creature_sim.movement import DEFAULT_MOVEMENTS
from creature_sim.movement_policy import GreedyMovementPolicy


def make_creature(stamina: int, position: int = 0) -> Creature:
    """creature wit not wings or legs so it can only crawl with speed 1 and cost 1"""
    return Creature(
        body=Body(),
        health=10,
        stamina=stamina,
        base_power=1,
        movement_policy=GreedyMovementPolicy(),
        position=position,
    )


def chase(predator: Creature, prey: Creature) -> bool:
    return ChasePhase(DEFAULT_MOVEMENTS).run(predator, prey)


def test_predator_catches_a_close_prey() -> None:
    assert chase(make_creature(5), make_creature(0, position=1))


def test_predator_without_stamina_never_moves() -> None:
    predator = make_creature(0)
    assert not chase(predator, make_creature(5, position=3))
    assert predator.position == 0


def test_predator_runs_out_before_reaching_far_prey() -> None:
    predator = make_creature(3)
    assert not chase(predator, make_creature(0, position=100))
    assert predator.position == 3


def test_tired_prey_stands_still_and_gets_caught() -> None:
    assert chase(make_creature(10), make_creature(0, position=5))


def test_equal_crawlers_never_close_the_gap() -> None:
    predator, prey = make_creature(5), make_creature(5, position=2)
    assert not chase(predator, prey)
    assert predator.stamina == 0
    assert prey.position - predator.position == 2


def test_same_start_with_stamina_is_caught_after_first_move() -> None:
    predator = make_creature(5)
    assert chase(predator, make_creature(0))
    assert predator.position == 1


def test_same_start_without_stamina_escapes() -> None:
    assert not chase(make_creature(0), make_creature(0))
