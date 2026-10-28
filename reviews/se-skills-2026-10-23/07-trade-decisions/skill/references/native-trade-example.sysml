// Synthetic mechanism example only. metric is an artificial common scale to
// minimize, not Blue Dog data, utility weights, costs or physical measurements.
// Supply ONLY alternatives already assessed as admissible for the proposed use.
package DecisionMechanismExample {
    private import ScalarValues::*;
    private import TradeStudies::*;
    part def Option { attribute metric : Real [1]; }
    part a : Option { attribute :>> metric = 10; }
    part b : Option { attribute :>> metric = 10; }
    analysis compare : TradeStudy {
        subject : Option [1..*] = (a,b);
        objective : MinimizeObjective;
        calc :>> evaluationFunction {
            in part option :>> alternative : Option;
            return :>> result : Real = option.metric;
        }
        return part :>> selectedAlternative : Option;
    }
    // Inspect both evaluations and tied flags. First selection is not a
    // justified preference or authorized project decision. Missing metric is
    // an input error, not zero. Try b=9 and b=11 to expose order sensitivity.
}
