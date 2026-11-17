// אבחון: רכב חירום של אירוע שעומד במקום. node evt_still.js <build> <out.json> [realSecs=420] [shotsDir]
// אירועים אקראיים מהירים (__TC_EVT.fast); כל 2 שנ׳ — כל רכב של התנועה עם v.evt ו-still מעל 15 / 40 שנ׳: המצב המלא (הצומת — c2.why, ‏taxiRoute, הרכב שלפניו, הרמזור).
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
(async () => {
  const [file, out, rs, shots] = process.argv.slice(2); const RS = +rs || 420; if (shots) fs.mkdirSync(shots, { recursive: true });
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] }); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const pe = []; p.on('pageerror', e => pe.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' }); await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  const ev = s => p.evaluate(x => { try { return window.__TC_DEV.ev(x) } catch (e) { return { ERR: String(e && e.message || e) } } }, s);
  await ev(`(typeof p34LibInit==='function'&&!window.P34&&p34LibInit(),1)`); await p.waitForTimeout(2000);
  await ev(`(PERF.hud&&perfHudToggle(),__TC_EVT.fast(1),1)`);
  const DUMP = `(()=>{const L=[];for(const v of TRAFFIC_CARS){if(!v.evt||(v.evt.still||0)<15)continue;const e=EVT.act.find(q=>q.id===v.evt.id)||{};const R=v.taxiRoute,c=v.c2||{};
   const ahead=TRAFFIC_CARS.filter(o=>o!==v&&o.edgeId===v.edgeId&&o.dirSign===v.dirSign&&(o.t-v.t)*v.dirSign>=0&&Math.hypot(o.x-v.x,o.y-v.y)<160).map(o=>({id:o.id,kind:o.kind,d:Math.round(Math.hypot(o.x-v.x,o.y-v.y)),sp:+(o.speed||0).toFixed(1),wait:!!o.wait,evt:o.evt?o.evt.id:null,why:o.c2?o.c2.why:null,lane:o.lane}));
   const near=TRAFFIC_CARS.filter(o=>o!==v&&Math.hypot(o.x-v.x,o.y-v.y)<60).map(o=>({id:o.id,d:Math.round(Math.hypot(o.x-v.x,o.y-v.y)),edge:o.edgeId,sp:+(o.speed||0).toFixed(1)}));
   L.push({t:+EVT.t.toFixed(1),car:v.id,kind:v.kind,x:Math.round(v.x),y:Math.round(v.y),edge:v.edgeId,tt:+(v.t||0).toFixed(3),dir:v.dirSign,lane:v.lane,sp:+(v.speed||0).toFixed(2),ts:v.targetSpeed,wait:!!v.wait,stuck:v.stuck,hop:v.hop,
    plan:v.plan?(v.plan.length||Object.keys(v.plan).slice(0,6).join(',')):null,c2:{why:c.why||null,granted:!!c.granted,inside:c.insideNode||null,blockT:c.blockT!=null?+(+c.blockT).toFixed(1):null,stop:c.stopPoint!=null?c.stopPoint:null,mv:c.mv?String(c.mv.id||c.mv.key||'mv'):null},
    route:R?{ph:R.phase,hold:!!R.hold,arr:!!R.arrived,n:(R.nodes||[]).length,pos:R.pos,nodes:(R.nodes||[]).slice(0,8),entry:R.entryNode,fe:R.finalEdgeId,fd:R.finalDirSign,ft:R.finalT!=null?+R.finalT.toFixed(3):null,fa:!!R.finalActive,tgt:[Math.round(R.targetX),Math.round(R.targetY)]}:null,
    evt:{id:v.evt.id,ph:v.evt.ph,still:+(v.evt.still||0).toFixed(1),rr:v.evt.rrAt,tgt:[Math.round(v.evt.tx||0),Math.round(v.evt.ty||0)]},ev:{type:e.type,ph:e.ph,x:Math.round(e.x||0),y:Math.round(e.y||0),rt:e.rt!=null?+e.rt.toFixed(1):null,arr:e.arr||null,dist:Math.round(Math.hypot(v.x-(e.x||0),v.y-(e.y||0)))},
    ahead,near,csvc:!!v.csvc,c5:!!v.c5,cl:!!v.cl})}return L})()`;
  const R = { build: path.basename(file), dumps: [], shots: [] }; const seen = {}; const t0 = Date.now(); let maxStill = 0;
  while ((Date.now() - t0) / 1000 < RS) {
    await p.waitForTimeout(2000);
    const L = await ev(DUMP); if (!Array.isArray(L)) { R.err = L; break }
    for (const d of L) { maxStill = Math.max(maxStill, d.evt.still); const k = d.car + '|' + d.evt.id + '|' + (d.evt.still >= 40 ? 2 : 1); if (seen[k]) continue; seen[k] = 1; R.dumps.push(d);
      if (shots && d.evt.still >= 40) { await ev(`(State.mapQa||toggleMapQa(),Camera.x=${d.x},Camera.y=${d.y},Camera.zoom=2.2,1)`); await p.waitForTimeout(1200); const f = path.join(shots, 'still_' + d.car + '_' + Math.round(d.t) + '.png'); await p.screenshot({ path: f }); R.shots.push(f); await ev(`(State.mapQa&&toggleMapQa(),1)`) } }
  }
  R.st = await ev(`({t:EVT.t,st:EVT.st,log:EVT.log.slice(-60)})`); R.maxStill = maxStill; R.pageErrors = pe;
  fs.writeFileSync(out, JSON.stringify(R, null, 1)); console.log(JSON.stringify({ dumps: R.dumps.length, maxStill, still: R.st.st && R.st.st.still, stuck: R.st.st && R.st.st.stuck, pe: pe.length }));
  await b.close();
})().catch(e => { console.error(String(e).slice(0, 400)); process.exit(1) });
