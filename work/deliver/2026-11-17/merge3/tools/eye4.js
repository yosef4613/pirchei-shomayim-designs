// eye4.js — merge3 (17.11, גל 3): צילומים לעצמי בלבד (בדיקה בעין של מה שנכנס ל-int302; לא לדף). node eye4.js <game.html> <outdir>
// האי (המזרח, הצומת, רכבת המשא), השדה (האמפיבי על המים, המזוודות), המוסך (העבודה בתא), F9, המפה, TCBUSY — ושגיאות הדף.
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
  const cam = (x, y, z) => ev(`(()=>{State.mapQa=true;Camera.x=${x};Camera.y=${y};Camera.zoom=${z};return 1})()`);
  const js = (e, n) => ev(`(()=>{try{return JSON.stringify(${e}).slice(0,${n || 400})}catch(e){return 'ERR '+e.message}})()`);
  await ev(closeAll); await shot('00_start', 1500);
  R.islE = await js('window.__TC_ISL17E()'); R.islF = await js('window.__TC_ISLF()');
  await cam(8700, 6900, 0.6); await shot('01_island_east', 4000);
  await cam(8330, 7320, 0.9); await shot('02_island_junction', 3500);
  R.amph = await js('Object.keys(window.__TC_FCAMPH||{})', 200); R.bags = await js('Object.keys(window.__TC_FCBAGS||{})', 200);
  await cam(7800, 3530, 0.8); await shot('03_field_amph_water', 3500);
  await cam(7280, 935, 1.8); await shot('04_field_bags', 3500);
  R.gsvc = await js('window.__TC_GSVC.audit()'); R.fly = await js('Object.keys(window.__TC_FLY||{})', 200);
  await cam(4330, 2420, 1.5); await shot('05_garage_hall', 3500);
  R.busy = await js('(window.TCBUSY&&{top:TCBUSY.top&&TCBUSY.top(),keys:Object.keys(TCBUSY)})', 300);
  await ev(`(()=>{State.mapQa=false;return 1})()`); await ev(closeAll);
  await p.keyboard.press('F9'); await shot('06_f9', 2500); await p.keyboard.press('Escape'); await ev(closeAll);
  R.map = await ev(`(()=>{setMapOpen(true);return 1})()`); await shot('07_map', 3000); await ev(closeAll);
  R.errs = errs.slice(0, 10); R.nerr = errs.length;
  fs.writeFileSync(path.join(out, 'eye4.json'), JSON.stringify(R, null, 1)); console.log(JSON.stringify(R).slice(0, 3000)); await b.close();
})().catch(e => { console.error(String(e).slice(0, 400)); process.exit(1) });
