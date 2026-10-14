"""Blue Dog generated native calculation regressions."""
import numpy as np
import pytest


def test_real_operation_batch_matches_scalar():
    from tools.boat_analysis.generated import operation
    from tools.boat_analysis.evidence.records import input_record
    k = operation
    d, p, _, state, aero, mass, hydro = input_record('coupled-operation-audit.json')['inputs']
    states = np.tile(state, (5, 1)); states[:, 3] = np.linspace(1, 3, 5)
    shared = dict(design=d, parameters=p, aero=aero, mass=mass, hydro=hydro)
    result = k.batch(shared=shared, cases={'state': states}, chunk_size=2)
    expected = [list(k(**shared, state=s).values()) for s in states]
    np.testing.assert_allclose(result.values, expected, rtol=1e-13)
    states[2, 3] = 0
    with pytest.raises(ValueError, match='case 2'):
        k.batch(shared=shared, cases={'state': states})


@pytest.mark.parametrize('name,inputs', [
    ('StripLoad', [[1.2, 2, 0, 5, 0, 3, 1, .1, .5, .2], [1.2, 2, 0, 6, 0, 3, 1, .1, .5, .2]]),
    ('SpeedRetention', [[0, 10], [20, 10]]),
    ('WindSample', [[10, 10, .0002, 1, 0, 0, 0, 1, .05], [10, 10, .0002, 2, 0, 0, 0, 1, .05]])])
def test_real_surface_output_types(name, inputs):
    from tools.boat_analysis import generated
    export={'StripLoad':'strip_load','SpeedRetention':'speed_retention','WindSample':'wind_sample'}[name]
    calculation=getattr(generated,export)
    expected=np.array([calculation(x=v).as_array() for v in inputs])
    actual=calculation.batch(shared={},cases={'x':inputs})
    np.testing.assert_allclose(actual.values,expected,rtol=1e-14)


def test_generated_runtime_recovers_after_a_failed_row():
    from tools.boat_analysis.generated import strip_load as k
    valid = [1.2, 2, 0, 5, 0, 3, 1, .1, .5, .2]
    invalid = valid.copy(); invalid[3] = 0  # zero apparent speed: division by zero
    result = k.batch(shared={}, cases={'x': [valid, invalid, valid]}, errors='collect')
    assert result.errors[0] is None and result.errors[1] and result.errors[2] is None
    assert np.isnan(result.values[1]).all()
    np.testing.assert_array_equal(result.values[0], result.values[2])
    np.testing.assert_array_equal(k(x=valid).as_array(), result.values[0])
