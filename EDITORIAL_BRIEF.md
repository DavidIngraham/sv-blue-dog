# Blue Dog revision brief — 16 October 2026

## Accepted owner decisions

- Audience: technically minded, new to this project, familiar with basic systems engineering but not necessarily SysML.
- Voice: personal first-person singular for owner decisions; plain, precise prose. Explain the engineering question, choices, evidence and consequence. Define specialist terms on first use. Avoid bureaucratic process narration, excessive disclaimers and unexplained "we" or "design team".
- IC-01 is the current working integration candidate. A refined IC-01-scale vessel is the intended FIRST physical build. The original CAD testbed is historical only, not a planned separate build. Component experiments still support the first build.
- Capsize alone must not end qualification when unassisted recovery restores required safety capabilities. Motor use, external intervention, or loss of required safety capability still end qualification. Inverted powered recovery is a disqualified recovery path.
- Compare soft sail, tail-controlled rigid wing and directly rotated fixed-camber wing equally for the finite Gorge mission. No selected rig or installed sensing stack is implied.
- Restructure freely: URLs, historical navigation and article boundaries are not constraints. Consolidate repeated material; retain useful evidence and provenance, not redundant public pages.
- Publish after checks. User expressly authorized publication. Do not ask again.

## Evidence and common facts

IC-01: 1.2 m overall length, 0.42 m beam, 20.060769 kg, 0.4 m2 wing; 1300 Wh main + 60 Wh independent recovery battery; 38.884 h conditional passage, 54.604567 h energy allowance, 936 Wh main departure, 833.937594 Wh required, 102.062406 Wh headroom. Bounded local integration: 10 completed courses, 8 safe aborted encounter approaches, 6 casualty/end-exposure approaches. NOT full-course safety, measured equipment or physical qualification.

Retained sizing reference: 1.2 m overall, 0.26 m beam, 10.312830 kg, 440 Wh, 33.868835 h, 48.336044 h energy allowance, 316.8 Wh departure, 312.826340 Wh required, 3.973660 Wh headroom. Separate earlier configuration.

Archived boats (1.4 m, 2.009 m) retain configuration-specific historical evidence. Different course lengths (65.786 / 65.989 km) and campaign counts (28 / 18 completions) must retain their dates/configurations, not be harmonized into one result. No numerical result becomes a physical measurement.

Native weather primary refers to OLD 2.009 m archive; current call returns westPass true / eastPass false. Do not claim current east-wind pass. Current frontier uses overall-length caps with separate mass/passage objectives; length-minimization and fixed-length continuation are diagnostic/historical workflows.

## Reader structure

Primary journey: story -> mission/context -> concise requirements -> candidate and sizing results -> sizing method -> physical trades (rig, construction/recovery, propulsion) -> sensing/encounters and energy -> mission execution -> reliability -> validation/next investigations.

Current maturity is a short dashboard/reference, not a repeated textbook. Development spirals is canonical history. Site/recovery/environment detail belongs in supporting evidence. Modeling/publishing and command/schema/compiler mechanics are contributor references. Requirements show short governing decisions then expandable authoritative statements without repeated ancestor prose.

Root agent owns final structure, navigation, terminology, rendering and integration. Agents own disjoint files; no commits/pushes until root integrates. Preserve archives byte-for-byte. Read AGENTS.md; owner decisions above supersede URL preservation and future testbed guidance.

## Implemented revision

The 14-article reading path is in `docs/index.md`. The current assessment and site/environment reference replace the old development-plan and SRR pages. Detailed reproduction material is in `docs/reference/`. Both the project site and personal-blog collection follow this structure.

The native supervisor distinguishes a safe, explicitly observed unassisted righting from a disqualifying casualty. The simulator suspends sailing and gate scoring while inverted; no righting dynamics or physical capability is inferred. Three rig concepts receive equal development consideration. Historical experiment bytes and source provenance remain unchanged.

Validation: 75 model documents parsed with no MCP diagnostics; 50 focused model/behavior checks passed. The full 496-test run passed 494 checks and identified two publishing identity failures caused by deduplicated statements. After fixing mixed native/compact diagram identity handling, all 41 affected documentation, model-view and traceability checks passed, including a new mixed-label regression. The 32-page publishing build and rendered-browser checks passed; geometry/reset, risk filters/details and expanded native diagrams were exercised. The JavaScript geometry and risk contracts passed for both site implementations.
