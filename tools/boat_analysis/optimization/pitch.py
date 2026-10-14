"""Resolve missing recovery samples with a denser, full-pitch root search.

This supplemental static diagnostic does not establish a dynamic recovery path.
"""
from tools.boat_analysis.evidence.records import input_record, input_path, output_path, source_hashes

import json
import numpy as np
from scipy.optimize import brentq
from tools.boat_analysis.model.vessel import CoupledModel
from tools.boat_analysis.model.hydrostatic_mesh import equilibrium
from tools.boat_analysis.model.runtime import ROOT
from tools.boat_analysis.evidence.records import digest,validate


def roots_at_roll(model,bodies,cg,mass,heel,density):
    cache={}
    def state(pitch):
        key=float(pitch)
        if key not in cache:cache[key]=equilibrium(model.hydro,bodies,cg,mass,heel,key,density)
        return cache[key]
    def residual(pitch):return state(pitch)['pitch_torque_Nm']
    nodes=np.linspace(-180,180,145)
    roots=[]
    for a,b in zip(nodes,nodes[1:]):
        fa,fb=residual(a),residual(b)
        if abs(fa)<1e-8:roots.append(float(a))
        if fa*fb<0:roots.append(float(brentq(residual,a,b,xtol=1e-8)))
    rows=[]
    for pitch in sorted(set(round(v,8) for v in roots)):
        r=dict(state(pitch))
        r['pitch_stable']=(residual(pitch+.001)-residual(pitch-.001))/.002<0
        r['righting_Nm']=-r['roll_torque_Nm']*float(np.cos(np.deg2rad(pitch)))
        rows.append(r)
    return rows


def run():
    saved=input_record('coupled-recovery.json')
    model=CoupledModel();x=[saved['design'][n] for n in model.c['designNames']]
    sources=['build/analysis/coupled-recovery.json','tools/boat_analysis/optimization/pitch.py','tools/boat_analysis/geometry/hydro.py','tools/boat_analysis/model/vessel.py']
    hashes=source_hashes(sources);rows=[]
    for c in saved['cases']:
        missing=[p for p in c['points'] if 'failure' in p]
        if not missing:continue
        if c['wing_state']!='sealed':raise ValueError('This diagnostic currently covers sealed-wing cases only')
        bodies,m,_,_=model.configuration(x,np.deg2rad(c['mast_trim_deg']),resolution=16)
        cg=[m['cgX'],m['cgY'],m['cgZ']]
        for p in missing:
            roots=roots_at_roll(model,bodies,cg,m['totalMass'],p['heel_deg'],c['density_kg_m3'])
            rows.append({'density_kg_m3':c['density_kg_m3'],'mast_trim_deg':c['mast_trim_deg'],'heel_deg':p['heel_deg'],'originalFailure':p['failure'],'roots':roots})
            print('PITCH',c['density_kg_m3'],p['heel_deg'],[(r['pitch_deg'],r['pitch_stable']) for r in roots],flush=True)
    validate(hashes)
    report={'sourceHashes':hashes,'qualified':False,'pitchRange_deg':[-180,180],'bracketStep_deg':2.5,'cases':rows,'scope':'Supplemental static root search for missing sealed-wing recovery samples. A finite sign-change grid may still miss tangent roots. Euler-angle coordinates near vertical pitch do not prove a continuous recovery path or global three-dimensional stability.'}
    output_path('coupled-pitch-diagnostic.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n',encoding='utf-8')


if __name__=='__main__':run()
