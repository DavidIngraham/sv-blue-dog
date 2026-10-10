package BlueDogSailTrade {
    doc /* Control architecture and section camber are independent design axes.
     * A cambered wing could also use aerodynamic tail control. These three named
     * configurations are a starting comparison, not mutually exclusive physics. */
    private import ScalarValues::*;
    enum def Evidence { unknown; passed; failed; }
    part def Candidate {
        attribute label : String;
        attribute membraneSail : Boolean;
        attribute aerodynamicTrim : Boolean;
        attribute concept : String;
        attribute durability : String;
        attribute energy : String;
        attribute sailing : String;
        attribute recovery : String;
        attribute manufacturing : String;
        attribute nextEvidence : String;
        // Ordered: wet/survival durability, energy, polar/progress, capsize/control,
        // manufacturing, lifting, voyage reliability. Unknown is never a failure.
        attribute gates : Evidence [7] ordered nonunique default =
            (Evidence::unknown, Evidence::unknown, Evidence::unknown, Evidence::unknown,
             Evidence::unknown, Evidence::unknown, Evidence::unknown);
    }
    part tailWing : Candidate {
        attribute :>> label = "Tail-controlled rigid wing";
        attribute :>> membraneSail = false;
        attribute :>> aerodynamicTrim = true;
        attribute :>> concept = "Freely rotating main wing, provisionally symmetric, with a tail and actuated elevator-like trim tab. Tail/wing aerodynamic moments set incidence; no assumption of a powered whole-wing bearing.";
        attribute :>> durability = "Avoids sailcloth flogging and sheets; retains bearing, tab linkage, tail-boom, skin/joint and wave-impact failure modes. Rigid wings are not automatically storm-proof.";
        attribute :>> energy = "Low trim-energy potential from aerodynamic balance; measure bearing friction, tab hinge moment and failure-state power. No transfer of full-size Saildrone wattage to Blue Dog.";
        attribute :>> sailing = "Test both tacks and low-Reynolds-number main-wing/tail interaction. Tail authority, stall, gust response and faulted-tab loads remain open.";
        attribute :>> recovery = "Include main wing, tail, boom, tab, actuator and any counterweight as separate mass/volume bodies. Check free, jammed and failed trim states plus sealed, flooded and draining states.";
        attribute :>> manufacturing = "Compatible in principle with printed ribs and glass skins; extra bearings, waterproof actuation, alignment and tail clearance need design.";
        attribute :>> nextEvidence = "Low-speed trim bench; unpowered and jammed-tab gust tests; wet-cycle endurance; actual rig mass/CG and compartment geometry.";
        metadata rationale : ModelingMetadata::Rationale { text = "Lead development choice based on passive trim and removing cloth/line wear mechanisms, not demonstrated Blue Dog reliability. See sail-trade.md for primary sources and limitations."; }
    }
    part camberedWing : Candidate {
        attribute :>> label = "Original cambered wing concept";
        attribute :>> membraneSail = false;
        attribute :>> aerodynamicTrim = false;
        attribute :>> concept = "Original CrescentWing manufacturing concept retained. Camber reversal and the intended trim mechanism have not yet been established; a powered whole-wing trim is only the comparison assumption.";
        attribute :>> durability = "Avoids cloth flogging but retains skin, seam, bearing and trim-drive fatigue; a camber-changing mechanism would add joints and failure modes.";
        attribute :>> energy = "Measure whole-wing moment, holding power and jam loads. A balanced pivot could reduce demand; no inherent high-power verdict is assumed.";
        attribute :>> sailing = "Measure positive and negative lift polars on both tacks. Fixed camber must not inherit the symmetric-wing model; reversal/flap geometry must be explicit if used.";
        attribute :>> recovery = "Use actual crescent/swept geometry, dry and retained-water CG, sealed volume, trim angle and failed-drive position. Manufacturing CAD is not qualified challenge-vessel geometry.";
        attribute :>> manufacturing = "Closest to the existing CAD and useful for coupons/prototypes. Benefits from fewer tail parts; exact actuator and reversal architecture remain unresolved.";
        attribute :>> nextEvidence = "Confirm intended camber/trim mechanism; inspect CAD section and stations; measure both-tack polars and drive power before quantitative comparison.";
        metadata issue : ModelingMetadata::Issue { text = "Owner clarification of original camber/trim mechanism is pending. Do not silently assume reversible camber or reject fixed camber as incapable of sailing both tacks."; }
    }
    part softSail : Candidate {
        attribute :>> label = "Triangular soft sail";
        attribute :>> membraneSail = true;
        attribute :>> aerodynamicTrim = false;
        attribute :>> concept = "Triangular woven-polyester sail on mast and boom with sheet control. Reefing/furling is a design option requiring explicit mechanism, mass and fault analysis; battens and reinforcement are not excluded.";
        attribute :>> durability = "Flogging, flutter, chafe, UV/stitching degradation and sheet wear create unattended-maintenance concerns. Durable cloth, battens and anti-chafe design can mitigate them; no lifetime failure is established.";
        attribute :>> energy = "Sheet/winch energy and holding strategy must be measured; self-locking or balanced arrangements may have low static draw. Do not assume a continuously powered servo.";
        attribute :>> sailing = "Both-tack sailing is conventional in principle; actual reefed and unreefed low-Re polars are needed. Useful benchmark for mass and performance.";
        attribute :>> recovery = "Lower membrane mass and negligible sealed cloth volume can help, but model mast/boom buoyancy, immersion drag, trapped water and sheet snagging separately.";
        attribute :>> manufacturing = "Simple sailmaking and repair, low rig-mass potential; requires sailcloth and rigging rather than printing every component. Hull FDM/glass requirement does not prohibit a soft sail.";
        attribute :>> nextEvidence = "Unattended flogging/chafe/UV exposure and sheet fault tests over declared mission hours; autonomous depower and recovery demonstration.";
        metadata rationale : ModelingMetadata::Rationale { text = "Deprioritized for the long unattended objective by engineering judgment, not rejected against a measured requirement. Still credible for a shorter Gorge test or performance benchmark."; }
    }
    analysis def TradeAssessment {
        subject candidate : Candidate;
        out attribute candidateName : String = candidate.label;
        out attribute gateCount : Integer = SequenceFunctions::size(candidate.gates);
        out attribute knownFailure : Boolean = candidate.gates->ControlFunctions::exists { in gate : Evidence; gate == Evidence::failed };
        out attribute evidenceComplete : Boolean = candidate.gates->ControlFunctions::forAll { in gate : Evidence; gate != Evidence::unknown };
        out attribute qualified : Boolean = gateCount == 7 and candidate.gates->ControlFunctions::forAll { in gate : Evidence; gate == Evidence::passed };
        out attribute requirementVerdict : String = if knownFailure ? "Failed gate" else if qualified ? "Passed declared gates" else "Inconclusive: evidence missing";
        // Explicit development policy, not an inferred failure probability or weighted score.
        return developmentDecision : String = if knownFailure ? "Resolve verified failure before selection" else
            if qualified ? "Eligible for selection; compare validated margins" else
            if candidate.aerodynamicTrim and not candidate.membraneSail ? "Lead development candidate" else
            if not candidate.membraneSail ? "Retain comparison candidate" else
            "Deprioritize for long unattended service; retain prototype benchmark";
        objective assess { require constraint { gateCount == 7 } }
    }
    analysis tailAssessment : TradeAssessment { subject :>> candidate = tailWing; }
    analysis camberAssessment : TradeAssessment { subject :>> candidate = camberedWing; }
    analysis softAssessment : TradeAssessment { subject :>> candidate = softSail; }
    dependency durabilityCriterion from TradeAssessment to BlueDogRequirements::wetMechanicalIntegrity;
    dependency stormWindCriterion from TradeAssessment to BlueDogRequirements::gorgeSurvivalWind;
    dependency stormWaveCriterion from TradeAssessment to BlueDogRequirements::oceanSurvivalWaves;
    dependency energyCriterion from TradeAssessment to BlueDogRequirements::sustainedEnergyFeasibility;
    dependency progressCriterion from TradeAssessment to BlueDogRequirements::legProgress;
    dependency capsizeCriterion from TradeAssessment to BlueDogRequirements::selfRighting;
    dependency controlCriterion from TradeAssessment to BlueDogRequirements::capsizeControlRecovery;
    dependency liftCriterion from TradeAssessment to BlueDogRequirements::liftMass;
    dependency reliabilityCriterion from TradeAssessment to BlueDogRequirements::missionSuccessProbability;
    dependency reliabilityEvidence from TradeAssessment to BlueDogRequirements::reliabilityEvidence;
    dependency architectureScope from Candidate to BlueDog::Architecture::HullAndRig;
    dependency failureReview from TradeAssessment to BlueDogDFMEA::starter::sailJam;

    part def RigBody {
        doc /* Input contract for the next geometry-based capsize model. Boat-fixed
         * x forward, y port, z up; all lengths m, mass kg, volume m3, time s.
         * Geometry must resolve wetted shape at each heel/pitch/trim; these scalar
         * properties alone do not establish a righting curve. */
        attribute component : String;
        attribute dryMassKg : Real;
        attribute dryCG : Real [3] ordered nonunique;
        attribute sealedVolumeM3 : Real;
        attribute sealedVolumeCentroid : Real [3] ordered nonunique;
        attribute floodableVolumeM3 : Real;
        attribute retainedWaterMassKg : Real;
        attribute retainedWaterCG : Real [3] ordered nonunique;
        attribute fillTimeS : Real;
        attribute drainTimeS : Real;
        attribute geometryReference : String;
        attribute geometryEvidenceAccepted : Boolean default false;
    }
    calc def BuoyancyMomentSensitivity {
        in displacedVolumeM3 : Real;
        in signedHorizontalLeverM : Real;
        in waterDensityKgM3 : Real;
        return momentNm : Real;
        waterDensityKgM3 * 9.80665 * displacedVolumeM3 * signedHorizontalLeverM
    }
    analysis buoyancyIllustration {
        doc /* Ten litres fully immersed at +/-1 m horizontal lever in freshwater.
         * This is a sensitivity example, not a candidate volume or predicted GZ. */
        out attribute positiveMomentNm : Real = BuoyancyMomentSensitivity(0.01,1,1000);
        out attribute negativeMomentNm : Real = BuoyancyMomentSensitivity(0.01,-1,1000);
    }
    dependency geometryForRecovery from RigBody to BlueDogRequirements::selfRighting;
}
package BlueDogSailTradeDocuments {
    private import DocumentQueries::*;
    calc def Candidates :> Query { Named(qualifiedName = ("BlueDogSailTrade::tailWing", "BlueDogSailTrade::camberedWing", "BlueDogSailTrade::softSail")) }
    calc def Concepts :> Query { Project(source = Candidates(), columns = (Column(name = "Candidate", path = "label"), Column(name = "Definition", path = "concept"))) }
    calc def Durability :> Query { Project(source = Candidates(), columns = (Column(name = "Candidate", path = "label"), Column(name = "Durability and reliability", path = "durability"), Column(name = "Energy", path = "energy"))) }
    calc def Recovery :> Query { Project(source = Candidates(), columns = (Column(name = "Candidate", path = "label"), Column(name = "Sailing performance", path = "sailing"), Column(name = "Recovery geometry", path = "recovery"))) }
    calc def Manufacturing :> Query { Project(source = Candidates(), columns = (Column(name = "Candidate", path = "label"), Column(name = "Construction", path = "manufacturing"), Column(name = "Next evidence", path = "nextEvidence"))) }
    calc def Results :> Query { Project(source = Named(qualifiedName = ("BlueDogSailTrade::tailAssessment", "BlueDogSailTrade::camberAssessment", "BlueDogSailTrade::softAssessment")), columns = (Column(name = "Candidate", path = "candidateName"), Column(name = "Development decision", path = "developmentDecision"), Column(name = "Requirement verdict", path = "requirementVerdict"))) }
    calc def Traces :> Query { Project(source = WhereType(source = Descendants(source = Named(qualifiedName = "BlueDogSailTrade")), type = "Dependency"), columns = (Column(name = "Analysis element", cell = { in row : KerML::Root::Dependency; row.client }), Column(name = "Requirement / architecture", cell = { in row : KerML::Root::Dependency; row.supplier }))) }
    part def Report :> Document {
        attribute redefines title = "Sail architecture trade study";
        part scope : Paragraph { attribute redefines text = "Preliminary qualitative development selection. All physical requirement gates remain unknown. No numeric reliability rates or arbitrary weighted scores are assigned. The lead concept is not mission-qualified; the soft sail is deprioritized, not proven noncompliant. Sources and decision rationale: sail-trade.md."; }
        part decision : Section { attribute redefines title = "Native analysis conclusion"; part rows : Table { calc rows : Results; } }
        part concepts : Section { attribute redefines title = "Candidate definitions"; part rows : Table { calc rows : Concepts; } }
        part durability : Section { attribute redefines title = "Durability and energy"; part rows : Table { calc rows : Durability; } }
        part recovery : Section { attribute redefines title = "Performance and capsize"; part rows : Table { calc rows : Recovery; } }
        part construction : Section { attribute redefines title = "Manufacturing and evidence"; part rows : Table { calc rows : Manufacturing; } }
        part trace : Section { attribute redefines title = "Requirement and architecture links"; part rows : Table { calc rows : Traces; } }
    }
}
