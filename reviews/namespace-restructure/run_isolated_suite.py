import json, os, subprocess, time
from pathlib import Path
root=Path.cwd()
out=root/'.tools/namespace-tests';out.mkdir(exist_ok=True)
modules=sorted(root.glob('tests/test_*.py'))+[root/'experiments/inland-navigation/test_navigation.py']
results=[]
for module in modules:
    start=time.monotonic();name=module.stem
    print('START '+str(module.relative_to(root)),flush=True)
    with (out/(name+'.log')).open('w') as log:
        p=subprocess.run([str(root/'.venv/bin/python'),'-m','pytest',str(module.relative_to(root)),'-q','--durations=10','--junitxml='+str(out/(name+'.xml'))],stdout=log,stderr=subprocess.STDOUT,env={**os.environ,'GOMEMLIMIT':'3GiB','GOGC':'50'},timeout=1800)
    row=dict(module=str(module.relative_to(root)),exitCode=p.returncode,seconds=round(time.monotonic()-start,2))
    results.append(row);(out/'results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(row),flush=True)
print('COMPLETE '+str(len(results)),flush=True)

raise SystemExit(int(any(row["exitCode"] for row in results)))
