"""Repeatable virtual mission campaigns; rates and polars remain hypotheses."""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import asdict
import json
from pathlib import Path

import numpy as np
from shapely.geometry import LineString

from tools.boat_analysis.environment.routing import build
from tools.boat_analysis.environment.trajectories import WeatherHistory
from tools.boat_analysis.evidence.records import source_hashes, validate
from tools.boat_analysis.mission.engine import Event, mission_inputs, simulate
from tools.boat_analysis.mission.traffic import Traffic
from tools.boat_analysis.model.runtime import ROOT


def _lines(geometry):
    if geometry.geom_type == 'LineString':
        return [geometry]
    return [line for part in getattr(geometry,'geoms',[]) for line in _lines(part)]


def traffic_scenarios(inputs, route, water, groups, seed):
    """Chart-based transits and local small-craft maneuvers, not AIS replay.

    Rates mean generated appearances across the modeled reach per hour. A
    recommended-track fragment does not imply a complete commercial voyage.
    Independent streams per class preserve prefixes when the horizon changes.
    """
    actors=[]
    streams=np.random.SeedSequence(seed).spawn(len(inputs['trafficNames']))
    for index,(name,stream) in enumerate(zip(inputs['trafficNames'],streams)):
        rng=np.random.default_rng(stream)
        beam=inputs['trafficBeams'][index];length=inputs['trafficLengths'][index]
        domain=water.buffer(-max(beam/2,length/2))
        if index in (0,4):
            # The ENC archive covers a larger reach than the active circuit.
            # Generate commercial appearances only within this route's bounds.
            domain=domain.intersection(route.envelope)
            tracks=[line for candidate in _lines(groups['RECTRC'])
                    for line in _lines(candidate.intersection(domain)) if line.length>length*2]
        else:
            tracks=[]
            # Along-route traffic plus local crossing/trolling/skiing patterns.
            for station in np.linspace(0,route.length,80):
                center=np.array(route.interpolate(station).coords[0])
                tangent=np.array(route.interpolate(min(route.length,station+10)).coords[0])-np.array(route.interpolate(max(0,station-10)).coords[0])
                tangent/=np.linalg.norm(tangent);normal=np.array([-tangent[1],tangent[0]])
                for vector in (tangent,normal):
                    candidate=LineString([center-300*vector,center+300*vector])
                    for line in _lines(candidate.intersection(domain)):
                        if line.length>100:
                            coords=list(line.coords)
                            # Fishing and ski traffic may reverse direction.
                            if index in (1,2):coords=coords+coords[-2::-1]+coords[1:]
                            tracks.append(LineString(coords))
        if not tracks:
            raise ValueError('No chart-contained scenario tracks for '+name)
        rate=inputs['trafficRates'][index]
        if rate<0:raise ValueError('Negative traffic rate')
        if rate==0:continue
        seconds=0.
        while True:
            seconds+=rng.exponential(3600/rate)
            if seconds>=inputs['time'][1]*3600:break
            # Recreation/fishing arrivals restricted to the declared daytime
            # scenario window; commercial traffic can occur at night.
            if index in (1,2,3) and not inputs['weather'][11]<=(inputs['weather'][13]+seconds/3600)%24<=inputs['weather'][12]:continue
            track=tracks[int(rng.integers(len(tracks)))]
            if rng.random()<.5:track=LineString(list(track.coords)[::-1])
            actors.append(Traffic(name,track,float(seconds),inputs['trafficSpeeds'][index],
                                  length,beam,inputs['trafficSeparation'][index]))
    return sorted(actors,key=lambda a:a.start_seconds)


def run(count=32, seed=None, destination=None, candidate=None):
    paths=[p.relative_to(ROOT).as_posix() for folder in ['models','tools/boat_analysis/mission','tools/boat_analysis/environment']
           for p in (ROOT/folder).rglob('*') if p.suffix in ('.py','.sysml')]
    paths+=['evidence/course/2026-10-11/chart-features.geojson','evidence/course/2026-10-11/chart-extraction.json','uv.lock','tools/boat_analysis/model/runtime.py','tools/boat_analysis/model/install.py','tools/boat_analysis/evidence/records.py']
    if candidate:
        candidate=Path(candidate).resolve()
        paths.append(candidate.relative_to(ROOT).as_posix())
    hashes=source_hashes(paths)
    inputs=mission_inputs()
    if candidate:
        from tools.boat_analysis.optimization.search import Problem
        from tools.boat_analysis.mission.candidate import configure
        record=json.loads(candidate.read_text())
        validate(record['sourceHashes'])
        p=Problem();z=np.array(record['smallestFeasibleZ'])
        if not p.feasible(z):raise ValueError('Candidate fails current search screens')
        inputs=configure(inputs,p,p.evaluate(z))
        hashes.update(record['sourceHashes'])
    course,water,groups,gates,route=build()
    seed=int(inputs['time'][5]) if seed is None else seed
    seeds=np.random.SeedSequence(seed).spawn(count)
    records=[]
    for number,stream in enumerate(seeds):
        weather_seed,traffic_seed=stream.generate_state(2).tolist()
        traffic=traffic_scenarios(inputs,route,water,groups,traffic_seed)
        weather=WeatherHistory(inputs['weather'],inputs['time'][1],weather_seed)
        result=simulate(inputs,route,water,gates,weather=weather,traffic=traffic,
                        events=[Event(6*3600,'communications_loss',2*3600)])
        record=asdict(result)
        record.update(index=number,weather_seed=weather_seed,traffic_seed=traffic_seed,
                      generated_traffic=dict(Counter(a.name for a in traffic)))
        records.append(record)
        print(number,result.outcome,result.cause,round(result.elapsed_seconds/3600,2),flush=True)
    validate(hashes)
    report={'sourceHashes':hashes,'seed':seed,'inputs':inputs,'courseInputs':course,
            'oneWayReferenceM':route.length,'equivalentSizingLegM':course['referenceLegLengthM'],'referenceCircuitM':2*course['referenceLegLengthM'],'results':records,
            'outcomes':dict(Counter(r['outcome'] for r in records)),
            'probabilityScope':'Conditional scenario frequencies under uncalibrated weather/traffic hypotheses and conceptual performance; not estimated real mission success probability',
            'evidenceType':'virtual','physicalQualification':False}
    destination=destination or ROOT/'build/analysis/mission-campaign.json'
    Path(destination).parent.mkdir(parents=True,exist_ok=True)
    Path(destination).write_text(json.dumps(report,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--count',type=int,default=32)
    parser.add_argument('--seed',type=int)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--candidate',type=Path)
    args=parser.parse_args()
    if args.count<1:parser.error('count must be positive')
    run(args.count,args.seed,args.output,args.candidate)
