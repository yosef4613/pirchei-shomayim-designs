// 17.11 · portraits — בדיקה: __TC_POR_QA, הודעות / שיחה נכנסת / חלון שיחה / רשימת השיחות / כרטיסי העבודות, צילומים לבדיקה בעין (פנימי בלבד), ורשימת כל הדמויות לדף הציור.
// node por_check.js <game.html> <out.json> [shots_dir]
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out, shots] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await b.newPage({ viewport: { width: 1600, height: 900 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300))); p.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text().slice(0, 200)) });
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' }); await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(3000); for (let i = 0; i < 4; i++) { try { if (await p.evaluate(() => !!document.getElementById('g77AsChoose'))) await p.keyboard.press('Enter') } catch (e) {} await p.waitForTimeout(400) }
  const ev = s => p.evaluate(s => window.__TC_DEV.ev(s), s);
  const R = { errs };
  R.qa = await ev('window.__TC_POR_QA()');
  R.all = await ev('window.__TC_POR_ALL()');
  const shot = async n => { if (shots) { fs.mkdirSync(shots, { recursive: true }); await p.screenshot({ path: path.join(shots, n + '.png') }) } };
  // messages from a few people and a place, then the messages app
  R.msgs = await ev(`(()=>{for(const w of ['st-shimon','st-aharon','st-shmulik','s9-yossi','st-naftali','pl-club','st-post'])g77MsgIn(w,'בדיקת דיוקן — שלום!',{silent:true});setPhoneOpen(true);State.phoneApp='msgs';renderPhone();const b=document.getElementById('phoneBody');return{svgs:b.querySelectorAll('.g77Av.tcPorAv svg').length,places:b.querySelectorAll('.g77Av:not(.tcPorAv)').length,img:b.querySelectorAll('img,image').length}})()`);
  await p.waitForTimeout(500); await shot('1_msgs');
  R.thread = await ev(`(()=>{const x=document.querySelector('[data-msg-open="st-shimon"]');if(x)x.click();const b=document.getElementById('phoneBody');return{head:!!b.querySelector('.g77Th .hd .g77Av.tcPorAv svg')}})()`);
  await p.waitForTimeout(400); await shot('2_thread');
  // the calls app
  R.calls = await ev(`(()=>{const s=g77St();s.calls.push({id:'CALL-t1',who:'st-david',at:Date.now(),state:'missed'},{id:'CALL-t2',who:'st-shimon',at:Date.now(),state:'answered'});State.phoneApp='calls';renderPhone();const b=document.getElementById('phoneBody');return{rows:b.querySelectorAll('.tcPorRow .tcPorMini svg').length,grid:b.querySelectorAll('.tcPorGrid svg').length,text:/לא נענתה/.test(b.textContent)}})()`);
  await p.waitForTimeout(400); await shot('3_calls');
  // the jobs (the families)
  R.jobs = await ev(`(()=>{State.phoneApp='missions';renderPhone();const b=document.getElementById('phoneBody');return{cards:b.querySelectorAll('.missionRow').length,fam:b.querySelectorAll('.missionRow.tcFam').length,icons:b.querySelectorAll('.missionRow .tcFamIc').length,heads:b.querySelectorAll('.missionGroupHead .tcFamIc').length,fams:[...new Set([...b.querySelectorAll('.missionRow.tcFam')].map(e=>e.dataset.fam))]}})()`);
  await p.waitForTimeout(400); await shot('4_jobs');
  await ev('setPhoneOpen(false)');
  // the incoming call
  R.ring = await ev(`(()=>{g77Sp().q.length=0;g77CallIn('st-shmulik','dlg-none',{ring:30});const e=document.getElementById('g77Ring');return{shown:!!e&&e.style.display!=='none',svg:!!(e&&e.querySelector('.av.tcPorAv svg'))}})()`);
  await p.waitForTimeout(400); await shot('5_ring');
  await ev(`g77SpEnd('declined')`);
  // the dialog
  R.dlg = await ev(`(()=>{g77DlgAdd('por-test',{who:'st-shimon',start:'a',rows:{a:{text:'בוא, ננסה להניע את הטנדר של סבא.',end:1}}});g77DlgOpen('por-test','talk');const d=document.getElementById('g77Dlg');return{svg:!!(d&&d.querySelector('.av.tcPorAv svg'))}})()`);
  await p.waitForTimeout(800); await shot('6_dlg');
  await ev('g77DlgClose(true)');
  R.dataImage = await p.evaluate(() => document.documentElement.outerHTML.split('data:image').length - 1);
  R.qa2 = await ev('window.__TC_POR_QA()');
  fs.writeFileSync(out, JSON.stringify(R, null, 1)); console.log(JSON.stringify({ qa: R.qa.ok, why: R.qa.why, contacts: R.qa.contacts, faces: R.qa.faces, things: R.qa.things, msgs: R.msgs, thread: R.thread, calls: R.calls, jobs: R.jobs, ring: R.ring, dlg: R.dlg, dataImage: R.dataImage, errs: errs.length, errs0: errs.slice(0, 5) }, null, 0));
  await b.close();
})().catch(e => { console.error(e); process.exit(1) });
