"""Compare native semantic projections before and after record normalization."""
import json
import sys
from dataclasses import asdict
from pathlib import Path
from tools.boat_analysis.model.runtime import ROOT, connection, model_files

OUT = Path(__file__).parent
PROJECTION = '''package DecisionMigrationReview {
    private import DocumentQueries::*;
    calc def Records :> Query {
        Project(source = WhereType(source = WhereType(source = Descendants(source = Named(qualifiedName =
            ("BlueDogDesignDecisions", "BlueDogRequirementDecisions", "BlueDogRequirementBasis"))),
            type = "USAGE"), type = ("TYPES")), columns = (
            Column(name="ID", path="qualifiedName"), Column(name="Short ID", path="shortName"),
            Column(name="Disposition", path="disposition"), Column(name="Question", path="question"),
            Column(name="Evidence", path="evidenceNeeded"), Column(name="Owner", path="owner"),
            Column(name="Accepted", path="accepted"), Column(name="Rationale", path="rationale.text"),
            Column(name="Issue", path="issue.text")))
    }
    calc def Links :> Query {
        Project(source = WhereType(source = Descendants(source = Named(qualifiedName =
            ("BlueDogDesignDecisions", "BlueDogRequirementDecisions", "BlueDogRequirementBasis"))),
            type = "Dependency"), columns = (
            Column(name="Client", cell={ in row : KerML::Root::Dependency; row.client }),
            Column(name="Supplier", cell={ in row : KerML::Root::Dependency; row.supplier })))
    }
}'''

def snapshot(after=False):
    projection = PROJECTION.replace('USAGE', 'ItemUsage' if after else 'PartUsage').replace('"TYPES"',
        '"EngineeringDecisions::DecisionRecord"' if after else
        '"BlueDogDesignDecisions::Decision", "BlueDogRequirementDecisions::OpenDecision"')
    sources = tuple((str(p), p.read_text()) for p in (*model_files(), ROOT/'tools/publishing/reference.sysml'))
    m = connection().parse_sources((*sources, (str(OUT/'projection.sysml'), projection)), strict=True)
    names = {'records':'DecisionMigrationReview::Records', 'links':'DecisionMigrationReview::Links',
        'allocations':'BlueDogRequirementBasisDocuments::AllocationClosureRows',
        'working':'BlueDogDecisionDocuments::WorkingRecords', 'open':'BlueDogDecisionDocuments::OpenRecords'}
    tables = {k: asdict(m.run_document_query(v)) for k,v in names.items()}
    return json.loads(json.dumps(tables, default=str))

if __name__ == '__main__':
    if len(sys.argv)!=2 or sys.argv[1] not in ('before','after'):
        raise SystemExit('Choose before (original capture only) or after (preservation check).')
    after = sys.argv[-1] == 'after'
    if not after and (OUT/'preserved-before.json').exists():
        raise FileExistsError('The original native baseline must not be overwritten.')
    current = snapshot(after)
    (OUT / ('preserved-after.json' if after else 'preserved-before.json')).write_text(json.dumps(current, indent=2)+'\n')
    if after:
        previous = json.loads((OUT/'preserved-before.json').read_text())
        for name in previous:
            # Native row element kinds change PartUsage -> ItemUsage, but IDs,
            # projected values, short IDs and resolved dependency endpoints must not.
            record_ids = {r['element']['id'] for r in current['records']['rows']}
            def normalize(value):
                if isinstance(value, list):
                    return [normalize(v) for v in value]
                if isinstance(value, dict):
                    return {k: ('RecordUsage' if k == 'type' and value.get('id') in record_ids
                        and v in ('PartUsage', 'ItemUsage') else normalize(v)) for k,v in value.items()}
                return value
            old = {r['element']['id']:normalize(r['cells']) for r in previous[name]['rows']}
            new = {r['element']['id']:normalize(r['cells']) for r in current[name]['rows']}
            assert old == new, name
        print('Preserved native record values, questions, IDs, rationale, issues, dependency endpoints, 14 contexts and 80 allocation reviews.')
    print({name:len(table['rows']) for name,table in current.items()})
