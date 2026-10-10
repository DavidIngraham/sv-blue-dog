# Coupled design search: native replay

<!-- Generated from SysML by scripts/render_requirements.py; edit the model, not this file. -->

[Search method, results and limitations](<design-search.md>)

Recomputed from the saved geometry and operating states using the current SysML equations. A valid audit does not mean a feasible design. The nominal study covers only 5 m/s wind; neither study establishes physical compliance. An absent passage duration means upstream progress is nonpositive.

## Numerical checks

| Study | Bounds valid | Maximum scaled equilibrium error | Minimum scaled margin | Numerical fit | Full scenario set | Evidence accepted | Supported design |
| --- | --- | --- | --- | --- | --- | --- | --- |
| full\_envelope | true | 7.407134905434987e-10 | -2.5713211558444558 | false | true | false | false |
| nominal\_5ms | true | 3.8829568449472164e-10 | -1.8296785726049163 | false | false | false | false |

## Mission consequence

| Study | Worst upstream VMG (m/s) | Upstream passage possible | Conservative round trip (h) | Mission time met |
| --- | --- | --- | --- | --- |
| full\_envelope | -0.785660577922228 | false |  | false |
| nominal\_5ms | -0.41483928630245814 | false |  | false |
