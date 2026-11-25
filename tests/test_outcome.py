from creature_sim.outcome import Outcome


def test_messages_match_the_assignment() -> None:
    assert Outcome.PREY_ESCAPED.value == "Pray ran into infinity"
    assert Outcome.PREY_KILLED.value == "Some R-rated things have happened"
