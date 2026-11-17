// sl_tugs.js <game.html> <out.json> [maxS=6000] [shotDir] — sealife: "איתן" ו"גבור" עם "גלי הכרמל" — עבודה, מים בלבד, בלי חפיפות, ההמתנות; וצילומים לבדיקה עצמית
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out, maxS0, shotDir] = process.argv.slice(2); const MAXS = +(maxS0 || 6000);
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] }); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 900000, polling: 500 });
  await p.waitForTimeout(1500); const ev = s => p.evaluate(x => window.__TC_DEV.ev(x), s);
  const Q = `(()=>{const X=window.__TC_TUGX,s=X.state(),SH=S10KIT.c6d6.shipOf('BRT-D6'),ob=(id,x,y,h,L,B)=>({id,x,y,c:Math.cos(h),s:Math.sin(h),L,B});
   const O=[];for(const t of s.tugs)if(!t.home)O.push(ob(t.id,t.x,t.y,t.h,281.2,95.6));
   const ship=ob('BRT-D6',SH.x,SH.y,SH.h||0,SH.L,SH.B);let t1=null;try{const t=S14.dayT(S14.gmin())[1],P=S14.poseOf('TUG-1',t);t1=ob('TUG-1',P.x,P.y,P.h,281.2,95.6)}catch(e){}
   let fe=null;try{const F=a6FerryPose();fe=ob('FERRY',F.x,F.y,F.h!=null?F.h:(F.a||0),450,130)}catch(e){}
   const pts=o=>{const R=[];for(const [lx,ly] of[[o.L/2,0],[o.L*.3,o.B/2],[o.L*.3,-o.B/2],[-o.L/2,o.B/2],[-o.L/2,-o.B/2],[0,o.B/2],[0,-o.B/2],[0,0]])R.push([o.x+lx*o.c-ly*o.s,o.y+lx*o.s+ly*o.c]);return R};
   const inside=(P,q,m)=>{const x=P[0]-q.x,y=P[1]-q.y,u=x*q.c+y*q.s,v=-x*q.s+y*q.c;return Math.abs(u)<q.L/2-m&&Math.abs(v)<q.B/2-m};
   const hit=(a,b,m)=>pts(a).some(P=>inside(P,b,m))||pts(b).some(P=>inside(P,a,m));
   const bad=[];for(const o of O){if(pts(o).some(P=>{try{return!w3IsSea(P[0],P[1])}catch(e){return false}}))bad.push(o.id+':land');if(hit(o,ship,6))bad.push(o.id+'×ship');if(t1&&hit(o,t1,2))bad.push(o.id+'×TUG-1');if(fe&&hit(o,fe,2))bad.push(o.id+'×ferry')}
   if(O.length===2&&hit(O[0],O[1],2))bad.push('TUG-2×TUG-3');
   let clk='';try{const m=lgMinOfDay();clk=String(Math.floor(m/60)).padStart(2,'0')+':'+String(Math.floor(m%60)).padStart(2,'0')}catch(e){}
   return{clk,ph:s.ship.ph,shipY:s.ship.y,hold:s.ship.hold,job:s.job&&s.job.kind,wait:s.wait,tugs:s.tugs.map(t=>[t.id,t.x,t.y,t.mode,t.leg,t.att?1:0,t.home?1:0]),bad}})()`;
  const res = { samples: [], bad: [], phases: [], jobsDone: 0 }; let lastPh = null, t = 0, shots = 0;
  while (t < MAXS) {
    const r = await ev(Q); if (r.ph !== lastPh) { res.phases.push([t, r.clk, r.ph, r.job]); lastPh = r.ph }
    if (r.bad.length) res.bad.push([t, r.clk, r.bad.join(','), JSON.stringify(r.tugs)]);
    if (r.job || t % 60 === 0) res.samples.push([t, r.clk, r.ph, r.job, r.wait && r.wait.ph, r.tugs.map(x => x.slice(1, 5).join('/')).join(' | ')]);
    if (shotDir && r.job && shots < 8 && t % 30 === 0) { const tg = r.tugs.find(x => !x[6]); if (tg) { await ev(`perfCamera({x:${tg[1]},y:${tg[2]},zoom:.7})`); await p.waitForTimeout(1200); await p.screenshot({ path: path.join(shotDir, 'tug_' + (shots++) + '.png') }) } }
    const st = await ev(`window.__TC_TUGX.stats()`); res.jobsDone = st.jobs;
    if (st.dep >= 1 && st.arr >= 1 && !r.job) break;
    const step = r.job || (r.ph !== 'docked' && r.ph !== 'sea' && r.ph !== 'unload') ? 2 : 20;
    await ev(`window.__TC_SIM_STEP_QA({seconds:${step},warmup:0,every:${step}})`); t += step;
  }
  res.simS = t; res.stats = await ev(`window.__TC_TUGX.stats()`); res.tow = await ev(`window.__TC_TUGX.towWindow()`); res.err = await ev(`window.__TC_TUGX.err()`);
  res.ok = res.stats.dep >= 1 && res.stats.arr >= 1 && !res.bad.length && !res.err && res.stats.noTug === 0;
  fs.writeFileSync(out, JSON.stringify({ res, errs }, null, 1));
  console.log(JSON.stringify({ ok: res.ok, simS: t, stats: res.stats, bad: res.bad.slice(0, 8), phases: res.phases.slice(0, 40), tow: res.tow }).slice(0, 6000)); console.log('errs', JSON.stringify(errs)); await b.close();
})().catch(e => { console.error(String(e).slice(0, 300)); process.exit(1) });
