// בדיקת המסוקים והנפילה: node evt_heli.js <build> <out.json> [shotsDir] [maxSecs=300] — (1) אש במבנה + מסוק הכיבוי, (2) אש קצרה — המסוק חוזר, (3) נפילה לא מתחת לצמרת, (4) בורח + מסוק המשטרה
// (1) אש במבנה ליד השחקן (F9 — evtF9Go עם building) → מסוק הכיבוי ממריא מהגג של A4, מטיל, ממלא, מטיל, חוזר לגג (done == ok), והאש נכבית.
// (2) אש שנגמרת לפני שהמסוק סיים → המסוק חוזר ישר לגג.
// (3) "אדם נופל" — האיש לא מתחת לצמרת (לפי העצים שצוירו בפריים).
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
(async () => {
  const [file, out, shots, maxS] = process.argv.slice(2); const MAX = +maxS || 300;
  if (shots) fs.mkdirSync(shots, { recursive: true });
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] }); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const pe = []; p.on('pageerror', e => pe.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' }); await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  const ev = s => p.evaluate(x => { try { return window.__TC_DEV.ev(x) } catch (e) { return { ERR: String(e && e.message || e) } } }, s);
  const R = { build: path.basename(file), fire: {}, short: {}, fall: {} };
  await ev(`(typeof p34LibInit==='function'&&!window.P34&&p34LibInit(),1)`); await p.waitForTimeout(2500);
  await ev(`(EVT.next.fire=EVT.next.fall=EVT.next.flee=1e9,1)`);   // no random events during this check
  R.heli0 = await ev(`__TC_EVT.state().heli`);
  // (1) a building fire with the helicopter
  const id = await ev(`(()=>{const e=evtStart('fire',{near:true,f9:true,building:true});if(e)evtF9Watch(e);return e?e.id:null})()`); R.fire.id = id;
  const legs = [], ph = [], shot = {}; let minI = 9, dropsAt = null; const t0 = Date.now(); let sim0 = await ev('EVT.t');
  while ((Date.now() - t0) / 1000 < MAX) {
    await p.waitForTimeout(1000);
    const s = await ev(`(()=>{const S=__TC_EVT.state(),a=S.act.find(e=>e.id===${JSON.stringify(id)});return{t:S.t,a,h:S.heli,done:S.done.find(d=>d.id===${JSON.stringify(id)})||null,csvc:(window.__TC_SVC&&__TC_SVC.state().err)||null}})()`);
    if (s.ERR) { R.fire.err = s.ERR; break }
    if (s.h) { const k = s.h.leg + ':' + s.h.li; if (legs[legs.length - 1] !== k) legs.push(k) }
    if (s.a) { if (ph[ph.length - 1] !== s.a.ph) ph.push(s.a.ph); if (s.a.I != null) minI = Math.min(minI, s.a.I);
      if (shots && s.h && s.h.leg === 'hover' && s.h.evt && !shot['drop' + s.h.li] && s.h.li !== 5) { shot['drop' + s.h.li] = 1; await ev(`(State.mapQa||toggleMapQa(),Camera.x=${s.a.x},Camera.y=${s.a.y - 40},Camera.zoom=2,1)`); await p.waitForTimeout(1200); await p.screenshot({ path: path.join(shots, 'heli_drop' + s.h.li + '.png') }) }
      if (shots && s.a.ph === 'fight' && !shot.fight) { shot.fight = 1; await ev(`(State.mapQa||toggleMapQa(),Camera.x=${s.a.x},Camera.y=${s.a.y},Camera.zoom=2.2,1)`); await p.waitForTimeout(1200); await p.screenshot({ path: path.join(shots, 'fire_fight.png') }) } }
    R.fire.last = s;
    if (s.done && s.h && s.h.leg == null) break }
  R.fire.legs = legs; R.fire.phases = ph; R.fire.minI = minI; R.fire.sim = +((await ev('EVT.t')) - sim0).toFixed(1); R.fire.heli = await ev(`__TC_EVT.state().heli`);
  R.fire.ok = !!(R.fire.last && R.fire.last.done && R.fire.last.done.why === 'done' && legs.some(k => k.startsWith('hover')) && R.fire.heli && R.fire.heli.done === R.fire.heli.ok && R.fire.heli.done > (R.heli0 ? R.heli0.done : 0));
  // (2) the fire ends before the helicopter is done → straight back to its roof
  const id2 = await ev(`(()=>{const e=evtStart('fire',{near:true,building:true});return e?e.id:null})()`); R.short.id = id2;
  await p.waitForTimeout(9000);
  R.short.before = await ev(`__TC_EVT.state().heli`);
  await ev(`(()=>{const e=EVT.act.find(q=>q.id===${JSON.stringify(id2)});if(e){e.I=0;evtClose(e,'self')}return 1})()`);
  const t2 = Date.now(), legs2 = []; while ((Date.now() - t2) / 1000 < 180) { await p.waitForTimeout(1000); const h = await ev(`__TC_EVT.state().heli`); if (h) { const k = h.leg + ':' + h.li; if (legs2[legs2.length - 1] !== k) legs2.push(k); if (h.leg == null) { R.short.after = h; break } } }
  R.short.legs = legs2; R.short.ok = !!(R.short.after && R.short.after.done === R.short.after.ok && R.short.before && R.short.before.evt);
  // (3) a fall — not under a canopy (the trees of the frame around the camera)
  await ev(`(State.mapQa||toggleMapQa(),1)`);
  const f = await ev(`(()=>{const e=evtStart('fall',{near:true,f9:true});if(e)evtF9Watch(e);return e?{id:e.id,x:Math.round(e.x),y:Math.round(e.y)}:null})()`); R.fall.start = f;
  await p.waitForTimeout(2500);
  R.fall.check = await ev(`(()=>{const e=EVT.act.find(q=>q.id===${JSON.stringify(f && f.id)});return{trees:EVT_TREES.n,under:e?evtUnderTree(e.x,e.y):null,filtered:EVT.st.fall.tree||0,ph:e&&e.ph}})()`);
  if (shots && f) { await ev(`(Camera.x=${f.x},Camera.y=${f.y},Camera.zoom=2.4,1)`); await p.waitForTimeout(1200); await p.screenshot({ path: path.join(shots, 'fall_down.png') }) }
  R.fall.ok = !!(R.fall.check && R.fall.check.under === false);
  // (4) a runner — the police helicopter of A5 goes round him until the cuffs, then lands on its roof
  R.flee = {}; const fid = await ev(`(()=>{const e=evtStart('flee',{near:true,f9:true});if(e)evtF9Watch(e);return e?e.id:null})()`); R.flee.id = fid;
  const legs4 = [], ph4 = []; let near = 1e9, shotP = 0; const t4 = Date.now();
  while ((Date.now() - t4) / 1000 < MAX) {
    await p.waitForTimeout(1000);
    const s = await ev(`(()=>{const S=__TC_EVT.state(),a=S.act.find(e=>e.id===${JSON.stringify(fid)});return{a,h:S.pol,done:S.done.find(d=>d.id===${JSON.stringify(fid)})||null}})()`);
    if (s.ERR) { R.flee.err = s.ERR; break }
    if (s.h) { const k = s.h.leg + ':' + s.h.li; if (legs4[legs4.length - 1] !== k) legs4.push(k) }
    if (s.a) { if (ph4[ph4.length - 1] !== s.a.ph) ph4.push(s.a.ph); if (s.h && s.h.evt && s.h.leg === 'go' && s.h.li === 2) { near = Math.min(near, Math.hypot(s.h.x - s.a.x, s.h.y - s.a.y));
        if (shots && !shotP && s.h.z > 30) { shotP = 1; await ev(`(State.mapQa||toggleMapQa(),Camera.x=${s.a.x},Camera.y=${s.a.y - 60},Camera.zoom=1.6,1)`); await p.waitForTimeout(1200); await p.screenshot({ path: path.join(shots, 'pol_heli.png') }) } } }
    R.flee.last = s;
    if ((s.done || (s.a && (s.a.ph === 'custody' || s.a.ph === 'jail'))) && s.h && s.h.leg == null) break }
  R.flee.legs = legs4; R.flee.phases = ph4; R.flee.orbitMin = Math.round(near); R.flee.pol = await ev(`__TC_EVT.state().pol`);
  R.flee.ok = !!(legs4.some(k => k === 'go:2') && R.flee.pol && R.flee.pol.done === R.flee.pol.ok && R.flee.pol.done > 0 && ph4.includes('cuff') && near < 160);
  R.evtErr = await ev('EVT.err'); R.svcAudit = await ev(`window.__TC_SVC?__TC_SVC.audit().issues:null`);
  R.pageErrors = pe; R.ok = R.fire.ok && R.short.ok && R.fall.ok && R.flee.ok && !pe.length && !R.evtErr;
  fs.writeFileSync(out, JSON.stringify(R, null, 1));
  console.log(JSON.stringify({ ok: R.ok, fire: [R.fire.ok, R.fire.phases.join('>'), R.fire.legs.join(' '), R.fire.sim, R.fire.minI], short: [R.short.ok, R.short.legs.join(' ')], fall: [R.fall.ok, R.fall.check], flee: [R.flee.ok, R.flee.phases.join('>'), R.flee.legs.join(' '), R.flee.orbitMin], pe: pe.length, err: R.evtErr, svc: R.svcAudit }));
  await b.close();
})().catch(e => { console.error(String(e).slice(0, 400)); process.exit(1) });
