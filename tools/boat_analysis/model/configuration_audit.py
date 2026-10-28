"""Native configuration identity and resource-accounting scope audit."""
from dataclasses import asdict
import hashlib,json
from pathlib import Path
from .runtime import ROOT,connection,model_files
from .install import REVISION


def native_configuration_audit(sources=None):
    sources=tuple(sources) if sources is not None else tuple((str(p),p.read_text()) for p in model_files())
    q=ROOT/'tools/publishing/reference.sysml'
    m=connection().parse_sources((*sources,(str(q),q.read_text())),strict=True)
    tables={n:m.run_document_query('BlueDogConfigurationDocuments::'+n) for n in ('Contexts','Installation','Scopes','Allocations')}
    errors=[]
    expected={'currentCandidate':'BlueDog::Configurations::IC01::design','retainedSizing':'BlueDog::Evidence::SRRCurrent::candidate',
        'illustrativeLoads':'BlueDog::Configurations::Examples::Energy::sailing'}
    contexts={r.element.id.rsplit('::',1)[-1]:r for r in tables['Contexts']}
    for name,subject in expected.items():
        row=contexts.get(name)
        if row is None:errors.append('C01 Missing configuration context: '+name);continue
        if any(not c or c==('',) for c in (*row.cells[:2],*row.cells[3:])):
            errors.append('C01 Incomplete configuration context: '+row.element.id)
        if [x.id for x in row.cells[2]]!=[subject]:errors.append('C02 Wrong represented subject: '+row.element.id)
    for row in contexts.values():
        if any(not c or c==('',) for c in (*row.cells[:2],*row.cells[3:])):
            errors.append('C01 Incomplete configuration context: '+row.element.id)
    roots=sorted({child.id for root in m.roots for child in root.children()})
    def eq(key,values):return {'@type':'PrimitiveConstraint','property':key,'operator':'=','value':values}
    occurrences=m.query(scope=roots,select=['owner','type'],where={'@type':'CompositeConstraint',
        'operator':'and','constraint':[eq('@type',['PartUsage']),eq('type',['MarineDesign::Design','MarineDesign::Parameters'])]})
    # Namespace depth is organizational. Independent design/parameter usages
    # are owned by native packages, including deeply nested project namespaces;
    # usages inside parts/definitions remain contextual references.
    package_ids={row.id for row in m.query(scope=roots,select=[],where=eq('@type',['Package']))}
    top_design_parts=[r for r in occurrences if r.get('owner') in package_ids]
    represented={x.id for row in contexts.values() for x in row.cells[2]}
    for row in top_design_parts:
        if row.id not in represented:errors.append('C02 Unclassified top-level design/parameter part: '+row.id)
    for row in tables['Installation']:
        for i,expected_id in enumerate(('BlueDog::Configurations::IC01::design','BlueDog::Architecture::Physical::ic01')):
            if [x.id for x in row.cells[i]]!=[expected_id]:errors.append('C04 Wrong planned installation reference: '+row.element.id)
    for row in tables['Scopes']:
        if [x.id for x in row.cells[2]]!=['BlueDog::Configurations::IC01::design']:errors.append('C07 Wrong accounting configuration: '+row.element.id)
        if any(not c or c==('',) for i,c in enumerate(row.cells[:-1]) if i!=2):
            errors.append('C07 Incomplete accounting context: '+row.element.id)
        if m.eval(row.element.id+'.quantitiesValid') is not True:
            errors.append('C07 Invalid allocated quantity: '+row.element.id)
    # Native equality checks the documented owner relationship, without reimplementing rollup equations.
    owner_bindings={
        'ic01.mainStorage.nameplateEnergy':'BlueDog::Configurations::IC01::design.battery_Wh * 3600 [J]',
        'ic01.mainStorage.departureEnergy':'BlueDog::Configurations::Management::ic01.mainStorage.nameplateEnergy * BlueDog::Configurations::OperatingEnvironment::Inputs.usable_fraction * BlueDog::Configurations::OperatingEnvironment::Inputs.initial_fraction',
        'ic01.fixedEquipment.massAllocation':'BlueDog::Configurations::IC01::integration.fixedEquipmentKg * 1 [kg]',
        'ic01.sailingElectronics.averagePowerAllocation':'BlueDog::Configurations::IC01::integration.electronicsW * 1 [W]',
        'ic01.recoveryEssentials.averagePowerAllocation':'BlueDog::Configurations::IC01::integration.recoveryEssentialW * 1 [W]',
        'ic01.recoveryStorage.nameplateEnergy':'BlueDog::Configurations::IC01::integration.recoveryBatteryWh * 3600 [J]',
        'ic01.recoveryStorage.departureEnergy':'BlueDog::Configurations::IC01::integration.recoveryDepartureWh * 3600 [J]',
        'ic01.responseTiming.acquisitionLatency':'BlueDog::Configurations::IC01::integration.sensorLatencyS * 1 [s]',
        'ic01.responseTiming.assessmentLatency':'BlueDog::Configurations::IC01::integration.assessmentS * 1 [s]',
        'ic01.responseTiming.commandLatency':'BlueDog::Configurations::IC01::integration.commandS * 1 [s]',
        'ic01.responseTiming.maneuverDuration':'BlueDog::Configurations::IC01::integration.maneuverS * 1 [s]'}
    for feature,owner in owner_bindings.items():
        if m.eval('BlueDog::Configurations::Management::'+feature+' == '+owner,context_symbol_id='BlueDog::Configurations::Management') is not True:
            errors.append('C10 Accounting binding differs from its declared owner: '+feature)
    review=m.run_analysis('BlueDog::Configurations::Management::AccountingReview',subject='BlueDog::Configurations::Management::ic01').outputs
    open_installation=[name for name,cell in zip(tables['Installation'].columns[2:7],tables['Installation'].rows[0].cells[2:7]) if not cell]
    open_quantities=[dict(scope=r.element.id,missingPeak=not bool(r.cells[3])) for r in tables['Allocations'] if r.cells[2]]
    return dict(runtimeRevision=REVISION,modelHash=m.hash,
        sourceHashes={str(Path(p).relative_to(ROOT)):hashlib.sha256(t.encode()).hexdigest() for p,t in sources},
        auditSources={str(p.relative_to(ROOT)):hashlib.sha256(p.read_text().encode()).hexdigest() for p in (q,Path(__file__))},
        diagnostics=[str(d) for d in m.diagnostics],errors=errors,review=review,
        summary=dict(configurationContexts=len(contexts),accountingScopes=len(tables['Scopes'].rows),topLevelDesignParameterParts=len(top_design_parts)),
        missingInstallationRecords=open_installation,unboundedPowerPeaks=open_quantities,
        openRequiredQuantities=[r.element.id for r in tables['Scopes'] if m.eval(r.element.id+'.requiredQuantitiesPresent') is not True],
        designOccurrences=[dict(id=r.id,properties=r.properties,topLevel=r in top_design_parts) for r in occurrences],
        tables={n:asdict(t) for n,t in tables.items()},
        interpretation='Native context and bound-quantity inventory, not a complete installed BOM, measured budget, '
        'functional coverage proof or configuration acceptance. Blank quantities are not zero; row boundaries govern aggregation.')


def main():
    import argparse
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path);a=p.parse_args()
    r=native_configuration_audit()
    if a.output:a.output.write_text(json.dumps(r,default=str,indent=2)+'\n')
    print(json.dumps({k:r[k] for k in ('summary','review','errors','diagnostics','missingInstallationRecords','unboundedPowerPeaks')},indent=2))
    raise SystemExit(bool(r['errors'] or r['diagnostics']))


if __name__=='__main__':main()
