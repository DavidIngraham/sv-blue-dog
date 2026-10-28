"""Ingest recorded bus and target-observation measurements; never invent hardware data."""
import argparse,csv,hashlib,json,math
from pathlib import Path
import numpy as np
from tools.boat_analysis.model.runtime import load_model,analysis_values


def ingest(power_path, observation_path, metadata_path):
    paths=[Path(p) for p in (power_path,observation_path,metadata_path)]
    metadata=json.loads(paths[2].read_text())
    for key in ('installationId','pipelineRevision','conditions','clockBasis','instrument','operator','measuredOn'):
        if not isinstance(metadata.get(key),str) or not metadata[key].strip():raise ValueError('Missing measurement metadata: '+key)
    if metadata.get('measurementBoundary')!='regulated-bus':raise ValueError('Measure the complete declared stack at the regulated bus')
    if metadata.get('evidenceType') not in ('measured','synthetic-test'):raise ValueError('Explicit measured or synthetic-test evidence type required')
    with paths[0].open() as f: power=list(csv.DictReader(f))
    with paths[1].open() as f: observations=list(csv.DictReader(f))
    if len(power)<2 or not observations:raise ValueError('Power interval and target observations required')
    if any(float(row['voltage_v'])<=0 or float(row['current_a'])<0 for row in power):raise ValueError('Positive voltage and nonnegative current required')
    times=np.array([float(row['seconds']) for row in power]);watts=np.array([float(row['voltage_v'])*float(row['current_a']) for row in power])
    if not np.isfinite(times).all() or not np.isfinite(watts).all() or np.any(np.diff(times)<=0) or np.any(watts<0):raise ValueError('Invalid power samples')
    average=float(np.trapezoid(watts,times)/(times[-1]-times[0]))
    latency=[];misses=0;frames=[]
    for row in observations:
        frame=float(row['frame_seconds']);frames.append(frame)
        if not math.isfinite(frame) or not times[0]<=frame<=times[-1]:raise ValueError('Frame outside synchronized power record')
        if row['target_present']!='1':raise ValueError('Only independently confirmed target-present trials belong in this detection cohort')
        if row['detected'] not in ('0','1'):raise ValueError('Detection flag must be 0 or 1')
        if row['detected']=='0':misses+=1;continue
        decision=float(row['decision_seconds'])
        if not math.isfinite(decision) or not frame<=decision<=times[-1]:raise ValueError('Invalid synchronized decision time')
        latency.append(decision-frame)
    if len(set(frames))!=len(frames) or any(b<=a for a,b in zip(frames,frames[1:])):raise ValueError('Ordered distinct frame times required')
    replaced=float(metadata.get('replacedBaseElectronicsW',0))
    base=analysis_values('BlueDog::Analyses::EncounterFeasibility::Inputs')['baselineElectronicsW']
    if not math.isfinite(replaced) or not 0<=replaced<=base:raise ValueError('Replacement exceeds the existing base electronics allocation')
    if replaced and not metadata.get('replacementScope'):raise ValueError('Identify exactly which base functions the measured stack replaces')
    m=load_model()
    increment=float(m.calc('BlueDog::Analyses::EncounterFeasibility::InstalledIncrement',arguments=[average,replaced]).value)
    headroom=float(m.calc('BlueDog::Analyses::EncounterFeasibility::EnergyScreen',arguments=[increment]).value)
    capacity=float(m.calc('BlueDog::Analyses::EncounterFeasibility::CapacityLowerBound',arguments=[increment]).value)
    return dict(metadata=metadata,sourceFiles={str(p.resolve()):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
        averageBusW=average,observedPeakBusW=float(max(watts)),maximumPowerSampleGapS=float(max(np.diff(times))),
        maximumObservedLatencyS=max(latency) if latency else None,latencyP95S=float(np.quantile(latency,.95)) if latency else None,
        targetPresentFrames=len(observations),missedFrames=misses,missFraction=misses/len(observations),
        incrementalBusW=increment,remainingCandidateWh=headroom,fixedPassageCapacityLowerBoundWh=capacity,
        physicalQualification=False,hardwareSelected=False,
        resizingStatus='requires coupled mass, packaging, peak and passage replay; fixed-passage capacity is not a feasible resized design')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--power',required=True);p.add_argument('--observations',required=True);p.add_argument('--metadata',required=True);p.add_argument('--output',required=True)
    a=p.parse_args();result=ingest(a.power,a.observations,a.metadata)
    Path(a.output).write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
