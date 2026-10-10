"""Native sail concept assessment and document publication."""
import json
from .render_requirements import MODELS, ROOT, native

MODEL = ROOT/'models/sail-trade.sysml'
MODELS_TRADE = MODELS+(MODEL,)
CASES = ('tailAssessment','camberAssessment','softAssessment','buoyancyIllustration')


def publication_outputs():
    args=[]
    for case in CASES:args+=['-analysis','BlueDogSailTrade::'+case]
    audit=native(*args,'-json',models=MODELS_TRADE)
    data=json.loads(audit)
    if data['status']!='holds' or data.get('diagnostics'):raise ValueError('Sail trade native analysis failed')
    report=native('-render-document','BlueDogSailTradeDocuments::Report',models=MODELS_TRADE)
    return {ROOT/'docs/sail-trade-results.md':report,ROOT/'docs/analysis/sail-trade.json':audit}


if __name__=='__main__':
    for path,contents in publication_outputs().items():path.write_text(contents,encoding='utf-8')
