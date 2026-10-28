// Interactive geometry only. Native sizing contracts supply every editable value.
const labels={length_m:'Hull length (m)',beam_m:'Hull beam (m)',bottom_depth_m:'Bottom depth (m)',deck_height_m:'Deck height (m)',sail_m2:'Wing area (m²)',sail_AR:'Wing aspect ratio',camber_scale:'Wing camber scale',wing_thickness_scale:'Wing thickness scale',mast_fraction:'Mast chord fraction',mast_x_fraction:'Mast position / hull length',keel_m2:'Keel area (m²)',keel_span_m:'Keel span (m)',rudder_m2:'Rudder area (m²)',rudder_span_m:'Rudder span (m)',rudder_arm_fraction:'Rudder arm / hull length',ballast_kg:'Ballast (kg)',battery_Wh:'Battery capacity (Wh)',panel_m2:'Solar panel area (m²)',wing_torque_Nm:'Wing drive torque (N·m)',rudder_torque_Nm:'Rudder drive torque (N·m)',hull_glass_kg_m2:'Hull dry glass (kg/m²)',wing_glass_kg_m2:'Wing dry glass (kg/m²)',keel_glass_kg_m2:'Keel dry glass (kg/m²)',rudder_glass_kg_m2:'Rudder dry glass (kg/m²)',hull_rib_pitch_m:'Hull rib spacing (m)',foil_rib_pitch_m:'Foil rib spacing (m)',battery_x_fraction:'Battery longitudinal fraction',battery_z_fraction:'Battery vertical fraction',hull_fullness_exponent:'Hull fullness exponent'};
const colors={hull:'#6a9cae',wing:'#dfc38b',keel:'#4a9794',rudder:'#d17a49',ballast:'#697885'};
const meanings={bottom_depth_m:'Hull bottom below the geometric datum; not solved draft.',deck_height_m:'Deck height above the geometric datum.',sail_AR:'Wing span squared divided by planform area.',camber_scale:'Multiplier on the exported reference wing camber.',wing_thickness_scale:'Geometric thickness multiplier; no new aerodynamic polar is generated.',mast_fraction:'Mast pivot location along the wing chord, measured from the leading edge.',mast_x_fraction:'Mast fore/aft location as a fraction of hull length from midships.',battery_x_fraction:'Battery fore/aft location as a fraction of hull length.',battery_z_fraction:'Battery vertical placement fraction used by native mass accounting.',hull_fullness_exponent:'Longitudinal section scale: cosine of station angle raised to this power.',airNu:'Air kinematic viscosity (m²/s).',waterNu:'Water kinematic viscosity (m²/s).',batteryWhKg:'Battery specific energy (Wh/kg).',ballastDensity:'Ballast density (kg/m³).',assemblyLimitKg:'One-person handling mass allocation (kg).'};
const words=n=>n.replace(/([a-z])([A-Z])/g,'$1 $2').replaceAll('_',' ');
export function dimensions(d,p) {
 return {wingSpan:Math.sqrt(d.sail_m2*d.sail_AR),wingChord:Math.sqrt(d.sail_m2/d.sail_AR),
 keelChord:d.keel_m2/d.keel_span_m,rudderChord:d.rudder_m2/d.rudder_span_m,
 batteryMass:d.battery_Wh/p.batteryWhKg,ballastVolume:d.ballast_kg/p.ballastDensity};
}
export function geometry(d,p,section) {
 const faces=[];
 const face=(points,part)=>faces.push({points,part});
 const quad=(a,b,c,e,part)=>{face([a,b,c],part);face([a,c,e],part);};
 const N=24,M=16,rings=[];
 for(let i=0;i<=N;i++){
  const a=-Math.PI/2+Math.PI*i/N,x=d.length_m/2*Math.sin(a),s=Math.max(0,Math.cos(a))**d.hull_fullness_exponent;
  const ring=[];
  for(let j=0;j<=M;j++){const phi=-Math.PI/2+Math.PI*j/M;ring.push([x,d.beam_m/2*s*Math.sin(phi),-d.bottom_depth_m*s*Math.cos(phi)]);}
  ring.push([x,d.beam_m/2*s,d.deck_height_m],[x,-d.beam_m/2*s,d.deck_height_m]);rings.push(ring);
 }
 for(let i=1;i<rings.length;i++)for(let j=0;j<rings[i].length;j++){const k=(j+1)%rings[i].length;quad(rings[i-1][j],rings[i][j],rings[i][k],rings[i-1][k],'hull');}
 const extrude=(profile,z0,z1,part)=>{
  for(let i=0;i<profile.length;i++){let j=(i+1)%profile.length,a=[...profile[i],z0],b=[...profile[j],z0],c=[...profile[j],z1],e=[...profile[i],z1];quad(a,b,c,e,part);}
  // A fan is sufficient for these single-section sketch caps.
  for(const z of [z0,z1])for(let i=1;i<profile.length-1;i++)face([[...profile[0],z],[...profile[i],z],[...profile[i+1],z]],part);
 };
 const q=dimensions(d,p),profile=[];
 for(const side of [1,-1]){const indices=section.u.map((_,i)=>i);if(side<0)indices.reverse();for(const i of indices)profile.push([(section.u[i]-d.mast_fraction)*q.wingChord+d.mast_x_fraction*d.length_m,-(section.mean[i]*d.camber_scale+side*section.half[i]*d.wing_thickness_scale)*q.wingChord]);}
 extrude(profile,d.deck_height_m,d.deck_height_m+q.wingSpan,'wing');
 for(const part of ['keel','rudder']){
  const chord=d[part+'_m2']/d[part+'_span_m'],offset=part==='rudder'?-d.rudder_arm_fraction*d.length_m:0,points=[];
  for(let i=0;i<48;i++){const a=2*Math.PI*i/48;points.push([offset+chord/2*Math.cos(a),.06*chord*Math.sin(a)]);}
  extrude(points,-d.bottom_depth_m,-d.bottom_depth_m-d[part+'_span_m'],part);
 }
 // Smooth volume-equivalent 3:1:1 bulb; the analysis uses a volume-normalized mesh.
 const r=Math.cbrt(q.ballastVolume/(4*Math.PI)),z=-d.bottom_depth_m-d.keel_span_m-r;
 const point=(a,b)=>[3*r*Math.cos(a)*Math.cos(b),r*Math.cos(a)*Math.sin(b),z+r*Math.sin(a)];
 for(let i=0;i<12;i++)for(let j=0;j<24;j++){const a=-Math.PI/2+i*Math.PI/12,b=j*Math.PI/12;quad(point(a,b),point(a+Math.PI/12,b),point(a+Math.PI/12,b+Math.PI/12),point(a,b+Math.PI/12),'ballast');}
 return faces;
}
export async function renderExplorer(root,url) {
 const response=await fetch(url);if(!response.ok)throw Error('Design inputs could not load');
 const data=await response.json();if(data.version!==1||!Array.isArray(data.fields))throw Error('Unsupported design contract');
 if(!document.querySelector('link[data-design-explorer]')){const css=document.createElement('link');css.rel='stylesheet';css.href=new URL('./design-explorer.css',import.meta.url);css.dataset.designExplorer='';document.head.append(css);}
 root.className='design-explorer';
 root.innerHTML=`<header><span class="eyebrow">Explore the design space</span><h3>One boat. Connected decisions.</h3><p>Change a dimension and watch the sketch. Open the other input groups to explore the full sizing contract.</p></header>
 <div class="explorer-layout"><div class="explorer-visual"><canvas tabindex="0" aria-label="Parametric boat sketch. Drag to rotate; arrow keys rotate; plus and minus zoom."></canvas><div class="explorer-actions"><button data-view="iso">3D</button><button data-view="side">Side</button><button data-view="front">Front</button><button data-view="top">Top</button><button data-view="in" aria-label="Zoom in">+</button><button data-view="out" aria-label="Zoom out">−</button></div><p class="explorer-legend">Blue hull · Sand wing · Teal keel · Orange rudder · Slate ballast<br>Neutral wing pose; datum plane is not a solved waterline.</p><div class="explorer-stats"></div><p class="explorer-status" role="status" aria-live="polite"></p></div>
 <div class="explorer-inputs"><label class="explorer-search">Find an input<input type="search" placeholder="Try ballast, camber or battery"></label><div class="explorer-fields"></div></div></div>
 <div class="explorer-actions"><button class="explorer-reset">Reset candidate</button><button class="explorer-save">Download configuration</button><label class="explorer-import">Load configuration<input type="file" accept=".json,application/json"></label></div>
 <p class="explorer-scope">Geometry and simple dimensional quantities update here. Mass distribution, sailing performance, structural margins, recovery and mission completion require a new native analysis. Changes are local to your browser.</p>
 <details class="explorer-process"><summary>How the optimizer uses these inputs</summary><ol><li><strong>Propose a boat.</strong> The 29 design variables define geometry, construction, ballast, storage and drives. Physical assumptions stay fixed for a sizing run.</li><li><strong>Find sailing balance.</strong> Adjust six operating values—speed, heading, wing incidence, leeway, rudder and heel—for eight wind/mode/tack cases. Native calculations evaluate mass, forces, moments, loads and power.</li><li><strong>Restore feasibility.</strong> SciPy seeks zero balance residuals and nonnegative constraint margins. More iterations alone do not establish feasibility.</li><li><strong>Compare alternatives.</strong> Sweep overall-length caps and optimize mass and conditional passage time separately. All 29 design variables, including hull length, and 48 operating values remain free. Retain feasible alternatives for comparison; warm-start later searches from them.</li><li><strong>Challenge the result.</strong> Refined mesh and free-pitch checks, recovery studies, weather/traffic mission replay and eventually physical tests determine what evidence the candidate actually has.</li></ol><p>The sliders use the model’s search brackets. They are neither requirements nor a guarantee that every combination is physically valid.</p></details>
 <details class="explorer-contract"><summary>Model sources and complete solver settings</summary><p class="explorer-source"></p><pre></pre></details>`;
 const values={design:{},parameters:{},materials:{}};
 const fieldMap=new Map(),groups=new Map();
 const designGroup=n=>/^(length|beam|bottom|deck|hull_fullness)/.test(n)?'Hull':/^(sail|camber|wing_thickness|mast)/.test(n)?'Wing':/^(keel_m|keel_span|rudder_m|rudder_span|rudder_arm|ballast)/.test(n)?'Appendages and ballast':/glass|rib/.test(n)?'Construction':'Equipment and installation';
 for(const field of data.fields){
  if(!values[field.kind]||!Number.isFinite(field.value))throw Error('Invalid model field');
  values[field.kind][field.name]=field.value;
  const group=field.kind==='design'?designGroup(field.name):field.kind==='parameters'?'Physical and equipment assumptions':'Construction process assumptions';
  if(!groups.has(group)){const details=document.createElement('details');details.open=group==='Hull'||group==='Wing';const summary=document.createElement('summary');summary.textContent=group;details.append(summary);root.querySelector('.explorer-fields').append(details);groups.set(group,details);}
  const row=document.createElement('div');row.className='explorer-field';row.dataset.search=(words(field.name)+' '+(labels[field.name]||'')).toLowerCase();
  const label=document.createElement('label');label.textContent=labels[field.name]||words(field.name);const id=`explorer-${field.kind}-${field.name}`;label.htmlFor=id;
  const input=document.createElement('input');input.type='number';input.id=id;input.step='any';input.value=Number(field.value.toPrecision(6));
  const hint=document.createElement('small');hint.textContent=field.kind==='design'?'Design variable · '+field.minimum+' to '+field.maximum:'Fixed assumption in a sizing run · '+field.kind;
  if(meanings[field.name]){label.title=meanings[field.name];hint.textContent+=' · '+meanings[field.name];}
  if(field.kind!=='design'){input.min=field.name==='elevatedEquipmentXFraction'?'-1':'0';if(/Efficiency|Fraction|Coverage|Knockdown/.test(field.name)&&field.name!=='elevatedEquipmentXFraction')input.max='1';}
  row.append(label,input,hint);
  let slider;
  if(field.kind==='design'){input.min=field.minimum;input.max=field.maximum;slider=document.createElement('input');slider.type='range';slider.min=field.minimum;slider.max=field.maximum;slider.step=(field.maximum-field.minimum)/1000;slider.value=field.value;slider.setAttribute('aria-label',labels[field.name]||words(field.name));row.append(slider);slider.addEventListener('input',()=>{input.value=slider.value;change();});}
  const change=()=>{if(!input.checkValidity()||input.value===''){input.setAttribute('aria-invalid','true');root.querySelector('.explorer-save').disabled=true;status.textContent='Enter a finite number inside the model search bracket. The sketch retains the last valid value.';return;}input.removeAttribute('aria-invalid');values[field.kind][field.name]=Number(input.value);if(slider)slider.value=input.value;update();};
  input.addEventListener('input',change);groups.get(group).append(row);fieldMap.set(field.kind+'.'+field.name,{field,input,slider,row});
 }
 const status=root.querySelector('.explorer-status'),canvas=root.querySelector('canvas'),ctx=canvas.getContext('2d');
 let yaw=-.65,pitch=.22,zoom=1,faces=[],drag=null;
 function draw(){
  const rect=canvas.getBoundingClientRect(),w=rect.width,h=rect.height,dpr=window.devicePixelRatio||1;canvas.width=w*dpr;canvas.height=h*dpr;ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,w,h);
  if(!faces.length)return;
  const all=faces.flatMap(f=>f.points),lo=[0,1,2].map(i=>Math.min(...all.map(p=>p[i]))),hi=[0,1,2].map(i=>Math.max(...all.map(p=>p[i]))),center=lo.map((v,i)=>(v+hi[i])/2),extent=Math.max(...hi.map((v,i)=>v-lo[i]));
  const scale=Math.min(w,h)*.74/extent*zoom;
  const project=v=>{let x=v[0]-center[0],y=v[1]-center[1],z=v[2]-center[2],a=x*Math.cos(yaw)-y*Math.sin(yaw),b=x*Math.sin(yaw)+y*Math.cos(yaw);return [w/2+a*scale,h/2-(z*Math.cos(pitch)-b*Math.sin(pitch))*scale,b*Math.cos(pitch)+z*Math.sin(pitch)];};
  const items=faces.map(f=>({...f,q:f.points.map(project)})).sort((a,b)=>a.q.reduce((s,p)=>s+p[2],0)-b.q.reduce((s,p)=>s+p[2],0));
  for(const f of items){ctx.beginPath();f.q.forEach((p,i)=>i?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1]));ctx.closePath();ctx.fillStyle=colors[f.part];ctx.fill();ctx.strokeStyle='rgba(30,50,55,.12)';ctx.lineWidth=.4;ctx.stroke();}
  const a=project([-values.design.length_m/2,0,0]),b=project([values.design.length_m/2,0,0]);ctx.setLineDash([4,4]);ctx.strokeStyle='#ac4b2d';ctx.beginPath();ctx.moveTo(a[0],a[1]);ctx.lineTo(b[0],b[1]);ctx.stroke();ctx.setLineDash([]);
  ctx.fillStyle='#526561';ctx.font='12px system-ui';ctx.fillText('Hull '+values.design.length_m.toFixed(2)+' m · drag to orbit',12,h-14);
 }
 function update(){
  const d=values.design,p=values.parameters;
  if(root.querySelector('[aria-invalid=true]')){status.textContent='Correct the invalid input before exporting this configuration.';return;}
  if(p.ballastDensity<=0||p.batteryWhKg<=0){status.textContent='Battery specific energy and ballast density must be positive.';root.querySelector('.explorer-save').disabled=true;return;}
  if(p.wingMoveFraction+p.wingHoldingFraction>1){status.textContent='Wing movement and holding duty fractions must sum to at most 1.';root.querySelector('.explorer-save').disabled=true;return;}
  root.querySelector('.explorer-save').disabled=false;
  faces=geometry(d,p,data.wingSection);draw();
  const q=dimensions(d,p),stats=root.querySelector('.explorer-stats');stats.replaceChildren();
  for(const [label,value] of [['Wing span',q.wingSpan.toFixed(2)+' m'],['Wing chord',q.wingChord.toFixed(2)+' m'],['Keel chord',q.keelChord.toFixed(2)+' m'],['Rudder chord',q.rudderChord.toFixed(2)+' m'],['Battery allocation',q.batteryMass.toFixed(2)+' kg'],['Ballast volume',(q.ballastVolume*1000).toFixed(2)+' L']]){const item=document.createElement('div'),strong=document.createElement('strong'),small=document.createElement('span');strong.textContent=value;small.textContent=label;item.append(strong,small);stats.append(item);}
  const changed=data.fields.filter(f=>values[f.kind][f.name]!==f.value).length;
  const cap=data.solverInputs.maximumOverallLengthM;
  const envelope=Number.isFinite(cap)?` · Challenge limit ${cap} m overall; ${d.length_m>cap?'this hull already exceeds it':'full appendage sweep still needs native checking'}.`:'';
  status.textContent=(changed?`${changed} inputs changed · unsolved configuration`:'Archived geometry · no live feasibility solve')+envelope;
 }
 canvas.addEventListener('pointerdown',e=>{drag=[e.clientX,e.clientY];canvas.setPointerCapture(e.pointerId);});
 canvas.addEventListener('pointermove',e=>{if(!drag)return;yaw+=(e.clientX-drag[0])*.008;pitch=Math.max(-Math.PI/2,Math.min(Math.PI/2,pitch+(e.clientY-drag[1])*.008));drag=[e.clientX,e.clientY];draw();});
 for(const event of ['pointerup','pointercancel'])canvas.addEventListener(event,()=>drag=null);
 const views={iso:[-.65,.22],side:[0,0],front:[Math.PI/2,0],top:[0,Math.PI/2]};
 for(const button of root.querySelectorAll('[data-view]'))button.onclick=()=>{const v=button.dataset.view;if(views[v]){[yaw,pitch]=views[v];zoom=1;}else zoom=Math.max(.5,Math.min(3,zoom*(v==='in'?1.2:1/1.2)));draw();};
 canvas.addEventListener('keydown',e=>{if(!['ArrowLeft','ArrowRight','ArrowUp','ArrowDown','+','-'].includes(e.key))return;e.preventDefault();if(e.key==='ArrowLeft')yaw-=.1;if(e.key==='ArrowRight')yaw+=.1;if(e.key==='ArrowUp')pitch=Math.min(Math.PI/2,pitch+.1);if(e.key==='ArrowDown')pitch=Math.max(-Math.PI/2,pitch-.1);if(e.key==='+')zoom=Math.min(3,zoom*1.2);if(e.key==='-')zoom=Math.max(.5,zoom/1.2);draw();});
 new ResizeObserver(draw).observe(canvas);
 const sync=()=>{for(const {field,input,slider} of fieldMap.values()){input.value=Number(values[field.kind][field.name].toPrecision(6));input.removeAttribute('aria-invalid');if(slider)slider.value=input.value;}update();};
 root.querySelector('.explorer-reset').onclick=()=>{for(const f of data.fields)values[f.kind][f.name]=f.value;sync();};
 root.querySelector('.explorer-save').onclick=()=>{const blob=new Blob([JSON.stringify({version:1,sourceRevision:data.revision,baseline:data.baseline,status:'unsolved',...values},null,2)],{type:'application/json'}),href=URL.createObjectURL(blob),a=document.createElement('a');a.href=href;a.download='blue-dog-proposed-design.json';a.click();setTimeout(()=>URL.revokeObjectURL(href),1000);};
 root.querySelector('input[type=file]').onchange=async e=>{try{const file=e.target.files[0];if(!file)return;if(file.size>100000)throw Error('Configuration is too large');const v=JSON.parse(await file.text());if(v.version!==1)throw Error('Unsupported configuration');for(const f of data.fields){const value=v[f.kind]?.[f.name],control=fieldMap.get(f.kind+'.'+f.name).input; if(!Number.isFinite(value)||(control.min!==''&&value<Number(control.min))||(control.max!==''&&value>Number(control.max)))throw Error('Invalid or missing input: '+f.name);}for(const f of data.fields)values[f.kind][f.name]=v[f.kind][f.name];sync();}catch(error){status.textContent=error.message;}finally{e.target.value='';}};
 root.querySelector('input[type=search]').oninput=e=>{const term=e.target.value.toLowerCase();for(const {row} of fieldMap.values())row.hidden=!row.dataset.search.includes(term);for(const details of groups.values()){details.hidden=![...details.querySelectorAll('.explorer-field')].some(r=>!r.hidden);if(term&&!details.hidden)details.open=true;}};
 const source=root.querySelector('.explorer-source');source.textContent=`${data.fields.length} inputs exported from SysML. Baseline: ${data.baseline}. `;
 const link=document.createElement('a');link.href=`https://github.com/DavidIngraham/sv-blue-dog/blob/${encodeURIComponent(data.revision)}/models/blue-dog.sysml`;link.textContent='Native input definitions';source.append(link);
 root.querySelector('.explorer-contract pre').textContent=JSON.stringify({solverInputs:data.solverInputs,sourceHashes:data.sourceHashes},null,2);
 update();root.dataset.ready='true';
}
