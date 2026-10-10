"""Bounded interpolation of the saved OpenVSP inviscid response.

Returns CL, induced CD and pitching moment about midchord. Viscous drag,
stall limits and discrepancy factors belong to the engineering model, not
this adapter. The grid is not an experimentally validated polar.
"""
import json
import numpy as np
from scipy.interpolate import RegularGridInterpolator
from .native_design_kernel import ROOT
from .study_open_sizing import validate

class WingPolar:
    def __init__(self):
        self.path=ROOT/'docs/analysis/wing-polar-grid.json'
        data=json.loads(self.path.read_text());validate(data['driverHashes'])
        rows=[r for r in data['cases'] if not r['reverseChord'] and r['camberScale']>0]
        if {r['cadSha256'] for r in rows}!={json.loads((ROOT/'docs/analysis/wing-geometry.json').read_text())['sha256']}:
            raise ValueError('Polar CAD provenance mismatch')
        self.axes=[np.array(sorted({r[key] for r in rows})) for key in ['aspect','camberScale']]+[np.array(rows[0]['values']['Alpha'])]
        values=np.empty(tuple(len(a) for a in self.axes)+(3,))
        for i,ar in enumerate(self.axes[0]):
            for j,camber in enumerate(self.axes[1]):
                matching=[r for r in rows if r['aspect']==ar and r['camberScale']==camber]
                if len(matching)!=1:raise ValueError('Missing or duplicate polar cell')
                row=matching[0]
                if not np.array_equal(row['values']['Alpha'],self.axes[2]):raise ValueError('Inconsistent incidence grid')
                values[i,j]=np.array([row['values'][key] for key in ['CLtot','CDi','CMytot']]).T
        if not np.isfinite(values).all() or np.min(values[:,:,:,1]) < -1e-10:raise ValueError('Invalid aerodynamic response')
        self.interpolator=RegularGridInterpolator(self.axes,values,bounds_error=True)
    def evaluate(self,aspect,camber,alpha_deg):
        point=np.asarray([aspect,camber,alpha_deg],dtype=float)
        if not np.isfinite(point).all():raise ValueError('Nonfinite aerodynamic input')
        return self.interpolator(point[None])[0]
