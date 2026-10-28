"""Prevent stale-input substitution and unsupported interpretation of native analyses."""
import hashlib,json
from pathlib import Path
import pytest
from tools.boat_analysis.evidence import records
from tools.boat_analysis.model.runtime import ROOT,connection,model_files,load_model
from tools.boat_analysis.model.credibility_audit import native_credibility_audit
from tests.native_edits import delete_symbols, set_values, edit_sources


@pytest.fixture
def inputs(tmp_path,monkeypatch):
    work=tmp_path/'build/analysis';work.mkdir(parents=True)
    monkeypatch.setattr(records,'ROOT',tmp_path);monkeypatch.setattr(records,'WORK',work)
    for name in ('source.sysml','driver.py'):(tmp_path/name).write_text(name)
    record={'sourceHashes':{'source.sysml':records.digest(tmp_path/'source.sysml')},
        'driverHashes':{'driver.py':records.digest(tmp_path/'driver.py')}}
    (work/'result.json').write_text(json.dumps(record))
    return tmp_path,work,record


@pytest.mark.parametrize('accessor',(records.input_record,records.input_path))
@pytest.mark.parametrize('field',('sourceHashes','driverHashes'))
def test_both_access_paths_check_both_fingerprints(inputs,accessor,field):
    root,work,record=inputs
    name=next(iter(record[field]));(root/name).write_text('changed')
    with pytest.raises(ValueError,match='Stale'):accessor('result.json')


def test_no_fingerprints_is_not_a_current_result(inputs):
    _,work,_=inputs;(work/'result.json').write_text('{}')
    with pytest.raises(ValueError,match='Unproven'):records.input_record('result.json')


def test_missing_current_record_never_implicitly_uses_archive(inputs,monkeypatch):
    monkeypatch.setattr(records,'baseline_record',lambda name:pytest.fail('Implicit baseline substitution'))
    with pytest.raises(FileNotFoundError,match='Missing current'):records.input_record('missing.json')
    with pytest.raises(FileNotFoundError,match='Missing current'):records.input_path('missing.json')


@pytest.mark.parametrize('purpose,name',(('reference','wing-geometry.json'),('reference','wing-polar-grid.json'),('initial_guess','coupled-fixed-design.json')))
def test_explicit_historical_roles_use_manifest_checked_reader(inputs,monkeypatch,purpose,name):
    calls=[]
    monkeypatch.setattr(records,'baseline_record',lambda n:calls.append(n) or {'scope':'original'})
    assert records.input_record(name,purpose=purpose)=={'scope':'original'}
    assert calls==[name]


@pytest.mark.parametrize('name,purpose',(('coupled-sizing-search.json','reference'),('wing-geometry.json','initial_guess'),('result.json','unknown'),('../result.json','current')))
def test_role_cannot_disguise_current_results_or_wrong_kind(inputs,name,purpose):
    with pytest.raises(ValueError):records.input_record(name,purpose=purpose)


def test_current_valid_record_and_path_agree(inputs):
    _,work,record=inputs
    assert records.input_record('result.json')==record
    assert records.input_path('result.json')==work/'result.json'


def test_native_use_inventory_covers_definitions_and_configured_usages():
    r=native_credibility_audit()
    assert not r['errors'] and not r['diagnostics']
    assert r['summary']['analysisCases']==r['summary']['registeredCases']==110
    assert set(r['summary']['nativeTypes'])=={'AnalysisCaseDefinition','AnalysisCaseUsage'}
    assert r['summary']['useCategories']['HistoricalReview']==13


@pytest.mark.parametrize('mutation',('new_case','nested_case','missing_annotation','missing_domain'))
def test_native_inventory_detects_missing_scope_or_use(mutation):
    sources=[(str(p),p.read_text()) for p in model_files()]
    if mutation=='new_case':sources.append((str(ROOT/'reviews/untagged.sysml'),'package Untagged { analysis sample { out value : ScalarValues::Real = 1; } }'))
    elif mutation=='nested_case':
        sources.append((str(ROOT/'reviews/nested-untagged.sysml'),'package Untagged { package Nested { analysis sample { out value : ScalarValues::Real = 1; } } }'))
    elif mutation=='missing_annotation':
        sources=delete_symbols(sources,'BlueDog::Analyses::AnalysisCredibility::use001')
    else:
        sources=set_values(sources,{'BlueDog::Analyses::AnalysisCredibility::Equipment::domain':'""'})
    assert native_credibility_audit(sources)['errors']


def test_new_nested_typed_analysis_is_registered_without_a_package_list_edit():
    sources=[(str(p),p.read_text()) for p in model_files()]
    owner='BlueDog::Analyses::SyntheticExtension::Nested'
    def extend(editor):
        editor.add_member('BlueDog::Analyses','package','SyntheticExtension')
        editor.add_member('BlueDog::Analyses::SyntheticExtension','package','Nested')
        editor.add_member(owner,'analysis','sample')
        editor.add_member(owner+'::sample','attribute','value',
                          type='ScalarValues::Real',direction='out',value='1')
        editor.add_metadata(owner,'BlueDog::Analyses::AnalysisCredibility::UseIntent',
            name='purpose',about=[owner+'::sample'],values={
                'category':'"Synthetic"',
                'intendedUse':'"Exercise typed inventory discovery."',
                'domain':'"A constant scalar test case."',
                'excludedUses':'"No engineering capability evidence."',
                'evidenceNeeded':'"Software regression only."'})
    result=native_credibility_audit(edit_sources(sources,extend))
    assert not result['errors'] and not result['diagnostics']
    assert result['summary']['analysisCases']==result['summary']['registeredCases']==111
    assert result['summary']['useCategories']['Synthetic']==1
    assert any(row['element']['id']==owner+'::sample' for row in result['table']['rows'])


FLAGS=('intendedUseReviewed','configurationApplicable','domainApplicable','inputPedigreeReviewed','implementationVerified',
    'validationAdequateForUse','uncertaintyReported','sensitivityReviewed','defectsDispositioned','limitationsReported')


@pytest.mark.parametrize('missing',FLAGS)
def test_each_proposed_use_precondition_is_required(missing):
    arguments=[name!=missing for name in FLAGS]
    assert load_model().calc('BlueDog::Analyses::AnalysisCredibility::UsePreconditions',arguments=arguments).value is False


def test_review_preconditions_dont_require_a_passing_design_result():
    assert load_model().calc('BlueDog::Analyses::AnalysisCredibility::UsePreconditions',arguments=[True]*len(FLAGS)).value is True
    with pytest.raises(Exception):load_model().calc('BlueDog::Analyses::AnalysisCredibility::UsePreconditions',arguments=[True]*9)


def test_registered_reference_role_preserves_unchanged_geometry_consumers(inputs,monkeypatch):
    calls=[]
    monkeypatch.setattr(records,'baseline_record',lambda name:calls.append(name) or {'scope':'original'})
    assert records.input_record('wing-geometry.json')=={'scope':'original'}
    assert calls==['wing-geometry.json']
    with pytest.raises(FileNotFoundError,match='Missing current'):
        records.input_record('wing-geometry.json',purpose='current')


def test_use_limitations_are_published_as_native_content(rendered_site):
    page=(rendered_site/'imports/docs/simulation-studies.md').read_text()
    assert 'Analysis purposes, domains and limitations' in page
    assert 'No demonstrated thrust' in page
    assert 'Excluded interpretations' in page
    assert 'sysml-report BlueDogAnalysisDocuments' not in page
