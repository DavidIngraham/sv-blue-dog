package DeclarativeStudyFixtures {
    private import ScalarValues::*;
    doc /* Synthetic native execution contracts for declarative study reuse.
     * Values test software behavior and do not represent a physical design. */
    part def Configuration {
        attribute capacity : Real;
        attribute label : String;
    }
    part baseline : Configuration {
        attribute :>> capacity = 12;
        attribute :>> label = "Baseline configuration";
    }
    part alternate : Configuration {
        attribute :>> capacity = 20;
        attribute :>> label = "Alternate configuration";
    }
    analysis def Scale {
        subject target : Configuration;
        in attribute gain : Real;
        out attribute product : Real = target.capacity * gain;
        out attribute label : String = target.label;
        assert constraint positiveGain { gain > 0 }
    }
    package Cases {
        // Reverse lexical declaration order makes deterministic sorting observable.
        analysis zeta : Scale {
            subject :>> target = baseline;
            in attribute :>> gain = 2;
        }
        analysis alpha : Scale {
            subject :>> target = baseline;
            in attribute :>> gain = 1;
        }
    }
    analysis inputOnly {
        subject context : Configuration = baseline;
        in attribute x : Real;
        out attribute value : Real = x;
    }
    analysis failedObjective {
        out attribute value : Real = -1;
        assert constraint positive { value > 0 }
    }
    analysis dimensionalInput {
        subject context : Configuration = baseline;
        in attribute distance : ISQ::LengthValue;
        out attribute doubled : ISQ::LengthValue = distance * 2;
    }
    analysis exactValues {
        out attribute ratio : Real = 1 / 3;
        out attribute text : String = "1/3 is a label";
        out attribute accepted : Boolean = false;
    }
}
