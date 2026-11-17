// בדיקה מקצה לקצה של הפעולות (actions, 17.11): פותחים את המקום (F), לוחצים בכפתור של הכרטיס (לחיצה אמיתית), לוחצים F במקלדת ליד החפץ,
// מחכים לאנימציה — ובודקים: השלב התקדם, החפץ ביד / התוצאה בעולם. צילומים — רק לבדיקה בעין (לא לדף).
// node e2e_actions.js <game.html> <out.json> [shots_dir]
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out, shots] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] }); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const pe = []; p.on('pageerror', e => pe.push(String(e).slice(0, 240)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' }); await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(1500);
  const ev = s => p.evaluate(x => window.__TC_DEV.ev(x), s);
  const R = { cases: [], pe };
  const cases = [['S9-ST-E4', 2], ['S9-ST-F3', 4], ['S12-ST-C1', 2], ['S13-ST-F8', 3], ['S9-ST-E5', 1], ['S14-ST-B7', 2], ['S9-ST-E5', 3],
    ['S11-ST-B6', 3, `try{ensureFishingSchema().inventory.push({id:COAST_FISH[0].id,kg:1})}catch(e){}`], ['S15-ST-G0', 2]];   // + חיפוש (find): הולכים עד המקום הנסתר   // שלב המתנה (w:1): הכפתור מופיע כשיש דג — ואז מסירה בעולם
  for (const [id, n, pre] of cases) {
    const r = { id, n };
    try {
      r.setup = await ev(`(()=>{${pre || ''};const A=__TC_SACT,S=S9STORY.ST['${id}'],s=S.steps[${n}-1],f=g77St().flags;f['s9:${id}']=${n};delete f['s9:${id}:done'];A.SA.cur=null;
        const sp=A.spec('${id}',${n});if(sp&&['give','plant','hang'].includes(sp.k)||sp&&sp.opt.use){A.SA.carry={id:'${id}',o:'crate',c:'#e9f1f6',nm:'בדיקה',u:0}}
        const p=navPoiRegistry()[s.poi];if(State.phoneOpen)setPhoneOpen(false);PlayerProfile.mode='walk';PlayerPed.x=p.x;PlayerPed.y=p.y+4;Camera.x=p.x;Camera.y=p.y;Camera.zoom=2.2;
        let opened=false;try{opened=interactNearbyPoi()}catch(e){return{err:String(e)}}return{poi:s.poi,opened,phone:!!State.phoneOpen,app:State.phoneApp,iid:State.interactionId}})()`);
      await p.waitForTimeout(600);
      const btn = await p.$(`[data-s9-step="${id}"]`);
      r.btn = btn ? (await btn.innerText()).slice(0, 80) : null;
      if (!btn) { r.ok = false; r.why = 'אין כפתור בכרטיס'; R.cases.push(r); continue }
      await btn.click(); await p.waitForTimeout(400);
      r.armed = await ev(`(()=>{const c=__TC_SACT.SA.cur;return c?{k:c.k,phase:c.phase,R:c.R,d:Math.hypot(PlayerPed.x-c.pt.x,PlayerPed.y-c.pt.y),phone:!!State.phoneOpen,hud:String(hudGoalText()).slice(0,90)}:null})()`);
      if (shots) await p.screenshot({ path: path.join(shots, id + '_' + n + '_a.png') });
      if (r.armed && r.armed.k === 'find') { r.far = await ev(`(()=>{const ok=__TC_SACT.F();return{ok,found:__TC_SACT.SA.cur.found,hud:String(hudGoalText()).slice(0,70)}})()`);
        await ev(`(()=>{const c=__TC_SACT.SA.cur;PlayerPed.x=c.pt.x+8;PlayerPed.y=c.pt.y;return 1})()`); await p.waitForTimeout(600); r.found = await ev(`!!(__TC_SACT.SA.cur&&__TC_SACT.SA.cur.found)`) }
      const q = r.armed && r.armed.k === 'sort' ? 3 : 1;
      for (let i = 0; i < q; i++) {
        await p.keyboard.press('KeyF'); await p.waitForTimeout(500);
        if (i === 0) { r.work = await ev(`(()=>{const c=__TC_SACT.SA.cur;return c?{phase:c.phase,prog:+c.prog.toFixed(2),hud:String(hudGoalText()).slice(0,60)}:null})()`); if (shots) await p.screenshot({ path: path.join(shots, id + '_' + n + '_b.png') }) }
        await p.waitForTimeout(3600);
      }
      if (shots) await p.screenshot({ path: path.join(shots, id + '_' + n + '_c.png') });
      r.after = await ev(`(()=>{const A=__TC_SACT;return{step:S9STORY.step('${id}'),done:S9STORY.done('${id}'),cur:A.SA.cur&&A.SA.cur.phase,carry:A.SA.carry&&A.SA.carry.nm,wear:!!A.SA.wear,res:A.SA.res.length,err:A.err(),hud:String(hudGoalText()).slice(0,80)}})()`);
      r.ok = (r.after.step === n + 1 || r.after.done) && !r.after.err;
    } catch (e) { r.ok = false; r.err = String(e).slice(0, 200) }
    R.cases.push(r);
  }
  // שלבי נסיעה: פעולה בהגעה (ZS-A5 #2 — המעטפה של המלון), ונסיעה שדורשת רכב (ZS-D3 #3) — ברגל לא מתקדם, ברכב כן
  try { const r = { id: 'ZS-A5', n: 2, drive: 1 };
    r.setup = await ev(`(()=>{const S=S9STORY.ST['ZS-A5'],s=S.steps[1],f=g77St().flags;f['s9:ZS-A5']=2;delete f['s9:ZS-A5:done'];__TC_SACT.SA.cur=null;if(State.phoneOpen)setPhoneOpen(false);
      const d=s.__saDrive;PlayerProfile.mode='walk';PlayerPed.x=d[0]-20;PlayerPed.y=d[1];Camera.x=d[0];Camera.y=d[1];return{d,r:s.drive[2]}})()`);
    await p.waitForTimeout(1500); r.armed = await ev(`(()=>{const c=__TC_SACT.SA.cur;return c?{id:c.id,k:c.k,phase:c.phase}:null})()`);
    if (shots) await p.screenshot({ path: path.join(shots, 'ZS-A5_2_a.png') });
    await p.keyboard.press('KeyF'); await p.waitForTimeout(2600);
    r.after = await ev(`({step:S9STORY.step('ZS-A5'),err:__TC_SACT.err()})`); r.ok = !!r.armed && r.after.step === 3 && !r.after.err; R.cases.push(r) } catch (e) { R.cases.push({ id: 'ZS-A5', ok: false, err: String(e).slice(0, 200) }) }
  try { const r = { id: 'ZS-D3', n: 3, car: 1 };
    r.walk = await ev(`(()=>{const s=S9STORY.ST['ZS-D3'].steps[2],f=g77St().flags;f['s9:ZS-D3']=3;delete f['s9:ZS-D3:done'];__TC_SACT.SA.cur=null;const d=s.__saDrive;PlayerProfile.mode='walk';PlayerPed.x=d[0];PlayerPed.y=d[1];Camera.x=d[0];Camera.y=d[1];return{d,r:s.drive[2]}})()`);
    await p.waitForTimeout(2000); r.walkStep = await ev(`({step:S9STORY.step('ZS-D3'),hud:String(hudGoalText()).slice(0,80)})`);
    r.car = await ev(`(()=>{const s=S9STORY.ST['ZS-D3'].steps[2],d=s.__saDrive;PlayerCar.x=d[0];PlayerCar.y=d[1];PlayerProfile.mode='vehicle';return s.drive[2]})()`);
    await p.waitForTimeout(2200); r.carStep = await ev(`S9STORY.step('ZS-D3')`);
    r.ok = r.walkStep.step === 3 && r.carStep === 4; await ev(`(()=>{PlayerProfile.mode='walk';return 1})()`); R.cases.push(r) } catch (e) { R.cases.push({ id: 'ZS-D3', ok: false, err: String(e).slice(0, 200) }) }
  // הביקור במקום (הביקורת 32): F ליד המגדל / האצטדיון, לחיצה אמיתית על "תצפית" / "כרטיס" + "צפה", ההליכה לדלת, המעלית / הקופה, הגג / היציע — ו-E במקלדת: חזרה למקום
  const hasVis = await ev(`!!(__TC_SACT&&__TC_SACT.visStart)`);   // בבנייה בלי הביקור — מדלגים (לא נכשל)
  for (const [pid, acts, kind] of hasVis ? [['A5-OFFICE', ['view'], 'roof'], ['A3-STADIUM', ['ticket', 'watch'], 'stand']] : []) {
    const r = { id: 'visit ' + kind };
    try {
      r.setup = await ev(`(()=>{if(State.phoneOpen)setPhoneOpen(false);__TC_SACT.SA.cur=null;PlayerProfile.money+=2000;const p=PLC_POIS['${pid}'];PlayerProfile.mode='walk';PlayerPed.x=p.x;PlayerPed.y=p.y;Camera.x=p.x;Camera.y=p.y;
        let o=false;try{o=interactNearbyPoi()}catch(e){return{err:String(e)}}return{at:[p.x,p.y],opened:o,phone:!!State.phoneOpen,iid:State.interactionId}})()`);
      await p.waitForTimeout(700);
      for (const a of acts) { const btn = await p.$(`button[data-plc="${a}"]`); if (!btn) { r.why = 'אין כפתור ' + a; break } await btn.click(); await p.waitForTimeout(500) }
      r.started = await ev(`(()=>{const V=__TC_SACT.VIS.v;return V?{ph:V.ph,kind:V.kind}:null})()`);
      await p.waitForTimeout(kind === 'roof' ? 7800 : 6000);
      r.on = await ev(`(()=>{const V=__TC_SACT.VIS.v;return V?{ph:V.ph,hide:V.hide,cam:[Math.round(Camera.x),Math.round(Camera.y)],goal:[Math.round(V.D.cam.x),Math.round(V.D.cam.y)],z:+Camera.zoom.toFixed(2),hud:String(hudGoalText()).slice(0,80)}:null})()`);
      if (shots) await p.screenshot({ path: path.join(shots, 'visit_' + kind + '.png') });
      await p.keyboard.press('KeyE'); await p.waitForTimeout(kind === 'roof' ? 7000 : 4600);
      r.after = await ev(`(()=>{const V=__TC_SACT.VIS.v,p=PLC_POIS['${pid}'];return{v:V?V.ph:null,back:Math.round(Math.hypot(PlayerPed.x-p.x,PlayerPed.y-p.y)),mode:PlayerProfile.mode,err:__TC_SACT.VIS.err}})()`);
      r.ok = !!(r.started && r.on && r.on.ph === 'on' && r.on.hide && r.after && r.after.v === null && r.after.back < 2 && !r.after.err);
    } catch (e) { r.ok = false; r.err = String(e).slice(0, 200) }
    R.cases.push(r);
  }
  R.saveFlag = await ev(`(()=>{const f=g77St().flags;return{carry:f['sa:carry']||null,wear:f['sa:wear']||null}})()`);
  R.figs = await ev(`(()=>{const E=__TC_SACT.E;return{arrivals:E.arrivals||0,drawn:E.figDrawn||0,trunk:E.trunk||0,list:__TC_SACT.figs?__TC_SACT.figs().length:null}})()`);
  // ההדגמה לבעלים: ‎#dev&sact=S12-ST-C1:2‎ — השחקן במקום, והמסך של המקום פתוח עם הכפתור "← במשחק"
  try { const q = await b.newPage({ viewport: { width: 1280, height: 800 } }); const pe2 = []; q.on('pageerror', e => pe2.push(String(e).slice(0, 200)));
    await q.goto('file://' + path.resolve(file) + '#dev&sact=S12-ST-C1:2', { waitUntil: 'commit' }); await q.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
    for (let i = 0; i < 50; i++) { await q.waitForTimeout(500); const d = await q.evaluate(() => !!(window.__TC_SACT && window.__TC_SACT.E.demo)); if (d) break }   // הבנייה כבדה יותר — מחכים להדגמה עד 25 שנ׳ (לא 4 קבועות)
    await q.waitForTimeout(800); const r = await q.evaluate(() => window.__TC_DEV.ev(`({demo:__TC_SACT.E.demo||null,phone:!!State.phoneOpen,btn:(document.querySelector('[data-s9-step]')||{}).innerText||null})`));
    r.id = 'demo S12-ST-C1:2'; r.pe = pe2; r.ok = !!(r.demo && r.demo.opened && r.phone && r.btn && /במשחק/.test(r.btn)) && !pe2.length; if (shots) await q.screenshot({ path: path.join(shots, 'demo_S12-ST-C1_2.png') }); R.cases.push(r); await q.close() } catch (e) { R.cases.push({ id: 'demo', ok: false, err: String(e).slice(0, 200) }) }
  R.ok = R.cases.every(c => c.ok) && !pe.length;
  fs.writeFileSync(out, JSON.stringify(R, null, 1)); console.log(JSON.stringify({ ok: R.ok, cases: R.cases.map(c => [c.id, c.n, c.ok, c.after && c.after.step, c.after && c.after.carry]), pe: pe.length }));
  await b.close();
})().catch(e => { console.error(String(e).slice(0, 400)); process.exit(1) });
