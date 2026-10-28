package BlueDogConfigurationDocuments {
    private import DocumentQueries::*;
    calc def Contexts :> Query {
        Project(source = WhereType(source = Descendants(source = Named(qualifiedName = "BlueDogConfigurationManagement")),
            type = "BlueDogConfigurationManagement::ContextRecord"), columns = (
            Column(name = "ID", path = "identifier"), Column(name = "Role", path = "role"),
            Column(name = "Represented subject", path = "representedSubject"),
            Column(name = "Intended use", path = "intendedUse"), Column(name = "Revision basis", path = "revisionBasis")))
    }
    calc def Installation :> Query {
        Project(source = Named(qualifiedName = "BlueDogConfigurationManagement::ic01Installation"), columns = (
            Column(name = "Planned design", path = "design"), Column(name = "Planned assembly", path = "assembly"),
            Column(name = "Actual article", path = "articleId"), Column(name = "Hardware revision", path = "hardwareRevision"),
            Column(name = "Software/data revision", path = "softwareDataRevision"), Column(name = "Procedure revision", path = "procedureRevision"),
            Column(name = "Reconciliation record", path = "reconciliationRecord"),
            Column(name = "Reconciled", path = "configurationReconciled")))
    }
    calc def Scopes :> Query {
        Project(source = WhereType(source = Descendants(source = Named(qualifiedName = "BlueDogConfigurationManagement::ic01")),
            type = "BlueDogConfigurationManagement::ResourceScope"), columns = (
            Column(name = "Scope", path = "label"), Column(name = "Quantity kind", path = "quantityKind"),
            Column(name = "Configuration", path = "configuration"), Column(name = "Boundary", path = "boundary"),
            Column(name = "Mode", path = "mode"), Column(name = "Owner role", path = "ownerRole"),
            Column(name = "Basis", path = "basis"), Column(name = "Closure evidence", path = "closureEvidenceNeeded"),
            Column(name = "Ready preconditions", path = "ready")))
    }
    calc def Allocations :> Query {
        Project(source = WhereType(source = Descendants(source = Named(qualifiedName = "BlueDogConfigurationManagement::ic01")),
            type = "BlueDogConfigurationManagement::ResourceScope"), columns = (
            Column(name = "Scope", path = "label"), Column(name = "Mass allowance", path = "massAllocation"),
            Column(name = "Average/active power allowance", path = "averagePowerAllocation"), Column(name = "Peak bound", path = "peakPowerBound"),
            Column(name = "Nameplate energy", path = "nameplateEnergy"), Column(name = "Departure energy", path = "departureEnergy"),
            Column(name = "Acquisition latency", path = "acquisitionLatency"), Column(name = "Assessment latency", path = "assessmentLatency"),
            Column(name = "Command latency", path = "commandLatency"), Column(name = "Maneuver duration", path = "maneuverDuration")))
    }
    part def ConfigurationRegister :> Document {
        attribute redefines title = "Configuration contexts and planned installation";
        part contexts : Table { calc rows : Contexts; }
        part installation : Table { calc rows : Installation; }
    }
    part def BudgetRegister :> Document {
        attribute redefines title = "IC-01 accounting scopes and allocated quantities";
        part scopes : Table { calc rows : Scopes; }
        part values : Table { calc rows : Allocations; }
    }
}
