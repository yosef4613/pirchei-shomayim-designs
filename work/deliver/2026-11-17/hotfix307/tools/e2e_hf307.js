// hotfix307 (18.11): עותק של actions2/tools/e2e_actions2.js — המקש של השלב הוא G (לא F). המקור:
// actions2 — מקצה לקצה בדפדפן (לולאת המשחק האמיתית, מקשים ולחיצות אמיתיים): (1) הסיפור הראשי — עוצרים ברכב ליד שמעון (O-1): לא נפתח; F → יוצא, הולך, לוחץ יד → השיחה;
// (2) פעולה (S9-ST-E4 #2 — המפסק): הכרטיס → F → הולך, מתכופף, מרים → השלב הבא; (3) שלב שיחה בכרטיס (S9-ST-E4 #1): הכפתור → הולך ומדבר → השלב הבא;
// (4) הגעה ברכב (ZS-D3 #3): עוצרים בטבעת — לא מתקדם; F → יוצא → השלב הבא; (5) חץ באמצע — עוצר. צילומים — רק לבדיקה בעין שלי.
// node e2e_actions2.js <game.html> <out.json> [shots_dir]
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out, shots] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] }); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const pe = []; p.on('pageerror', e => pe.push(String(e).slice(0, 240)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' }); await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(1500);
  const ev = s => p.evaluate(x => window.__TC_DEV.ev(x), s);
  const shot = async n => { if (shots) try { await p.screenshot({ path: path.join(shots, n + '.png') }) } catch (e) { } };
  const R = { cases: [], pe };
  const keep = await ev(`(()=>{window.__a2keep=JSON.stringify(g77St());return 1})()`);
  // (1) הסיפור הראשי
  try { const r = { id: 'O-1 talk' };
    r.setup = await ev(`(()=>{const st=g77St();st.main={v:1,on:true,ch:'O',mi:'O-1',step:0,st:{},done:{},rows:[],sent:{},q:[],pc:[],news:[],van:null,began:0};delete st.flags['st:d-O-shimon'];if(State.phoneOpen)setPhoneOpen(false);
      const b=TCSTORY.bring('PLAYER-HOME');PlayerCar.speed=0;Camera.zoom=2.2;return{b:!!b,mode:PlayerProfile.mode,cur:TCSTORY.cur()&&TCSTORY.cur().s.talk}})()`);
    await p.waitForTimeout(3500);
    r.wait = await ev(`(()=>{const M=__TC_SACT.MS;return{open:!!g77S().open,armed:M.cur&&M.cur.kind,reached:!!(TCSTORY.E.cool||{})['talk:d-O-shimon'],hud:String(hudGoalText()).slice(0,80),mode:PlayerProfile.mode}})()`);
    if (!r.wait.armed) { r.direct = await ev(`(()=>{const x=g77DlgOpen('d-O-shimon','talk');return{x,open:!!g77S().open,armed:__TC_SACT.MS.cur&&__TC_SACT.MS.cur.kind}})()`) }
    await shot('ms_a_wait');
    await p.keyboard.press('KeyG'); await p.waitForTimeout(900); await shot('ms_b_walk');
    r.mid = await ev(`(()=>{const q=__TC_SACT.PS.q;return{ps:!!q,step:q&&q.steps[q.i]&&(q.steps[q.i].p||q.steps[q.i].k),mode:PlayerProfile.mode,hud:String(hudGoalText()).slice(0,80)}})()`);
    await p.waitForTimeout(1300); await shot('ms_c_pose');
    await p.waitForTimeout(7500); await shot('ms_d_dialog');
    r.after = await ev(`(()=>{const O=g77S().open,A=__TC_SACT;return{open:O&&O.id,mode:PlayerProfile.mode,ps:!!A.PS.q,last:A.PS.last,err:A.err(),fsLog:(A.E.fsLog||[]).filter(q=>q[0]==='st-shimon'),psLog:(A.PS.log||[]).slice(-8),fig:(()=>{const f=A.FIG['st-shimon'];return f?{pt:f.pt&&[f.pt.x|0,f.pt.y|0],hold:f.hold,arrived:f.arrived,hide:f.hide,src:f.src}:null})()}})()`);
    r.ok = !r.wait.open && (r.wait.armed === 'talk' || (r.direct && r.direct.armed === 'talk')) && r.after.open === 'd-O-shimon' && r.after.mode === 'walk';
    await ev(`(()=>{try{g77DlgClose(true)}catch(e){}return 1})()`); R.cases.push(r) } catch (e) { R.cases.push({ id: 'O-1', ok: false, err: String(e).slice(0, 200) }) }
  // (2) פעולה: הכרטיס → F
  for (const [id, n] of [['S9-ST-E4', 2], ['S12-ST-C1', 2]]) { const r = { id, n };
    try { r.setup = await ev(`(()=>{const A=__TC_SACT,S=S9STORY.ST['${id}'],s=S.steps[${n}-1],f=g77St().flags;f['s9:${id}']=${n};delete f['s9:${id}:done'];A.SA.cur=null;A.SA.carry=null;
        const p=navPoiRegistry()[s.poi];if(State.phoneOpen)setPhoneOpen(false);PlayerProfile.mode='walk';PlayerPed.x=p.x;PlayerPed.y=p.y+4;Camera.x=p.x;Camera.y=p.y;Camera.zoom=2.4;let o=false;try{o=interactNearbyPoi()}catch(e){}return{opened:o,phone:!!State.phoneOpen}})()`);
      await p.waitForTimeout(600); const btn = await p.$(`[data-s9-step="${id}"]`); r.btn = btn ? (await btn.innerText()).slice(0, 80) : null;
      if (!btn) { r.ok = false; r.why = 'אין כפתור'; R.cases.push(r); continue }
      await btn.click(); await p.waitForTimeout(500);
      r.armed = await ev(`(()=>{const c=__TC_SACT.SA.cur;return c?{k:c.k,phase:c.phase,phone:!!State.phoneOpen,step:S9STORY.step('${id}')}:null})()`);
      await p.waitForTimeout(1500); r.still = await ev(`({step:S9STORY.step('${id}'),phase:__TC_SACT.SA.cur&&__TC_SACT.SA.cur.phase})`);   // בלי F — לא זז
      await p.keyboard.press('KeyG'); await p.waitForTimeout(500); await shot(id + '_' + n + '_a');
      r.mid = await ev(`(()=>{const q=__TC_SACT.PS.q,c=__TC_SACT.SA.cur;return{ps:!!q,step:q&&q.steps[q.i]&&(q.steps[q.i].p||q.steps[q.i].k),phase:c&&c.phase,story:S9STORY.step('${id}')}})()`);
      await p.waitForTimeout(900); await shot(id + '_' + n + '_b'); await p.waitForTimeout(4500); await shot(id + '_' + n + '_c');
      r.after = await ev(`({step:S9STORY.step('${id}'),carry:__TC_SACT.SA.carry&&__TC_SACT.SA.carry.nm,last:__TC_SACT.PS.last,err:__TC_SACT.err()})`);
      r.ok = r.armed && r.still.step === n && r.after.step === n + 1 && !r.after.err && !!(r.after.last && r.after.last.seen.some(k => /^sa|^marshal/.test(k)));   // mid — רק למידע (תחת עומס הדגימה מאחרת)
    } catch (e) { r.ok = false; r.err = String(e).slice(0, 200) } R.cases.push(r) }
  // (3) שלב שיחה בכרטיס
  try { const id = 'S9-ST-E4', n = 1, r = { id, n, plain: 1 };
    r.setup = await ev(`(()=>{const A=__TC_SACT,S=S9STORY.ST['${id}'],s=S.steps[0],f=g77St().flags;f['s9:${id}']=1;delete f['s9:${id}:done'];A.SA.cur=null;const p=navPoiRegistry()[s.poi];if(State.phoneOpen)setPhoneOpen(false);
      PlayerProfile.mode='walk';PlayerPed.x=p.x;PlayerPed.y=p.y+4;Camera.x=p.x;Camera.y=p.y;Camera.zoom=2.4;let o=false;try{o=interactNearbyPoi()}catch(e){}return{opened:o}})()`);
    await p.waitForTimeout(600); const btn = await p.$(`[data-s9-step="${id}"]`); r.btn = btn ? (await btn.innerText()).slice(0, 80) : null;
    if (btn) { await btn.click(); await p.waitForTimeout(700); await shot('plain_a');
      r.mid = await ev(`(()=>{const q=__TC_SACT.PS.q;return{ps:!!q,step:q&&q.steps[q.i]&&(q.steps[q.i].p||q.steps[q.i].k),story:S9STORY.step('${id}'),phone:!!State.phoneOpen}})()`);
      await p.waitForTimeout(1500); await shot('plain_b'); await p.waitForTimeout(7000);
      r.after = await ev(`({step:S9STORY.step('${id}'),last:__TC_SACT.PS.last,err:__TC_SACT.err()})`); r.ok = !r.mid.phone && r.after.step === 2 && !!(r.after.last && r.after.last.tag === 'card:S9-ST-E4#1' && r.after.last.seen.some(k => /^sa/.test(k))) } else r.ok = false;
    R.cases.push(r) } catch (e) { R.cases.push({ id: 'plain', ok: false, err: String(e).slice(0, 200) }) }
  // (4) הגעה ברכב
  try { const r = { id: 'ZS-D3', n: 3, car: 1 };
    r.setup = await ev(`(()=>{const s=S9STORY.ST['ZS-D3'].steps[2],f=g77St().flags;f['s9:ZS-D3']=3;delete f['s9:ZS-D3:done'];__TC_SACT.SA.cur=null;const d=s.__saDrive;let b=false;try{b=!!TCSTORY.bring(s.poi)}catch(e){}if(!b){PlayerProfile.mode='vehicle';PlayerCar.x=d[0];PlayerCar.y=d[1]}PlayerCar.speed=0;Camera.zoom=2;return{d,r:s.drive[2],car:[Math.round(PlayerCar.x),Math.round(PlayerCar.y)],dist:Math.round(Math.hypot(PlayerCar.x-d[0],PlayerCar.y-d[1]))}})()`);
    await p.waitForTimeout(2500); r.wait = await ev(`(()=>{const c=__TC_SACT.SA.cur;return{step:S9STORY.step('ZS-D3'),armed:c&&c.k,hud:String(hudGoalText()).slice(0,80)}})()`); await shot('drive_a');
    await p.keyboard.press('KeyG'); await p.waitForTimeout(1200); await shot('drive_b');
    r.mid = await ev(`({mode:PlayerProfile.mode,ps:!!__TC_SACT.PS.q,step:S9STORY.step('ZS-D3')})`); await p.waitForTimeout(9000);
    r.after = await ev(`({step:S9STORY.step('ZS-D3'),mode:PlayerProfile.mode,last:__TC_SACT.PS.last,err:__TC_SACT.err()})`);
    r.ok = r.wait.step === 3 && r.wait.armed === 'meet' && r.mid.mode === 'walk' && r.after.step === 4; R.cases.push(r) } catch (e) { R.cases.push({ id: 'ZS-D3', ok: false, err: String(e).slice(0, 200) }) }
  // (5) חץ באמצע — עוצר
  try { const id = 'S9-ST-E4', n = 2, r = { id, n, cancel: 1 };
    await ev(`(()=>{const A=__TC_SACT,S=S9STORY.ST['${id}'],s=S.steps[1],f=g77St().flags;f['s9:${id}']=2;A.SA.cur=null;A.SA.carry=null;const p=navPoiRegistry()[s.poi];PlayerProfile.mode='walk';PlayerPed.x=p.x+20;PlayerPed.y=p.y+6;A.arm('${id}',true);return 1})()`);
    await p.keyboard.press('KeyG'); await p.waitForTimeout(250); await p.keyboard.down('ArrowLeft'); await p.waitForTimeout(200); await p.keyboard.up('ArrowLeft');
    r.after = await ev(`({ps:!!__TC_SACT.PS.q,phase:__TC_SACT.SA.cur&&__TC_SACT.SA.cur.phase,step:S9STORY.step('${id}'),why:__TC_SACT.PS.why})`);
    r.ok = !r.after.ps && r.after.phase === 'go' && r.after.step === 2; R.cases.push(r) } catch (e) { R.cases.push({ id: 'cancel', ok: false, err: String(e).slice(0, 200) }) }
  await ev(`(()=>{try{PlayerProfile.story=JSON.parse(window.__a2keep)}catch(e){}return 1})()`);
  R.ok = R.cases.every(c => c.ok) && !pe.length; R.pass = R.cases.filter(c => c.ok).length + ' / ' + R.cases.length;
  fs.writeFileSync(out, JSON.stringify(R, null, 1)); console.log(JSON.stringify({ ok: R.ok, pass: R.pass, pe: pe.length })); await b.close();
})().catch(e => { console.error(e); process.exit(1) });
