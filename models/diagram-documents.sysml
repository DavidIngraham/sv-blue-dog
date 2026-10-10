package BlueDogDiagramDocuments {
    private import DocumentQueries::*;
    part def RequirementsDiagram :> Document {
        attribute redefines title = "Requirement derivation";
        part diagram : Diagram {
            attribute redefines direction = "BT";
            ref redefines source = BlueDogViews::requirements;
        }
    }
    part def ArchitectureDiagram :> Document {
        attribute redefines title = "Boat definition and composition";
        part diagram : Diagram {
            attribute redefines direction = "TB";
            ref redefines source = BlueDogArchitectureViews::architecture;
        }
    }
    part def ContextDiagram :> Document {
        attribute redefines title = "Mission context";
        part diagram : Diagram {
            attribute redefines direction = "TB";
            ref redefines source = BlueDogArchitectureViews::context;
        }
    }
    part def DetailDiagram :> Document {
        attribute redefines title = "Detailed composition";
        part diagram : Diagram {
            attribute redefines direction = "TB";
            ref redefines source = BlueDogArchitectureViews::detail;
        }
    }
    part def UseCasesDiagram :> Document {
        attribute redefines title = "Use cases and requirements";
        part diagram : Diagram {
            attribute redefines direction = "TB";
            ref redefines source = BlueDogUseCaseViews::operations;
        }
    }
}
