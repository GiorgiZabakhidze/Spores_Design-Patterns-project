import pytest

from creature_sim.creature import Body, Creature
from creature_sim.movement_policy import GreedyMovementPolicy
from creature_sim.outcome import Outcome
from creature_sim.power import Claws, ClawSize, Teeth, TeethSharpness
from creature_sim.reporting import ConsoleReporter, describe


def make_creature(body: Body | None = None) -> Creature:
    return Creature(
        body=body or Body(),
        health=10,
        stamina=20,
        base_power=5,
        movement_policy=GreedyMovementPolicy(),
        position=7,
    )


def test_describe_creature_without_extras() -> None:
    text = describe("Predator", make_creature())
    assert text == (
        "Predator: position=7 health=10 stamina=20 power=5 "
        "legs=0 wings=0 extras=[] attack=5"
    )


def test_describe_lists_extras_in_order() -> None:
    body = Body(
        legs=2,
        power_modifiers=(Claws(ClawSize.BIG), Teeth(TeethSharpness.SHARP)),
    )
    text = describe("Pray", make_creature(body))
    assert "extras=[big claws, sharp teeth]" in text
    assert text.endswith("attack=23")


def test_report_start_prints_header_and_both_creatures(
    capsys: pytest.CaptureFixture[str],
) -> None:
    ConsoleReporter().report_start(3, make_creature(), make_creature())
    lines = capsys.readouterr().out.splitlines()
    assert lines[0] == "=== Simulation #3 ==="
    assert lines[1].startswith("Predator: ")
    assert lines[2].startswith("Prey: ")


def test_report_outcome_prints_the_message(
    capsys: pytest.CaptureFixture[str],
) -> None:
    ConsoleReporter().report_outcome(Outcome.PREY_ESCAPED)
    assert capsys.readouterr().out == "Pray ran into infinity\n"
