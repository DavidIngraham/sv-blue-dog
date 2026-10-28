"""Native model regression helpers; publication builds use tools.publishing."""
from tools.boat_analysis.model.runtime import ROOT, model_files, native as execute
from markdown_it import MarkdownIt
MODELS = model_files()

def native(*args, models=None):
    if any(arg in ('-render', '-render-document', '-render-documents') for arg in args):
        args = (*args, '-render-show', 'qualifiers,typings')
    files = tuple(models) if models is not None else MODELS
    views = ROOT / '.tools/regression-inline-views.sysml'
    bodies = [token.content for path in sorted((ROOT/'docs').rglob('*.md'))
              for token in MarkdownIt().parse(path.read_text(encoding='utf-8'))
              if token.type == 'fence' and token.info.startswith('sysml-view ')]
    views.parent.mkdir(exist_ok=True)
    views.write_text('\n'.join(bodies), encoding='utf-8')
    return execute(*args, models=(*files, ROOT/'tools/publishing/reference.sysml', ROOT/'tests/fixtures/regression-views.sysml', views))

def native_graph():
    return native("-render", "BlueDogViews::requirements", "-render-form", "dot")

def native_register():
    return native("-render-document", "BlueDogDocuments::RequirementsRegister")

def native_recovery_trade():
    arguments = []
    for candidate in ("waterExample", "airExample"):
        name = f"BlueDog::Analyses::RecoveryPropulsionTrade::{candidate}"
        arguments.extend(("-instantiate", name, "-analysis",
                          f"BlueDog::Analyses::RecoveryPropulsionTrade::RecoverySizing {name}"))
    return native(*arguments, "-json")

def native_energy_case():
    return native("-instantiate", "BlueDog::Configurations::Examples::Energy::sailing", "-analysis",
                  "BlueDog::Analyses::Energy::BudgetRollup BlueDog::Configurations::Examples::Energy::sailing",
                  "-instantiate", "BlueDog::Configurations::Examples::Energy::campaign", "-analysis",
                  "BlueDog::Analyses::Energy::SustainedOperation BlueDog::Configurations::Examples::Energy::campaign", "-json")

def native_sailing_case():
    arguments = []
    for example, analysis in (
        ("upstreamHeadwind", "PolarDemandAndHullScreen"),
        ("upstreamTailwind", "PolarDemandAndHullScreen"),
        ("downstreamHeadwind", "PolarDemandAndHullScreen"),
        ("downstreamTailwind", "PolarDemandAndHullScreen"),
        ("oceanIllustration", "PolarDemandAndHullScreen"),
        ("gorgeWesterly", "PolarVoyageAssessment"),
        ("gorgeEasterly", "PolarVoyageAssessment"),
        ("upstreamHeadwind", "SailingSensitivity"),
    ):
        subject = f"BlueDog::Configurations::Examples::Sailing::{example}"
        arguments.extend(("-instantiate", subject, "-analysis", f"BlueDog::Analyses::Sailing::{analysis} {subject}"))
    return native(*arguments, "-json")
