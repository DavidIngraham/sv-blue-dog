"""Independent interpreter reference experiments for hydrostatics and actuation."""
from tools.boat_analysis.evidence.records import output_path
from tools.boat_analysis.model.runtime import ROOT
SOURCE = ROOT/'models/blue-dog.sysml'

def prepare():
    from tools.boat_analysis.model.runtime import MODELS,native
    models=MODELS+(SOURCE,)
    audit=native('-analysis','BlueDog::Analyses::Hydrostatics::analyticExample','-json',models=models)
    output_path('hydrostatics-audit.json').write_text(audit,encoding='utf-8')
    actuator=native('-analysis','BlueDog::Analyses::WingActuator::accountingExample','-json',models=MODELS+(ROOT/'models/blue-dog.sysml',ROOT/'models/blue-dog.sysml'))
    output_path('wing-actuator-audit.json').write_text(actuator,encoding='utf-8')

if __name__ == '__main__': prepare()
