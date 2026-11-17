// exit_clear.js <build> <out.json> — airfront: לכל יציאה של חניון S16 (S16M / S16C / S16R) — האם הגוף של מכונית שמחכה לרווח בנקודה K (ph 'merge')
// נוגע (vehicleBodiesOverlap, המרווח של המנוע: 1.4 למכונית, 1.8 לאוטובוס) בגוף של רכב שנוסע בנתיבים של הכביש שאליו יוצאים; וכמה צריך להזיז את K אחורה
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
(async () => {
  const [file, out] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] }); const p = await b.newPage({ viewport: { width: 1000, height: 700 } });
  const pe = []; p.on('pageerror', e => pe.push(String(e).slice(0, 200)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' }); await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  const r = await p.evaluate(() => window.__TC_DEV.ev(`(()=>{const out={};
   const mAssets=[...new Set([...S16P.cars.map(c=>c.asset+'|'+c.ref)])];
   const lAssets=[...new Set([...TRAFFIC_CARS.map(c=>c.asset+'|'+(c.ref||'Sedan')),...BUS_VEHICLES.map(c=>c.asset+'|'+(c.ref||'Bus')+'|bus')])];
   const hl={};for(const a of mAssets){const [as,rf]=a.split('|');const s=vehicleCollisionShape(as,rf,0,0,0);hl[a]={hl:+s.halfLength.toFixed(1),r:+(s.radius||s.halfWidth||0).toFixed(1)}}
   const hl2={};for(const a of lAssets){const [as,rf]=a.split('|');const s=vehicleCollisionShape(as,rf,0,0,0);hl2[a]={hl:+s.halfLength.toFixed(1),r:+(s.radius||s.halfWidth||0).toFixed(1)}}
   out.mShapes=hl;out.lShapes=hl2;
   for(const id in S16P.lots){const L=S16P.lots[id],K={x:L.K[0],y:L.K[1]},kh=L.kHead,J=L.join;const e=byEdge[L.outEdge];const nl=(e&&(e.lanes||e.laneCount))||2;
    const lanes=[];for(let k=0;k<4;k++){const q=lane2(L.outEdge,L.outDir,k);if(q)lanes.push([k,q])}
    const o={K,kHead:kh,J:{x:+J.x.toFixed(1),y:+J.y.toFixed(1),h:+J.heading.toFixed(2)},lanes:lanes.map(([k,q])=>({k,ax:+q.ax.toFixed(1),ay:+q.ay.toFixed(1),ux:+q.ux.toFixed(2),uy:+q.uy.toFixed(2)})),hit:{}};
    for(let d=0;d<=40;d+=2){const kx=K.x-Math.cos(kh)*d,ky=K.y-Math.sin(kh)*d;const hits=[];
     for(const ma of mAssets){const [as,rf]=ma.split('|');const me=vehicleCollisionShape(as,rf,kx,ky,kh);
      for(const la of lAssets){const [bs,brf,bus]=la.split('|');const m=bus?1.8:1.4;
       for(const [k,q] of lanes){const pj=(J.x-q.ax)*q.ux+(J.y-q.ay)*q.uy;let hit=false;for(let s=pj-90;s<=pj+90;s+=2){const x=q.ax+q.ux*s,y=q.ay+q.uy*s,h=Math.atan2(q.uy,q.ux);const ob=vehicleCollisionShape(bs,brf,x,y,h);if(vehicleBodiesOverlap(me,ob,m)){hit=true;break}}if(hit){hits.push(ma.split('|')[0]+'×'+bs+'@'+k)}}}}
     o.hit[d]=hits.length?hits.length+': '+[...new Set(hits)].slice(0,8).join(' '):0;if(!hits.length)break}
    out[id]=o}
   return JSON.stringify(out)})()`));
  fs.writeFileSync(out, r); console.log(r.slice(0, 3000)); console.log('pe', pe.length); await b.close();
})().catch(e => { console.error(String(e).slice(0, 300)); process.exit(1) });
