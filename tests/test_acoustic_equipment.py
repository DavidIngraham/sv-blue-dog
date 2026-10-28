"""Native accounting preserves incomplete installations as unsupported."""
import pytest
from tools.boat_analysis.model.runtime import load_model, numerical_value


def test_recorder_allowance_includes_nominal_phantom_supply_once_and_keeps_partial_budget():
    result=numerical_value(load_model().run_analysis('BlueDog::Configurations::AcousticEquipment::Budget').outputs)
    assert result['passiveNominalPhantomSupplyW']==pytest.approx(.2304)
    assert result['passivePlanningRailLowW']==pytest.approx(4.5)
    assert result['passivePlanningBatteryLowW']==pytest.approx(5)
    assert result['passivePlanningBatteryHighW']==pytest.approx(10)
    assert result['passivePlanningMassKg']==pytest.approx(1.01)
    assert result['narrowBeamPlanningMassKg']==pytest.approx(.74)
    assert result['multibeamPlanningMassKg']==pytest.approx(1.05)
    assert result['installedBudgetComplete'] is False
    assert result['physicalQualification'] is False


@pytest.mark.parametrize('candidate',['passiveArray','narrowBeamForward','multibeamForward'])
def test_catalogue_specs_never_supply_observation_or_recovery_acceptance(candidate):
    instance=load_model().instantiate('BlueDog::Configurations::AcousticEquipment::'+candidate)
    for gate in ('detectionRangeDemonstrated','bearingAccuracyDemonstrated','metricRangeDemonstrated',
                 'relativeMotionDemonstrated','latencyDemonstrated','dayNightCoverageDemonstrated',
                 'invertedObservationDemonstrated','independentRecoveryComplete',
                 'installedBudgetComplete','hardwareSelected','physicalQualification'):
        assert getattr(instance,gate) is False,gate
