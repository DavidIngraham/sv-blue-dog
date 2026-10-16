# Seeing hazards early enough to act

**OOSEM:** System requirements, logical behavior, trades and virtual evidence · [Current assessment](current-assessment.md)

Can Blue Dog detect a hazard early enough to avoid it? I first work backward from closing speed and maneuver time to the observation distance needed. Then I compare sensing approaches, their electrical cost and the behavior of IC-01 when those capabilities operate together.

## Challenge the detection-distance allocation

The [encounter allocation](../models/analyses/encounter-review.sysml) measures distance from the nearest physical extent of the target. A tow includes its barges; a reported antenna position is not its boundary. The native calculation is:

**required distance = closing speed × (acquisition + processing + command + maneuver + contingency time) + separation + relative-position allowance.**

The declared baseline uses 5 seconds for acquisition, 1 for processing, 2 for command, 15 for maneuvering and 15 for contingency, plus 10 m relative-position allowance and target-specific separation. Ownship contributes 3 m/s to the head-on closing-speed bound. These are engineering allocations, not observed encounter statistics or legal stand-off distances.

```sysml-report BlueDogEncounterStudyDocuments::Detection
```

The fast-powerboat case drives **724 m**, rounded to the current **750 m** acquisition allocation. Doubling its maneuver time to 30 seconds requires **994 m**. Keeping the 15-second maneuver but increasing processing to five seconds requires **796 m**. Neither variation fits 750 m. The study sweeps six target classes, three maneuver allowances and three processing delays: **54 cases**.

Slower targets require less closing distance, but a person-sized target in darkness can still be the harder sensing problem. The table does not relax the existing 750 m acceptance envelope for its six traffic classes. A future class-specific allocation needs measured detection and maneuver evidence, explicit operating conditions and an owner-reviewed requirement change. Weed-response calculations remain separate sensitivities; they do not assign that traffic requirement to vegetation.

The executed timing comparison uses **30-second and one-second assessment schedules**, **two-second command delivery** and a persistent **15-second maneuver**. Pending commands hold the previous heading until delivery; frequent updates cannot restart or shorten a maneuver. The native timing criterion distinguishes the declared schedules, but a passing simulated schedule is not a measurement of installed response.

In the replay timing screen, the one-second allowance represents the wait to the next assessment; it is not also charged as another processing delay. Sensor delivery adds one or two seconds. Including both gives **742 m** for the radar-assisted hypothesis and **760 m** for the vision hypothesis at one-second assessment. At 30-second assessment the same bounds are **1,264 m** and **1,282 m**. The vision hypothesis therefore exceeds 750 m even with the faster schedule. The radar-assisted daylight craft hypothesis only narrowly fits; its night and low-target hypotheses still do not.

These are serial allowances for a fresh response opportunity, not measured latency distributions. A pending command or active maneuver blocks selection of another heading; one-second margin checks can request abort but cannot pre-empt that maneuver. The occupied-response analysis below adds that wait. Passing the declared schedule criterion does not verify the complete avoidance deadline.

### A hazard arriving during a turn

The [class-specific encounter envelope](reference/encounter-envelope.md) separates
the observation needed for a tow, fast craft, person, stationary obstacle and
vegetation. It compares head-on, crossing and same-course closure and includes
the time already committed to another command or maneuver. Acquisition may
overlap that occupied interval; the model counts the overlap once.

For the fast head-on case with one-second sensor delivery, the fresh-response
bound is 742 m. If a 17-second
command-and-maneuver interval begins as the target enters the acquisition
envelope, the bound becomes 940 m. If 17 seconds remain when the usable track
arrives, it becomes 1,048 m. Those are different timing conditions, not
interchangeable margins. None reduces the current 750 m requirement, and none
establishes that 750 m is sufficient for every encounter.

The [finite-turn experiment](reference/maneuver-dynamics.md) also challenges the
15-second maneuver assumption. Its uncalibrated turn, tack and gybe cases take
different times; insufficient steering authority can leave a turn unfinished.
Without a supported observation or maneuver bound, the envelope reports an
unsupported case rather than a finite required range.

## Choosing an installed sensing stack

I need a complete observation pipeline: acquisition, detection, tracking, range and motion estimation, fusion and timely delivery to guidance. IC-01 allocates 8 W of additional sensing and compute demand to make that choice concrete. Camera count, field of view and frame rate affect both observation coverage and power. Carrier electronics, storage, conversion, cooling and any lens cleaning or heating belong in the installation too. Measure useful observations and battery demand together under the intended workload and temperature.

