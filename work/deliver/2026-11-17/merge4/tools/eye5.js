// eye5.js — merge4 (17.11, גל 4; על בסיס merge3/tools/eye4.js): צילומים לעצמי בלבד (בדיקה בעין של מה שנכנס ל-int303; לא לדף). node eye5.js <game.html> <outdir>
// האי (היבשה של E9, לולאת המזרח, הצומת המרומזר), הים (הגוררות של sealife, הנפט), האירועים (F9 ← אירועים — אש), כלי W17 (הסוכנות, SP-06), F9, המפה — ושגיאות הדף.
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
  R.e9 = await js('(()=>{const r=window.ISL17E9||null;return r&&{ok:r.ok,err:r.err,v:r.v,off:r.off}})()'); R.islE = await js('window.__TC_ISL17E&&window.__TC_ISL17E()'); R.islE9 = await js('window.__TC_ISL17E9&&window.__TC_ISL17E9()');
  await cam(5400, 7350, 0.55); await shot('01_e9_land', 4000);
  await cam(8700, 6900, 0.6); await shot('02_island_east_loop', 4000);
  await cam(8330, 7320, 0.9); await shot('03_island_signal', 3500);
  R.tugs = await js('window.__TC_TUGX&&window.__TC_TUGX()', 500); R.oil = await js('window.__TC_OIL&&window.__TC_OIL()', 500);
  await cam(3800, 5800, 0.6); await shot('04_sea_tugs_ferry', 3500);
  R.evt = await js('window.__TC_EVT&&Object.keys(window.__TC_EVT)', 300); R.perf = await js('window.__TC_PERF17&&window.__TC_PERF17()', 300);
  R.w17 = await js('(typeof W17RIDE!=="undefined"&&Object.keys(W17RIDE))||(window.__TC_W17&&Object.keys(window.__TC_W17))||null', 300);
  await ev(`(()=>{State.mapQa=false;return 1})()`); await ev(closeAll);
  await p.keyboard.press('F9'); await shot('05_f9', 2500); await p.keyboard.press('Escape'); await ev(closeAll);
  R.map = await ev(`(()=>{setMapOpen(true);return 1})()`); await shot('06_map', 3000); await ev(closeAll);
  R.build = await js('(window.TC_BUILD_ID||document.title)', 80);
  R.errs = errs.slice(0, 10); R.nerr = errs.length;
  fs.writeFileSync(path.join(out, 'eye5.json'), JSON.stringify(R, null, 1)); console.log(JSON.stringify(R).slice(0, 3000)); await b.close();
})().catch(e => { console.error(String(e).slice(0, 400)); process.exit(1) });
