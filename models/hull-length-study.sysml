package BlueDogHullLengthStudy {
    private import ScalarValues::*;
    private import BlueDogDesignSearch::settings;
    analysis def LengthInputs {
        doc /* Remove the exploratory length cap only. The retained body-mass
         * model implies bodyMass >= shellMass >= 2 * skin_kg_m2 * length * beam.
         * With beam >= settings.lower#(2), no feasible design can exceed this ceiling.
         * Other mass and hardware constraints still apply, often more tightly. */
        out attribute massImpliedLengthCeiling : Real = settings.assembly_limit_kg / (2 * settings.skin_kg_m2 * settings.lower#(2));
        out attribute relaxedUpper : Real [*] ordered nonunique = (massImpliedLengthCeiling,
            (2..SequenceFunctions::size(settings.upper))->ControlFunctions::collect { in i : Integer; settings.upper#(i) });
        out attribute sweepLengths : Real [*] ordered = (2, 3.5, 5, 8, 12, 20);
    }
    analysis limits : LengthInputs;
}
package BlueDogHullLengthDocuments {
    private import DocumentQueries::*;
    calc def Cases :> Query {
        Named(qualifiedName = ("BlueDogHullLengthResults::full_envelopeAudit", "BlueDogHullLengthResults::nominal_5msAudit",
            "BlueDogHullLengthResults::fixed_2Audit", "BlueDogHullLengthResults::fixed_3_5Audit", "BlueDogHullLengthResults::fixed_5Audit",
            "BlueDogHullLengthResults::fixed_8Audit", "BlueDogHullLengthResults::fixed_12Audit", "BlueDogHullLengthResults::fixed_20Audit"))
    }
    calc def Summary :> Query {
        Project(source = Cases(), columns = (
            Column(name = "Study", path = "caseLabel"), Column(name = "Waterline length (m)", path = "waterlineLength"),
            Column(name = "Balanced and hardware feasible", path = "operatingFeasible"),
            Column(name = "Worst upstream VMG (m/s)", path = "worstGroundVMG"),
            Column(name = "Numerical mission fit", path = "numericalFeasible"),
            Column(name = "Supported design", path = "supportedDesign")))
    }
    part def LengthReport :> Document {
        attribute redefines title = "Hull length relaxation: native replay";
        part guide : Paragraph { part link : Link { attribute redefines text = "Method and interpretation"; attribute redefines target = "design-search.md#does-a-longer-hull-solve-it"; } }
        part context : Paragraph { attribute redefines text = "Only the length bound changes. The numerical search uses a mass-implied ceiling, not the former 3.5 m exploratory cap. Fixed-length rows cover the nominal 5 m/s wind cases only. Ignore VMG for any row that is not balanced and hardware feasible. A failed local search is not a global infeasibility proof."; }
        part values : Table { calc rows : Summary; }
    }
}
