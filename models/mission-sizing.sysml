package BlueDogMissionSizing {
    private import ScalarValues::*;
    doc /* Two-metre waterline baseline; route profiles are illustrative. Separate
     * assemblies and construction recipes are design choices, not mission evidence. */
    part def Policy {
        attribute waterline : Real = 2;
        attribute assemblyLimit : Real = 15;
        attribute attachmentMass : Real = 0.6;
        attribute ribWall : Real = 0.0008;
        attribute ribPitch : Real = 0.04;
        attribute cgBelowBottom : Real = 0.02;
        attribute maneuverRetention : Real = 0.95;
        attribute routeWeights : Real [2] ordered nonunique = (0.5, 0.5);
        attribute currents : Real [2] ordered nonunique = (0.5, 1.0);
        attribute winds : Real [2] ordered nonunique = (5, 8);
        attribute legDistance : Real = 100000;
        attribute allowedHours : Real = 72;
        attribute targetMargin : Real = 0.10;
    }
    part policy : Policy;
    analysis Inputs {
        out attribute extraParameters : Real [*] ordered nonunique = (policy.assemblyLimit, policy.attachmentMass, policy.ribWall, policy.ribPitch, policy.cgBelowBottom);
        out attribute routeParameters : Real [*] ordered nonunique = (policy.maneuverRetention, policy.routeWeights, policy.currents, policy.legDistance, policy.allowedHours);
        out attribute routeWinds : Real [2] ordered nonunique = policy.winds;
        out attribute waterline : Real = policy.waterline;
        out attribute targetMargin : Real = policy.targetMargin;
    }
    requirement def LowMassCenter {
        doc /* The loaded center of gravity shall lie at least 20 mm below the hull bottom in the preliminary sizing screen. */
        metadata workStatus : ModelingMetadata::StatusInfo { status = ModelingMetadata::StatusKind::open; }
        comment conditions /* A proposed conservative allocation, not a large-angle righting or capsize acceptance test. Fixed equipment and attachment allowance are at the waterline. Both loading extremes require later geometry-based analysis. */
        attribute clearance : Real;
        require constraint acceptance { clearance >= policy.cgBelowBottom }
    }
    requirement lowMassCenter : LowMassCenter;
    dependency stabilityBasis from lowMassCenter to BlueDogRequirements::selfRighting;
    calc def EvaluateCase {
        in d : Real [*] ordered nonunique;
        in p : Real [*] ordered nonunique;
        in s : Real [*] ordered nonunique;
        // Architecture selector p98: zero is conventional 8% infill; one is ribs.
        // Transverse full-section ribs occupy wall/pitch of the foil core volume.
        // No printed stiffness credit; glass skins still carry global bending.
        attribute parameters : Real [*] ordered nonunique = (1..97)->ControlFunctions::collect { in i : Integer;
            if i == 12 ? p#(i) + p#(100) else
            if i == 61 ? 1.0 else if i == 62 ? 1.0 else if i == 63 ? 0.0 else
            if i == 83 ? (if p#(98) > 0.5 ? p#(101) / p#(102) else p#(i)) else p#(i) };
        attribute r : Real [*] ordered nonunique = BlueDogOpenSizing::EvaluateCase(d, parameters, s);
        attribute battery : Real = d#(11)/p#(14);
        attribute wing : Real = r#(82);
        attribute body : Real = r#(51) - battery - wing;
        attribute mass : Real = r#(50);
        attribute draft : Real = r#(53);
        // Recover the corrected mass moment from the exact same hydrostatic model.
        attribute waterplaneI : Real = p#(8)*d#(1)*d#(2)*d#(2)*d#(2)/12;
        attribute buoyancyMoment : Real = -p#(3)*(d#(1)*d#(2)*draft*p#(7)*draft/2 + d#(9)/p#(4)*(draft+d#(6)));
        attribute weightMoment : Real = p#(3)*waterplaneI + buoyancyMoment - r#(11)*mass;
        attribute cg : Real = weightMoment/mass;
        return values : Real [*] ordered nonunique;
        (r#(1),
         r#(2),
         r#(3),
         r#(4),
         1.0,
         r#(6),
         (p#(99)-NumericalFunctions::max(body,NumericalFunctions::max(wing,battery)))/p#(99),
         r#(8),
         r#(9),
         r#(10),
         r#(11),
         r#(12),
         r#(13),
         r#(14),
         r#(15),
         r#(16),
         r#(17),
         r#(18),
         r#(19),
         r#(20),
         r#(21),
         r#(22),
         r#(23),
         r#(24),
         r#(25),
         r#(26),
         r#(27),
         r#(28),
         r#(29),
         r#(30),
         r#(31),
         r#(32),
         r#(33),
         r#(34),
         r#(35),
         r#(36),
         r#(37),
         r#(38),
         r#(39),
         r#(40),
         r#(41),
         r#(42),
         r#(43),
         r#(44),
         r#(45),
         r#(46),
         (-draft-cg-p#(103))/0.1,
         r#(47),
         r#(48),
         r#(49),
         r#(50),
         r#(51),
         r#(52),
         r#(53),
         r#(54),
         r#(55),
         r#(56),
         r#(57),
         r#(58),
         r#(59),
         r#(60),
         r#(61),
         r#(62),
         r#(63),
         r#(64),
         r#(65),
         r#(66),
         r#(67),
         r#(68),
         r#(69),
         r#(70),
         r#(71),
         r#(72),
         r#(73),
         r#(74),
         r#(75),
         r#(76),
         r#(77),
         r#(78),
         r#(79),
         r#(80),
         r#(81),
         r#(82),
         r#(83),
         r#(84),
         r#(85),
         r#(86),
         r#(87),
         r#(88),
         r#(89),
         body,
         battery,
         cg,
         -draft-cg)
    }
    calc def Route {
        in v : Real [4] ordered nonunique;
        in q : Real [7] ordered nonunique;
        // Four points: 5 m/s up/down, 8 m/s up/down. Easterly aligned wind.
        // Currents are along-route ground-frame values; winds are water-relative.
        attribute up : Real = q#(2)*(q#(1)*v#(1)-q#(4)) + q#(3)*(q#(1)*v#(3)-q#(5));
        attribute down : Real = q#(2)*(q#(1)*v#(2)+q#(4)) + q#(3)*(q#(1)*v#(4)+q#(5));
        attribute hours : Real = if up > 0 and down > 0 ? q#(6)/up/3600 + q#(6)/down/3600 else 1000000.0;
        attribute margin : Real = NumericalFunctions::min(up/0.5-1, NumericalFunctions::min(down/0.5-1, q#(7)/hours-1));
        return result : Real [4] ordered nonunique;
        (up, down, hours, margin)
    }
    dependency routeProgress from Route to BlueDogRequirements::legProgress;
    dependency routeDuration from Route to BlueDogRequirements::passageDuration;
    dependency assemblyHandling from EvaluateCase to BlueDogRequirements::liftMass;
    dependency manufacturing from EvaluateCase to BlueDogStructure::hybridConstruction;
    dependency structuralChecks from EvaluateCase to BlueDogStructure::structuralIntegrity;
    dependency recoveryScreen from EvaluateCase to lowMassCenter;
    part def Evidence {
        attribute numericalFit : Boolean = false;
        attribute fullAngleStability : Boolean = false;
        attribute capsizeReleases : Boolean = false;
        attribute controlRecovery : Boolean = false;
        attribute constructionProof : Boolean = false;
        attribute polarValidation : Boolean = false;
        attribute routeEvidence : Boolean = false;
    }
    analysis def Readiness {
        subject evidence : Evidence;
        return supported : Boolean = evidence.numericalFit and evidence.fullAngleStability and evidence.capsizeReleases and evidence.controlRecovery and evidence.constructionProof and evidence.polarValidation and evidence.routeEvidence;
    }
    part pendingEvidence : Evidence;
    analysis currentReadiness : Readiness { subject :>> evidence = pendingEvidence; }
    dependency capsizeGate from Readiness to BlueDogRequirements::selfRighting;
    dependency controlGate from Readiness to BlueDogRequirements::capsizeControlRecovery;
    dependency environmentGate from Readiness to BlueDogRequirements::cruiseEvidence;
}
