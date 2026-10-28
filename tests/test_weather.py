"""Weather evidence integrity, missing data and non-concealment of failed routes."""
from datetime import datetime, timedelta
import hashlib
import json

import pytest

from tools.boat_analysis.environment.climatology import DIRECTORY, aggregate, classify, observations, policy
from tools.boat_analysis.model.runtime import ROOT, native_value


@pytest.fixture(scope='module')
def weather_policy():
    return policy()


def test_from_direction_and_missing_wind(weather_policy):
    p = weather_policy
    assert classify(270, 50, p) == 'west'
    assert classify(90, 50, p) == 'east'
    assert classify(360, 50, p) == 'other'
    assert classify(-9999, 10, p) == 'light'
    assert classify(-9999, 50, p) == 'unknown'
    assert classify(90, -9999, p) == 'unknown'
    assert classify(45, 20, p) == 'east'
    assert classify(225, 20, p) == 'west'


def test_window_selection_does_not_peek_and_gaps_are_not_success(weather_policy):
    p = dict(weather_policy, firstYear=2024, lastYear=2024)
    start = datetime(2024, 6, 1)
    records = {start+timedelta(hours=i):'west' for i in range(100)}
    records[start+timedelta(hours=60)] = 'east'
    rows = aggregate(records, p)
    row = next(r for r in rows if r['season']=='warm')
    # Launches at 6..28 have complete futures, all containing the later easterly.
    assert row['selectedWindows'] == 23
    assert row['windowsWithEast'] == 23
    assert row['incompleteWindows'] > 0
    assert sum(row[k+'Hours'] for k in ('west','east','light','other','unknown')) == row['expectedHours']


def test_frozen_archive_matches_native_projection(weather_policy):
    from tools.boat_analysis.environment.climatology import STATIONS
    manifest = json.loads((DIRECTORY/'manifest.json').read_text())
    assert len(manifest['sources']) == 20
    for item in manifest['sources']:
        assert hashlib.sha256((DIRECTORY/item['file']).read_bytes()).hexdigest() == item['sha256']
    from tools.boat_analysis.evidence.projection import read_projection
    projection = read_projection('gorge-wind')
    for name, station in STATIONS.items():
        records = {}
        for year in range(weather_policy['firstYear'], weather_policy['lastYear']+1):
            records.update(observations(DIRECTORY/f'{station}-{year}.gz',weather_policy))
        for row in aggregate(records, weather_policy):
            body = projection.split(f'part {name}_{row["season"]} :',1)[1].split('}',1)[0]
            for key, value in row.items():
                assert f'attribute :>> {key} = {json.dumps(value)};' in body


def test_native_probability_does_not_average_failed_duration(run_model):
    source = '''package WeatherRegression {
      private import ScalarValues::*;
      analysis check {
        out attribute coverage : Real = MarineWeather::TwoRegimeCoverage(0.25,true,false);
        out attribute duration : Real = MarineWeather::ConditionalPassageHours(0.25,true,false,48,1000000);
        out attribute none : Real = MarineWeather::TwoRegimeCoverage(1,true,false);
        out attribute emptyDuration : Real = MarineWeather::ConditionalPassageHours(1,true,false,48,1000000);
        out attribute bothDuration : Real = MarineWeather::ConditionalPassageHours(0.25,true,true,48,68);
      }
    }'''
    code, report = run_model(source, '-analysis','WeatherRegression::check')
    assert code == 0
    values = {v['name']:native_value(v['value']) for v in report['checks'][0]['values']}
    assert values == dict(coverage=.75,duration=48,none=0,emptyDuration=0,bothDuration=53)


def test_profiles_keep_safety_constraints_and_report_east():
    import sys
    if sys.platform != 'linux':pytest.skip('Compiled Linux/GCC kernels')
    import numpy as np
    from tools.boat_analysis.optimization.search import Problem
    challenge, annual = Problem(4,'challenge'), Problem(4,'all-season')
    z = challenge.initial()
    a, b = challenge.evaluate(z), annual.evaluate(z)
    assert not challenge.require_east and annual.require_east
    extra = set(annual.constraint_names)-set(challenge.constraint_names)
    assert extra == {'easterly downstream progress','easterly upstream progress','easterly duration'}
    for i,name in enumerate(challenge.constraint_names):
        if name=='voyageEnergyMargin':
            # Requiring both directions uses the longer passage for storage.
            assert b['ineq'][annual.constraint_names.index(name)] <= a['ineq'][i]
            assert b['concept']['passageHours'] >= a['concept']['passageHours']
            continue
        assert a['ineq'][i] == pytest.approx(b['ineq'][annual.constraint_names.index(name)])
    np.testing.assert_allclose(a['route'],b['route'])
    np.testing.assert_allclose(a['westerlyRoute'],b['westerlyRoute'])
