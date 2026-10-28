"""Reproduce synthetic maneuver trajectories; no sensor or qualification claims."""
import json

from tools.boat_analysis.evidence.records import output_path, source_hashes
from tools.boat_analysis.model.runtime import analysis_values
from tools.boat_analysis.mission.maneuver import ManeuverDynamics


def run():
    inputs = analysis_values('BlueDog::Analyses::ManeuverDynamics::StudyInputs')
    runs = []
    for interval in inputs['intervalsS']:
        for index, name in enumerate(inputs['names']):
            dynamics = ManeuverDynamics(inputs['initialHeadingDeg'][index],
                                        initial_speed=inputs['initialSpeedMps'][index])
            position = [0., 0.]
            samples = []
            completed = None
            seconds = 0.
            while seconds < inputs['horizonS'] - 1e-9:
                dt = min(interval, inputs['horizonS'] - seconds)
                state = dynamics.step(inputs['targetHeadingDeg'][index],
                                      inputs['targetSpeedMps'][index], dt,
                                      kind=inputs['kinds'][index],
                                      rudder_fraction=inputs['rudderFractions'][index])
                position = [p + (v+c)*dt for p, v, c in
                            zip(position, state['velocity'], inputs['currentMps'])]
                seconds += dt
                if completed is None and not state['turning']:
                    completed = seconds
                samples.append(dict(seconds=seconds, positionM=position[:],
                                    headingDeg=state['headingDeg'], speedMps=state['speedMps']))
            runs.append(dict(name=name, intervalS=interval,
                             headingCompleteS=completed, censored=completed is None,
                             finalPositionM=position, samples=samples))
    record = dict(scope='Synthetic component trajectories with unvalidated coefficients; '
                       'no sensing simulation, route qualification or calibrated IC-01 bound.',
                  qualified=False, inputs=inputs, coefficients=dynamics.coefficients,
                  sourceHashes=source_hashes([
                      'tools/boat_analysis/mission/maneuver.py',
                      'tools/boat_analysis/mission/maneuver_study.py']), runs=runs)
    output_path('maneuver-study.json').write_text(json.dumps(record, indent=2)+'\n')
    envelope = dict(scope='Native encounter timing sensitivities; original traffic '
                          'requirement unchanged; weed cases are separate sensitivities.',
                    qualified=False,
                    outputs=analysis_values('BlueDog::Analyses::EncounterEnvelope::Summary'),
                    sourceHashes=record['sourceHashes'])
    output_path('encounter-envelope.json').write_text(json.dumps(envelope, indent=2)+'\n')
    return record


if __name__ == '__main__':
    result = run()
    for row in result['runs']:
        print(row['name'], row['intervalS'], row['headingCompleteS'], row['finalPositionM'])
