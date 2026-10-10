"""Publish the current resistance implementation and geometry applicability result."""
import json
from .native_design_kernel import ROOT
from .study_open_sizing import validate


def publication():
    r=json.loads((ROOT/'docs/analysis/hull-resistance-domain.json').read_text(encoding='utf-8'));validate(r['sourceHashes'])
    lines=['# Hull resistance','',
    '**The coupled search still uses its earlier wave-drag approximation. The replacement below is implemented and checked independently; geometry integration and a new optimization remain outstanding.**','',
    'The native [SysML calculation](../models/hull-resistance.sysml) implements equation 1.7 and table 2 of [Keuning and Katgert (2008)](https://www.scribd.com/document/346520042/Keuning-2008-pdf). It calculates upright, untrimmed bare-hull residuary resistance. Viscous hull drag and appendage drag must be added separately. Linear interpolation between published Froude-number rows is our implementation choice.','',
    'The adapter rejects negative resistance and coordinates outside the table-1 envelope. Those coordinate bounds are only necessary screens: they do not establish support for every combination inside the box. We restrict use to Froude numbers 0.15–0.60 because higher-speed regressions contain fewer tested hulls. This is an analysis applicability limit, not a vessel requirement or proof of physical infeasibility.','',
    '## Current hull geometry','',
    'The audit extracts static upright canoe-body waterline, displacement, waterplane, buoyancy/flotation centers and section coefficients from the actual convex hull mesh. Appendage displacement is excluded from the regression inputs. Native immersed-volume calculations independently check the extracted volume. Mast trim and pitch are fixed at zero for this diagnostic.','',
    '| Design | Waterline (m) | Beam/waterline | Prismatic coefficient | Midship coefficient | Outside screening envelope |','|---|---:|---:|---:|---:|---|']
    for c in r['cases']:
        h=c['hullFeatures'];lines.append(f"| {c['case']} | {h[0]:.3f} | {h[1]/h[0]:.3f} | {h[7]:.3f} | {h[8]:.3f} | {', '.join(c['outsideEnvelope'])} |")
    lines+=['','The original two-metre family also misses the prismatic-coefficient screen. Replacing the equation alone would therefore be insufficient. The next geometry revision must allow longitudinal fullness to vary, then recompute these coordinates from the loaded hull before feasibility and length minimization. The previous 0.8 m candidate remains an invalid minimum-size conclusion.','',
    '## Reproduction and evidence','',
    'Export with `uv run python -m scripts.native_hull_resistance`. In the Linux SciPy/GCC environment, run `python -m scripts.audit_hull_resistance` and `python -m pytest tests/test_hull_resistance.py`. Regenerate this page with `python -m scripts.publish_hull_resistance`.','',
    'Checks cover independent substitution of a published coefficient row, native/interpreter agreement, Froude interpolation, geometric/density scaling, domain rejection, analytic box geometry and native/mesh volume agreement. These verify implementation; they do not validate predicted resistance against tow measurements.','',
    'Evidence: [arithmetic replay](analysis/hull-resistance-audit.json), [geometry audit](analysis/hull-resistance-domain.json), [current coupled results](coupled-results.md). Sail-induced pitch, heel effects, added resistance in waves and rounded-wing viscous/separated-flow behavior remain unresolved physical-model limitations.','']
    return '\n'.join(lines)


if __name__=='__main__':(ROOT/'docs/hull-resistance.md').write_text(publication(),encoding='utf-8')
