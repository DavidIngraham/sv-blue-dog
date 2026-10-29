import hashlib,json,subprocess
from pathlib import Path
root=Path.cwd();review=root/'reviews/standalone-gorge-challenge'
base=json.loads(Path('/home/david/repos/sv-blue-dog-declarative/.tools/baseline-source.json').read_text())
original=Path(base['source'])
def git(path,*args):return subprocess.check_output(['git','-C',str(path),*args],text=True)
changed=[name for name,sha in base['sourceHashes'].items() if not (original/name).is_file() or hashlib.sha256((original/name).read_bytes()).hexdigest()!=sha]
report=dict(original=str(original),checkedOriginalFiles=len(base['sourceHashes']),changedOriginalFiles=changed,
    originalHeadUnchanged=git(original,'rev-parse','HEAD').strip()==base['sourceHead'],
    originalDirtyStatusUnchanged=git(original,'status','--porcelain=v1','-z').split('\0')==base['sourceStatus'],
    declarativeClean=not git(Path('/home/david/repos/sv-blue-dog-declarative'),'status','--porcelain=v1').strip(),
    namespaceWorktreeClean=not git(Path('/home/david/repos/sv-blue-dog-namespaces'),'status','--porcelain=v1').strip(),
    namespaceHead=git(Path('/home/david/repos/sv-blue-dog-namespaces'),'rev-parse','HEAD').strip(),
    frozenSourceDiff=git(root,'diff','--name-only','e73d456','--','evidence/runs','reviews/declarative-analysis-refactor','reviews/namespace-restructure','reviews/shared-analysis-namespace','experiments/inland-navigation/results.json').splitlines())
report['sharedAnalysisWorktreeClean']=not git(Path('/home/david/repos/sv-blue-dog-analysis-namespaces'),'status','--porcelain=v1').strip()
report['sharedAnalysisHead']=git(Path('/home/david/repos/sv-blue-dog-analysis-namespaces'),'rev-parse','HEAD').strip()
assert report['sharedAnalysisWorktreeClean'] and report['sharedAnalysisHead']=='e73d45624e9eedafc79f22f8559219195e9b313d'
assert not changed and report['originalHeadUnchanged'] and report['originalDirtyStatusUnchanged'] and report['declarativeClean'] and report['namespaceWorktreeClean'] and report['namespaceHead']=='556cd79e266394cae9e9b371a86941f50295cffc' and not report['frozenSourceDiff'],report
(review/'preservation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
