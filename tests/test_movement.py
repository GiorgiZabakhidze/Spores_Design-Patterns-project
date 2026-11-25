"""Tests for movement.py — read these as the *specification* of what to build.

Run only these with:  .venv/bin/python -m pytest tests/test_movement.py -v
"""

from dataclasses import dataclass

import pytest

from creature_sim.movement import (
    DEFAULT_MOVEMENTS,
    Crawling,
    Flying,
    Hopping,
    Movement,
    Running,
    Walking,
)


# A tiny fake creature. It is NOT a subclass of anything — it just *has*
# legs, wings and stamina, which is all the `Mover` protocol asks for.
# That is "duck typing": if it walks like a duck... it can Walk.
@dataclass
class FakeMover:
    legs: int = 0
    wings: int = 0
    stamina: int = 100


# ------------------------------------------------- the table from the task
@pytest.mark.parametrize(
    ("movement", "required_stamina", "cost", "speed"),
    [
        (Crawling(), 0, 1, 1),
        (Hopping(), 20, 2, 3),
        (Walking(), 40, 2, 4),
        (Running(), 60, 4, 6),
        (Flying(), 80, 4, 8),
    ],
)
def test_movement_matches_table(
    movement: Movement, required_stamina: int, cost: int, speed: int
) -> None:
    assert movement.required_stamina == required_stamina
    assert movement.cost == cost
    assert movement.speed == speed


# ------------------------------------------------- body requirements
def test_anyone_can_crawl() -> None:
    assert Crawling().can_be_used_by(FakeMover(legs=0, wings=0))
    assert Crawling().can_be_used_by(FakeMover(legs=4, wings=2))


def test_hopping_needs_one_leg() -> None:
    assert not Hopping().can_be_used_by(FakeMover(legs=0))
    assert Hopping().can_be_used_by(FakeMover(legs=1))


@pytest.mark.parametrize("movement", [Walking(), Running()])
def test_walking_and_running_need_two_legs(movement: Movement) -> None:
    assert not movement.can_be_used_by(FakeMover(legs=1))
    assert movement.can_be_used_by(FakeMover(legs=2))


def test_flying_needs_two_wings() -> None:
    assert not Flying().can_be_used_by(FakeMover(wings=1, legs=4))
    assert Flying().can_be_used_by(FakeMover(wings=2))


# ------------------------------------------------- stamina requirements
@pytest.mark.parametrize(
    ("movement", "too_little"),
    [(Hopping(), 19), (Walking(), 39), (Running(), 59), (Flying(), 79)],
)
def test_not_enough_stamina(movement: Movement, too_little: int) -> None:
    rich_body = FakeMover(legs=4, wings=4, stamina=too_little)
    assert not movement.can_be_used_by(rich_body)


def test_cannot_crawl_with_zero_stamina() -> None:
    # Our assumption (open question #1): you can only move if stamina >= cost.
    assert not Crawling().can_be_used_by(FakeMover(stamina=0))
    assert Crawling().can_be_used_by(FakeMover(stamina=1))


# ------------------------------------------------- the registry
def test_default_movements_has_all_five() -> None:
    names = {movement.name for movement in DEFAULT_MOVEMENTS}
    assert names == {"Crawling", "Hopping", "Walking", "Running", "Flying"}
