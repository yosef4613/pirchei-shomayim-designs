// eye.js — צילומים לעצמי בלבד (בדיקה בעין של מה שנכנס ל-int299; לא לדף). node eye.js <game.html> <outdir>
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
(async () => {
  const [file, out] = process.argv.slice(2); fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 1280, height: 800 } }); const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 240)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 900000, polling: 500 });
  const ev = s => p.evaluate(s => Promise.resolve(window.__TC_DEV.ev(s)), s).catch(e => 'EV-ERR ' + String(e).slice(0, 200));
  const R = {}; const shot = async (n, w) => { await p.waitForTimeout(w || 2500); await p.screenshot({ path: path.join(out, n + '.png') }) };
  const esc = async () => { await p.keyboard.press('Escape').catch(() => {}); await p.waitForTimeout(400) };
  await shot('00_start', 2000);
  R.icon = await p.evaluate(() => { const l = [...document.querySelectorAll('link[rel~=icon]')]; return { n: l.length, href: l.map(x => x.href.slice(0, 12)), ok: window.__TC_ICON } });
  R.stadium = await ev(`(()=>{State.mapQa=true;Camera.x=770;Camera.y=2420;Camera.zoom=4.5;return LEAGUE4.signLine()})()`); await shot('01_stadium', 3000);
  R.map = await ev(`(()=>{setMapOpen(true);return JSON.stringify(window.__TC_MMIS&&window.__TC_MMIS.S?window.__TC_MMIS.S.n:null)})()`); await shot('02_map', 3000); await ev(`setMapOpen(false)`);
  R.msgs = await ev(`(()=>{setPhoneOpen(true);openPhoneApp('msgs');return document.getElementById('phoneBody').innerText.slice(0,300)})()`); await shot('03_phone_msgs', 2000);
  R.journal = await ev(`(()=>{openPhoneApp('journal');return document.getElementById('phoneBody').innerText.slice(0,300)})()`); await shot('03b_phone_journal', 1500);
  R.calls = await ev(`(()=>{openPhoneApp('calls');return document.getElementById('phoneBody').innerText.slice(0,200)})()`); await shot('03c_phone_calls', 1500);
  await ev(`setPhoneOpen(false)`);
  R.f9 = await ev(`(()=>{tcF9Open();return 1})()`); await shot('04_f9', 2500); R.f9b = await ev(`(()=>{const e=document.querySelector('#tcF9,#tcf9,.tcF9');return e?e.innerText.slice(0,300):'no-el'})()`); await esc(); await ev(`(()=>{try{tcF9Open()}catch(e){}return 1})()`); await esc();
  R.gst = await ev(`(()=>{try{return JSON.stringify(window.__TC_GST.open('garage'))}catch(e){return 'ERR '+e.message}})()`); await shot('05_garage', 3000); R.gstAudit = await ev(`(()=>{try{return JSON.stringify(window.__TC_GST.audit()).slice(0,300)}catch(e){return 'ERR '+e.message}})()`); await esc();
  R.sea = await ev(`(()=>{State.mapQa=true;Camera.x=3000;Camera.y=6400;Camera.zoom=0.44;return JSON.stringify(window.__TC_SEATREES.stats().n)})()`); await shot('06_sea_c8', 4000);
  R.stand = await ev(`(()=>{const s=Object.values(S15D.stands)[0];State.mapQa=true;Camera.x=s.cx;Camera.y=s.nose;Camera.zoom=1.6;return s.cx+','+s.nose})()`); await shot('07_field', 4000);
  R.lock = await ev(`(()=>{State.mapQa=false;PlayerProfile.mode='walk';PlayerPed.x=2300;PlayerPed.y=1760;Camera.x=2300;Camera.y=1650;Camera.zoom=.8;return JSON.stringify(window.__TC_LOCK.E)})()`); await shot('08_lock', 3000);
  R.mb = await ev(`(()=>{const MB=window.__TC_MB;return MB&&MB.state?JSON.stringify(MB.state()).slice(0,400):'no'})()`);
  R.tut = await ev(`(()=>{try{return JSON.stringify(window.__TC_TUT.state()).slice(0,300)}catch(e){return 'ERR '+e.message}})()`);
  R.cut = await ev(`(()=>{try{TCCUT.play('1-van');return 1}catch(e){return 'ERR '+e.message}})()`); await shot('09_cut', 3500); await shot('09b_cut', 3000); await ev(`(()=>{try{window.__TC_CUT.end()}catch(e){}return 1})()`);
  R.errs = errs.slice(0, 10); R.nerr = errs.length;
  // בלי #dev — מסך הטעינה
  const p2 = await b.newPage({ viewport: { width: 1280, height: 800 } }); const e2 = []; p2.on('pageerror', e => e2.push(String(e).slice(0, 240)));
  await p2.goto('file://' + path.resolve(file), { waitUntil: 'commit' }); await p2.waitForTimeout(5000); await p2.screenshot({ path: path.join(out, '10_boot_a.png') });
  await p2.waitForTimeout(40000); await p2.screenshot({ path: path.join(out, '10_boot_b.png') }); R.boot = { errs: e2.slice(0, 5), n: e2.length, title: await p2.title() };
  fs.writeFileSync(path.join(out, 'eye.json'), JSON.stringify(R, null, 1)); console.log(JSON.stringify(R).slice(0, 3000)); await b.close();
})().catch(e => { console.error(String(e).slice(0, 400)); process.exit(1) });
