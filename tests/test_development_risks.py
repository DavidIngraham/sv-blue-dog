"""Risk publication must preserve unknown likelihood and standard metadata identity."""
from tests.native_cases import native, MODELS


def test_risk_actions_are_published_from_model():
    report = native('-render-document', 'BlueDogRiskDocuments::Actions')
    for number in range(1, 7):
        assert report.count(f'| R-{number:03d} |') == 1
    assert report.count('No residual-risk acceptance recorded.') == 6
    assert 'owner reviews disposition' in report
    assert 'coupled loss-of-sensing' in report


def test_standard_risk_metadata_and_unknown_probability(tmp_path):
    source = tmp_path / 'risk-query.sysml'
    source.write_text('''package RiskCheck {
        private import DocumentQueries::*;
        calc def Rows :> Query {
            Project(source = WhereMetadata(source = Descendants(source = Named(qualifiedName = "BlueDog::Analyses::DevelopmentRisks")), 'metadata' = "RiskMetadata::Risk"), columns = (
                Column(name = "Risk", path = "risk.identifier"),
                Column(name = "Likelihood", path = "risk.technicalRisk.probability")))
        }
        part def Report :> Document { attribute redefines title = "Risk metadata test"; part table : Table { calc rows : Rows; } }
    }''', encoding='utf-8')
    report = native('-render-document', 'RiskCheck::Report', models=(*MODELS, source))
    for number in range(1, 7):
        assert f'| R-{number:03d} |  |' in report


def test_assessment_basis_and_evidence_are_published():
    report = native('-render-document', 'BlueDogRiskDocuments::Assessments')
    for number in range(1, 7):
        assert report.count(f'| R-{number:03d} |') == 1
    from tools.boat_analysis.evidence.records import ROOT,run_record
    candidate=run_record(ROOT/'evidence/runs/2026-10-15-integrated-candidate','integrated-sizing.json')
    headroom=100*candidate['replay']['concept']['voyageEnergyMargin']
    assert f'{headroom:.3f} Wh' in report
    assert 'integrated-candidate/integrated-mission.json' in report
    assert 'wave-performance/summary.json' in report
    assert 'Possible' in report and 'Demonstrated' in report
    assert 'Low' in report and 'High' in report
