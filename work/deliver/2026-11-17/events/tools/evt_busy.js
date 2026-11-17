// בדיקת סדר השכבות (TCBUSY, ‏009_tcbusy של missions): node evt_busy.js <build> <out.json> [tcbusy.js]
// אם TCBUSY לא בבנייה (master עוד בלי 009_tcbusy) — נטען מהקובץ (ברירת מחדל: העותק של missions 7f46c1e ליד הכלי), כדי לבדוק את החיבור של האירועים.
// (1) שכבה גבוהה (cutscene) על המסך → אירוע אקראי לא מתחיל, ההודעה של אירוע מ-F9 לא עולה ונשמרת; (2) clear → ההודעה עולה, ‏'event' על המסך
// (הכרטיס חסום) ו-top === 'event'; (3) אחרי שההודעה יורדת — 'event' לא על המסך; 0 שגיאות דף, ‏evt_events ok.
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
(async () => {
  const [file, out, fx] = process.argv.slice(2); const FX = fx || path.join(__dirname, 'tcbusy_fixture_missions_7f46c1e.js');
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] }); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const pe = []; p.on('pageerror', e => pe.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' }); await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  const ev = s => p.evaluate(x => { try { return window.__TC_DEV.ev(x) } catch (e) { return { ERR: String(e && e.message || e) } } }, s);
  const R = { build: path.basename(file), steps: {} }; const C = R.steps;
  await ev(`(typeof p34LibInit==='function'&&!window.P34&&p34LibInit(),1)`); await p.waitForTimeout(2000);
  R.inBuild = await ev(`typeof TCBUSY!=='undefined'`);
  if (!R.inBuild) { await p.addScriptTag({ content: fs.readFileSync(FX, 'utf8') }); R.injected = path.basename(FX) }
  R.has = await ev(`typeof TCBUSY!=='undefined'&&typeof TCBUSY.blocks`);
  await ev(`(EVT.next.fire=EVT.next.fall=EVT.next.flee=1e9,1)`);
  const toast = `((document.getElementById('toast')||{}).textContent||'')`;
  // 1 — a higher layer on the screen
  await ev(`(TCBUSY.set('cutscene',{why:'qa-evt',ttl:60000}),1)`); await p.waitForTimeout(300);
  const h0 = await ev(`EVT.st.hushed||0`);
  const w0 = await ev(`NPC_PEDESTRIANS.length`);
  const id = await ev(`(()=>{const e=evtStart('fall',{near:true,f9:true});return e?e.id:null})()`); R.id = id;
  await p.waitForTimeout(600);
  C.blocked = await ev(`({quiet:evtQuiet(),blocks:TCBUSY.blocks('event'),top:TCBUSY.top(),event:TCBUSY.is('event'),pend:EVT.pend.length,hushed:(EVT.st.hushed||0)-${h0},toast:${toast}.includes('אדם נפל')})`);
  C.walkers0 = await ev(`(()=>{const e=EVT.act.find(q=>q.id===${JSON.stringify(id)}),n=e&&e.npc;return{before:${w0},now:NPC_PEDESTRIANS.length,inList:!!n&&NPC_PEDESTRIANS.includes(n),out:!!(n&&n.evtOut)}})()`);
  const n0 = await ev(`EVT.st.fire.n`); await ev(`(EVT.next.fire=EVT.t,1)`); await p.waitForTimeout(2500);
  C.random = await ev(`({started:EVT.st.fire.n-${n0},later:+(EVT.next.fire-EVT.t).toFixed(1)})`);
  // 2 — the layer is gone → the message that waited comes up, and the event is the top layer
  await ev(`(EVT.next.fire=1e9,TCBUSY.clear('cutscene'),1)`); let up = null; const t1 = Date.now();
  while (Date.now() - t1 < 6000) { await p.waitForTimeout(250); const s = await ev(`({toast:${toast}.includes('אדם נפל'),pend:EVT.pend.length,late:EVT.st.late||0,event:TCBUSY.is('event'),card:TCBUSY.blocks('card'),top:TCBUSY.top()})`); if (s.toast && !s.pend) { up = s; up.ms = Date.now() - t1; break } }
  C.freed = up;
  // 3 — the message goes down → the event layer is off the screen
  let off = null; const t2 = Date.now();
  while (Date.now() - t2 < 12000) { await p.waitForTimeout(400); const s = await ev(`({event:TCBUSY.is('event'),top:TCBUSY.top(),card:TCBUSY.blocks('card')})`); if (!s.event) { off = s; off.ms = Date.now() - t2; break } }
  C.cleared = off;
  // 4 — a message without a higher layer — straight up (no waiting)
  const l0 = await ev(`EVT.st.late||0`); await ev(`(()=>{const e=EVT.act.find(q=>q.id===${JSON.stringify(id)});evtSay(e,'בדיקה — הודעה בלי שכבה');return 1})()`); await p.waitForTimeout(400);
  C.direct = await ev(`({toast:${toast}.includes('בדיקה — הודעה בלי שכבה'),late:(EVT.st.late||0)-${l0},event:TCBUSY.is('event'),pend:EVT.pend.length})`);
  // the walker of the event stays in the list (the finding of cutscenes: npc_pedestrian_prototype_5_to_10 in #dev), hidden from the walkers' step; roadAudit with the event on
  C.walkers = await ev(`(()=>{const e=EVT.act.find(q=>q.id===${JSON.stringify(id)}),n=e&&e.npc,r=roadAudit(),L=r.checks||r.results||[],f=k=>{const c=L.find(q=>(q.name||q.id)===k);return c?!!(c.ok??c.pass):null};
    return{before:${w0},now:NPC_PEDESTRIANS.length,inList:!!n&&NPC_PEDESTRIANS.includes(n),out:!!(n&&n.evtOut),check:f('npc_pedestrian_prototype_5_to_10'),evt:f('evt_events'),failed:(r.failed||[]).map(x=>String(x).slice(0,80)).slice(0,6)}})()`);
  R.state = await ev(`(()=>{const S=__TC_EVT.state();return{layer:S.layer,pend:S.pend,st:{hushed:S.st.hushed,late:S.st.late,dropped:S.st.dropped,busySet:S.st.busySet}}})()`);
  R.qa = await ev(`(()=>{const q=__TC_EVT.qa();return{ok:q.ok,issues:q.issues}})()`); R.tcbusy = await ev(`TCBUSY.state()`);
  R.pageErrors = pe;
  const B = C.blocked || {}, F = C.freed, X = C.cleared, D = C.direct || {};
  const W0 = C.walkers0 || {}, Wk = C.walkers || {};
  R.ok = !!(R.has && id && W0.now === W0.before && W0.inList && W0.out && Wk.evt === true && B.quiet && B.blocks && B.top === 'cutscene' && !B.event && B.pend === 1 && B.hushed >= 1 && !B.toast && C.random && C.random.started === 0 && C.random.later > 20
    && F && F.event && F.card && F.top === 'event' && F.late >= 1 && X && !X.event && D.toast && D.late === 0 && !D.pend && R.qa && R.qa.ok && !pe.length);
  fs.writeFileSync(out, JSON.stringify(R, null, 1));
  console.log(JSON.stringify({ ok: R.ok, inBuild: R.inBuild, walkers0: C.walkers0, walkers: C.walkers, blocked: B, random: C.random, freed: F, cleared: X, direct: D, qa: R.qa, pe: pe.length }));
  await b.close();
})().catch(e => { console.error(String(e).slice(0, 400)); process.exit(1) });
