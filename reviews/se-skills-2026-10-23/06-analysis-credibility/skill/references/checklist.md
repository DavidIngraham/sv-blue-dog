# Credibility review checklist

For each applicable check record scope, native evidence, correction or open work,
and the consequence for proposed use. Do not count an unknown as a passing check.

| ID | Review question / evidence expected | Basis |
| --- | --- | --- |
| A01 | Is the decision question and intended use explicit? | A4.1.1.1;B AppendixF |
| A02 | Are consequence/criticality and review effort proportionate? | A4.1.1.2;D6.1.2 |
| A03 | Are definitions, configured usages and nested analyses inventoried? | G7.23;local completeness control |
| A04 | Are configuration, operating domain and proposed use compatible? | A4.3.1;B5.6.1 |
| A05 | Are model assumptions, exclusions and permissible interpretations clear? | A4.2.1.5-.9;B AppendixC |
| A06 | Are input data pedigree, units, frames, revisions and conversions traceable? | A4.2.1.1-.4;B5.6.1.3 |
| A07 | Are source AND driver fingerprints and actual runtime recorded? | A4.2.1;4.3.8;local reproducibility control |
| A08 | Do both record and path APIs reject stale or unproven current results? | A4.3.1;local provenance control |
| A09 | Are archived reference data and numerical initial guesses explicitly scoped? | A4.3.1;B AppendixF |
| A10 | Are historical bytes/source revisions preserved without relabeling? | A4.3.8;local evidence control |
| A11 | Has implementation verification addressed equation/algorithm/unit defects? | A4.2.3;G7.19 |
| A12 | Are discretization, solver convergence and numerical sensitivity suitable? | A4.2.3;4.3.5 |
| A13 | Is validation relevant and independent of calibration for the proposed use? | A4.2.5;4.3.1 |
| A14 | Are uncertainty, correlation, sensitivity and coverage reported? | A4.2.7;4.3.3/.5;F7 |
| A15 | Are defects, extrapolations and out-of-domain results visible? | A4.1.1.8;4.3.1 |
| A16 | Does reporting separate execution, feasibility, validation and acceptance? | A AppendixE;C6.7;G7.23-.24 |
| A17 | Do negative controls detect missing input, stale data and wrong subject? | A4.2.3;local regression control |
| A18 | Are limitations, next evidence and affected decisions/docs reconciled? | A4.3.6/.8;C6.8;E6.4 |

Useful probes: a good source hash with a bad driver hash; a stale input requested
by path; a missing current sizing result when an archive exists; legitimate archived
CAD reference use; a newly added unclassified analysis; successful execution that
finds a design criterion false; a physical-use claim supported only by regression.
