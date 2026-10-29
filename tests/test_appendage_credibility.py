"""Native geometry screens reject loopholes and preserve valid boundary cases."""
import json
import pytest
from tools.boat_analysis.model.runtime import ROOT, native, native_value


def test_native_geometry_boundaries_and_independent_oracle(tmp_path):
    # Chords .2/.1, AR 4/2: separation at arm .5 is .35 m.
    d=[1.,.3,.05,.1,1.,3.,1.,1.,.5,0.,.16,.8,.02,.2,.5,5.,100.,.1,2.,2.,.4,.4,.4,.4,.1,.1,0.,.5,1.5]
    variants=[d.copy() for _ in range(4)]
    variants[1][12:15]=[.092052956586,.08,.516405261684]
    variants[2][14]=.1 # intersects keel sweep
    variants[3][10]=1. # keel chord 1.25 m exceeds hull
    expressions=[]
    for i,x in enumerate(variants):
        vector='('+','.join(map(str,x))+')'
        expressions.append(f'out attribute case{i} : Real [5] ordered nonunique = Analysis::Marine::Appendages::GeometryMargins({vector},2,0.02);')
    path=tmp_path/'geometry.sysml'
    path.write_text('package GeometryTest { private import ScalarValues::*; analysis check { '+''.join(expressions)+' } }')
    model=ROOT/'models/libraries/analysis.sysml'
    report=json.loads(native('-analysis','GeometryTest::check','-json',models=(model,path)))
    assert report['status']=='holds'
    values={v['name']:native_value(v['value']) for v in report['checks'][0]['values']}
    assert values['case0']==pytest.approx([1,0,.8,0,.33])
    assert values['case1'][1]<-.9 and values['case1'][3]<0
    assert values['case2'][4]<0
    assert values['case3'][2]<0


def test_rudder_torque_arm_matches_modeled_stock():
    report=json.loads(native('-analysis','BlueDog::Configurations::OperatingEnvironment::Inputs','-json'))
    values={v['name']:native_value(v['value']) for v in report['checks'][0]['values']}
    assert values['hinge_fraction']==pytest.approx(.25)
