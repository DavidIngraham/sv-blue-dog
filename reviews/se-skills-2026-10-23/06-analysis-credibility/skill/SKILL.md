---
name: engineering-analysis-credibility
description: Audit and improve engineering analysis intended use, assumptions, verification, validation, uncertainty, numerical sensitivity and result provenance. Use for simulation credibility reviews and authorized corrections to models or evidence pipelines.
---

# Engineering analysis credibility

Decide what a particular analysis can support for its proposed engineering use.
Read the [checklist](references/checklist.md) and [inspected sources](references/sources.md).
Use the project's native analysis and recording facilities; do not add a second
result ontology or reimplement model equations in an audit.

1. Establish the question, consequence of an incorrect result, intended use,
   configuration, domain and proposed interpretation. Distinguish model capability
   from applicability of a particular run. An input export or software fixture is
   not a physical prediction; a credible calculation may find an infeasible design.
2. Inventory definitions AND configured/nested usages, inputs, native objectives,
   assumptions, supporting data, software, numerical methods and current defects.
   Classify historical reviews, references and starting guesses explicitly.
3. Trace actual inputs to configuration and provenance. Check source AND driver
   fingerprints, runtime revision, units/frames, revisions of external data and
   immutable archive manifests. Missing current results must not silently become
   archived design values. Historical records retain their original sources.
4. Assess implementation verification, numerical convergence and comparison with
   independent evidence appropriate to the use. Separate validation observations
   from calibration/tuning data. Record uncertainty, sensitivity, extrapolation,
   dependencies and limitations; unknown uncertainty stays unknown.
5. Apply authorized corrections to model contracts, provenance and affected
   documentation. Preserve mission policy and historical evidence. Do not invent
   tolerances, confidence scores, validation data or acceptance authority.
6. Exercise stale/missing inputs, wrong configurations and domain boundaries as
   well as nominal execution. Save native results and actual source/runtime
   fingerprints, including dirty-tree content when relevant. Report unresolved
   defects and what evidence would permit the next use.

NASA agency standards become mandatory only through the project's adopted basis.
A review predicate records supplied assertions; it cannot inspect evidence or
accept a physical system. Use source guidance proportionately rather than imposing
all simulation activities on a simple arithmetic export.
