// A read-only view of model-authored risks. No ratings are inferred in the browser.
export const statusName = risk => (risk.status || 'Unspecified').split('::').pop();
export function filterRisks(risks, {kind='', status='', query=''}={}) {
 const needle=query.trim().toLowerCase();
 return risks.filter(r=>(!kind || r.kind===kind) && (!status || statusName(r)===status) &&
  (!needle || Object.values(r).join(' ').toLowerCase().includes(needle)));
}
export function groupRisks(risks) {
 return [...new Set(risks.map(r=>r.kind))].sort().map(kind=>({kind, risks:risks.filter(r=>r.kind===kind)}));
}
export function validateData(data) {
 if(data.version!==1 || !Array.isArray(data.risks) || !Array.isArray(data.likelihood) || !Array.isArray(data.consequence)) throw Error('Unsupported risk data');
 const ids=new Set();
 for(const r of data.risks) {
  if(!r.identifier || ids.has(r.identifier) || !r.kind || !r.statement || !r.status) throw Error('Incomplete risk record');
  if(r.likelihood && !data.likelihood.includes(r.likelihood) || r.consequence && !data.consequence.includes(r.consequence)) throw Error('Unknown rating');
  ids.add(r.identifier);
 }
 return data;
}
const riskBand = (data,risk) => data.bands?.[data.likelihood.indexOf(risk.likelihood)]?.[data.consequence.indexOf(risk.consequence)] || '';
const title = value => value.charAt(0).toUpperCase()+value.slice(1);
let sequence=0;
export async function renderRiskExplorer(root, url) {
 const response=await fetch(url,{signal:AbortSignal.timeout(20000)});
 if(!response.ok) throw Error(`Risk data returned HTTP ${response.status}`);
 mountRiskExplorer(root,validateData(await response.json()));
}
export function mountRiskExplorer(root,data) {
 validateData(data);
 if(!document.querySelector('link[data-risk-explorer]')) {
  const css=document.createElement('link');css.rel='stylesheet';css.href=new URL('./risk-explorer.css',import.meta.url);css.dataset.riskExplorer='';document.head.append(css);
 }
 root.className='risk-explorer';root.replaceChildren();
 const prefix=`risk-explorer-${++sequence}`;
 const el=(tag,text,className)=>{const node=document.createElement(tag);if(text!==undefined)node.textContent=text;if(className)node.className=className;return node;};
 const heading=el('h3','Risk explorer');root.append(heading);
 root.append(el('p','Select a risk ID to read its assessment and next action. Each risk type has a separate cube.','risk-help'));
 const controls=el('div',undefined,'risk-filters');root.append(controls);
 function select(label,values) {
  const wrap=el('label',label), input=el('select');
  const all=el('option',`All ${label==='Risk type'?'types':'statuses'}`);all.value='';input.append(all);
  for(const value of values){const option=el('option',title(value));option.value=value;input.append(option);}
  wrap.append(input);controls.append(wrap);return input;
 }
 const kind=select('Risk type',[...new Set(data.risks.map(r=>r.kind))].sort());
 const status=select('Status',[...new Set(data.risks.map(statusName))].sort());
 const searchLabel=el('label','Search risks'),search=el('input');search.type='search';search.placeholder='ID, description or evidence';searchLabel.append(search);controls.append(searchLabel);
 const reset=el('button','Clear filters');reset.type='button';controls.append(reset);
 const count=el('p',undefined,'risk-count');count.setAttribute('role','status');root.append(count);
 const cubes=el('div',undefined,'risk-cubes');root.append(cubes);
 const detail=el('section',undefined,'risk-detail');detail.id=prefix+'-detail';detail.setAttribute('aria-label','Selected risk');root.append(detail);
 let selected=null;
 function showDetail(focus=false) {
  detail.replaceChildren();
  const risk=data.risks.find(r=>r.identifier===selected);
  if(!risk){detail.append(el('p','Select a risk in a cube to see its description, evidence and reduction action.'));return;}
  const h=el('h4',`${risk.identifier} · ${title(risk.area)}`);h.tabIndex=-1;detail.append(h);
  detail.append(el('p',`${title(risk.kind)} · ${title(statusName(risk))} · ${risk.likelihood || 'Unassessed'} / ${risk.consequence || 'Unassessed'} · ${risk.confidence || 'Unassessed'} confidence${riskBand(data,risk) ? ' · '+title(riskBand(data,risk))+' risk' : ''}`,'risk-summary'));
  const list=el('dl');detail.append(list);
  const fields=[['Risk description','statement'],['Consequence if unresolved','effect'],['Assessment basis','basis'],['Evidence gap','uncertainty'],['Work priority','priority'],['Why investigate','priorityRationale'],['Reduction action','reductionAction'],['Closure evidence','closureEvidence'],['Disposition','disposition'],['Assessment scope','scope'],['Assessed on','assessedOn'],['Assessor','assessor'],['Owner','owner']];
  for(const [label,key] of fields)if(risk[key])list.append(el('dt',label),el('dd',risk[key]));
  if(risk.evidence){
   list.append(el('dt','Supporting evidence'));const evidence=el('dd');
   for(const path of risk.evidence.split(';').map(p=>p.trim()).filter(Boolean)){
    const line=el('div');
    if(/^(models|docs|evidence|tests)\/[\w./-]+$/.test(path) && !path.split('/').includes('..') && /^[a-f0-9]{40}$/.test(data.revision)){
     const link=el('a',path);link.href=`https://github.com/DavidIngraham/sv-blue-dog/blob/${data.revision}/${path}`;line.append(link);
    }else line.textContent=path;
    evidence.append(line);
   }
   list.append(evidence);
  }
  const back=el('a','Back to cubes');back.href='#'+prefix+'-cubes';back.onclick=event=>{event.preventDefault();cubes.scrollIntoView({block:'start'});cubes.focus({preventScroll:true});};detail.append(back);
  if(focus){detail.scrollIntoView({block:'start'});h.focus({preventScroll:true});}
 }
 cubes.id=prefix+'-cubes';cubes.tabIndex=-1;
 function riskLink(risk){
  const link=el('a',risk.identifier,'risk-point');link.href='#'+detail.id;link.dataset.riskId=risk.identifier;
  link.setAttribute('aria-label',`${risk.identifier}: ${risk.area}; show risk details`);
  if(selected===risk.identifier)link.setAttribute('aria-current','true');
  link.onclick=event=>{event.preventDefault();selected=risk.identifier;for(const p of cubes.querySelectorAll('.risk-point')){if(p.dataset.riskId===selected)p.setAttribute('aria-current','true');else p.removeAttribute('aria-current');}showDetail(true);};
  return link;
 }
 function update(){
  const visible=filterRisks(data.risks,{kind:kind.value,status:status.value,query:search.value});
  if(!visible.some(r=>r.identifier===selected))selected=null;
  count.textContent=`${visible.length} of ${data.risks.length} risks shown`;cubes.replaceChildren();
  if(!visible.length)cubes.append(el('p','No risks match these filters. Clear filters to show the inventory.'));
  for(const group of groupRisks(visible)){
   const section=el('section',undefined,'risk-kind');section.append(el('h4',title(group.kind)+' risk cube'));
   const scroll=el('div',undefined,'risk-grid-scroll');scroll.tabIndex=0;scroll.setAttribute('aria-label',`${title(group.kind)} risk cube; scroll horizontally on narrow screens`);
   const grid=el('table',undefined,'risk-grid');grid.append(el('caption','Likelihood of redesign or scope restriction ↑ · Consequence if unresolved →'));
   const head=el('thead'),hr=el('tr');hr.append(el('th','Likelihood / Consequence'));
   for(const value of data.consequence){const th=el('th',value);th.scope='col';hr.append(th);}head.append(hr);grid.append(head);
   const body=el('tbody');
   for(const likelihood of [...data.likelihood].reverse()){
    const row=el('tr'),th=el('th',likelihood);th.scope='row';row.append(th);
    for(const consequence of data.consequence){const cell=el('td');const entries=group.risks.filter(r=>r.likelihood===likelihood&&r.consequence===consequence);const band=riskBand(data,{likelihood,consequence});if(['low','moderate','high'].includes(band)){cell.className='risk-band-'+band;cell.setAttribute('aria-label',`${likelihood}, ${consequence}: ${band} risk`);cell.title=title(band)+' risk';}for(const r of entries)cell.append(riskLink(r));row.append(cell);}body.append(row);
   }
   grid.append(body);scroll.append(grid);section.append(scroll);
   const unknown=group.risks.filter(r=>!r.likelihood||!r.consequence);
   if(unknown.length){const p=el('p','Unassessed: ');for(const r of unknown)p.append(riskLink(r));section.append(p);}
   if(data.bands){const legend=el('div',undefined,'risk-legend');for(const band of ['low','moderate','high'])legend.append(el('span',title(band)+' risk','risk-band-'+band));section.append(legend);}
   section.append(el('p','Qualitative judgments; not probabilities of accidents. Demonstrated means a current limitation already restricts the conclusion. No residual-risk acceptance implied.','risk-help'));
   cubes.append(section);
  }
  showDetail();
 }
 kind.onchange=status.onchange=search.oninput=update;
 reset.onclick=()=>{kind.value=status.value=search.value='';update();};update();
}
