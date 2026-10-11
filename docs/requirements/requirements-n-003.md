# N-003 Stability and fouling: mission-to-detail thread

Follow this topic from its originating mission or project constraint through the intermediate obligations to its acceptance criteria. Arrows point toward the source: **derive** identifies an acceptance outcome, **refine** adds precision, and **dependency** records a design basis.

[All requirement threads](../requirements.md) · [Modeling method](../methods/modeling.md)

```sysml-view Page_requirements_n_003_0::thread direction=BT statements=true
package Page_requirements_n_003_0 {
    private import StandardViewDefinitions::*;
    private import DiagramLayout::*;
    view thread : GeneralView {
        filter @SysML::RequirementUsage;
        expose BlueDog::Goals::hawaiiVoyage;
        expose GorgeChallenge::transGorgeChallenge;
        expose GorgeChallenge::courseCompletion;
        expose GorgeChallenge::emergencyIntervention;
        expose GorgeChallenge::sailingPropulsion;
        expose BlueDogRequirements::roundTrip;
        expose BlueDogRequirements::safeRecovery;
        expose BlueDogRequirements::environmentalEnvelope;
        expose BlueDogRequirements::gorgeEnvironment;
        expose BlueDogRequirements::recoveryPropulsion;
        expose BlueDogRequirements::stabilityAndFouling;
        expose BlueDogRequirements::capsizeControlRecovery;
        expose BlueDogRequirements::recoveryPropulsorWeeds;
        expose BlueDogRequirements::selfRighting;
        expose BlueDogRequirements::submergedWeedPassage;
        expose BlueDogRequirements::weedBlockageResponse;
        expose BlueDogRequirements::weedSnagShedding;
        metadata Layout about BlueDog::Goals::hawaiiVoyage { x = 0; y = 0; }
        metadata Layout about GorgeChallenge::transGorgeChallenge { x = 320; y = 0; }
        metadata Layout about GorgeChallenge::courseCompletion { x = 0; y = 400; }
        metadata Layout about GorgeChallenge::emergencyIntervention { x = 320; y = 400; }
        metadata Layout about GorgeChallenge::sailingPropulsion { x = 640; y = 400; }
        metadata Layout about BlueDogRequirements::roundTrip { x = 0; y = 800; }
        metadata Layout about BlueDogRequirements::safeRecovery { x = 320; y = 800; }
        metadata Layout about BlueDogRequirements::environmentalEnvelope { x = 0; y = 1200; }
        metadata Layout about BlueDogRequirements::gorgeEnvironment { x = 320; y = 1200; }
        metadata Layout about BlueDogRequirements::recoveryPropulsion { x = 640; y = 1200; }
        metadata Layout about BlueDogRequirements::stabilityAndFouling { x = 0; y = 1600; }
        metadata Layout about BlueDogRequirements::capsizeControlRecovery { x = 0; y = 2000; }
        metadata Layout about BlueDogRequirements::recoveryPropulsorWeeds { x = 320; y = 2000; }
        metadata Layout about BlueDogRequirements::selfRighting { x = 640; y = 2000; }
        metadata Layout about BlueDogRequirements::submergedWeedPassage { x = 960; y = 2000; }
        metadata Layout about BlueDogRequirements::weedBlockageResponse { x = 0; y = 2180; }
        metadata Layout about BlueDogRequirements::weedSnagShedding { x = 320; y = 2180; }
    }
}
```

## Continue the breakdown

- [Capsize control recovery](requirements-n-052.md)
- [Recovery propulsor weeds](requirements-n-056.md)
- [Self righting](requirements-n-051.md)
- [Submerged weed passage](requirements-n-053.md)
- [Weed blockage response](requirements-n-055.md)
- [Weed snag shedding](requirements-n-054.md)
