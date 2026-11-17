// 28.10 · the owner 09:18 / 09:21 — "every zone checked by everything that must be in it, metre by metre; only what is built".
// The automatic half of the audit of one or more built zones, on a grid of 100 × 100 px (10 × 10 m) cells:
//   per cell   — what the code puts there: road surface share (pointRoad on a 10 px lattice), lamps, signal poles, trees, props,
//                stalls, buildings, crosswalks, accesses, bus stops;
//   flags      — anything standing on the road (lamp, pole, tree, prop, stall, building, entrance), a pole the walker passes through
//                (K‑171 / K‑177), a stall or tree inside a building, a lamp or tree inside a stall, a lamp within ±40 px of the axis of an
//                access (K‑187), a stretch of street of more than 200 px with no lamp within 60 px (part ה), a stall smaller than 62 × 32;
//   pictures   — 6 shots per zone at zoom 2.85 (the zoom of the owner's close-ups), the game paused, with the camera of every shot, so
//                the cell grid can be drawn on them (zonegrid.py) and every cell judged by eye.
// node zoneaudit.js <build.html> <outdir> <zones: C2,D2,…>
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, outdir, zl] = process.argv.slice(2); const ZONES = zl.split(','); fs.mkdirSync(path.join(outdir, 'shots'), { recursive: true });
  /* 28.10 10:24 — also the names declared later in a comma chain (const A=[],E3_CAR_STALLS=[],… — they were missed and E3 counted 0 stalls) */
  const src = fs.readFileSync(file, 'utf8'); const names = [...new Set([...src.matchAll(/(?:\b(?:const|let|var)\s+|,\s*)([A-Z][A-Z0-9_]{2,})\s*=\s*\[/g)].map(m => m[1]))];
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await b.newPage({ viewport: { width: 1920, height: 953 } });
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' }); await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForFunction(() => window.__TC_DEV.ev('typeof G78_PC!=="undefined"&&G78_PC.ready'), null, { timeout: 120000, polling: 500 });
  await p.waitForTimeout(2000);
  const R = await p.evaluate(([names, ZONES]) => window.__TC_DEV.ev(`(()=>{const names=${JSON.stringify(names)},ZONES=${JSON.stringify(ZONES)};
   const CH=MAP_CHUNKS.map(c=>({id:c.id,x:c.x,y:c.y,w:c.w,h:c.h}));const C=Object.fromEntries(CH.map(c=>[c.id,c]));
   const L={};for(const n of names){let v;try{v=eval(n)}catch(e){continue}if(!Array.isArray(v)||!v.length)continue;const pts=v.filter(o=>o&&typeof o==='object'&&isFinite(o.x)&&isFinite(o.y));if(pts.length<v.length*.6)continue;L[n]=pts}
   const kind=n=>/STREET_LIGHTS$|_LIGHTS$/.test(n)?'lamp':/SIGNAL_POLES$|_POLES$/.test(n)?'pole':/TREES$/.test(n)?'tree':/STALLS$|^PARKED_CARS$/.test(n)?'stall':/BUILDINGS$|^LOTS$|VILLAS$/.test(n)?'bld':/SOLIDS$/.test(n)?'solid':/^CROSSWALKS$/.test(n)?'cross':/ACCESS|CURB_CUTS|_PADS$/.test(n)?'access':/BUS_STOPS$/.test(n)?'stop':/_PROPS$|_FIXTURES$|_STATIC$/.test(n)?'prop':null;
   const road=(x,y)=>{try{const e=pointRoad(x,y);return e?(e.id||e.name||'road'):null}catch(e){return null}};
   const blk=(x,y,r)=>{try{return !!personBlockedAt(x,y,r)}catch(e){return null}};const SKIP=new Set(((typeof G78_PC!=='undefined'&&G78_PC.skip)||[]).map(s=>typeof s==='object'?(s.id||s[3]||JSON.stringify(s)):s));
   const rectOf=o=>(o.w>0&&o.h>0)?{x:+o.x,y:+o.y,w:+o.w,h:+o.h}:o.asset==='PK2-CURB-V'?{x:+o.x,y:+o.y,w:20,h:42}:o.asset==='PK2-CURB-H'?{x:+o.x,y:+o.y,w:42,h:20}:null;   /* 28.10 13:45: a curb cut given by its asset — x, y is the top corner of a 20 × 42 (V) / 42 × 20 (H) cut, not its centre (A‑B3‑03, A‑D3‑02) */ const inR=(x,y,r,pad=0)=>x>=r.x+pad&&x<=r.x+r.w-pad&&y>=r.y+pad&&y<=r.y+r.h-pad;
   const N=Object.fromEntries(NODES.map(n=>[n.id,n]));
   const out={};
   for(const z of ZONES){const c=C[z];if(!c){out[z]={err:'no chunk'};continue}
    const nx=Math.ceil(c.w/100),ny=Math.ceil(c.h/100),cells=[];for(let j=0;j<ny;j++)for(let i=0;i<nx;i++)cells.push({id:z+'-'+String(i+1).padStart(2,'0')+'-'+String(j+1).padStart(2,'0'),i,j,x:c.x+i*100,y:c.y+j*100,road:0,n:{},flags:[]});
    const cellAt=(x,y)=>{const i=Math.floor((x-c.x)/100),j=Math.floor((y-c.y)/100);return (i>=0&&j>=0&&i<nx&&j<ny)?cells[j*nx+i]:null};
    for(const q of cells){let k=0,r=0;for(let a=5;a<100;a+=10)for(let b2=5;b2<100;b2+=10){k++;if(road(q.x+a,q.y+b2))r++}q.road=Math.round(100*r/k)}
    const obj={lamp:[],pole:[],tree:[],stall:[],bld:[],solid:[],cross:[],access:[],stop:[],prop:[]};
    for(const [n,v] of Object.entries(L)){const k=kind(n);if(!k)continue;for(const o of v){let x=+o.x,y=+o.y;const r=rectOf(o);if((k==='lamp'||k==='pole')){try{const q=poleFit(o);x=q.x;y=q.y}catch(e){}}
      const cx=r?r.x+r.w/2:x,cy=r?r.y+r.h/2:y;if(!(cx>=c.x&&cx<c.x+c.w&&cy>=c.y&&cy<c.y+c.h))continue;obj[k].push({n,id:o.id||'',x:Math.round(x),y:Math.round(y),cx:Math.round(cx),cy:Math.round(cy),r,label:o.label||o.name||'',acc:!!(o.acc||o.accessible),ev:!!(o.ev||o.charge||o.charger||o.evc)})}}
    for(const [k,arr] of Object.entries(obj))for(const o of arr){const q=cellAt(o.cx,o.cy);if(q)q.n[k]=(q.n[k]||0)+1}
    const flag=(o,f,extra)=>{const q=cellAt(o.cx,o.cy);if(q)q.flags.push(Object.assign({f,n:o.n,id:o.id,x:o.cx,y:o.cy},extra||{}))};
    for(const k of ['lamp','pole','tree','prop'])for(const o of obj[k]){const rd=road(o.x,o.y);if(rd)flag(o,k+'OnRoad',{road:rd});if(k!=='prop'){const bl=blk(o.x,o.y,3);if(bl===false)flag(o,SKIP.has(o.id)?k+'NarrowSkip':k+'NoBlock')}}
    for(const o of obj.stall){const r=o.r;if(!r)continue;const pts=[[o.cx,o.cy],[r.x+2,r.y+2],[r.x+r.w-2,r.y+2],[r.x+2,r.y+r.h-2],[r.x+r.w-2,r.y+r.h-2]];const on=pts.filter(([a,b2])=>road(a,b2)).length;if(on>=2)flag(o,'stallOnRoad',{corners:on});
      const lo=Math.min(r.w,r.h),hi=Math.max(r.w,r.h);if(!/PARKED/.test(o.n)&&(lo<30||hi<58))flag(o,'stallSmall',{w:r.w,h:r.h});for(const B of obj.bld)if(B.r&&inR(o.cx,o.cy,B.r,1)){flag(o,'stallInBld',{bld:B.id});break}}
    for(const o of obj.bld){const r=o.r;if(!r)continue;const pts=[[o.cx,o.cy],[r.x+3,r.y+3],[r.x+r.w-3,r.y+3],[r.x+3,r.y+r.h-3],[r.x+r.w-3,r.y+r.h-3]];const on=pts.filter(([a,b2])=>road(a,b2)).length;if(on)flag(o,'bldOnRoad',{corners:on})}
    for(const k of ['lamp','tree','pole'])for(const o of obj[k]){for(const s of obj.stall)if(s.r&&!/PARKED/.test(s.n)&&inR(o.x,o.y,s.r,1)){flag(o,k+'InStall',{stall:s.id});break}if(k==='tree')for(const B of obj.bld)if(B.r&&inR(o.x,o.y,B.r,2)){flag(o,'treeInBld',{bld:B.id});break}}
    /* K‑187: a lamp or pole within ±40 px of the axis of an access (the access rectangle, along its long side) */
    /* 28.10 10:20 — an access given only as a point (D3‑PK‑FUEL‑IN …) has no rectangle: a 24 × 24 box around the point, so it is checked too (it was skipped — A‑D3‑02) */
    {const seen=new Set();for(const a of obj.access){const r=a.r||{x:a.x-12,y:a.y-12,w:24,h:24};const ax=r.x+r.w/2,ay=r.y+r.h/2;
      /* which way does a car go through it? toward the road: probe beyond each side */
      const v=!!(road(ax,r.y-15)||road(ax,r.y+r.h+15)),hz=!!(road(r.x-15,ay)||road(r.x+r.w+15,ay));const DIRV={'D5-HOLD-W-ACCESS':true,'D5-HOLD-E-ACCESS':true};const vert=(a.id in DIRV)?DIRV[a.id]:v&&!hz?true:hz&&!v?false:r.h>=r.w;   /* 28.10 13:45: the corner aprons of the D5 hold yard are crossed north–south (A‑D5‑02 was a false alarm; p365 K187_DIR) */
      for(const o of obj.lamp.concat(obj.pole)){const key=o.id+'|'+(a.id||a.n);if(seen.has(key))continue;const d=vert?Math.abs(o.x-ax):Math.abs(o.y-ay),along=vert?(o.y>=r.y-30&&o.y<=r.y+r.h+30):(o.x>=r.x-30&&o.x<=r.x+r.w+30);
       if(along&&d<=40){seen.add(key);flag(o,'lampAtAccess',{access:a.id||a.n,d:Math.round(d),axis:vert?'v':'h'})}}}}
    /* the lamp rule: along every street of the zone, no stretch of more than 200 px without a lamp beside it (within 70 / 100 / 150 px of the centre line — street / avenue / arterial) */
    const lamps=obj.lamp,gaps=[];for(const e of EDGES){const A=N[e.a],B=N[e.b];if(!A||!B)continue;const Ln=Math.hypot(B.x-A.x,B.y-A.y);if(Ln<1)continue;const ux=(B.x-A.x)/Ln,uy=(B.y-A.y)/Ln;
      const s=[];for(let t=0;t<=Ln;t+=20){const x=A.x+ux*t,y=A.y+uy*t;if(x>=c.x&&x<c.x+c.w&&y>=c.y&&y<c.y+c.h)s.push(t)}if(s.length<2)continue;const t0=s[0],t1=s[s.length-1];
      const at=lamps.map(o=>{const vx=o.x-A.x,vy=o.y-A.y,t=vx*ux+vy*uy,d=Math.abs(vx*uy-vy*ux);return (t>=t0-60&&t<=t1+60&&d<=({arterial:150,avenue:100,local:70}[e.cls]||70))?t:null}).filter(t=>t!==null).sort((a,b2)=>a-b2);
      const pts=[t0].concat(at.filter(t=>t>t0&&t<t1),[t1]);let worst=0,wt=0;for(let i=1;i<pts.length;i++){if(pts[i]-pts[i-1]>worst){worst=pts[i]-pts[i-1];wt=(pts[i]+pts[i-1])/2}}
      if(worst>200&&!(at.length===0&&t1-t0<200)){const x=Math.round(A.x+ux*wt),y=Math.round(A.y+uy*wt);gaps.push({edge:e.id,cls:e.cls,name:e.name,len:Math.round(t1-t0),lamps:at.length,gap:Math.round(worst),x,y});const q=cellAt(x,y);if(q)q.flags.push({f:'darkStretch',n:'EDGES',id:e.id,x,y,gap:Math.round(worst)})}}
    const SS=obj.stall.filter(o=>!/PARKED/.test(o.n)),special={stalls:SS.length,acc:SS.filter(o=>o.acc).length,ev:SS.filter(o=>o.ev).length,byList:{}};for(const o of SS){const b=special.byList[o.n]=special.byList[o.n]||{n:0,acc:0,ev:0};b.n++;if(o.acc)b.acc++;if(o.ev)b.ev++}
    const counts={};for(const q of cells)for(const f of q.flags)counts[f.f]=(counts[f.f]||0)+1;
    out[z]={chunk:c,nx,ny,special,objects:Object.fromEntries(Object.entries(obj).map(([k,v])=>[k,v.length])),counts,gaps,cells,obj}}
   return {build:BUILD,zones:out}})()`), [names, ZONES]);
  fs.writeFileSync(path.join(outdir, 'audit.json'), JSON.stringify(R));
  for (const z of ZONES) { const q = R.zones[z]; console.log(z, JSON.stringify(q.objects), JSON.stringify(q.counts), 'gaps', q.gaps.length, 'special', JSON.stringify(q.special)) }
  // the pictures — 2 × 3 shots per zone at zoom 2.85, the game paused
  await p.evaluate(() => window.__TC_DEV.ev(`(()=>{State.paused=true;try{G77_ASV.on=false}catch(e){}return 1})()`));
  // only the world: every element that is not the game canvas or one of its ancestors is hidden (the HUD, the minimap, the key bar, the build tag)
  await p.evaluate(() => { const cv = [...document.querySelectorAll('canvas')].sort((a, b) => b.width * b.height - a.width * a.height)[0]; const keep = new Set(); for (let e = cv; e; e = e.parentElement) keep.add(e);
    for (const e of document.body.querySelectorAll('*')) if (!keep.has(e) && !e.contains(cv)) e.style.visibility = 'hidden'; cv.style.visibility = 'visible' });
  const shots = [];
  for (const z of ZONES) {
    const c = R.zones[z].chunk; const Z = 2.85, vw = 1920 / Z, vh = 953 / Z;
    const xs = [c.x + vw / 2, c.x + c.w - vw / 2], ny = Math.ceil(c.h / (vh - 40)), ys = [];
    for (let j = 0; j < ny; j++) ys.push(c.y + vh / 2 + j * ((c.h - vh) / Math.max(1, ny - 1)));
    for (let j = 0; j < ys.length; j++) for (let i = 0; i < xs.length; i++) {
      await p.evaluate(([x, y, Z]) => window.__TC_DEV.ev(`(()=>{Camera.x=${x};Camera.y=${y};Camera.zoom=${Z};return 1})()`), [xs[i], ys[j], Z]);
      await p.waitForTimeout(1200);
      const cam = await p.evaluate(() => window.__TC_DEV.ev(`(()=>({x:Camera.x,y:Camera.y,z:Camera.zoom}))()`));
      const fn = `${z}_${j + 1}${i + 1}.jpg`; await p.screenshot({ path: path.join(outdir, 'shots', fn), type: 'jpeg', quality: 82 }); shots.push({ z, fn, cam, W: 1920, H: 953 });
    }
    process.stdout.write(z + ' ');
  }
  fs.writeFileSync(path.join(outdir, 'shots.json'), JSON.stringify(shots, null, 1)); console.log('\nshots', shots.length); await b.close();
})().catch(e => { console.error(e); process.exit(1) });
