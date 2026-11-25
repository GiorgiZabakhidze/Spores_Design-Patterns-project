import pytest

from creature_sim.power import (
    Claws,
    ClawSize,
    Teeth,
    TeethSharpness,
    apply_modifiers,
)

BASE_POWER = 5


@pytest.mark.parametrize(
    ("size", "expected"),
    [(ClawSize.SMALL, 10), (ClawSize.MEDIUM, 15), (ClawSize.BIG, 20)],
)
def test_claws_multiply(size: ClawSize, expected: int) -> None:
    assert Claws(size).apply(BASE_POWER) == expected


@pytest.mark.parametrize(
    ("sharpness", "expected"),
    [
        (TeethSharpness.SHARP, 8),
        (TeethSharpness.SHARPER, 11),
        (TeethSharpness.SHARPEST, 14),
    ],
)
def test_teeth_add(sharpness: TeethSharpness, expected: int) -> None:
    assert Teeth(sharpness).apply(BASE_POWER) == expected


def test_claws_then_teeth() -> None:
    modifiers = [Claws(ClawSize.BIG), Teeth(TeethSharpness.SHARP)]
    assert apply_modifiers(BASE_POWER, modifiers) == 23


def test_teeth_then_claws() -> None:
    modifiers = [Teeth(TeethSharpness.SHARP), Claws(ClawSize.BIG)]
    assert apply_modifiers(BASE_POWER, modifiers) == 32


def test_no_modifiers_keeps_base_power() -> None:
    assert apply_modifiers(BASE_POWER, []) == BASE_POWER


def test_str_is_readable() -> None:
    assert str(Claws(ClawSize.BIG)) == "big claws"
    assert str(Teeth(TeethSharpness.SHARPER)) == "sharper teeth"
