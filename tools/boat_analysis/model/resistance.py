"""Native Delft bare-hull regression adapter with explicit applicability screening."""
from tools.boat_analysis.evidence.records import output_path

import json
from tools.boat_analysis.model.runtime import ROOT
from tools.boat_analysis.evidence.records import digest


def prepare():
    from tools.boat_analysis.model.runtime import load_model, numerical_value
    model=ROOT/'models/libraries/marine/hull-resistance.sysml'
    h=[2,.6,.15,.071973,.85,1.05,1.1,.55,.727]
    speeds=[fn*(9.80665*2)**.5 for fn in [.15,.4,.425,.6,.65]]
    rows=[numerical_value(load_model().calc('MarineResistance::Evaluate',
          arguments=[h, v, 1000.0, 9.80665]).value) for v in speeds]
    hashes={'models/libraries/marine/hull-resistance.sysml':digest(model),'tools/boat_analysis/model/resistance.py':digest(ROOT/'tools/boat_analysis/model/resistance.py')}
    from tools.boat_analysis.generated import HullResistanceResult
    names = tuple(HullResistanceResult.__dataclass_fields__)
    record={'sourceHashes':hashes,'scope':'Synthetic arithmetic fixtures, not measured resistance validation. Fn 0.65 deliberately exceeds the implementation coverage limit. The same native calculation is used by the coupled operating model.','hull':h,'density':1000,'gravity':9.80665,'cases':[{'speed_m_s':v,'outputs':dict(zip(names,r))} for v,r in zip(speeds,rows)],'qualified':False}
    output_path('hull-resistance-audit.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')


def evaluate(hull, speed, density=1000., gravity=9.80665, *, require_domain=True):
    """Evaluate the model and optionally enforce its empirical applicability envelope."""
    from tools.boat_analysis.generated import hull_resistance
    result = hull_resistance(hull=hull, speed=speed, density=density, gravity=gravity)
    if require_domain:
        failures = [name for name, value in result.items()
                    if name.endswith(('_lower', '_upper')) and value < -1e-12]
        if failures:
            raise ValueError('Outside Delft screening envelope: ' + ', '.join(failures))
        if result.resistance_N < 0:
            raise ValueError('Negative residuary regression result; no silent clamp')
    return result


if __name__ == '__main__': prepare()
