from creature_sim.__main__ import SIMULATION_COUNT


def test_runs_one_hundred_simulations() -> None:
    assert SIMULATION_COUNT == 100
