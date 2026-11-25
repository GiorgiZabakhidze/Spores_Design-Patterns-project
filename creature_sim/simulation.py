"""goes through one whole simulation pipeline"""

from creature_sim.chase import ChasePhase
from creature_sim.creature import Creature
from creature_sim.evolution import Evolver
from creature_sim.fight import FightPhase
from creature_sim.outcome import Outcome
from creature_sim.reporting import SimulationReporter


class Simulation:
    def __init__(
        self,
        evolver: Evolver,
        chase: ChasePhase,
        fight: FightPhase,
        reporter: SimulationReporter,
    ) -> None:
        self._evolver = evolver
        self._chase = chase
        self._fight = fight
        self._reporter = reporter

    def run(self, sim_no: int) -> Outcome:
        predator = self._evolver.evolve_predator()
        prey = self._evolver.evolve_prey()
        self._reporter.report_start(sim_no, predator, prey)
        outcome = self._resolve(predator, prey)
        self._reporter.report_outcome(outcome)
        return outcome

    def _resolve(self, predator: Creature, prey: Creature) -> Outcome:
        if self._chase.run(predator, prey):
            return self._fight.run(predator, prey)
        return Outcome.PREY_ESCAPED
