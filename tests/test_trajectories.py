import pytest
from tools.boat_analysis.environment.trajectories import WeatherHistory


PARAMETERS = (270, 7, .4, 36, .2, .85, .8, .15, .8, .08, .03, 6, 18, 8)


def test_seed_reproduces_history_and_longer_run_preserves_prefix():
    short = WeatherHistory(PARAMETERS, 48, 123)
    repeat = WeatherHistory(PARAMETERS, 48, 123)
    long = WeatherHistory(PARAMETERS, 240, 123)
    assert short.rows == repeat.rows == long.rows[:49]
    assert short.rows != WeatherHistory(PARAMETERS, 48, 124).rows


def test_deterministic_history_has_day_night_and_nonnegative_conditions():
    history = WeatherHistory(PARAMETERS, 24, 1, stochastic=False, departure_hour=0)
    assert history.at(0).solar_fraction == 0
    assert history.at(12*3600).solar_fraction > 0
    assert history.at(23*3600).solar_fraction == 0
    assert all(row.wind_mps == 7 and row.current_mps == .4 for row in history.rows)
    with pytest.raises(ValueError):
        history.at(25*3600)
