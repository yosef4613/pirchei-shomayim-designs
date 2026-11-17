// 8.11 · סבב 9ס של מפת הדרכים — מה שבנוי במשחק (S7F265), לטבלת ההתאמה מפה↔משחק ולעמודת "היום" של הקווים.
// node probe_s7f265.js <game.html> <out.json>
// קורא בלבד: הרשת (צמתים, קטעים, נתיבים), הרמזורים, מעברי החצייה, התחנות והקווים, המבנים והמגרשים של כל אזור, האגם והמזחים.
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  const r = await p.evaluate(() => window.__TC_DEV.ev(`(()=>{
   const R=v=>(typeof v==='number')?Math.round(v*10)/10:v;
   let seen=new WeakSet();
   function ser(v,d){
     if(v===null||v===undefined)return v;
     const t=typeof v;
     if(t==='number')return R(v); if(t==='string')return v.length>400?v.slice(0,400):v; if(t==='boolean')return v;
     if(t==='function')return undefined;
     if(t!=='object')return undefined;
     if(typeof HTMLElement!=='undefined'&&(v instanceof HTMLElement))return undefined;
     if(typeof ImageBitmap!=='undefined'&&(v instanceof ImageBitmap))return undefined;
     if(typeof OffscreenCanvas!=='undefined'&&(v instanceof OffscreenCanvas))return undefined;
     if(typeof Path2D!=='undefined'&&(v instanceof Path2D))return undefined;
     if(seen.has(v))return '[ref]'; seen.add(v);
     if(d<=0)return Array.isArray(v)?('[arr '+v.length+']'):'[obj]';
     if(v instanceof Map)return ser(Object.fromEntries(v),d);
     if(v instanceof Set)return ser([...v],d);
     if(Array.isArray(v)||ArrayBuffer.isView(v)){const a=[];const n=Math.min(v.length,3000);for(let i=0;i<n;i++)a.push(ser(v[i],d-1));if(v.length>n)a.push('[+'+(v.length-n)+']');return a}
     const o={};let k=0;for(const key of Object.keys(v)){if(++k>200)break;const s=ser(v[key],d-1);if(s!==undefined)o[key]=s}return o}
   const o={err:{}};
   const get=(name,d)=>{try{const v=eval(name);seen=new WeakSet();o[name]=ser(v,d)}catch(e){o.err[name]=String(e).slice(0,200)}};
   try{o.title=document.title}catch(e){}
   for(const k of ['BUILD','BUILD_ID','FILE_SCOPE','GAME_VERSION','VERSION'])get(k,2);
   // the network
   o.nodes=NODES.map(n=>{const q={id:n.id,x:R(n.x),y:R(n.y),kind:n.kind||n.type||''};for(const k of Object.keys(n))if(!(k in q)&&['number','string','boolean'].includes(typeof n[k]))q[k]=R(n[k]);return q});
   o.edges=EDGES.map(e=>{const q={id:e.id,a:e.a,b:e.b,name:e.name||'',cls:e.cls||'',future:!!e.future,half:(typeof _ROAD_HALF==='function'?R(_ROAD_HALF(e)):null),
     pts:(e.pts||[]).map(t=>[R(t.x??t[0]),R(t.y??t[1])])};for(const k of Object.keys(e))if(!(k in q)&&['number','string','boolean'].includes(typeof e[k]))q[k]=R(e[k]);
     for(const k of ['lanes','lanesA','lanesB','lanesFwd','lanesBack','dirLanes'])if(e[k]!==undefined&&typeof e[k]==='object')q[k]=ser(e[k],2);return q});
   o.signals=[...SIGNAL_NODE_IDS]; o.inter=INTERSECTION_NODES.map(n=>n.id);
   o.xw=CROSSWALKS.map(c=>({id:c.id,road:c.roadId,node:c.signalNode||null,x:R(c.x),y:R(c.y),sig:!!c.signalized}));
   try{o.zebra=ZEBRA_XW.map(z=>({id:z.id,road:z.roadId,node:z.node||null,x:R(z.x),y:R(z.y)}))}catch(e){o.err.zebra=String(e)}
   o.drawn=[];for(const k of ['A34D','A34_BASE','D3ND','C3D','C4ND','D4ND','C5ND','D5ND','B4G','B3LOOKD','B3NG','A5ND','A5G','B5ND','E3ND','P560D','P560']){let D;try{D=eval(k)}catch(e){D=undefined}if(!D||!Array.isArray(D.zebra))continue;
    for(const z of D.zebra){const cx=(z[0]+z[2])/2,cy=(z[1]+z[3])/2;let r=null,bd=1e9;for(const q of EDGES){const a=_NODE_BY_ID[q.a],b=_NODE_BY_ID[q.b];if(!a||!b)continue;const L=Math.hypot(b.x-a.x,b.y-a.y)||1,t=((cx-a.x)*(b.x-a.x)+(cy-a.y)*(b.y-a.y))/(L*L);if(t<0||t>1)continue;const d=Math.abs((b.x-a.x)*(cy-a.y)-(b.y-a.y)*(cx-a.x))/L;if(d<bd){bd=d;r=q.id}}
     o.drawn.push({id:k+'.zebra@'+Math.round(cx)+','+Math.round(cy),src:k,road:r,x:R(cx),y:R(cy),rect:z.slice(0,4).map(R)})}}
   try{o.tRule=P523.tRule.map(q=>[q[0],q[1]])}catch(e){o.err.tRule=String(e)}
   try{o.zoneOf={};for(const n of NODES)o.zoneOf[n.id]=r76Zone(n.x,n.y)}catch(e){o.err.zoneOf=String(e)}
   // the buses
   get('BUS_LINES',2); get('BUS_LINE_INFO',3); get('BUS_STOP_SPECS',3);
   try{o.stops=ALL_BUS_STOPS.map(s=>{const q={};for(const k of Object.keys(s))if(['number','string','boolean'].includes(typeof s[k]))q[k]=R(s[k]);return q})}catch(e){o.err.stops=String(e)}
   try{o.term=Object.fromEntries(Object.entries(BUS_TERMINAL_STOPS).map(([l,s])=>[l,{id:s.id,x:R(s.x),y:R(s.y),chunk:s.chunk}]))}catch(e){o.err.term=String(e)}
   o.routes={};try{for(const l of BUS_LINES){const rt=busRouteForLine(l);o.routes[l]=ser(rt,3)}}catch(e){o.err.routes=String(e)}
   try{o.pt=ser(__TC_PUBLIC_TRANSPORT(),4)}catch(e){o.err.pt=String(e)}
   try{o.busVehicles=BUS_VEHICLES.length}catch(e){}
   // the zones
   get('ACTIVE_REGIONS',2); get('MAP_CHUNKS',3);
   o.looks={};for(const c of 'ABCDEFGH')for(let i=0;i<10;i++){const z=c+i;for(const s of ['LOOK','ND','G','D']){try{const v=eval(z+s);if(v)o.looks[z+s]=typeof v}catch(e){}}}
   for(const k of ['BUILDINGS','LOTS','C2_LOTS','C2_BUILDINGS','B3_BUILDINGS','C4_BUILDINGS','D4_BUILDINGS','D2_BOX','D2_BUILDINGS','D2_SHOPS','D2_PARKING','D2_ACCESS','D2_FORECOURTS','D2_CONNECTORS','D2_ISLANDS','D2_POOL',
     'E3_BUILDINGS','E3_LOTS','E3_PLATFORMS','E3_TRACKS','E4_TRACKS','E4_BUILDINGS','E5_BUILDINGS','E5_TRACKS','D5_BUILDINGS','A6_BUILDINGS','A6_LOTS','B6_BUILDINGS','B5_BUILDINGS','C5_BUILDINGS','C5_LOTS',
     'A4_BUILDINGS','A4_LOTS','B4_BUILDINGS','B4_LOTS','B3N_BUILDINGS','B3N_LOTS','C3_LOTS','B2_LAKE','B2_PIER','B2_PIER_INFO','B2_FISH_PLATFORMS','B12','B12E','B12_BOAT','B12L','A6_PIER','B6_PIERS',
     'PORT_BUILDINGS','APT_BUILDINGS','EW2_BUILDINGS','E2_BUILDINGS','PG_ZONE','P560','P560D','RB2'])get(k,4);
   for(const k of ['A34D','D3ND','C3D','C4ND','D4ND','C5ND','D5ND','B4G','B3LOOKD','B3NG','A5ND','A5G','B5ND','E3ND','A2ND','A2G','B2ND','B1ND','C2ND','D2ND','E4ND'])get(k,3);
   o.pipe=[];try{for(const k of Object.keys(window))if(/PIPE/.test(k))o.pipe.push(k)}catch(e){}
   return o})()`));
  r.pageErrors = errs.slice(0, 20);
  fs.writeFileSync(out, JSON.stringify(r)); console.log('nodes', r.nodes.length, 'edges', r.edges.length, 'xw', r.xw.length, 'stops', (r.stops || []).length, 'title', r.title, 'errs', Object.keys(r.err).length, 'bytes', JSON.stringify(r).length);
  await b.close();
})();
