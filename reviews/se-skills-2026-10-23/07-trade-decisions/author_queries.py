"""Compose native projections; original open questions/owners keep their own source."""
from tools.boat_analysis.model.runtime import ROOT
p=ROOT/'tools/publishing/reference.sysml';text=p.read_text();start=text.index('package BlueDogDecisionDocuments {');tail=text[start:];criteria=tail[tail.index('    calc def Criteria'):tail.index('    part def DecisionRegister')]
lines=['package BlueDogDecisionDocuments {','    private import DocumentQueries::*;']
base='BlueDogDecisionContext::Context::'
columns=[('Record','qualifiedName'),('Kind',base+'kind'),('Question',base+'decisionQuestion'),('Scope',base+'scope'),('Responsible role',base+'ownerRole'),('Mandatory basis',base+'criteriaBasis'),('Comparison basis',base+'comparisonBasis'),('Reopening trigger',base+'reopenTrigger'),('Recorded disposition','disposition'),('Needed evidence','evidenceNeeded'),('Actual disposition record',base+'dispositionRecord'),('Actual authority',base+'authorityIdentity'),('Actual decision date',base+'decisionDate'),('Implementation evidence',base+'implementationEvidence'),('Open-question acceptance','accepted')]
for query,root,kind in [('WorkingRecords','BlueDogDesignDecisions','Decision'),('OpenRecords','BlueDogRequirementDecisions','OpenDecision')]:
    lines+=['    calc def '+query+' :> Query {','        Project(source = WhereType(source = WhereType(source = Descendants(source = Named(qualifiedName = "'+root+'")), type = "PartUsage"), type = "'+root+'::'+kind+'"), columns = (']
    cols=[(label,('question' if label=='Question' else 'owner' if label=='Responsible role' else path) if query=='OpenRecords' else path) for label,path in columns if not (query=='WorkingRecords' and label=='Open-question acceptance') and not (query=='OpenRecords' and label=='Recorded disposition')]
    lines.append(',\n'.join('            Column(name = "'+label+'", path = "'+path+'")' for label,path in cols)+'))')
    lines.append('    }')
lines+=[criteria,'    part def DecisionRegister :> Document {','        attribute redefines title = "Decision questions, dispositions and reopening conditions";','        part working : Table { calc rows : WorkingRecords; }','        part open : Table { calc rows : OpenRecords; }','    }','    part def CriterionRegister :> Document {','        attribute redefines title = "Declared rig evidence groups and requirement basis";','        part criteria : Table { calc rows : Criteria; }','        part basis : Table { calc rows : Basis; }','    }','}']
p.write_text(text[:start]+'\n'.join(lines)+'\n')
