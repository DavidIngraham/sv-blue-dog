# Sustained operation: follow energy through the mission

This analysis starts in [virtual design](development-plan.md#virtual-design) and develops toward [physical verification](development-plan.md#physical-validation). It takes mission profiles, installed loads, harvesting assumptions and storage characteristics as inputs, and informs battery and solar sizing, actuator duty limits, energy-management behavior and the bench measurements needed to assess those predictions.

The reusable energy framework adds the installed loads once, including standby demand and conversion losses, then propagates stored energy through a chronological mission profile. An explicit timeline prevents declaration order from becoming an accidental mission schedule. Peak supply demand is checked separately from average energy balance.

The framework accounts for usable storage, charge/discharge limits and efficiencies, self-discharge, intermittent harvesting and the recovery reserve. We split intervals where an outage, duty change or burst can change the minimum stored energy; averages alone cannot establish transient capability. The coupled sizing run uses a simpler day/night balance, overnight reserve and peak-demand screen for each sailing state. It does not yet feed a complete voyage weather-and-load timeline into the chronological framework.

```sysml-view Page_energy_0::EnergySemantics direction=BT
package Page_energy_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view EnergySemantics : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDogRequirements::sustainedEnergyFeasibility;
        expose BlueDogRequirements::sustainedReserveProtection;
        expose BlueDogRequirements::SustainedReserveProtectionCriterion;
        expose BlueDogEnergy::SustainedEnergyVerification;
        expose BlueDog::Architecture::missionContext::boat::energy;
        metadata Layout about BlueDogRequirements::sustainedEnergyFeasibility { x = 0; y = 0; }
        metadata Layout about BlueDogRequirements::sustainedReserveProtection { x = 360; y = 0; }
        metadata Layout about BlueDogRequirements::SustainedReserveProtectionCriterion { x = 0; y = 200; }
        metadata Layout about BlueDogEnergy::SustainedEnergyVerification { x = 360; y = 200; }
        metadata Layout about BlueDog::Architecture::missionContext::boat::energy { x = 0; y = 400; }
    }
}
```

Moving a wing and holding it still are different electrical loads. A non-backdrivable drive may reduce motor holding current but still consumes controller power and incurs moving losses. Its locked failure state also affects recovery. The sizing calculation treats direct aerodynamic moment uncertainty independently of credited lift: lowering the assumed propulsion benefit does not automatically lower the direct pitching-moment load. Both quantities still need measurements.

The current conservative primary replay satisfies the modeled energy screens with energy constraints enforced in every operating case. Under the energy stress hypothesis, all eight constrained attempts fail and the solver reports energy-unconstrained diagnostics instead. Their passage times do not establish sustained operation. Handling, adverse sailing performance and recovery remain separate gates in the [results](results.md). Numerical energy balance is conditional on the supplied profile. The model's energy-evidence decision records the review needed before accepting measurements for an installed configuration. A bounded campaign cannot establish indefinite service.

[Sizing](sizing.md) couples these loads to geometry and motion, first using the conservative primary aerodynamic assumptions and then re-solving controls under additional energy and combined stresses. [Current results](results.md) report those cases separately. [Reliability](reliability.md) considers how passage time increases unattended exposure.
