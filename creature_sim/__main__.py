"""run 100 simulations"""

from random import Random

from creature_sim.chase import ChasePhase
from creature_sim.evolution import Evolver
from creature_sim.fight import FightPhase
from creature_sim.movement import DEFAULT_MOVEMENTS
from creature_sim.movement_policy import GreedyMovementPolicy
from creature_sim.reporting import ConsoleReporter
from creature_sim.simulation import Simulation

SIMULATION_COUNT = 100


def build_simulation() -> Simulation:
    evolver = Evolver(Random(), GreedyMovementPolicy())
    return Simulation(
        evolver, ChasePhase(DEFAULT_MOVEMENTS), FightPhase(), ConsoleReporter()
    )


def main() -> None:
    simulation = build_simulation()
    for sim_no in range(1, SIMULATION_COUNT + 1):
        simulation.run(sim_no)


if __name__ == "__main__":
    main()
