"""Risk publication must preserve unknown likelihood and standard metadata identity."""
from tests.native_cases import native, MODELS


def test_risk_actions_are_published_from_model():
    report = native('-render-document', 'BlueDogRiskDocuments::Actions')
    for number in range(1, 7):
        assert report.count(f'| R-{number:03d} |') == 1
    assert report.count('Open; no residual-risk acceptance recorded') == 6
    assert 'owner reviews disposition' in report
    assert 'coupled loss-of-sensing' in report


def test_standard_risk_metadata_and_unknown_probability(tmp_path):
    source = tmp_path / 'risk-query.sysml'
    source.write_text('''package RiskCheck {
        private import DocumentQueries::*;
        calc def Rows :> Query {
            Project(source = WhereMetadata(source = Descendants(source = Named(qualifiedName = "BlueDogRisks")), 'metadata' = "RiskMetadata::Risk"), columns = (
                Column(name = "Risk", path = "risk.identifier"),
                Column(name = "Likelihood", path = "risk.technicalRisk.probability")))
        }
        part def Report :> Document { attribute redefines title = "Risk metadata test"; part table : Table { calc rows : Rows; } }
    }''', encoding='utf-8')
    report = native('-render-document', 'RiskCheck::Report', models=(*MODELS, source))
    for number in range(1, 7):
        assert f'| R-{number:03d} |  |' in report
