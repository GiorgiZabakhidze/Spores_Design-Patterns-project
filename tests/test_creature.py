from creature_sim.creature import Body, Creature
from creature_sim.movement import DEFAULT_MOVEMENTS
from creature_sim.movement_policy import GreedyMovementPolicy
from creature_sim.power import Claws, ClawSize, Teeth, TeethSharpness

BASE_POWER = 5


def make_creature(
    body: Body | None = None,
    health: int = 10,
    stamina: int = 100,
) -> Creature:
    return Creature(
        body=body or Body(),
        health=health,
        stamina=stamina,
        base_power=BASE_POWER,
        movement_policy=GreedyMovementPolicy(),
    )


def test_attack_power_without_modifiers_is_base_power() -> None:
    assert make_creature().attack_power == BASE_POWER


def test_attack_power_follows_modifier_order() -> None:
    claws, teeth = Claws(ClawSize.BIG), Teeth(TeethSharpness.SHARP)
    claws_first = make_creature(Body(power_modifiers=(claws, teeth)))
    teeth_first = make_creature(Body(power_modifiers=(teeth, claws)))
    assert claws_first.attack_power == 23
    assert teeth_first.attack_power == 32


def test_legs_and_wings_come_from_body() -> None:
    creature = make_creature(Body(legs=2, wings=4))
    assert creature.legs == 2
    assert creature.wings == 4


def test_is_alive_edges() -> None:
    assert make_creature(health=1).is_alive
    assert not make_creature(health=0).is_alive
    assert not make_creature(health=-3).is_alive


def test_try_move_picks_the_fastest_available() -> None:
    creature = make_creature(Body(legs=2), stamina=65)
    assert creature.try_move(DEFAULT_MOVEMENTS)  # Running: speed 6, cost 4
    assert creature.position == 6
    assert creature.stamina == 61


def test_try_move_flies_when_it_has_wings_and_stamina() -> None:
    creature = make_creature(Body(wings=2), stamina=80)
    assert creature.try_move(DEFAULT_MOVEMENTS)  # Flying: speed 8, cost 4
    assert creature.position == 8
    assert creature.stamina == 76


def test_try_move_falls_back_when_stamina_is_low() -> None:
    creature = make_creature(Body(legs=2), stamina=30)
    assert creature.try_move(DEFAULT_MOVEMENTS)  # Hopping: speed 3, cost 2
    assert creature.position == 3
    assert creature.stamina == 28


def test_try_move_crawls_without_limbs() -> None:
    creature = make_creature(stamina=5)
    assert creature.try_move(DEFAULT_MOVEMENTS)  # Crawling: speed 1, cost 1
    assert creature.position == 1
    assert creature.stamina == 4


def test_try_move_with_zero_stamina_changes_nothing() -> None:
    creature = make_creature(Body(legs=2), stamina=0)
    assert not creature.try_move(DEFAULT_MOVEMENTS)
    assert creature.position == 0
    assert creature.stamina == 0


def test_creature_eventually_runs_out_of_stamina() -> None:
    creature = make_creature(stamina=3)
    moves = sum(creature.try_move(DEFAULT_MOVEMENTS) for _ in range(10))
    assert moves == 3
    assert creature.stamina == 0


def test_attack_reduces_only_the_target_health() -> None:
    attacker, target = make_creature(health=10), make_creature(health=10)
    attacker.attack(target)
    assert target.health == 10 - BASE_POWER
    assert attacker.health == 10


def test_attack_can_take_health_below_zero() -> None:
    attacker, target = make_creature(), make_creature(health=1)
    attacker.attack(target)
    assert target.health < 0
    assert not target.is_alive
