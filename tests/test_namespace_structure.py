"""Project namespace ownership is real native model structure."""
from tools.boat_analysis.model.runtime import ROOT,load_model,model_files
from tools.boat_analysis.studies.config import load_study
from tools.boat_analysis.studies.runner import resolve_selector


def test_project_has_one_native_root_and_reusable_libraries_remain_separate():
    files=model_files()
    project=[path for path in files if not path.is_relative_to(ROOT/'models/libraries')]
    assert project==[ROOT/'models/blue-dog.sysml']
    model=load_model()
    roots=dict(zip(model.documents,model.roots,strict=True))
    project_packages=[child for child in roots[str(project[0])].children() if child.kind=='package']
    assert [package.id for package in project_packages]==['BlueDog']
    for path in files:
        if path.is_relative_to(ROOT/'models/libraries'):
            packages=[child for child in roots[str(path)].children() if child.kind=='package']
            assert packages
            assert all(not package.id.startswith('BlueDog') for package in packages)


def test_engineering_areas_are_owned_packages_with_canonical_identities():
    model=load_model()
    packages=model.query(scope=['BlueDog'],select=['owner'],where={
        '@type':'PrimitiveConstraint','operator':'=','property':'@type','value':['Package']})
    owned={row.id for row in packages if row.get('owner')=='BlueDog'}
    expected={'BlueDog::'+name for name in ('Mission','Requirements','Architecture','Behavior',
        'Analyses','Configurations','Decisions','Verification','Evidence')}
    assert expected<=owned
    for identifier in expected:
        assert model.get(identifier).id==identifier
    assert model.get('BlueDogIntegratedCandidate') is None
    assert model.get('BlueDogRequirements') is None
    assert model.get('BlueDog::Analyses::IntegratedCandidate::RecoveryScreen') is not None
    assert model.get('BlueDog::Configurations::IC01::design') is not None


def test_real_studies_bind_canonical_owned_elements_without_alias_facades():
    model=load_model()
    for name in ('recovery.yaml','sail-trade.yaml','recovery-scenarios.yaml'):
        config=load_study(ROOT/'examples/studies'/name)
        for group in config.groups:
            for identifier in resolve_selector(model,group.select):
                assert identifier.startswith('BlueDog::Analyses::')
                assert model.get(identifier).id==identifier
            if group.subject:
                subject,=resolve_selector(model,group.subject)
                assert subject.startswith('BlueDog::Configurations::')
