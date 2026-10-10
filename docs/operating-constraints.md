# Operating rules and design constraints

Research baseline: October 9, 2026. These notes guide S-004 and S-005; they do not establish authorization to deploy an autonomous vessel.

## Vessel versus buoy

The Microtransat community does have a specific basis for the buoy/oceanographic-device interpretation; the earlier version of these notes omitted that evidence.

| Source | What it establishes | Limit for Blue Dog |
| --- | --- | --- |
| [Boat Length, March 18, 2023](https://groups.google.com/g/microtransat/c/ZCm62dVztJ4) | Paul Miller attributes the 2.4 m overall race limit to a USCG interpretation treating smaller craft as oceanographic devices. | A participant's report; the thread does not supply the underlying agency determination or its conditions. |
| [Microtransat FAQ](https://www.microtransat.org/faq.php) | Organizers report UK/French coastguard conversations supporting buoy classification, but a differing IMO view. | Evidence of differing interpretations, not a current ruling for this project. |
| [2026 race discussion, April 14](https://groups.google.com/g/microtransat/c/DuZiwjFllE8) | Francis Roussel discusses a 2.5 m threshold. | Country, regulatory purpose and conditions matter; length alone is insufficient. |
| [French regulation discussion, August 24-25, 2026](https://groups.google.com/g/microtransat/c/0_jdHs-k-cY) | Participants discuss French maritime-drone rules and contrast the UK MGN 702 exemption. | Do not import the thread's one-metre or nationality conclusions into a US design requirement. |
| [Current MCA MGN 702 Amendment 2, January 19, 2026](https://www.gov.uk/government/publications/mgn-702-m-amendment-2-maritime-autonomous-surface-ships-of-less-than-25-metres-in-loa/mgn-702-m-amendment-2-maritime-autonomous-surface-ships-of-less-than-25-metres-in-loa) | An actual conditional exemption from specified certification requirements for eligible MASS below 2.5 m. The guidance explicitly retains other maritime requirements. | It still describes these craft as vessels; this is not a US buoy exemption. |

The August thread links [French Decree 2024-461](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000049583905). It is a useful jurisdiction-specific lead, not authority for the Columbia River. The unresolved US question is the underlying USCG oceanographic-device interpretation: its text, date, purpose, scope and continuing applicability to an autonomous sailing research craft, including powered recovery and station keeping. No correspondence has been sent on the user's behalf.

For now S-005 retains classification review and S-004 retains mode-dependent conspicuity. The 2.4 m race limit is a relevant candidate design constraint, not yet a proven legal safe harbor or a user-selected hull limit. USCG's public FAQ uses transportation capability to explain vessel status, including transportation of services. [USCG navigation FAQ](https://navcen.uscg.gov/navigation-rules-faqs)

If an installation is an aid to maritime navigation, 33 CFR 66.01-1 requires permission to establish it. That provision neither declares every scientific buoy an aid nor supplies a blanket exemption for small research platforms. Whether it applies to a proposed observation installation must be resolved for that installation. [33 CFR 66.01-1](https://www.ecfr.gov/current/title-33/chapter-I/subchapter-C/part-66/subpart-66.01/section-66.01-1)

## Length affects equipment, not a general permission to operate

Rule 25 contains lighting provisions for sailing vessels below 7 m. Rule 23 contains alternatives for power-driven vessels below 12 m, and narrower conditions for some vessels below 7 m. These are conditional equipment provisions, not maximum allowable dimensions for an unmanned boat. Powered recovery also requires review of the applicable power-driven mode. Inland and International wording must be applied to the correct waters. [USCG amalgamated navigation rules, Rules 3, 23 and 25](https://navcen.uscg.gov/navigation-rules-amalgamated)

Accordingly, no 7 m or 12 m hull-size requirement has been invented. S-005 requires measurement and classification; S-004 requires the resulting lighting, shapes, and sound-signal arrangements. An unattended design cannot rely on a human holding up a torch as its implemented response.

## Project constraints now in the model

- **P-001:** one-person transport, launch, and recovery. P-001 proposes a 15 kg per-lift limit and a measurable sheltered handling demonstration.
- **P-002:** each oriented print job, including supports, brim, raft and required clearance, fits the user-selected 250 × 250 × 250 mm usable build envelope.
- **N-001 through N-003:** separate Gorge/ocean envelopes, marine durability, stability, and fouling response. Quantitative operating, survival, immersion, thermal, exposure and self-righting requirements are now specified; see [environmental qualification](environmental-envelope.md).
- **R-001/R-002:** motor for testing and recovery, challenge-mode interlock and event logging, protected propulsion, and a quantified recovery energy reserve. Thrust must be demonstrated for the recovery current envelope.
- **C-101/C-102:** telemetry and shore equipment, antenna/power/coverage budgets, authenticated emergency commands, and retained autonomous behavior during link loss. No modem, service, AIS transmitter, or radio licensing exemption is selected.

Next decisions are review of the proposed handling targets, the course gates and recovery locations, and validation of the environmental design targets against route observations. Radio authorization and applicable vessel/installation permissions remain recorded review items rather than component satisfaction claims.
