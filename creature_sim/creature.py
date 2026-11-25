"""characteristics of a creature and it's abilities"""

from collections.abc import Sequence
from dataclasses import dataclass

from creature_sim.movement import Movement
from creature_sim.movement_policy import MovementPolicy
from creature_sim.power import PowerModifier, apply_modifiers


@dataclass(frozen=True)
class Body:
    legs: int = 0
    wings: int = 0
    power_modifiers: tuple[PowerModifier, ...] = ()


@dataclass
class Creature:
    body: Body
    health: int
    stamina: int
    base_power: int
    movement_policy: MovementPolicy
    position: int = 0

    @property
    def legs(self) -> int:
        return self.body.legs

    @property
    def wings(self) -> int:
        return self.body.wings

    @property
    def is_alive(self) -> bool:
        return self.health > 0

    @property
    def attack_power(self) -> int:
        return apply_modifiers(self.base_power, self.body.power_modifiers)

    def try_move(self, movements: Sequence[Movement]) -> bool:
        movement = self.movement_policy.choose(self, movements)
        if movement is None:
            return False

        self.stamina -= movement.cost
        self.position += movement.speed
        return True

    def attack(self, other: "Creature") -> None:
        other.health -= self.attack_power
