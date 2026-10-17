package BlueDogFailureModeling {
    private import ScalarValues::*;
    doc /* Project event propositions and Boolean gates used with standard CauseAndEffect connections. Unknown occurrence values remain unbound. No probabilities, independence or physical acceptance are inferred. */
    occurrence def Event { attribute description : String; attribute present : Boolean; }
    occurrence def AnyOf :> Event {
        doc /* OR: any listed input establishes the proposition in the declared exposure interval. */
        ref occurrence inputs : Event [1..*];
        attribute :>> present = inputs->ControlFunctions::exists { in x : Event; x.present };
    }
    occurrence def AllOf :> Event {
        doc /* AND: all listed inputs coexist in the declared exposure interval. Boolean conjunction does not imply temporal order or statistical independence. */
        ref occurrence inputs : Event [1..*];
        attribute :>> present = SequenceFunctions::size(inputs) > 0 and inputs->ControlFunctions::forAll { in x : Event; x.present };
    }
    analysis def Evaluate { subject proposition : Event; out attribute present : Boolean = proposition.present; }
}
