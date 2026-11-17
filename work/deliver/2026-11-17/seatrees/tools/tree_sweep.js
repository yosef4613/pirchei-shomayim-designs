// tree_sweep.js — סוכן seatrees (17.11): מוצא כל עץ / שיח / גדר חיה שמצויר בעולם, ובודק אם הגזע על מים.
// node tree_sweep.js <game.html> <out.json> [zoom=0.9]
// שיטה: עטיפה של TurboCity.draw, ‏KIT34.draw ו-KIT34.drawBody (הציירים של הצמחייה), סריקה של אריחי הקרקע (כמו k34Scan),
// ותנועה של המצלמה על כל העולם — כל ציור נרשם בנקודת העולם שלו (ההופכי של המטריצה של המצלמה / של האריח).
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out, zs] = process.argv.slice(2); const Z = +(zs || 0.9);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 240)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(1500);
  const ev = s => p.evaluate(s => Promise.resolve(window.__TC_DEV.ev(s)).then(v => typeof v === 'string' ? v : JSON.stringify(v)), s);
  await ev(`(()=>{
   const REC=window.__TSW={m:new Map(),n:0,on:true};
   const VEGRE=/^(tree|palm|bush|hedge|bed_|fern|reeds|grass|lily)/;
   const add=(src,t,c,x,y)=>{if(!REC.on)return;let m;try{m=c.getTransform()}catch(e){return}let wx,wy,mode;
     const px=m.a*x+m.c*y+m.e,py=m.b*x+m.d*y+m.f;
     if(c===GAME_CTX){const q=c34CamM();wx=(px-q[1])/q[0];wy=(py-q[2])/q[0];mode='frame'}
     else if(c.canvas&&c.canvas.width<=2){wx=px;wy=py;mode='scan'}else return;
     const k=src+'|'+t+'|'+Math.round(wx/2)+'|'+Math.round(wy/2);if(!REC.m.has(k))REC.m.set(k,{src,t,x:Math.round(wx),y:Math.round(wy),mode});REC.n++};
   const d0=TurboCity.draw;TurboCity.draw=function(c,id,x,y,o){try{if(typeof id==='string'&&/^TP-/.test(id)){let bx=0,by=0;try{const I=TurboCity.info(id,o||{});bx=I.w/2;by=I.h/2;const an=I.an||[],bb=an.find(a=>a[0]==='Base'||a[0]==='Trunk'||a[0]==='Pole Base');if(bb){bx=bb[1];by=bb[2]}}catch(e){}add('asset',id,c,x+bx,y+by)}}catch(e){}return d0.apply(this,arguments)};
   const k0=KIT34.draw;KIT34.draw=function(c,x,y,t){try{if(VEGRE.test(t))add('kit',t,c,x,y)}catch(e){}return k0.apply(this,arguments)};
   const k1=KIT34.drawBody;KIT34.drawBody=function(c,x,y,t){try{if(VEGRE.test(t))add('kitb',t,c,x,y)}catch(e){}return k1.apply(this,arguments)};
   REC.bl=[];try{if(typeof SEAT!=='undefined')SEAT.onDraw=(src,id,x,y,blk)=>{if(blk)REC.bl.push([Math.round(x),Math.round(y)])}}catch(e){}
   return 'ok'})()`);
  // סריקת האריחים (כמו k34Scan)
  const sc = await ev(`(()=>{try{k34Scan();return 'scan '+__TSW.m.size}catch(e){return 'scan err '+e}})()`); console.error(sc);
  // תנועת המצלמה
  const pts = []; const hw = 640 / Z, hh = 400 / Z;
  for (let y = -850 + hh; y < 7750 + hh; y += 2 * hh * 0.9) for (let x = hw; x < 9600 + hw; x += 2 * hw * 0.9) pts.push([Math.round(x), Math.round(y)]);
  for (const [x, y] of pts) { await ev(`__TC_DEV.cam({x:${x},y:${y},zoom:${Z}})`); await p.waitForTimeout(700); }
  // VEG_D, K34C.list, ובדיקת המים
  const r = await ev(`(()=>{const L=[...__TSW.m.values()];
    try{vegInit();vegFurnInit();for(const g of VEG.G){if(!g.ok)continue;for(const it of g.it)L.push({src:'VEG_D.t',t:VEG_D.ty[it[2]],x:it[0],y:it[1],mode:'data'})}for(const o of VEG.B){if(o[5])continue;L.push({src:'VEG_D.b',t:VEG_D.ty[o[2]],x:o[0],y:o[1],mode:'data'})}}catch(e){}
    try{for(const it of K34C.list)if(/^TP-/.test(it.id))L.push({src:'K34C.list',t:it.id,x:Math.round(it.x),y:Math.round(it.y),mode:'k34'})}catch(e){}
    try{for(const t of S12_TREES)L.push({src:'S12_TREES',t:t[2],x:t[0],y:t[1],mode:'data'})}catch(e){}
    const BL=new Set();for(const [x,y] of __TSW.bl||[])for(let i=-1;i<=1;i++)for(let j=-1;j<=1;j++)BL.add((Math.round(x/4)+i)+','+(Math.round(y/4)+j));
    const WP=/^(TP-WP-|lily_pads|reeds)/;
    const court=(()=>{let c;try{c=B4LOOK.data().court}catch(e){c=[2090,3240,2370,3390]}return[c[0]-20,c[1]-20,c[2]+20,c[3]+50]})(),pad=[3470,2405,80,120],lot=(()=>{try{const l=C3_LOTS.find(q=>q.kind==='player');return[l.x,l.y,l.x+l.w,l.y+l.h]}catch(e){return[2630,2266,3590,2545]}})();
    const W=[],Z={court:[],padIn:[],padSafety:[],lotVeg:[]};let blocked=0;
    for(const o of L){if(/^sign_/.test(o.t))continue;let w=false;try{w=WATERWALK.water(o.x,o.y,false)==='WATER'}catch(e){}let z='';try{z=tcZoneAt(o.x,o.y).code}catch(e){}o.zone=z;
     const isB=(o.mode==='frame'||o.mode==='scan')&&BL.has(Math.round(o.x/4)+','+Math.round(o.y/4));if(isB){o.blocked=1}
     if(w&&!WP.test(o.t)){if(isB)blocked++;else W.push(o)}
     if(isB)continue;
     if(/^VEG/.test(o.src)&&o.x>=court[0]&&o.x<=court[2]&&o.y>=court[1]&&o.y<=court[3])Z.court.push(o);
     const d=Math.hypot(o.x-pad[0],o.y-pad[1]);if(/^VEG/.test(o.src)){if(d<=pad[2])Z.padIn.push(o);else if(d<=pad[3])Z.padSafety.push(o);if(o.x>=lot[0]&&o.x<=lot[2]&&o.y>=lot[1]&&o.y<=lot[3])Z.lotVeg.push(o)}}
    let A=null;try{A=window.__TC_SEATREES&&window.__TC_SEATREES.audit()}catch(e){A={err:String(e)}}
    return {all:L.length,water:W.length,blockedOnWater:blocked,list:W,zones:{court:Z.court.length,padIn:Z.padIn.length,padSafety:Z.padSafety.length,lotVeg:Z.lotVeg.length},zoneList:Z,audit:A,allList:L}})()`);
  fs.writeFileSync(out, r);
  const R = JSON.parse(r); console.log('הכול ' + R.all + ' · גזעים על מים (מצוירים) ' + R.water + ' · נחסמו בציור ' + R.blockedOnWater + ' · במגרש B4 ' + R.zones.court + ' · במנחת ' + R.zones.padIn + ' + בטיחות ' + R.zones.padSafety + ' · VEG במגרש הבית ' + R.zones.lotVeg);
  const by = {}; for (const o of R.list) { const k = o.zone + ' ' + o.src + ' ' + o.t; by[k] = (by[k] || 0) + 1 } console.log(JSON.stringify(by));
  if (R.audit) console.log('audit בתוך המשחק: ' + JSON.stringify({ ok: R.audit.ok, water: (R.audit.water || []).length, zones: (R.audit.zones || []).length, n: R.audit.n, listsOnWater: R.audit.listsOnWater, err: R.audit.err || R.audit.vegErr }));
  const pass = R.water === 0 && R.zones.court === 0 && R.zones.padIn === 0 && R.zones.padSafety === 0 && R.zones.lotVeg === 0;
  console.log(pass ? 'SEATREES_GATE: עובר' : 'SEATREES_GATE: נכשל');
  if (errs.length) console.error('שגיאות דף: ' + errs.length + ' · ' + errs.slice(0, 4).join(' | '));
  await b.close(); process.exit(0);
})().catch(e => { console.error(String(e).slice(0, 400)); process.exit(1) });
