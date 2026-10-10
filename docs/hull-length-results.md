# Hull length relaxation: native replay

<!-- Generated from SysML by scripts/render_requirements.py; edit the model, not this file. -->

[Method and interpretation](<design-search.md#does-a-longer-hull-solve-it>)

Only the length bound changes. The numerical search uses a mass-implied ceiling, not the former 3.5 m exploratory cap. Fixed-length rows cover the nominal 5 m/s wind cases only. Ignore VMG for any row that is not balanced and hardware feasible. A failed local search is not a global infeasibility proof.

| Study | Waterline length (m) | Balanced and hardware feasible | Worst upstream VMG (m/s) | Numerical mission fit | Supported design |
| --- | --- | --- | --- | --- | --- |
| full\_envelope | 2.021360689294771 | true | -0.7856605779326346 | false | false |
| nominal\_5ms | 2.893420298571151 | true | -0.4148392856958909 | false | false |
| fixed\_2 | 2 | true | -0.43830080623787926 | false | false |
| fixed\_3\_5 | 3.5 | true | -0.421970437485911 | false | false |
| fixed\_5 | 5 | true | -0.4642899880317477 | false | false |
| fixed\_8 | 8 | true | -0.575105185268459 | false | false |
| fixed\_12 | 12 | true | -0.6979598677491431 | false | false |
| fixed\_20 | 20 | true | -1.1777441604389016 | false | false |
