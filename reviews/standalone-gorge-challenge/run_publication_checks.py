import json,os,subprocess,time
from pathlib import Path
root=Path.cwd();out=root/'.tools/gorge-final';out.mkdir(exist_ok=True)
from tools.boat_analysis.model.install import binary_path
python=str(root/'.venv/bin/python');env={**os.environ,'PYTHONPATH':str(root),'GOMEMLIMIT':'3GiB','GOGC':'50','OPENSYSML_BINARY':str(binary_path())}
commands=[
('reusable-runtime',['-m','pytest','packages/sysml-python/tests','-q','--junitxml='+str(out/'reusable-runtime.xml')]),
('projection-recorded',['-m','tools.boat_analysis.evidence.model','--check']),
('projection-current',['-m','tools.boat_analysis.evidence.model','--current','--check']),
('projection-continuation',['-m','tools.boat_analysis.evidence.continuation','2026-10-12-continuation','--check']),
('projection-finite',['-m','tools.boat_analysis.evidence.continuation','2026-10-12-finite-passage','--package','BlueDog::Evidence::FinitePassageSizing','--check']),
('projection-srr',['-m','tools.publishing.srr','--run','2026-10-13-srr-readiness','--check']),
('projection-frontier',['-m','tools.publishing.frontier','--run','2026-10-13-srr-frontier','--check']),
('projection-weather',['-m','tools.boat_analysis.environment.climatology','--check']),
('seeded-campaign',['-m','tools.boat_analysis.mission.campaign','--count','4']),
('sizing-figure',['-m','tools.publishing.sizing_progress']),
('course-map',['-m','tools.publishing.course_map']),
('course-satellite',['-m','tools.publishing.course_satellite']),
('wave-motion',['-m','tools.publishing.wave_motion','evidence/runs/2026-10-13-wave-motion']),
('wave-performance',['-m','tools.publishing.wave_performance','evidence/runs/2026-10-13-wave-performance']),
('publishing',['-m','tools.publishing.build'])]
results=[]
for name,args in commands:
    print('START '+name,flush=True);start=time.monotonic()
    with (out/(name+'.log')).open('w') as log:result=subprocess.run([python,*args],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=1800)
    row=dict(name=name,arguments=args,exitCode=result.returncode,seconds=round(time.monotonic()-start,2));results.append(row)
    (out/'results.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(row),flush=True)
    if result.returncode:raise SystemExit('Failed '+name)
subprocess.run(['git','diff','--exit-code','--','docs/figures'],check=True)
print('PUBLICATION CHECKS COMPLETE',flush=True)
