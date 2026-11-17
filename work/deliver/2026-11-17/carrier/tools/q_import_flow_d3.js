// q_import_flow_d3.js (carrier, 17.11 — עותק של q_import_flow.js של s10c, ועוד מדידה של הפריקה ב-D3: הדרך של המכונית, עמידה על יותר מנתיב אחד, הנתיב השמאלי) — הבדיקה של הפריקה מקצה לקצה במסוף היבוא (S10 ג; "בדיקה באמת" של הבעלים, D‑623):
//   node q_import_flow.js <game.html> <out.json> [simSec=3300]
// מריץ את הסימולציה עצמה מהר (simStep, בלי ציור — כמו vinv) מ-07:00 לאורך יום משחק ויותר, ומודד מתוך המשחק (window.__S10C, ‏LOGI):
//   כמה רכבים ירדו, כמה נכנסו לשורה הנכונה (דגם וצבע), כמה הובלו ל-D3, הזמן מהעגינה עד שהאונייה ריקה, הזמן של כל רכב מהרמפה עד המקום,
//   שאף רכב לא עמד יותר מ-20 שנ׳, שאין רכבת על המעבר כשהרמפה לא למעלה, שהמעבר פתוח לרכבים 75% לפחות וסגירה עד 90 שנ׳ (מחוץ לפריקה),
//   ושמספר הרכבים בשורות חוזר (אף רכב לא נוצר ולא נעלם בתוך העולם).
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
(async () => {
  const [file, out, simSec] = process.argv.slice(2); const SIM = +simSec || 3300;
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] }); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const pe = []; p.on('pageerror', e => pe.push(String(e && e.stack || e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready() && window.__S10C, null, { timeout: 600000, polling: 500 });
  const t0 = Date.now();
  const init = await p.evaluate(() => { const ev = s => window.__TC_DEV.ev(s); return ev(`({clk:gameClock().hhmm,pk:PARKED_CARS.filter(o=>/^PC10-IM/.test(o.id)).length,err:__S10C.err()})`) });

  await p.evaluate(() => window.__TC_DEV.ev(`(()=>{const R={n:0,red:0,redAt:null,tailMin:1e9,tailAt:null,multi:0,multiMaxS:0,multiAt:null,still:{},stillMax:0,stillAt:null,headOn:0,headOnAt:null,laneSeen:{},offPts:[],lanes:null,err:null,envRowMin:1e9,envRowAt:null,envStall:0,envStallAt:null,soldCcMin:1e9,soldCcAt:null,maxHalfLen:0,ccHeadOn:0,ccHeadOnAt:null,pairMin:1e9,pairAt:null};
   const capD=(a,b)=>{let m=1e9;for(let i=0;i<=4;i++)for(let j=0;j<=4;j++){const p=[a.ax+(a.bx-a.ax)*i/4,a.ay+(a.by-a.ay)*i/4],q=[b.ax+(b.bx-b.ax)*j/4,b.ay+(b.by-b.ay)*j/4];m=Math.min(m,Math.hypot(p[0]-q[0],p[1]-q[1])-a.radius-b.radius)}return m};
   const capR=(a,r)=>{let o=-1e9;for(let i=0;i<=4;i++){const x=a.ax+(a.bx-a.ax)*i/4,y=a.ay+(a.by-a.ay)*i/4;o=Math.max(o,Math.min(x+a.radius,r[2])-Math.max(x-a.radius,r[0])>0&&Math.min(y+a.radius,r[3])-Math.max(y-a.radius,r[1])>0?Math.min(Math.min(x+a.radius,r[2])-Math.max(x-a.radius,r[0]),Math.min(y+a.radius,r[3])-Math.max(y-a.radius,r[1])):-1)}return o};
   const STALLS=[[4247,2312,4320,2412],[4298,2270,4410,2298]];
   const LN=[];for(const l of LANE_LIST2){if(Math.max(l.ax,l.bx)<4050||Math.min(l.ax,l.bx)>4800||Math.max(l.ay,l.by)<2050||Math.min(l.ay,l.by)>2750)continue;LN.push(l)}
   const byE={};for(const l of LN){(byE[l.edge]=byE[l.edge]||[]).push(l)}
   for(const e in byE){const L=byE[e],r=L[0],nx=-r.uy,ny=r.ux,off=L.map(l=>(l.ax-r.ax)*nx+(l.ay-r.ay)*ny).sort((a,b)=>a-b);let sp=99;for(let i=1;i<off.length;i++)sp=Math.min(sp,Math.abs(off[i]-off[i-1]));if(sp>60||sp<8)sp=24;for(const l of L)l.__hw=sp/2}
   R.lanes=LN.length;const cont={};
   window.__crS=function(dt){try{R.n++;const C=S10CI.carrier,V=S10CI.cars.filter(o=>o.s10c&&/^(offdeck|road|leave)$/.test(o.s10c.m));if(C)V.push(C);
    for(const v of V){if(!(v.x>4100&&v.x<4750&&v.y>2100&&v.y<2700))continue;let sh;try{sh=trafficVehicleShape(v)}catch(e){continue}
     if(v.s10c&&v.s10c.m==='offdeck'){
      if(v.x>4252&&v.x<4320&&v.y>2312&&v.y<2412||v.x>4252&&v.x<4459&&v.y>2412&&v.y<2482){R.red++;R.redAt=R.redAt||[v.id,Math.round(v.x),Math.round(v.y)]}
      const tx=v.x-Math.cos(v.heading)*sh.halfLength,ty=v.y-Math.sin(v.heading)*sh.halfLength;if(v.s10c.st!=='d3north'&&v.s10c.st!=='d3sold'&&v.x<4262&&v.y<2300&&ty<R.tailMin){R.tailMin=+ty.toFixed(1);R.tailAt=[v.id,Math.round(v.x),Math.round(v.y),+v.heading.toFixed(2)]}
      R.maxHalfLen=Math.max(R.maxHalfLen,+sh.halfLength.toFixed(1));const st=v.s10c.st,mv=(v.speed||0)>.5;
      if(st!=='d3north'&&st!=='d3sold'&&v.x<4290&&v.y<2300){const e=Math.min(sh.ay,sh.by)-sh.radius;if(e<R.envRowMin){R.envRowMin=+e.toFixed(1);R.envRowAt=[v.id,Math.round(v.x),Math.round(v.y),+v.heading.toFixed(2)]}}
      for(const r of STALLS){const ov=capR(sh,r);if(ov>1&&st!=='d3north'){R.envStall++;R.envStallAt=R.envStallAt||[v.id,Math.round(v.x),Math.round(v.y),r.join(',')]}}
      if(st==='d3sold'&&C){try{const d=capD(sh,trafficVehicleShape(C));if(d<R.soldCcMin){R.soldCcMin=+d.toFixed(1);R.soldCcAt=[v.id,Math.round(v.x),Math.round(v.y)]}}catch(e){}}
      if(C&&C.x>4198&&C.x<4254&&C.y>2290&&C.y<2505&&Math.sin(C.heading)<-.5&&v.x>4198&&v.x<4254&&v.y>2290&&v.y<2505&&Math.sin(v.heading)>.5){R.ccHeadOn++;R.ccHeadOnAt=R.ccHeadOnAt||[v.id,Math.round(v.x),Math.round(v.y)]}
      if(mv&&v.x<4290)for(const o of V){if(o===v||o===C||!o.s10c||o.s10c.m!=='offdeck'||!((o.speed||0)>.5)||!(o.x<4290&&o.x>4100&&o.y>2100&&o.y<2700))continue;let so;try{so=trafficVehicleShape(o)}catch(e){continue}const d=capD(sh,so);if(d<R.pairMin){R.pairMin=+d.toFixed(1);R.pairAt=[v.id,o.id,Math.round(v.x),Math.round(v.y),Math.round(o.x),Math.round(o.y)]}}
      if(R.offPts.length<4000&&R.n%4===0)R.offPts.push([Math.round(v.x),Math.round(v.y)]);
      const sv=R.still[v.id]=(v.speed||0)<.5?(R.still[v.id]||0)+dt:0;if(sv>R.stillMax){R.stillMax=+sv.toFixed(1);R.stillAt=[v.id,Math.round(v.x),Math.round(v.y),v.s10c.waitBy||'']}
      if(v.x>4198&&v.x<4254&&v.y>2290&&v.y<2505){for(const o of lgOthers(v)){if(o===v||o===C||!(o.x>-9000)||(o.s10c&&/^(hold|deck|pool)$/.test(o.s10c.m)))continue;if(o.x>4198&&o.x<4254&&o.y>2290&&o.y<2505&&Math.cos(o.heading-v.heading)<-.5){R.headOn++;R.headOnAt=R.headOnAt||[v.id,o.id,Math.round(o.x),Math.round(o.y)]}}}}
     if((v.speed||0)>=.5){cont[v.id]=0;continue}
     let n=0;const used=[];for(const l of LN){const nx=-l.uy,ny=l.ux,la=(sh.ax-l.ax)*nx+(sh.ay-l.ay)*ny,lb=(sh.bx-l.ax)*nx+(sh.by-l.ay)*ny,ta=(sh.ax-l.ax)*l.ux+(sh.ay-l.ay)*l.uy,tb=(sh.bx-l.ax)*l.ux+(sh.by-l.ay)*l.uy;
      if(Math.max(ta,tb)<0||Math.min(ta,tb)>l.len)continue;const lo=Math.min(la,lb)-sh.radius,hi=Math.max(la,lb)+sh.radius,ov=Math.min(hi,l.__hw)-Math.max(lo,-l.__hw);if(ov>4){n++;used.push(l.id)}}
     if(n>=2){cont[v.id]=(cont[v.id]||0)+dt;if(cont[v.id]>=2){R.multi++;if(cont[v.id]>R.multiMaxS){R.multiMaxS=+cont[v.id].toFixed(1);R.multiAt=[v.id,Math.round(v.x),Math.round(v.y),used.join(' ')]}}}else cont[v.id]=0}
   }catch(e){R.err=R.err||String(e&&e.message||e)}};window.__crR=R;return R.lanes})()`));
  const trace = []; let done = 0;
  while (done < SIM) {
    const r = await p.evaluate((n) => window.__TC_DEV.ev(`(()=>{const L=SIM_LOOP,H=L.h;if(L.simNow==null)L.simNow=performance.now();const t0=performance.now();let k=0;
      while(k<${n}*60){simStep(H,L.simNow+H*1000);L.simNow+=H*1000;k++;if(k%30===0)__crS(H*30);}
      /* המעבר מחוץ לפריקה: כל 0.5 שנ׳ (בלוח הזמנים) — סגור כשגוף קרון חופף את הנתיב עכשיו או ב-8 השניות הבאות */
      const s=__S10C.state();return{T:s.T,clk:s.clk,ph:s.ship.ph,a:s.ship.a,hold:s.ship.hold,orders:s.orders,car:s.carrier&&[s.carrier.mode,s.carrier.site||s.carrier.to,s.carrier.deck.filter(Boolean).length,s.carrier.waitBy,s.carrier.blkBy,s.carrier.x,s.carrier.y,(()=>{try{const e=core2Explain(S10CI.carrier);return e&&(e.limit+':'+(e.lead||e.why||''))}catch(x){return''}})()],ms:Math.round(performance.now()-t0),err:__S10C.err(),lerr:LOGI.err}})()`), 30);
    done += 30; trace.push(r); if (r.err || r.lerr) break;
    if (Date.now() - t0 > 40 * 60000) break;
  }
  const fin = await p.evaluate(() => window.__TC_DEV.ev(`(()=>{const S=__S10C.stats(),st=__S10C.state();
    const pk=PARKED_CARS.filter(o=>/^PC10-IM/.test(o.id)).length;const cars=Object.entries(S.car).map(([id,c])=>Object.assign({id},c));
    /* המעבר מחוץ לפריקה (לוח הזמנים הנוכחי, מחזור שלם) */
    let cl=0,n=0,run=0,mx=0;const T0=SIM_LOOP.simNow+SIM_BENCH_OFS;for(let s=0;s<740;s+=.5){let c=false;for(const d of[0,2000,4000,6000,8000])if(S10CI.trainOnX(T0+s*1000+d)){c=true;break}n++;if(c){cl++;run+=.5;mx=Math.max(mx,run)}else run=0}
    const buyers=S10CI.cars.filter(v=>v.s10c.m==='road'||v.s10c.m==='leave').map(v=>{let e=null;try{e=core2Explain(v)}catch(x){}return[v.id,v.s10c.m,Math.round(v.x),Math.round(v.y),v.edgeId,v.routeIndex+'/'+(v.c5.route||[]).length,e&&(e.cls+':'+e.limit+':'+(e.lead||e.why||''))]});
    return{stats:S,state:st,pk,cars,buyers,xing:{closedPct:+(100*cl/n).toFixed(1),maxClosureS:mx},logi:__TC_LOGI.state().find(v=>v.id==='LOGI-CC-1'),lgStats:LOGI.stats,audit:(()=>{try{const a=lgPathAudit();return{ok:a.ok,solid:a.solid.filter(q=>/D6C|D3D/.test(q[0])),along:a.along.filter(q=>/D6C|D3D/.test(q[0]))}}catch(e){return String(e)}})(),log:__S10C.log().slice(-40)}})()`));
  const crd = await p.evaluate(() => window.__TC_DEV.ev(`(()=>{const R=window.__crR;return Object.assign({},R,{still:undefined,st:window.__CRD3?__CRD3.st():null,geo:window.__CRD3?__CRD3.geo():null,crErr:window.__CRD3?__CRD3.err():'אין __CRD3'})})()`));
  const S = fin.stats, calls = S.calls.map(c => ({ n: c.n, released: c.released, parked: c.parked, arrive: c.clkArr, rampDown: c.clkDown, empty: c.clkEmpty, allParked: c.clkAllParked,
    dockToEmptyS: c.tDown != null && c.tEmpty != null ? +(c.tEmpty - c.tDown).toFixed(1) : null, dockToAllParkedS: c.tDown != null && c.tAllParked != null ? +(c.tAllParked - c.tDown).toFixed(1) : null }));
  const rs = fin.cars.filter(c => c.rampToStall != null).map(c => c.rampToStall);
  const res = {
    build: path.basename(file), simSec: done, wallS: Math.round((Date.now() - t0) / 1000), start: init.clk, end: fin.state.clk,
    unloaded: S.released, parked: S.parked, parkedRight: S.parkedRight, parkedWrong: S.parkedWrong, loadedOnCarrier: S.loaded, deliveredD3: S.delivered, leftCity: S.left, refilled: S.refilled, lost: S.lost,
    calls, rampToStall: { n: rs.length, min: rs.length ? Math.min(...rs) : null, max: rs.length ? Math.max(...rs) : null, avg: rs.length ? +(rs.reduce((a, b) => a + b, 0) / rs.length).toFixed(1) : null },
    maxStillS: S.maxStill, still20: S.still20, trainOnCrossingWhileRampDown: S.xViol, rampDownSamples: S.xSamples, carOnCrossingWithTrain: S.xCarTrain,
    crossingOutsideUnload: fin.xing, importParked: { start: init.pk, end: fin.pk }, carrier: fin.logi, carrierTrips: fin.lgStats.trips, pathAudit: fin.audit, buyersOnRoad: fin.buyers, pageErrors: pe, err: fin.state && trace.length ? trace[trace.length - 1].err : null,
  };
  const fails = [];
  res.d3 = crd; if (crd.red) fails.push('D3: מכונית שירדה עברה בחניות / ברחבת המוסך'); if (crd.multi) fails.push('D3: עמידה על יותר מנתיב אחד'); if (crd.headOn) fails.push('D3: חזית מול חזית בנתיב השמאלי'); if (crd.tailMin < 2219) fails.push('D3: הזנב בשורת התצוגה'); if (crd.err || crd.crErr) fails.push('D3: שגיאה בדגימה / בחלק');
  if (crd.envRowMin < 2218.5) fails.push('D3: המעטפת של הסיבוב נכנסת לשורת התצוגה'); if (crd.envStall) fails.push('D3: המעטפת נכנסת לחניות'); if (crd.soldCcMin < 4) fails.push('D3: מכונית התצוגה ליד המוביל'); if (crd.ccHeadOn) fails.push('D3: המוביל ומכונית חזית מול חזית בנתיב'); if (crd.pairMin < 4) fails.push('D3: שתי מכוניות שיורדות — גוף ליד גוף');
  if (!(res.unloaded >= 12)) fails.push('ירדו פחות מ-12'); if (res.parkedWrong) fails.push('רכב בשורה לא נכונה'); if (!(res.deliveredD3 >= 3)) fails.push('לא הובלו ל-D3');
  if (res.maxStillS > 20) fails.push('רכב עמד יותר מ-20 שנ׳'); if (res.trainOnCrossingWhileRampDown) fails.push('רכבת על המעבר כשהרמפה לא למעלה'); if (res.carOnCrossingWithTrain) fails.push('רכב ורכבת על המעבר');
  if (res.crossingOutsideUnload.closedPct > 25 || res.crossingOutsideUnload.maxClosureS > 90) fails.push('המעבר סגור יותר מדי'); if (res.lost) fails.push('רכב אבד'); if (pe.length || res.err) fails.push('שגיאות');
  if (res.pathAudit && res.pathAudit.ok === false && (res.pathAudit.solid.length || res.pathAudit.along.length)) fails.push('מסלול המוביל במכשול / לאורך מדרכה');
  res.ok = !fails.length; res.fails = fails; res.trace = trace; res.log = fin.log;
  fs.writeFileSync(out, JSON.stringify(res, null, 1));
  console.log(JSON.stringify({ ok: res.ok, fails, d3: Object.assign({}, crd, { offPts: (crd.offPts||[]).length }), unloaded: res.unloaded, parked: res.parked, right: res.parkedRight, delivered: res.deliveredD3, left: res.leftCity, calls, rampToStall: res.rampToStall, maxStillS: res.maxStillS, xViol: res.trainOnCrossingWhileRampDown, xing: res.crossingOutsideUnload, pk: res.importParked, wallS: res.wallS, simSec: done, end: res.end }));
  await b.close();
})().catch(e => { console.error(String(e).slice(0, 400)); process.exit(1) });
