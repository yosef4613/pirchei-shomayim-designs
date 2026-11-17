// eye3.js — צילומים לעצמי בלבד (בדיקה בעין של מה שנכנס ל-int300; לא לדף). node eye3.js <game.html> <outdir>
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
  await ev(closeAll); await shot('00_start', 1500);
  R.ghall = await ev(`(()=>{try{return JSON.stringify(window.__TC_GHALL.audit()).slice(0,400)}catch(e){return 'ERR '+e.message}})()`);
  await cam(4330, 2420, 1.5); R.d3 = 'garage hall + carrier'; await shot('01_d3_garage_hall', 4000);
  await cam(4250, 2330, 1.1); await shot('02_d3_carrier_lane', 3000);
  R.fch = await ev(`(()=>{try{const F=window.__TC_FCH;return JSON.stringify(Object.keys(F)).slice(0,200)}catch(e){return 'ERR '+e.message}})()`);
  await cam(7280, 935, 1.8); await shot('03_field_bag_halls', 4000);
  await cam(7900, 935, 1.5); await shot('03b_field_gates', 3000);
  R.live = await ev(`(()=>{try{return JSON.stringify(window.__TC_LIVEADD.list())+' | '+JSON.stringify(TC_LIVE_ADD.zones.map(z=>z.rect))}catch(e){return 'ERR '+e.message}})()`);
  R.liveAudit = await ev(`(()=>{try{return JSON.stringify(window.__TC_LIVEADD.audit()).slice(0,400)}catch(e){return 'ERR '+e.message}})()`);
  R.ffFlights = await ev(`(()=>{try{return JSON.stringify(window.__TC_FIELDFIX.flights()).slice(0,300)}catch(e){return 'ERR '+e.message}})()`);
  const z = await ev(`(()=>{try{const r=TC_LIVE_ADD.zones[0].rect;return JSON.stringify(Array.isArray(r)?r:[r.x,r.y,r.x+r.w,r.y+r.h])}catch(e){return '[8600,1600,9400,2400]'}})()`);
  let zr = [8600, 1600, 9400, 2400]; try { zr = JSON.parse(z) } catch (e) {}
  await cam((zr[0] + zr[2]) / 2, (zr[1] + zr[3]) / 2, 0.7); await shot('04_field_east', 4000);
  R.evt = await ev(`(()=>{try{return JSON.stringify(window.__TC_EVT.state()).slice(0,400)}catch(e){return 'ERR '+e.message}})()`);
  R.signs = await ev(`(()=>{try{const S=window.__TC_SIGNS12;return JSON.stringify({rows:S.rows.length,a:S.name('S16-RENT'),b:S.name('E3-KIOSK')})}catch(e){return 'ERR '+e.message}})()`);
  R.sact = await ev(`(()=>{try{return JSON.stringify(window.__TC_SACT.table()).slice(0,300)}catch(e){return 'ERR '+e.message}})()`);
  await cam(1700, 5000, 1.2); await shot('05_pier_b7', 3500);
  R.mb = await ev(`(()=>{try{return JSON.stringify(window.__TC_MB.state()).slice(0,300)}catch(e){return 'ERR '+e.message}})()`);
  await ev(`(()=>{State.mapQa=false;return 1})()`); R.map = await ev(`(()=>{setMapOpen(true);return 1})()`); await shot('06_map', 3000); await ev(closeAll);
  R.errs = errs.slice(0, 10); R.nerr = errs.length;
  fs.writeFileSync(path.join(out, 'eye3.json'), JSON.stringify(R, null, 1)); console.log(JSON.stringify(R).slice(0, 3000)); await b.close();
})().catch(e => { console.error(String(e).slice(0, 400)); process.exit(1) });
