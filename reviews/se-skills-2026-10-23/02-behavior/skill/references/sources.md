# Sources and tailoring

Checked 2026-10-23. Agency guidance informs engineering practice rather than automatically becoming Blue Dog policy.

| ID | Inspected primary source | Relevant authority |
| --- | --- | --- |
| LD | [NASA SE Handbook 4.3](https://www.nasa.gov/reference/4-3-logical-decomposition/), 4.3.1.2.1-2 | Functions, inputs/outputs, failure effects, interfaces and end-to-end paths; agency guidance. |
| DSEG | [Defense SE Guidebook, September 2026](https://www.cto.mil/wp-content/uploads/2026/09/SE-Guidebook-2026.pdf), 6.2.3, printed132-135 | Behavioral/physical architecture, allocation and experimental validation; guidance, without imposing defense review gates. |
| S2 | [OMG SysML 2.0 Part 1, formal/2026-03-02](https://www.omg.org/spec/SysML/2.0/Language/PDF), 7.17.1-12, 7.18.1-4 | Normative actions, control, flow, assignment and state semantics. 7.17.1 distinguishes binding/transfer and fork/join/decision/merge. |
| IM | [NASA SE Handbook 6.3](https://www.nasa.gov/reference/6-3-interface-management/), 6.3.1.2.2-3 | Interface characteristics and integration checks. |
| PV | [NASA SE Handbook 5.3](https://www.nasa.gov/reference/5-3-product-verification/), 5.3.1.2 | Verification planning, execution and results; regression is one evidence source. |

Concrete fault-order tests and mutation controls are tailored applications. Acceptance outcomes come from actual project requirements and hazards. This skill does not select a safe state, watchdog interval or physical qualification. Full paid INCOSE/ISO texts were not inspected; no clause-level compliance claim is made for them.
