"""Check native coverage semantics and a real missing-objective failure."""
import hashlib
import json

import pytest

from tools.boat_analysis.model import audit
from tools.boat_analysis.model.runtime import model_files
from tests.native_edits import replace_unique, set_values


@pytest.fixture(scope='module')
def report():
    return audit.native_audit()


def test_current_coverage_distinguishes_plans_studies_and_future_scope(report):
    assert not report['errors']
    assert not report['diagnostics']
    assert report['summary']['requirements'] == 257
    assert report['summary']['currentWithObjectives'] == report['summary']['current'] == 245
    assert report['summary']['currentRequirements'] == 243
    assert report['summary']['currentStudyObjectives'] == 2
    assert report['summary']['future'] == 12
    assert {i for r in report['coverage'] if r['classification'] == 'study_objective' for i in r['ids']} == {'L-101', 'L-102'}
    assert all(not r['executedByAudit'] and not r['evidenceAcceptanceAssessed'] for r in report['coverage'])
    assert any(not r['verification'] for r in report['coverage'] if r['applicability'] == 'future_only')
    assert all(row['results'] for row in report['impactExamples'])


def test_removing_a_current_verification_objective_is_detected():
    sources = [(str(p), p.read_text()) for p in model_files()]
    needle = 'verify BlueDog::Requirements::roundTrip;'
    assert sum(text.count(needle) for _, text in sources) == 1
    altered = replace_unique(sources,needle,'')
    result = audit.native_audit(altered)
    assert 'Missing current verification objective: BlueDog::Requirements::roundTrip' in result['errors']


def test_unregistered_evidence_is_rejected(tmp_path, monkeypatch):
    directory = tmp_path/'evidence/runs/example'
    directory.mkdir(parents=True)
    (directory/'manifest.json').write_text(json.dumps({'files': {}, 'sourceRevision': 'example'}))
    (directory/'orphan.json').write_text('{}')
    monkeypatch.setattr(audit, 'ROOT', tmp_path)
    with pytest.raises(ValueError, match='Orphaned run JSON'):
        audit.archive_audit()


def test_explicit_current_mission_annotation_does_not_hide_missing_verification():
    sources = [(str(p), p.read_text()) for p in model_files()]
    altered = set_values(sources, {'BlueDog::Mission::Scope::applicability::mission':
                                   'BlueDog::Mission::Scope::MissionKind::gorge'})
    result = audit.native_audit(altered)
    assert result['summary']['future'] == 11
    assert 'Missing current verification objective: GorgeChallenge::repeatedOperation' in result['errors']


def test_manifest_input_artifact_change_is_rejected(tmp_path, monkeypatch):
    original = b'original input\n'
    (tmp_path/'input.json').write_bytes(original)
    monkeypatch.setattr(audit, 'ROOT', tmp_path)
    manifest = {'inputArtifacts': {'input.json': hashlib.sha256(original).hexdigest()}}
    assert audit.manifest_integrity(manifest) == (0, 1)
    (tmp_path/'input.json').write_bytes(original.replace(b'\n', b'\r\n'))
    assert audit.manifest_integrity(manifest) == (0, 1)
    (tmp_path/'input.json').write_bytes(b'altered input\n')
    with pytest.raises(ValueError, match='Archived input artifact mismatch'):
        audit.manifest_integrity(manifest)


def test_challenge_dependencies_stay_independent_and_blue_dog_adopts_them(report):
    dependencies=report['dependencies']
    internal=[r for r in dependencies if r['element']['id'].startswith('GorgeChallenge::')]
    assert internal
    assert all(v['id'].startswith('GorgeChallenge::') for row in internal for cell in row['cells'][:2] for v in cell)
    assert any(any(v['id'].startswith('BlueDog::') for v in row['cells'][0])
               and any(v['id'].startswith('GorgeChallenge::') for v in row['cells'][1])
               for row in dependencies)
