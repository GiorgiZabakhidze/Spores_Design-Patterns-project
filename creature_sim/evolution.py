"""evolution logic kickstart and the constants live here"""

from random import Random

from creature_sim.creature import Body, Creature
from creature_sim.movement_policy import MovementPolicy
from creature_sim.power import Claws, ClawSize, PowerModifier, Teeth, TeethSharpness

HEALTH_RANGE = (50, 100)
STAMINA_RANGE = (1, 100)
POWER_RANGE = (1, 10)
LEGS_RANGE = (0, 4)
WINGS_RANGE = (0, 4)
PREDATOR_POSITION = 0
PREY_POSITION_RANGE = (0, 1000)

CLAW_OPTIONS: tuple[Claws | None, ...] = (None, *map(Claws, ClawSize))
TEETH_OPTIONS: tuple[Teeth | None, ...] = (None, *map(Teeth, TeethSharpness))

# by default order, claw comes first to teeth, if u want any other way
#  we just swap these two, or if anything comes up we add one line
# for options above and add that in here as well
POWER_MODIFIER_OPTIONS = (CLAW_OPTIONS, TEETH_OPTIONS)


class Evolver:
    def __init__(self, random_gen: Random, policy: MovementPolicy) -> None:
        self._random_gen = random_gen
        self._policy = policy

    def evolve_predator(self) -> Creature:
        return self._evolve(PREDATOR_POSITION)

    def evolve_prey(self) -> Creature:
        return self._evolve(self._get_random(PREY_POSITION_RANGE))

    def _evolve(self, position: int) -> Creature:
        return Creature(
            body=self._evolve_body(),
            health=self._get_random(HEALTH_RANGE),
            stamina=self._get_random(STAMINA_RANGE),
            base_power=self._get_random(POWER_RANGE),
            movement_policy=self._policy,
            position=position,
        )

    def _evolve_body(self) -> Body:
        return Body(
            legs=self._get_random(LEGS_RANGE),
            wings=self._get_random(WINGS_RANGE),
            power_modifiers=self._evolve_modifiers(),
        )

    def _evolve_modifiers(self) -> tuple[PowerModifier, ...]:
        picks = (self._random_gen.choice(row) for row in POWER_MODIFIER_OPTIONS)
        return tuple(pick for pick in picks if pick is not None)

    def _get_random(self, bounds: tuple[int, int]) -> int:
        return self._random_gen.randint(*bounds)
