# Operating rules and design constraints

Research baseline: October 9, 2026. These notes guide S-004 and S-005; they do not establish authorization to deploy an autonomous vessel.

## Vessel versus buoy

There is no general unattended-buoy size exemption established by the sources reviewed. USCG describes vessel status in terms of transportation capability and explicitly includes unmanned craft in its lookout guidance. A sailing robot does not become a buoy simply by being unattended. Station keeping and an anchored observation mode need their own classification assessment. [USCG navigation FAQ](https://navcen.uscg.gov/navigation-rules-faqs)

If an installation is an aid to maritime navigation, 33 CFR 66.01-1 requires permission to establish it. That provision neither declares every scientific buoy an aid nor supplies a blanket exemption for small research platforms. Whether it applies to a proposed observation installation must be resolved for that installation. [33 CFR 66.01-1](https://www.ecfr.gov/current/title-33/chapter-I/subchapter-C/part-66/subpart-66.01/section-66.01-1)

## Length affects equipment, not a general permission to operate

Rule 25 contains lighting provisions for sailing vessels below 7 m. Rule 23 contains alternatives for power-driven vessels below 12 m, and narrower conditions for some vessels below 7 m. These are conditional equipment provisions, not maximum allowable dimensions for an unmanned boat. Powered recovery also requires review of the applicable power-driven mode. Inland and International wording must be applied to the correct waters. [USCG amalgamated navigation rules, Rules 3, 23 and 25](https://navcen.uscg.gov/navigation-rules-amalgamated)

Accordingly, no 7 m or 12 m hull-size requirement has been invented. S-005 requires measurement and classification; S-004 requires the resulting lighting, shapes, and sound-signal arrangements. An unattended design cannot rely on a human holding up a torch as its implemented response.

## Project constraints now in the model

- **P-001:** one-person transport, launch, and recovery. Lift mass, packed dimensions, procedure, and acceptable conditions remain to be set.
- **P-002:** parts fit the selected desktop printer. A typical printer has no universal build volume; select the printer or a project envelope before fixing dimensions. Qualify joints, seals, materials, orientation, and tolerances.
- **N-001 through N-003:** separate Gorge/ocean envelopes, marine durability, stability, and fouling response. Wind/current/wave and exposure limits remain open, not assumed from the historical one-metre concept.
- **R-001/R-002:** motor for testing and recovery, challenge-mode interlock and event logging, protected propulsion, and a quantified recovery energy reserve. Thrust must be demonstrated for the recovery current envelope.
- **C-101/C-102:** telemetry and shore equipment, antenna/power/coverage budgets, authenticated emergency commands, and retained autonomous behavior during link loss. No modem, service, AIS transmitter, or radio licensing exemption is selected.

Next decisions are the printer envelope, a practical one-person lift limit, the course gates and recovery locations, and a first measurable Gorge operating envelope. Radio authorization and applicable vessel/installation permissions remain recorded review items rather than component satisfaction claims.
