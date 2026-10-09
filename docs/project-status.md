# SV Blue Dog restart checklist

Prepared October 9, 2026 from the two-page OneNote export dated December 26, 2023 and a filename inventory of the local CAD folder. CAD geometry and physical hardware have not been inspected.

## Recovered baseline

- Aim: balance efficiency, reliability, and ease of manufacture.
- Performance goals: self-righting from inversion; weed resistance; resilience to a small hull breach, battery exhaustion, and software reset; communication; COLREGs compliance as an unverified goal.
- Design constraints: one-metre length; printable 250 x 250 hull cross-section (units not recorded); sealed hull; fin keel and ballast bulb; frame BOM below $100 and labour below four hours.
- "Symmetrical" appears as an isolated note; its intended scope is unresolved.
- Low power consumption is an explicit focus.
- CAD filenames include SV Bluedog.SLDASM, BluedogMast.SLDASM, hull sections, KeelShell.SLDPRT, and several wing/sail variants. Selection and build status are unknown.

## Candidate electronics recorded in 2023

| Function | Notes as recorded |
| --- | --- |
| Autopilot | STM32 H7; CAN transceiver; 6-DOF MEMS IMU; RM3100; SD card; power management and battery monitoring; LT3652; 18650 holder; Ublox M10Q; Express LRS/LORA Rx with ESP32; light controller |
| Communications | Rockblock 9603N?; Ublox cell modem |
| AIS | MSP430W; Si 4362; dAISy Mini AIS receiver reference |
| Air data | STM32 L4; CAN transceiver; AS5048B; hot-wire anemometer |

These are transcribed candidates, not verified part selections. Preserve the question mark on RockBLOCK and verify exact part numbers before procurement.

## Proposed next steps

1. Identify the current CAD assembly and document what has been built, purchased, or tested.
2. Confirm the dimensions, intended operating conditions, and meaning of the manufacturing cost target.
3. Create a mass, displacement, ballast, and righting assessment from the selected geometry.
4. Define sealing, ingress detection, and bilge-pump acceptance tests.
5. Create a power budget covering sensing, actuation, communications, and recovery modes.
6. Specify startup/reset behaviour and the minimum functions retained in limp mode.
7. Record existing test evidence before claiming progress in the public article.

## Publication handoff

Draft article: `docs/restarting-sv-blue-dog.md`.

The website already supports fetching Markdown directly from public source repositories. Once the source repository and ref are known, add an `sv-blue-dog` collection in the website's `publish-manifest.json`, with an article id such as `restarting` pointing to the draft path. Add a homepage project referencing that collection. Do not insert a guessed repository or a broken public link.

The public article needs the owner's review of build status and the proposed next steps. The supplied PDF and reference photograph have not been copied into the website.
