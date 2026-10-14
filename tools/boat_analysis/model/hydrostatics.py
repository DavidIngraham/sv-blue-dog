"""Independent interpreter reference experiments for hydrostatics and actuation."""
from tools.boat_analysis.evidence.records import output_path
from tools.boat_analysis.model.runtime import ROOT
SOURCE = ROOT/'models/analyses/recovery.sysml'

def prepare():
    from tools.boat_analysis.model.runtime import MODELS,native
    models=MODELS+(SOURCE,)
    audit=native('-analysis','BlueDogHydrostatics::analyticExample','-json',models=models)
    output_path('hydrostatics-audit.json').write_text(audit,encoding='utf-8')
    actuator=native('-analysis','BlueDogWingActuator::accountingExample','-json',models=MODELS+(ROOT/'models/vehicle/structure.sysml',ROOT/'models/analyses/actuation.sysml'))
    output_path('wing-actuator-audit.json').write_text(actuator,encoding='utf-8')

if __name__ == '__main__': prepare()
