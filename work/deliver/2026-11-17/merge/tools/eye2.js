// eye2.js — צילומים לעצמי בלבד (סבב 2 של הבדיקה בעין; לא לדף). node eye2.js <game.html> <outdir>
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
(async () => {
  const [file, out] = process.argv.slice(2); fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 1280, height: 800 } }); const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 240)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 900000, polling: 500 });
  const ev = s => p.evaluate(s => Promise.resolve(window.__TC_DEV.ev(s)), s).catch(e => 'EV-ERR ' + String(e).slice(0, 200));
  const R = {}; const shot = async (n, w) => { await p.waitForTimeout(w || 2500); await p.screenshot({ path: path.join(out, n + '.png') }) };
  const closeAll = `(()=>{try{if(PERF.hud)perfHudToggle()}catch(e){}try{setPhoneOpen(false)}catch(e){}try{setMapOpen(false)}catch(e){}return 1})()`;
  await ev(closeAll);
  R.gst = await ev(`(()=>{try{return JSON.stringify(window.__TC_GST.open('garage'))}catch(e){return 'ERR '+e.message}})()`); await shot('05_garage', 3500);
  await p.keyboard.press('Escape').catch(() => {}); await ev(closeAll);
  R.sea = await ev(`(()=>{State.mapQa=true;Camera.x=3000;Camera.y=6400;Camera.zoom=0.44;return JSON.stringify(window.__TC_SEATREES.stats().n)})()`); await shot('06_sea_c8', 4000);
  R.stand = await ev(`(()=>{const s=Object.values(S15D.stands)[0];State.mapQa=true;Camera.x=s.cx;Camera.y=s.nose;Camera.zoom=1.4;return s.cx+','+s.nose})()`); await shot('07_field', 4000);
  R.lock = await ev(`(()=>{State.mapQa=false;PlayerProfile.mode='walk';PlayerPed.x=2300;PlayerPed.y=1760;Camera.x=2300;Camera.y=1650;Camera.zoom=.8;return JSON.stringify(window.__TC_LOCK.E)})()`); await shot('08_lock', 3000);
  R.mb = await ev(`(()=>{const MB=window.__TC_MB;MB.force(true);try{__TC_STORY.jump('1-3')}catch(e){}delete g77St().board;MB.tick();return JSON.stringify(MB.state()).slice(0,500)})()`);
  await p.waitForTimeout(4000); R.card = await ev(`(()=>{const d=document.getElementById('tcMbCard');return d?d.style.display+' | '+d.innerText.slice(0,200):'none'})()`); await shot('11_board_card', 1000);
  R.map = await ev(`(()=>{setMapOpen(true);return 1})()`); await shot('12_board_map', 3000); await ev(closeAll);
  R.msgs = await ev(`(()=>{setPhoneOpen(true);openPhoneApp('msgs');return document.getElementById('phoneBody').innerText.slice(0,300)})()`); await shot('13_phone_msgs', 2500);
  R.journal = await ev(`(()=>{openPhoneApp('journal');return document.getElementById('phoneBody').innerText.slice(0,300)})()`); await shot('13b_journal', 2000); await ev(closeAll);
  R.cut = await ev(`(()=>{try{TCCUT.play('1-van');return 1}catch(e){return 'ERR '+e.message}})()`); await shot('09_cut', 3500); await shot('09b_cut', 3500); await ev(`(()=>{try{window.__TC_CUT.end()}catch(e){}return 1})()`);
  R.errs = errs.slice(0, 10); R.nerr = errs.length;
  try { const p2 = await b.newPage({ viewport: { width: 1280, height: 800 } }); const e2 = []; p2.on('pageerror', e => e2.push(String(e).slice(0, 240)));
    await p2.goto('file://' + path.resolve(file), { waitUntil: 'commit' }); await p2.waitForTimeout(8000); await p2.screenshot({ path: path.join(out, '10_boot_a.png'), timeout: 180000 }).catch(e => R.bootA = String(e).slice(0, 120));
    await p2.waitForTimeout(45000); await p2.screenshot({ path: path.join(out, '10_boot_b.png'), timeout: 180000 }).catch(e => R.bootB = String(e).slice(0, 120)); R.boot = { errs: e2.slice(0, 5), n: e2.length } } catch (e) { R.bootErr = String(e).slice(0, 200) }
  fs.writeFileSync(path.join(out, 'eye2.json'), JSON.stringify(R, null, 1)); console.log(JSON.stringify(R).slice(0, 3000)); await b.close();
})().catch(e => { console.error(String(e).slice(0, 400)); process.exit(1) });
