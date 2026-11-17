// style_dump.js — the runtime facts the city style guide is checked against (study/style/city_style.json).
// One JS expression, evaluated inside the game (window.__TC_DEV.ev); returns a JSON string.
// Run (always through nolock.sh):
//   cd clean_r2b_025637 && timeout 600 bash ../tools_pack/nolock.sh node <scratchpad>/probe_c2.js $PWD/out/<build>.html ../tools_pack/style_dump.js > ../study/style/dump_<build>.json
// It only reads; nothing in the game changes.
(()=>{
const R={meta:{build:(typeof BUILD!=='undefined'?BUILD:null),gate:(typeof ACTIVE_GATE!=='undefined'?ACTIVE_GATE:null),errors:[]}};
const g=n=>{try{return eval(n)}catch(e){return undefined}};
const rd=v=>Math.round(v*100)/100;
const sc=(o,keep)=>{const r={};if(!o||typeof o!=='object')return r;for(const k in o){let v;try{v=o[k]}catch(e){continue}if(v==null)continue;const t=typeof v;
  if(t==='number'){if(Number.isFinite(v))r[k]=rd(v)}else if(t==='string'||t==='boolean')r[k]=v;
  else if(Array.isArray(v)&&v.length<=12&&v.every(x=>typeof x==='number'))r[k]=v.map(rd);
  else if(keep&&keep.includes(k)&&typeof v==='object'){try{r[k]=JSON.parse(JSON.stringify(v))}catch(e){}}}return r};
const tryDo=(name,f)=>{try{f()}catch(e){R.meta.errors.push(name+': '+String(e&&e.message||e))}};
// 1. the road graph: every edge with its type, its width, its sidewalk and its lanes
tryDo('edges',()=>{const NB=g('_NODE_BY_ID')||{};const N2=g('NODES2');R.edges=EDGES.map(e=>{const a=NB[e.a]||(N2&&N2.get&&N2.get(e.a)),b=NB[e.b]||(N2&&N2.get&&N2.get(e.b));let T={};try{T=roadType(e)||{}}catch(_){}let ln=null;try{ln=laneCount2(e)}catch(_){}
  return Object.assign(sc(e),{ax:a&&rd(a.x),ay:a&&rd(a.y),bx:b&&rd(b.x),by:b&&rd(b.y),w:T.width,sw:T.sidewalk,med:T.median,tl:T.lanes,tlabel:T.label,lanes2:ln})})});
tryDo('nodes',()=>{R.nodes=NODES.map(n=>sc(n))});
tryDo('types',()=>{R.types=JSON.parse(JSON.stringify(TYPES));R.scale=JSON.parse(JSON.stringify(SCALE))});
// 2. the lamps: every list the game draws (drawStreetLights' lists), the zones' own lamps (ZONELOOK data)
tryDo('lights',()=>{R.lights=[];for(const n of ['STREET_LIGHTS','PARKING_LIGHTS','B3_PARKING_LIGHTS','C2_LIGHTS','E3_LIGHTS','E4_LIGHTS','E5_LIGHTS','PORT_LIGHTS','D4_LIGHTS','B2_LIGHTS','D2_LIGHTS']){const L=g(n);if(Array.isArray(L))for(const o of L)R.lights.push(Object.assign({list:n},sc(o)))}
  const LS=g('LANDSCAPE')||[];for(const o of LS)if(/^SL-/.test(o.asset||''))R.lights.push(Object.assign({list:'LANDSCAPE'},sc(o)))});
// 3. the trees: every *_TREES list, LANDSCAPE, the zone looks
tryDo('trees',()=>{R.trees=[];for(const n of ['A4_TREES','A6_TREES','B2_TREES','B6_TREES','C2_TREES','D2_TREES','D4_TREES','E2_TREES','E3_TREES','E4_TREES','E5_TREES','EW2_TREES','F2_TREES','G2_TREES']){const L=g(n);if(Array.isArray(L))for(const o of L){if(Array.isArray(o))R.trees.push({list:n,x:rd(o[0]),y:rd(o[1]),asset:o[2]});else R.trees.push(Object.assign({list:n},sc(o)))}}
  const LS=g('LANDSCAPE')||[];for(const o of LS)if(/^TP-/.test(o.asset||''))R.trees.push(Object.assign({list:'LANDSCAPE'},sc(o)))});
tryDo('looks',()=>{R.looks={};const L={D4ND:g('D4ND'),A34_BASE:g('A34_BASE'),C3D:g('C3D'),D3ND:g('D3ND'),C4ND:g('C4ND'),B3LOOKD:g('B3LOOKD')};try{L.B4LOOK=B4LOOK.data()}catch(e){}
  for(const k in L){const D=L[k];if(!D)continue;R.looks[k]={trees:(D.trees||[]).map(t=>[t[0],rd(t[1]),rd(t[2]),t[3]]),lamps:(D.lamps||[]).map(t=>[t[0],rd(t[1]),rd(t[2]),t[3]]),hedges:(D.hedges||[]).length,props:(D.props||[]).map(t=>[t[0],rd(t[1]),rd(t[2])]),marks:(D.marks||[]).map(m=>sc(m,['r']))}}});
// 4. the stalls: the game's one list (g77PkStalls) and the special stalls plan (R-54 / D‑333)
tryDo('stalls',()=>{R.stalls=g77PkStalls().map(s=>sc(s));const extra=[];for(const n of ['B3N_STALLS','C3_STALLS','D3N_STALLS','C4_STALLS','D4_STAFF_STALLS','A34_STALLS']){const L=g(n);if(Array.isArray(L))for(const q of L)extra.push(Object.assign({lot:n},sc(q)))}R.stallsZone=extra});
tryDo('special',()=>{const P=specialStallsPlan();if(P)R.special={lots:P.lots.map(l=>sc(l)),acc:[...P.acc],ev:[...P.ev],marks:P.marks.map(m=>sc(m,['r']))}});
tryDo('parked',()=>{R.parked=PARKED_CARS.map(o=>({id:o.id,asset:o.asset,ref:o.ref,x:rd(o.x),y:rd(o.y),h:rd(o.heading||0)}))});
// 5. the markings: crossings, signals, stop / give-way lines, the street names
tryDo('crosswalks',()=>{R.crosswalks=CROSSWALKS.map(c=>sc(c))});
tryDo('zebras',()=>{R.zebras=(typeof ZEBRA_XW!=='undefined'?ZEBRA_XW:[]).map(c=>sc(c))});   // R-76: the crossings without a signal too (C-29)
tryDo('signals',()=>{R.signals=SIGNALS.map(s=>sc(s));R.signalPoles=(g('SIGNAL_POLES')||[]).map(o=>sc(o))});
tryDo('stoplines',()=>{const L=g7SlBuild();R.stopLines=(L||[]).map(o=>sc(o));R.stopLineStyle=sc(G7_SL)});
tryDo('names',()=>{R.names=(g7RoadNameSpots()||[]).map(o=>sc(o));R.nameStyle=sc(G7_RN)});
// 6. the signs: every RF- plate in LANDSCAPE and in every *_PROPS list
tryDo('signs',()=>{R.signs=[];const LS=g('LANDSCAPE')||[];for(const o of LS)if(/^RF-/.test(o.asset||''))R.signs.push(Object.assign({list:'LANDSCAPE'},sc(o)));
  for(const n of ['A4_PROPS','A6_PROPS','B2_PROPS','B3_PROPS','B4_PROPS','B5_PROPS','B6_PROPS','C2_PROPS','C3_PROPS','C4_PROPS','C5_PROPS','D2_PROPS','D3_PROPS','D4_PROPS','E3_PROPS','E4_PROPS','E5_PROPS','EW2_PROPS','G2_PROPS','F2_PROPS','PORT_PROPS','E3_SIGNS','E1_SIGNS','PORT_SIGNS']){const L=g(n);if(Array.isArray(L))for(const o of L){if(o&&/^RF-/.test(o.asset||''))R.signs.push(Object.assign({list:n},sc(o)))}}});
// 7. the bus stops
tryDo('stops',()=>{R.stops=ALL_BUS_STOPS.map(o=>sc(o));R.stopKit={shelter:g('BUS_STOP_SHELTER_SCALE'),sign:g('BUS_STOP_SIGN_SCALE')};try{R.stopSpecs=JSON.parse(JSON.stringify(BUS_STOP_SPECS)).slice?JSON.parse(JSON.stringify(BUS_STOP_SPECS)).slice(0,80):null}catch(e){}});
// 8. the curb cuts and accesses
tryDo('access',()=>{R.access=[];for(const n of ['C4_ACCESS','D3_CURB_CUTS','B3_CURB_CUTS','C2_CURB_CUTS','B6_CURB_CUTS']){const L=g(n);if(Array.isArray(L))for(const o of L)R.access.push(Object.assign({list:n},sc(o)))}});
// 9. the buildings (the BLD40 types) and the seams
tryDo('buildings',()=>{R.buildings=(g('C4_BUILDINGS')||[]).map(o=>Object.assign(sc(o),{type:o.bld40&&o.bld40.type||o.type||null,rot:o.bld40&&o.bld40.rot,ent:o.entrance?[rd(o.entrance.x),rd(o.entrance.y)]:null,fp:o.fp&&typeof o.fp==='object'&&!Array.isArray(o.fp)?[rd(o.fp.x),rd(o.fp.y),rd(o.fp.w),rd(o.fp.h)]:null}))});
// 9b. the zones' own data as the game holds it now (the looks, the yards, the pads, the courts, the fences)
tryDo('zoneData',()=>{R.zoneData={};const L={A34D:g('A34D'),A34_BASE:g('A34_BASE'),C3D:g('C3D'),D3ND:g('D3ND'),C4ND:g('C4ND'),D4ND:g('D4ND'),B3LOOKD:g('B3LOOKD'),B3NG:g('B3NG'),B4G:g('B4G')};try{L.B4LOOK=B4LOOK.data()}catch(e){}
  try{const n=c3Lv(),V=g('C3LV');if(V){const v=V[n-1];L.C3LV={level:n,pad:v.pad||null,lamps:v.lamps||[],trees:v.trees||[]}}}catch(e){}
  for(const k in L){if(!L[k])continue;try{R.zoneData[k]=JSON.parse(JSON.stringify(L[k],(kk,v)=>typeof v==='number'?rd(v):v))}catch(e){R.meta.errors.push('zoneData '+k+': '+e)}}});
// 9c. the openings that K‑187 keeps clear of lamps, poles and trees (±40 px of every access axis)
tryDo('openings',()=>{k187Acc();R.openings=(K187.list||[]).map(o=>sc(o))});
tryDo('connectors',()=>{R.connectors=(g('ALL_CONNECTORS')||[]).map(c=>Object.assign(sc(c),{sig:(g('CONNECTOR_SIGNATURES')||{})[c.id]||null}));R.continuity=sc(g('CONTINUITY_PROTOCOL'))});
// 10. the sizes table (D‑238) as the game measures it
tryDo('sizes',()=>{const A=window.__TC_SZ&&window.__TC_SZ.audit();if(A)R.sizes={rows:A.rows,atTarget:A.atTarget,toChange:A.toChange,table:A.table.map(r=>sc(r))}});
return JSON.stringify(R)})()
