// ft2_paxprobe.js <build> <out.json> — fieldthru2: הפירוט המלא של s15pax ושל fc_bridge_types (ב-q_ingame הפירוט נקטע ב-300 תווים) — כדי למצוא למה P6 נכשל
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await b.newPage({ viewport: { width: 1000, height: 700 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(8000);
  const s = await p.evaluate(() => window.__TC_DEV.ev(`(()=>{const R={};try{R.pax=window.__TC_S15PAX.audit()}catch(e){R.paxErr=String(e)}try{R.fcbr=FCBR.audit()}catch(e){R.fcbrErr=String(e)}
   try{R.planErr=S15J.planErr;const P=s15jPlan();R.plan=P?P.flights.map(f=>({g:f.g,nA:f.nA,nD:f.nD,dur:f.dur})):null}catch(e){R.planE=String(e)}return JSON.stringify(R)})()`));
  fs.writeFileSync(out, s); console.log('ok', s.length, 'errs', errs.length); await b.close();
})().catch(e => { console.error(String(e).slice(0, 400)); process.exit(1) });
