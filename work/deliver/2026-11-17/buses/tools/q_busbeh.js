// q_busbeh.js <game.html> <out.json> [warm=420] [secs=900] [night=0] — buses (סבב 17.11): האוטובוסים מול המכוניות, במדידה.
// הרצה מהירה (__TC_SIM_STEP_QA) — כל שנייה: לכל רכב בכביש — הסוג (מכונית / אוטובוס של הקווים לפי קו / קואץ׳ / אוטובוס ישן / משאית ...),
// והאם עומד (מהירות < 0.5); לעומד — הסיבה (c2.limit של V2, או השלב + waitBy של הקווים), והשכבה שעצרה אותו (bend / rb-bus / bay ...) — לפי עטיפה
// של הפונקציות בזמן הבדיקה בלבד (לא במשחק). בסוף: שניות עמידה לכל סוג × סיבה, העמידה הארוכה ביותר לכל סוג, המגעים (contact) — מי נוגע במי.
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
const INSTR = `(()=>{const Q=window.__BQ={hold:{},rb:{},bay:{},lb:{},bo:{},gy:{}};const inc=(o,k)=>{o[k]=(o[k]||0)+1};
 try{const h0=holdLines2;holdLines2=function(v,lane){const a=(LE&&LE.st&&LE.st.bendHold)||0;const r=h0.apply(this,arguments);const b=(LE&&LE.st&&LE.st.bendHold)||0;if(b>a){inc(Q.hold,v.id);try{const id=LE.st.bendBy,o=VEH_BY_ID2.get(id)||TRAFFIC_CARS.find(q=>q.id===id),oc=o&&o.c2;let k='?';if(oc&&oc.mv)k='in-node';else if(oc&&oc.lane){const z=oc.lane.leBendS;k=(z!=null&&oc.s+oc.hl>=z-4)?'in-zone':((o.speed||0)>2?'moving-far':'still-far')}Q.bk=Q.bk||{};inc(Q.bk,k)}catch(e){}}return r}}catch(e){Q.e1=String(e)}
 try{const r0=lcRbBusYield;lcRbBusYield=function(v,mv,node){const r=r0.apply(this,arguments);if(r)inc(Q.rb,v.id);return r}}catch(e){Q.e2=String(e)}
 try{const k0=backoutStep2;backoutStep2=function(v){inc(Q.bo,v.id);return k0.apply(this,arguments)}}catch(e){Q.e3=String(e)}
 try{const l0=laneBackStep2;laneBackStep2=function(v){inc(Q.lb,v.id);return l0.apply(this,arguments)}}catch(e){Q.e4=String(e)}
 try{const g0=ghostYield2;ghostYield2=function(v){const r=g0.apply(this,arguments);if(r)inc(Q.gy,v.id);return r}}catch(e){Q.e5=String(e)}
 try{const d0=lnDrive;lnDrive=function(B,dt,vmax){const y0=LN.stats.yields||0;const r=d0.apply(this,arguments);if((LN.stats.yields||0)>y0){const one=!(B.ign instanceof Set),id=one?B.ign:[...B.ign].join(','),o=one?TRAFFIC_CARS.find(q=>q.id===B.ign):null,oc=o&&o.c2;Q.yn=(Q.yn||0)+1;Q.yl=Q.yl||[];if(Q.yl.length<60)Q.yl.push({t:+LN.t.toFixed(0),clk:gameClock().hhmm,no:B.no,ph:B.ph,at:B.at||null,x:Math.round(B.v.x),y:Math.round(B.v.y),hit:String(id),hitLn:o&&o.ln?o.ln.no+':'+o.ln.ph:null,lim:oc?String(oc.limit):null,hardBy:oc?oc.hardBy||null:null,lane:oc&&oc.lane?oc.lane.id:null,mv:oc&&oc.mv?oc.mv.id:null,lb:oc?oc.laneBack||0:null,bo:oc?!!oc.backout:null,rec:o?o.recoveries2||0:null,sp:o?+(o.speed||0).toFixed(1):null,ox:o?Math.round(o.x):null,oy:o?Math.round(o.y):null})}return r}}catch(e){Q.e6=String(e)}
 return Object.keys(Q).filter(k=>k.startsWith('e')).map(k=>Q[k])})()`;
const SAMPLE = `(()=>{const Q=window.__BQ,T=(v)=>{if(v.ln){const L=v.ln.L;return L&&L.id==='5'?'coach5':'ln'+(L?L.id:'?')}if(BUS_VEHICLES.includes(v))return'bus-old';const id=String(v.id);
  if(/^AI-CAR|^A4-CIV|^VH-/.test(id)||/^VH-/.test(String(v.asset||'')))return v.taxiRoute||v.taxi?'taxi':'car';const p=v.c2&&v.c2.profile;return 'oth:'+(p||(v.c5?'c5':'-'))};
 const o=[];const seen=new Set();for(const v of [...TRAFFIC_CARS,...BUS_VEHICLES]){if(seen.has(v))continue;seen.add(v);const t=T(v),sp=v.speed||0,c=v.c2;let why='';
  if(sp<0.5){if(c){why=String(c.limit||'?');if(why.startsWith('contact:')){const id=why.slice(8),w=VEH_BY_ID2.get(id);why='contact:'+(w?T(w):'sub')}else why=why.replace(/[0-9]+/g,'#')}
   else if(v.ln){why='ln:'+v.ln.ph+':'+String(v.ln.waitBy||'').replace(/[A-Z]+-?[0-9][-A-Z0-9_:#]*/g,'X').replace(/[0-9]+/g,'#').slice(0,40)}else why='nocore'}
  const hb=Q.hold[v.id]||0,rb=Q.rb[v.id]||0,bo=Q.bo[v.id]||0,lb=Q.lb[v.id]||0,gy=Q.gy[v.id]||0;
  o.push([String(v.id),t,+sp.toFixed(1),why,hb,rb,bo,lb,gy,Math.round(v.x),Math.round(v.y),c&&c.lane?c.lane.id:(v.ln?v.ln.ph:'')])}
 Q.hold={};Q.rb={};Q.bo={};Q.lb={};Q.gy={};const bk=Q.bk||{};Q.bk={};return{clk:gameClock().hhmm,o,bk}})()`;
