# Environmental design and qualification

N-001, N-002 and N-003 in [requirements.sysml](../models/requirements.sysml) now prescribe vessel behavior and measurable acceptance criteria. The [generated requirements register](requirements-register.md) contains the authoritative statements. These numerical choices are an initial engineering baseline selected for design work, not measured site extremes, proven capability or a completed Hawaii passage assessment. Their work status remains in SysML metadata.

| Parameter | Gorge operation | Ocean operation | 24-hour survival |
| --- | --- | --- | --- |
| Mean wind / gust | 3-15 / 20 m/s | 3-15 / 20 m/s | Up to 25 / 35 m/s |
| Significant wave height | Up to 1 m | Up to 3 m | Gorge 2 m; ocean 6 m |
| Peak wave period | 2-5 s | 5-20 s | Gorge 3-7 s; ocean 6-20 s |
| Current magnitude | Up to 1.5 m/s | Up to 1 m/s | Same respective current limits |
| Air / water temperature | 0-40 / 2-30 degC | 0-40 / 2-30 degC | Same temperature limits |
| Qualification duration without servicing | 72 hours | 30 days | 24 hours per profile |

Wind conventions, wave sampling, individual-wave severity, humidity, visibility, adverse relative directions and functional acceptance are specified in N-001. Operation requires navigation, autonomous sail/steering control, recording and telemetry when a link is available. Survival permits lost course progress but requires flotation, retained structure/state and position recording; sailing resumes autonomously after conditions recover. Calm handling and adverse currents do not magically guarantee station keeping or an upstream leg.

The selected Gorge profile makes short-period chop and strong wind a design load; the ocean profile adds larger, longer-period waves and salt exposure. These are deliberate target choices, not return-period statistics. Route/season measurements, hull response analysis and sailing polars must establish whether this baseline supports mission completion. A 30-day qualification campaign does not establish the eventual Hawaii voyage duration or indefinite reliability. Hurricanes, freezing/ice, surf-zone launch, log impacts and fishing-line entanglement are not claimed covered.

N-002 adds whole-assembly wet exposure, installed-enclosure immersion, dry-indicator acceptance, connector resistance, hot-sun operation and retained printed-material strength after UV/wet aging. N-003 adds timed self-righting at mission loading extremes and a reproducible vegetation-surrogate encounter. These address observable outcomes rather than asking someone to define an envelope later.

Qualification should combine controlled environmental exposure and instrumented sea trials. Record actual wind/wave/current histories, loading, temperatures, ingress indicators, power and control logs, and pre/post inspection results. Controlled facilities or validated load analysis are needed where field trials cannot safely/reproducibly supply the required conditions. Model validation and diagram generation only establish model consistency; they are not physical requirement verification.
