// בדיקת האירועים: F9 ← אירועים — לחיצה על כל כפתור, מעקב עד הסוף, ואז שעת משחק עם אירועים אקראיים מהירים.
// node evt_test.js <build> <out.json> [shotsDir] [hourSecs=130] [maxF9Secs=420]
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
(async () => {
  const [file, out, shots, hourS, maxS] = process.argv.slice(2); const HOUR = +hourS || 130, MAXF9 = +maxS || 420;
  if (shots) fs.mkdirSync(shots, { recursive: true });
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] }); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const pe = [], ce = []; p.on('pageerror', e => pe.push(String(e).slice(0, 300))); p.on('console', m => { if (m.type() === 'error') ce.push(m.text().slice(0, 200)) });
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' }); await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  const ev = s => p.evaluate(x => { try { return window.__TC_DEV.ev(x) } catch (e) { return { ERR: String(e && e.message || e) } } }, s);
  const R = { build: path.basename(file), f9: {}, hour: null, checks: {} };
  await ev(`(typeof p34LibInit==='function'&&!window.P34&&p34LibInit(),1)`); await p.waitForTimeout(2500);
  // 1 — F9: the tab, the card, the three buttons (a real click on the button)
  await ev(`(tcF9Open(),tcF9Show('events'),1)`); await p.waitForTimeout(500);
  R.checks.card = await ev(`!!document.querySelector('#tcF9 section[data-pane="events"] #evtF9')`);
  R.checks.buttons = await ev(`[...document.querySelectorAll('#evtF9 button[data-evtgo]')].map(b=>b.dataset.evtgo)`);
  const t0 = await ev('EVT.t'); const ids = {};
  for (const type of ['fire', 'fall', 'flee']) {
    await ev(`(tcF9Open(),tcF9Show('events'),1)`); await p.waitForTimeout(300);
    const before = await ev('EVT.act.map(e=>e.id)');
    try { await p.click('#evtF9 button[data-evtgo="' + type + '"]', { timeout: 5000 }) } catch (e) { R.f9[type] = { clickErr: String(e.message).slice(0, 160) }; await ev(`(document.querySelector('#evtF9 button[data-evtgo="${type}"]').click(),1)`) }   /* a toast over the button — the same click from the page */
    await p.waitForTimeout(400);
    const now = await ev('EVT.act.map(e=>e.id)'); ids[type] = now.find(x => !before.includes(x) && x.includes(type.toUpperCase())) || null;
    await p.waitForTimeout(1500);
    R.f9[type] = Object.assign(R.f9[type] || {}, { id: ids[type], panelHidden: await ev(`!PERF.hud`), cam: await ev(`[Math.round(Camera.x),Math.round(Camera.y),+Camera.zoom.toFixed(2)]`), follow: await ev(`(()=>{const F=EVT.follow,e=F&&EVT.act.find(q=>q.id===F.id);return F?{id:F.id,dist:e?Math.round(Math.hypot(Camera.x-e.x,Camera.y-e.y)):null}:null})()`) });
  }
  // follow the three until they close (phases seen, the time of each)
  const seen = { fire: [], fall: [], flee: [] }, shot = {}; let lastT = 0; const tStart = Date.now();
  while ((Date.now() - tStart) / 1000 < MAXF9) {
    await p.waitForTimeout(1500);
    const s = await ev(`__TC_EVT.state()`); if (!s || s.ERR) { R.stateErr = s; break }
    for (const type of ['fire', 'fall', 'flee']) { const a = s.act.find(e => e.id === ids[type]); if (a) { const L = seen[type]; const k = a.ph + (a.k ? ':' + a.k : ''); if (L[L.length - 1] !== k) L.push(k);
      const want = { fire: ['coming', 'fight', 'cool'], fall: ['down', 'load', 'unload'], flee: ['foot', 'cuff', 'board', 'jail'] }[type];
      if (shots && want.includes(a.ph) && !shot[type + a.ph]) { shot[type + a.ph] = 1; await ev(`(State.mapQa||toggleMapQa(),Camera.x=${a.x},Camera.y=${a.y},Camera.zoom=2.2,1)`); await p.waitForTimeout(1300); await p.screenshot({ path: path.join(shots, type + '_' + a.ph + '.png') }) } } }
    const open = ['fire', 'fall', 'flee'].filter(t => ids[t] && s.act.some(e => e.id === ids[t])); lastT = s.t;
    if (!open.length) break }
  const s1 = await ev(`__TC_EVT.state()`);
  for (const type of ['fire', 'fall', 'flee']) { const d = (s1.done || []).find(q => q.id === ids[type]); R.f9[type].phases = seen[type]; R.f9[type].closed = d || null; R.f9[type].ok = !!(d && d.why === 'done') }
  R.f9.simSecs = +(lastT - t0).toFixed(1); R.f9.realSecs = Math.round((Date.now() - tStart) / 1000);
  // the F9 card shows the state, and the camera button works on an active one
  R.checks.cardState = await ev(`(tcF9Open(),tcF9Show('events'),(document.querySelector('#evtF9St')||{}).textContent||'').slice(0,300)`);
  await ev(`(PERF.hud&&perfHudToggle(),1)`);
  // 2 — an hour of the game (120 s of the world): random events, fast
  await ev(`__TC_EVT.fast(1)`); const h0 = await ev(`({t:EVT.t,clock:gameClock().hhmm,st:JSON.parse(JSON.stringify(EVT.st))})`); const tH = Date.now(); let maxStill = 0, samples = 0, frozen = 0, lastClock = null, sameClock = 0; const types = {};
  while ((Date.now() - tH) / 1000 < HOUR * 3) {
    await p.waitForTimeout(2000); samples++;
    const s = await ev(`({t:EVT.t,clock:gameClock().min,act:EVT.act.map(e=>e.type+':'+e.ph),st:EVT.st,still:Math.max(0,...TRAFFIC_CARS.filter(v=>v.evt).map(v=>v.evt.still||0)),err:EVT.err})`);
    if (lastClock != null && s.clock === lastClock) sameClock++; lastClock = s.clock; maxStill = Math.max(maxStill, s.still); for (const a of s.act) types[a] = (types[a] || 0) + 1;
    if (s.t - h0.t >= HOUR) break }
  const h1 = await ev(`({t:EVT.t,clock:gameClock().hhmm,st:EVT.st,done:EVT.done.slice(-20),err:EVT.err,act:EVT.act.map(e=>({id:e.id,ph:e.ph,len:+(EVT.t-e.t0).toFixed(0)})),c4f:__TC_C4F.audit().issues,qa:__TC_EVT.qa()})`);
  R.hour = { simSecs: +(h1.t - h0.t).toFixed(1), clock: [h0.clock, h1.clock], samples, sameClock, maxStill, phasesSeen: types, st: h1.st, done: h1.done, act: h1.act, c4f: h1.c4f, qa: h1.qa, err: h1.err };
  R.pageErrors = pe; R.consoleErrors = ce.slice(0, 20);
  R.ok = !pe.length && !h1.err && ['fire', 'fall', 'flee'].every(t => R.f9[t].ok) && R.checks.card === true && h1.st.still === 0 && sameClock === 0;
  fs.writeFileSync(out, JSON.stringify(R, null, 1)); console.log(JSON.stringify({ ok: R.ok, f9: Object.fromEntries(['fire', 'fall', 'flee'].map(t => [t, [R.f9[t].ok, (R.f9[t].closed || {}).why, (R.f9[t].closed || {}).len, R.f9[t].phases.join('>')]])), sim: R.f9.simSecs, hour: [R.hour.simSecs, R.hour.clock, R.hour.st.still, maxStill], behind: R.hour.st.behind ? [R.hour.st.behind.max, R.hour.st.behind.n, R.hour.st.behind.at] : null, heli: [R.hour.st.fire.heli || 0, R.hour.st.flee.heli || 0], qa: R.hour.qa && R.hour.qa.issues, pe: pe.length, err: h1.err }));
  await b.close();
})().catch(e => { console.error(String(e).slice(0, 400)); process.exit(1) });