(async () => {
  const [file, out, warmA, secsA, nightA] = process.argv.slice(2); const warm = +warmA || 420, secs = +secsA || 900, night = +nightA || 0;
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] }); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 900000, polling: 500 });
  await p.waitForTimeout(1500);
  const ev = s => p.evaluate(s => window.__TC_DEV.ev(s), s);
  const step = s => p.evaluate(s => { window.__TC_SIM_STEP_QA({ seconds: s, warmup: 0, every: s }); return 1 }, s);
  const t0 = Date.now(); await step(warm);
  if (night) await ev('gameClockSet(0,35)');
  const ie = await ev(INSTR);
  const A = {}, MX = {}, run = {}, CT = {}, LAY = {}, N = {}, BK = {}; let clk0 = null, clk1 = null;
  for (let i = 0; i < secs; i++) {
    await step(1); const r = await ev(SAMPLE); if (!clk0) clk0 = r.clk; clk1 = r.clk;
    for (const q of r.o) {
      const [id, t, sp, why, hb, rb, bo, lb, gy, x, y, lane] = q; N[t] = N[t] || new Set(); N[t].add(id);
      const L = LAY[t] = LAY[t] || { bend: 0, rbYieldToBus: 0, backout: 0, laneBack: 0, ghostYield: 0, stopS: 0, moveS: 0 };
      L.bend += hb ? 1 : 0; L.rbYieldToBus += rb ? 1 : 0; L.backout += bo ? 1 : 0; L.laneBack += lb ? 1 : 0; L.ghostYield += gy ? 1 : 0;
      if (sp < 0.5) { L.stopS++; const k = t + ' | ' + (hb ? 'bend-hold' : why); A[k] = (A[k] || 0) + 1; run[id] = (run[id] || 0) + 1;
        if (!MX[t] || run[id] > MX[t].s) MX[t] = { s: run[id], id, why: hb ? 'bend-hold' : why, x, y, lane, at: r.clk };
        if (why.startsWith('contact:')) { const kk = t + '>' + why.slice(8); CT[kk] = (CT[kk] || 0) + 1 } }
      else { L.moveS++; run[id] = 0 }
    }
    for (const [k, v] of Object.entries(r.bk || {})) BK[k] = (BK[k] || 0) + v;
    if (i % 100 === 0) console.log('t', i, r.clk, ((Date.now() - t0) / 1000).toFixed(0) + 's');
  }
  let aud = null; try { aud = await ev("typeof busesAudit==='function'?busesAudit():({old:{paused:BUS_LINES_PAUSED,vehicles:BUS_VEHICLES.length},lines:LN_LINES.map(L=>L.id),buses:LN.bus.length,le:LE.st})") } catch (e) { aud = String(e).slice(0, 200) }
  let lns = null; try { lns = await ev("({frz:LN.aud&&LN.aud.frz?{max:LN.aud.frz.max,n:LN.aud.frz.n,info:(LN.aud.frz.info||[]).map(q=>[q.no,q.ph,q.x,q.y,q.t,q.waitBy])}:null,stats:{...LN.stats},le:(typeof LE!=='undefined'?{...LE.st}:null),lcz:(typeof LCZ!=='undefined'?{...LCZ.st}:null)})") } catch (e) { lns = String(e).slice(0, 200) }
  let yl = null; try { yl = await ev('({n:window.__BQ.yn||0,list:window.__BQ.yl||[]})') } catch (e) { yl = String(e).slice(0, 200) }
  const by = {}; for (const [k, v] of Object.entries(A)) { const [t, w] = k.split(' | '); (by[t] = by[t] || []).push([w, v]) }
  for (const t in by) by[t].sort((a, b) => b[1] - a[1]);
  const share = {}; for (const t in LAY) { const L = LAY[t]; share[t] = { n: N[t].size, stopShare: +(L.stopS / Math.max(1, L.stopS + L.moveS)).toFixed(3), ...L } }
  const R = { build: path.basename(file), aud, lns, busFirst: yl, warm, secs, night, clk0, clk1, instrErr: ie, share, bendBlocker: BK, longest: MX, contacts: CT, reasons: by, errs, wallS: ((Date.now() - t0) / 1000) | 0 };
  fs.writeFileSync(out, JSON.stringify(R, null, 1)); console.log(JSON.stringify({ share, longest: MX }).slice(0, 3000)); console.log('errs', errs.length); await b.close();
})().catch(e => { console.error(String(e).slice(0, 600)); process.exit(1) });
