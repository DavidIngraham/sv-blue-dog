# N-001 environmental envelope

<!-- Generated from SysML by scripts/render_requirements.py; edit the model, not this file. -->

[All requirement views](<../requirements-views.md>)

[Qualification conditions, rationale, open issues and verification](<../requirements-context.md>)

**N-001 EnvironmentalEnvelope** — The vessel shall retain the functions required by its selected environmental profile and operating mode.

**N-002 MarineDurability** — The vessel shall retain required function and structural integrity through its selected wet-exposure campaign.

**N-003 StabilityAndFouling** — The vessel shall autonomously tolerate capsize and submerged aquatic vegetation, including milfoil-like stems.

**N-030 AirTemperature** — The vessel shall retain mode-appropriate functions at ambient air temperatures from 0 to 40 degC.

**N-031 WaterTemperature** — Immersed hull, appendages and equipment shall retain mode-appropriate functions in water from 2 to 30 degC.

**N-032 Humidity** — Installed equipment shall retain operational functions at 0–100 percent relative humidity, including condensation.

**N-033 Visibility** — The vessel shall provide mode-appropriate navigation and traffic response across the specified visibility conditions.

**N-034 CalmOperation** — With harvesting disabled and mean wind below 3 m/s, the vessel shall retain calm-mode functions above the R-002 reserve for 24 continuous hours.

**N-035 EnvelopeTransition** — The vessel shall select survival or sailing operation according to the defined environmental transition conditions.

## N-001 derivation 1

```mermaid
---
config:
  fontFamily: "Helvetica, Arial, sans-serif"
  theme: base
  themeCSS: ".edgeLabel rect { opacity: 1 !important; } .cluster-label .nodeLabel { text-align: center; }"
  themeVariables:
    fontFamily: "Helvetica, Arial, sans-serif"
    fontSize: "14px"
    primaryColor: "#FFFFFF"
    secondaryColor: "#FFFFFF"
    tertiaryColor: "#FFFFFF"
    background: "#FFFFFF"
    primaryBorderColor: "#181818"
    primaryTextColor: "#000000"
    lineColor: "#181818"
    textColor: "#000000"
    noteBkgColor: "#FEFFDD"
    noteBorderColor: "#181818"
    noteTextColor: "#000000"
    clusterBkg: "#FFFFFF"
    clusterBorder: "#181818"
    edgeLabelBackground: "#FFFFFF"
---
%% BlueDogViews::environmentalEnvelope1 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 161 node(s) without a position, left undrawn, and 249 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**environmentalEnvelope : EnvironmentalEnvelope**`")
  n1("`*«requirement»*
**marineDurability : MarineDurability**`")
  n2("`*«requirement»*
**stabilityAndFouling : StabilityAndFouling**`")
  n3("`*«requirement»*
**airTemperature : AirTemperature**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## N-001 derivation 2

```mermaid
---
config:
  fontFamily: "Helvetica, Arial, sans-serif"
  theme: base
  themeCSS: ".edgeLabel rect { opacity: 1 !important; } .cluster-label .nodeLabel { text-align: center; }"
  themeVariables:
    fontFamily: "Helvetica, Arial, sans-serif"
    fontSize: "14px"
    primaryColor: "#FFFFFF"
    secondaryColor: "#FFFFFF"
    tertiaryColor: "#FFFFFF"
    background: "#FFFFFF"
    primaryBorderColor: "#181818"
    primaryTextColor: "#000000"
    lineColor: "#181818"
    textColor: "#000000"
    noteBkgColor: "#FEFFDD"
    noteBorderColor: "#181818"
    noteTextColor: "#000000"
    clusterBkg: "#FFFFFF"
    clusterBorder: "#181818"
    edgeLabelBackground: "#FFFFFF"
---
%% BlueDogViews::environmentalEnvelope2 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 162 node(s) without a position, left undrawn, and 255 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
%% layout: n3 x=600 y=200
flowchart BT
  n0("`*«requirement»*
**environmentalEnvelope : EnvironmentalEnvelope**`")
  n1("`*«requirement»*
**waterTemperature : WaterTemperature**`")
  n2("`*«requirement»*
**humidity : Humidity**`")
  n3("`*«requirement»*
**visibility : Visibility**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
  n3 -.->|"derive"| n0
```

## N-001 derivation 3

```mermaid
---
config:
  fontFamily: "Helvetica, Arial, sans-serif"
  theme: base
  themeCSS: ".edgeLabel rect { opacity: 1 !important; } .cluster-label .nodeLabel { text-align: center; }"
  themeVariables:
    fontFamily: "Helvetica, Arial, sans-serif"
    fontSize: "14px"
    primaryColor: "#FFFFFF"
    secondaryColor: "#FFFFFF"
    tertiaryColor: "#FFFFFF"
    background: "#FFFFFF"
    primaryBorderColor: "#181818"
    primaryTextColor: "#000000"
    lineColor: "#181818"
    textColor: "#000000"
    noteBkgColor: "#FEFFDD"
    noteBorderColor: "#181818"
    noteTextColor: "#000000"
    clusterBkg: "#FFFFFF"
    clusterBorder: "#181818"
    edgeLabelBackground: "#FFFFFF"
---
%% BlueDogViews::environmentalEnvelope3 — requirement rendering (view def GeneralView, filter @RequirementUsage)
%% not represented: 185 node(s) without a position, left undrawn, and 315 edge(s) at them
%% layout: n0 x=0 y=0
%% layout: n1 x=0 y=200
%% layout: n2 x=300 y=200
flowchart BT
  n0("`*«requirement»*
**environmentalEnvelope : EnvironmentalEnvelope**`")
  n1("`*«requirement»*
**calmOperation : CalmOperation**`")
  n2("`*«requirement»*
**envelopeTransition : EnvelopeTransition**`")
  n1 -.->|"derive"| n0
  n2 -.->|"derive"| n0
```

[Continue: N-002 marine durability](<requirements-n-002.md>)

[Continue: N-003 stability and fouling](<requirements-n-003.md>)

[Continue: N-033 visibility](<requirements-n-033.md>)

[Continue: N-035 envelope transition](<requirements-n-035.md>)
