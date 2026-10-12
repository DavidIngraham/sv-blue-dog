import numpy as np
import pytest
from tools.boat_analysis.mission.candidate import Performance


def test_velocity_envelope_interpolation_and_no_extrapolation():
    p=Performance({'winds':[5,8], 'velocities':[[[0,0],[1,1],[1,-1],[-1,1],[-1,-1]],[[0,0],[2,2],[2,-2],[-2,2],[-2,-2]]]})
    assert p.speeds(5,0)==pytest.approx(1)
    assert p.speeds(6.5,90)==pytest.approx(1.5)
    assert p.speeds(8,45)==pytest.approx(2*np.sqrt(2))
    assert np.array_equal(p.speeds(4,np.array([0,90,180])),[0,0,0])
    assert p.speeds(9,0)==0


def test_native_passage_energy_and_packaging_oracle():
    import sys
    if sys.platform!='linux':pytest.skip('Native adapter requires GCC')
    from tools.boat_analysis.model.operating import ConceptKernel
    k=ConceptKernel()
    d=np.ones(29);d[16]=400
    m=np.ones(21);m[13]=.01
    g=np.ones(60);g[4]=.05
    k.contract['environment']=[0.]*24
    q=k.contract['environment'];q[14]=.8;q[15]=.8;q[16]=.9;q[19]=.1;q[22]=20
    r=k.evaluate(d,m,g,20,8,policy=[1.25,6,200000,500,.5])
    assert r['passageHours']==31
    assert r['departureWh']==288
    assert r['requiredWh']==pytest.approx(333.1)
    assert r['voyageEnergyMargin']==pytest.approx(-.451)
    assert r['batteryVolumeM3']==.002
    assert r['equipmentVolumeM3']==.006
    assert r['availableVolumeM3']==.02
    assert r['installationVolumeMargin']==pytest.approx(1.2)
    d[16]=500
    assert k.evaluate(d,m,g,20,8,policy=[1.25,6,200000,500,.5])['voyageEnergyMargin']>0


def test_candidate_storage_uses_net_bus_power_and_reports_missing_coverage():
    from shapely.geometry import LineString,box
    from tools.boat_analysis.mission.engine import simulate
    inputs={'controlPeriodSeconds':10,'gateNames':['eastGate'],'gateDirections':[1],
            'gateApproachM':20,'time':[10,10/3600,10,20,0,1],
            'energy':[100,80,10,10,0,0,.8,.5],
            'storage':{'selfDischargeW':1,'maxChargeW':5},
            'dimensions':[2,.5,3],'weather':[270,7,0,36,.2,.85,0,.15,.8,.08,0,6,18,8],
            'performance':{'winds':[3,4],'velocities':[[[1,1],[1,-1],[-1,1],[-1,-1]]]*2,'scope':'test'},
            'angles':[0,180],'speedRatios':[0,0]}
    route=LineString([(0,0),(-100,0)]);water=box(-200,-100,100,100)
    gates={'eastGate':LineString([(0,-100),(0,100)])}
    result=simulate(inputs,route,water,gates,save_every=1,classify=lambda *facts:'censored')
    assert result.outside_performance_coverage_seconds==10
    assert result.minimum_energy_wh==pytest.approx(80-21*10/3600)
