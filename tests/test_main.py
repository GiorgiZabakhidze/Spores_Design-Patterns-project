import pytest

from creature_sim.__main__ import SIMULATION_COUNT, main
from creature_sim.outcome import Outcome


def test_main_runs_all_simulations(capsys: pytest.CaptureFixture[str]) -> None:
    main()
    lines = capsys.readouterr().out.splitlines()
    headers = [line for line in lines if line.startswith("=== Simulation #")]
    messages = {outcome.value for outcome in Outcome}
    outcomes = [line for line in lines if line in messages]
    assert len(headers) == SIMULATION_COUNT
    assert len(outcomes) == SIMULATION_COUNT