The [physical configuration comparison](reference/sensing-configurations.md)
now identifies actual camera, compute and AIS components and distinguishes
continuous coverage from a scanning installation. Their power, mounting and
backup-sensing gaps feed the next boat-sizing decision. They have no credited
detection range yet. The abstract range hypotheses below remain historical
experiment inputs; they are not predictions for these components.

### Coverage requires complementary observations

AIS reports cooperating transmitters. It includes some recreational vessels carrying Class B equipment as well as mandated commercial traffic, but absence of an AIS report does not establish clear water. [USCG carriage requirements](https://www.navcen.uscg.gov/ais-requirements) and [IMO AIS operating guidance](https://www.navcen.uscg.gov/sites/default/files/pdf/ais/references/IMO_A1106_29_Revised_guidelines.pdf) describe that boundary.

| Candidate sensing layer | Useful evidence | What the trade must challenge |
| --- | --- | --- |
| AIS | Reported identity, position and motion of equipped traffic | Non-transmitters, stale or incorrect reports, and the full extent of a tug and tow |
| Visible cameras, with thermal as a separate option | Non-cooperative craft, people, buoys and visible debris | Glare, darkness, fog, spray, fouled lenses, wave occlusion, range ambiguity and low targets from a small boat |
| Passive acoustics: microphones or hydrophones | Audible signals or machinery/propeller sounds that may cue another sensor | Quiet sailboats, paddlers and debris; wind, flow and own-boat noise; localization and ambiguous sources |
| Active acoustic ranging/sonar | Returns from targets within the chosen sensor's beam and propagation domain | Above-water versus submerged coverage, near-surface clutter, range, update rate and installation constraints |
| Radar | Independent ranging and tracking candidate for non-cooperative traffic | Small-target returns, sea clutter, near-field coverage, mounting, mass and power |

Vision and acoustic sensing therefore cannot be credited with capturing everything. [River-watercraft vision experiments](https://publications.ri.cmu.edu/storage/publications/pub_files/2013/5/ARMS2013_VOO.pdf) illustrate both capability and the challenge of water reflections. [NOAA's acoustic work](https://www.fisheries.noaa.gov/new-england-mid-atlantic/science-data/marine-mammal-acoustics) explains how noise masks passive observations; applying passive sensing to Blue Dog would require vessel-specific evidence. Quiet hazards are a reason to investigate complementary sensing, not to assume acoustic detection.

### Hydrophones and forward-looking sonar

A hydrophone is an underwater receiver; a passive sonar system adds acquisition and processing, and potentially an array for bearing estimation. A single receiver detecting a sound does not by itself establish target range or a collision track. Active sonar transmits a pulse and measures returning echoes. [NOAA explains the active/passive distinction](https://oceanservice.noaa.gov/facts/sonar.html). For collision avoidance, evaluate a forward-looking geometry rather than assuming a downward-looking depth sounder observes the path ahead.

For Blue Dog, compare a hydrophone or compact array as a powered-traffic cue, and forward-looking sonar as a candidate for submerged or partly submerged hazards. Neither has selected hardware or a credited detection range. Test quiet targets as well as powered craft, surface/bottom reflections, bubbles and wakes, and masking from water flow, actuators and recovery propulsion. Mounting depth, array aperture, wet connectors, drag and fouling belong in the installation trade. Underwater coverage does not establish coverage of obstacles entirely above water.

Budget receiver preamplifiers, digitizers, continuous processing and data recording for passive sensing; add transmitter peak demand, ping duty and echo processing for active sonar. Passive means no transmitted acoustic pulse, not zero electrical demand. Measure useful range/bearing and update latency alongside average and peak battery-bus demand. Acoustic cues may direct cameras or strengthen a fused track, but any power-saving schedule must preserve the required detection lead time.

The [physical acoustic comparison](reference/acoustic-sensing.md) now identifies
an Aquarian hydrophone array with synchronized acquisition, a Cerulean
Omniscan 450 FS narrow-beam sonar and a Sonoptix ECHO multibeam sonar. Passive
listening could cue a powered target; active sonar can range a return from a
quiet submerged object. Neither observation establishes all-bearing surface
traffic coverage. The comparison separates head specifications from complete
installation demand, useful target evidence and independent recovery.

### Weed detection and avoidance

Active sonar can detect submerged vegetation: [BioSonics' aquatic-habitat echo sounder](https://www.biosonicsinc.com/products/mx-aquatic-habitat-echosounder/) explicitly supports mapping submerged aquatic vegetation. This supports investigating the sensing principle; it does not establish real-time avoidance performance on Blue Dog. A downward survey image obtained after passing over vegetation is different from a timely forward obstacle observation.

Include dense rooted beds, sparse stems, floating mats and drifting strands as distinct cases. Measure detection distance, missed hazards, false alarms and estimated extent at the depths swept by the keel, rudder and recovery propulsor. Test bottom/surface clutter, turbid water, bubbles, boat motion and different approach angles. A reliable return from a dense bed cannot be generalized to every thin strand. Passive hydrophones do not provide a dependable warning for quiet vegetation; visible cameras may complement sonar for exposed mats.

Avoidance must keep the entire underwater swept volume clear with uncertainty allowance, while respecting current, available sailing directions and turning response. The mission experiment should include weed patches and drifting vegetation as independent ground truth, compare timely avoidance with late/missed observations, and assess loss of propulsion or steering if fouling occurs. Recovery routes must also remain usable. Measure sonar power and processing latency, and check that the transducer mount, cables and any guard do not create new snag points. This remains a testable candidate capability, not credited weed protection.

### Can probability justify a smaller sensing obligation?

The present traffic scope includes sailboats and paddlers. Its uniform 750 m
allocation can be challenged using class-specific closing speed, uncertainty
and achieved response; removing a target class is a different decision.
L-104 allows explicitly reviewed residual risk, but no accepted probability
threshold or measured class-specific exposure currently supports such an
exclusion. The [requirement-scope review](reference/encounter-envelope.md#can-i-exclude-a-rare-or-difficult-target-class)
separates that possibility from the provisional mission-reliability objective.
Quiet targets remain test cases for the acoustic alternatives.

## Compare sensing and energy together

```sysml-report BlueDogEncounterStudyDocuments::Energy
```

Every entry is an **assumed combined envelope**, not predicted hardware performance. The ranges are daylight values; the model also declares night factors, latency, misses and track age. Equipped targets use a separate 1,500 m AIS hypothesis. The radar-assisted case assumes longer craft range but still a limited low-target range. Hydrophone cueing receives **no unsupported range improvement**: it adds load while its useful cueing benefit remains unmeasured. Forward-looking sonar changes only the weed-range hypothesis, from 20 to 40 m; it is not credited with detecting every surface target.

The power entries are hypothetical **additional bus loads**, including the proposed acquisition/processing increment. They do not replace the unresolved 4.5 W electronics lump. A real shared-compute design must reconcile replacement loads once. Here the native energy screen charges each increment over the retained candidate's 48.34-hour allowance at 90% discharge efficiency, with no solar credit. All four hypotheses exceed the candidate's roughly 4 Wh headroom. They cannot be selected as drop-in installations on that budget.

The four-stack screening trials use the reference candidate's stored energy and baseline demand with the conceptual mission polar, not a correlated candidate maneuver model. Short-run remaining charge is not voyage feasibility. IC-01 has its own coupled resizing and local chronological replay; its static full-passage energy screen remains separate from complete charted-course execution.

## Observations drive guidance; truth scores consequences

The simulated observation system samples independent traffic and weed truth. It applies target-class range, day/night range factors, random missed detections at the declared probability, delayed delivery, bounded position error, track expiry and scheduled dropouts. AIS coverage applies only to actors explicitly equipped in the scenario. A lost track does not imply clear water.

Guidance receives delivered tracks extrapolated at constant velocity. It does not receive future turns, future appearances or the target's complete scripted path. Exact instantaneous velocity and target dimensions remain hypotheses; this study does not include false positives, clutter-dependent errors, mast occlusion or correlated image/acoustic physics. Range is an all-bearing proxy: sonar beam direction and mounting are not represented. Detection distance uses a circle enclosing the target footprint, which can trigger earlier than the nearest rectangular hull; this optimistic approximation is another reason these cases cannot qualify acquisition range. Position uncertainty expands the perceived footprint.

Independent truth checks executed motion continuously for collision and required clearance. An unseen obstacle can therefore produce a recorded safety violation; truth cannot secretly veto a sailing command. Weed geometry is a separate target class, with contact scored against the swept vessel footprint. This is a coarse proxy for underwater contact, not a resolved keel, rudder or propeller snag model.

An explicit perfect-truth baseline remains available for comparison and for reproducing older experiments. Each result identifies which observation mode it used. The paired study uses the imperfect provider for every sensing hypothesis and retains observations, supervisory decisions, movement history and stopping causes.

## Close the candidate loop

IC-01 links an allocated sensing envelope to one-second guidance assessments, explicit command and maneuver clocks, candidate-specific sailing performance and separately accounted recovery energy. Day/night runs pair clear water, a non-AIS crossing, a stationary low target and a weed patch across fixed seeds. Additional cases exercise the solved wind endpoints, primary sensing/steering/power loss, capsize, recovery after passage standby, finer integration and degraded capabilities. The synthetic reach is 600 m between gates in a 700 m wide water domain, with two hypothetical shore approaches. It is a representative integration exercise, not the complete charted Gorge mission.

Normal sailing must complete; an encounter may complete or deliberately abort and reach a recovery approach safely. These outcomes remain separate. A collision, clearance violation, unsupported sailing state, exhausted recovery bank or censored trajectory prevents the applicable acceptance condition from passing. The [native closure requirement](../models/analyses/integrated-candidate.sysml) also requires compatible sizing and explicit assumptions. The [physical evidence plan](validation-plan.md#exercise-decisions-before-physical-integration) identifies what must replace those assumptions.

This case set does not cover every high-speed encounter, occupied-maneuver arrival, false positive, correlated obscuration or recovery-route blockage. Those are specific additions needed before extending the result to the full course.

The archived 15 October 2026 [IC-01 record](../evidence/runs/2026-10-15-integrated-candidate/integrated-mission.json) passes the seven native closure conditions. Of 18 nominal/encounter runs, **10 complete** and **eight safely abort to recovery approaches**. All six casualty/end-of-exposure runs reach an approach; these use powered recovery and remain disqualified challenge attempts. The archived capsize case tests inverted powered recovery. It does not test unassisted self-righting: unassisted righting may preserve qualification when safety functions remain available while inverted and upright control is restored, without motor use or outside intervention. The clear-water and weed cases preserve their classifications at half-second integration. Eighteen upright/inverted reserve samples fit the independent bank after full energy-exposure standby. Shared primary/recovery power failure and an empty recovery bank produce shore contact, while the short-range weed sensitivity safely aborts. That one short-range result does not establish a reduced sensing requirement. No successful admitted case records collision, clearance violation or unsupported sailing performance.

## Follow an unsuccessful attempt to its consequence

An abort must lead somewhere. The simulator continues powered recovery or current-driven drift until an approach, physical contact or the declared horizon. Energy exhaustion does not stop the boat moving. Shore contact is an adverse event; reaching a water approach does not establish capture, retention or access for retrieval. Those distinctions make recovery limitations visible rather than counting a stopped simulation as a safe outcome.

The [earlier paired continuation study](reference/encounter-continuation.md) exposed contacts and unresolved drift in a conceptual-vessel comparison. Its 40 runs and four added-load hypotheses belong to that configuration, not IC-01. The [development history](simulation-spirals.md) explains the changes those failures motivated. Current-only drift and point-mass recovery still need measured maneuver, windage and wave behavior before they can support a real recovery decision.

## Measurements that could change the choice

Before equipment selection, collect time-stamped detections and misses against independent target truth across target class, range, bearing, lighting, glare and spray. Record first acquisition, tracking gaps, position error, end-to-end latency, processor temperature and average/peak installed bus demand. Separate held-out encounters from calibration data. Use the same recorded encounters for candidate pipelines so a comparison does not confound hardware with different traffic.

Measure the boat's achieved swept maneuver and time under both tacks, low wind and adverse current. Compare the resulting detection-distance envelope with the pipeline's measured observation envelope; reject unsupported conditions rather than shortening the required distance by assumption. Repeat at finer control periods only when the implementation and maneuver model support them.

For recovery, establish surveyed water approaches and shore access, installed upright and inverted thrust/power, current authority, retention and retrieval arrangements. Inject loss of sensing, steering and power to establish which recovery functions remain independent. Until those measurements exist, the useful outcome is an explicit architecture gap and a testable experiment, not risk closure.

**Next:** [Power and energy budget for the Gorge candidate](energy.md) · [Series guide](index.md)
