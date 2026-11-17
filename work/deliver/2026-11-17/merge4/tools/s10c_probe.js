// s10c_probe.js — merge4 (17.11): למה "גלי הכרמל" (S10CI — אוניית הרכבים) לא חוזרת מהים ב-sl_tugs של sealife (arr 0 ב-6000 שנ׳ על try7921).
// node s10c_probe.js <game.html> <out.json> [maxS=2700] — צעדים של 20 שנ׳ (__TC_SIM_STEP_QA), רושם כל שינוי של שלב האונייה, ובנקודות 600 / 1200 / הסוף: __S10C.state / stats / log.
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out, maxS0] = process.argv.slice(2); const MAXS = +(maxS0 || 2700);
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] }); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 900000, polling: 500 });
  await p.waitForTimeout(1500); const ev = s => p.evaluate(x => window.__TC_DEV.ev(x), s);
  const R = { build: path.basename(file), ph: [], snaps: {} }; let last = null, t = 0;
  const snap = async k => { R.snaps[k] = await ev(`(()=>{const S=window.__S10C;return{t:${t},st:S.state(),stats:S.stats(),log:S.log(),err:S.err()}})()`) };
  while (t < MAXS) {
    const s = await ev(`(()=>{const S=window.__S10C.state();return{clk:S.clk,ph:S.ship.ph,hold:S.ship.hold,pool:S.pool,cars:S.cars.length}})()`);
    if (s.ph !== last) { R.ph.push([t, s.clk, s.ph, s.hold, s.pool, s.cars]); last = s.ph; if (s.ph === 'in1') break }
    if (t === 600 || t === 1200) await snap('t' + t);
    await ev(`window.__TC_SIM_STEP_QA({seconds:20,warmup:0,every:20})`); t += 20;
  }
  await snap('end'); R.errs = errs; fs.writeFileSync(out, JSON.stringify(R, null, 1));
  const e = R.snaps.end; console.log(JSON.stringify({ build: R.build, t, ph: R.ph, pool: e.st.pool, stats: e.stats, cars: e.st.cars.slice(0, 12), err: e.err, errs }).slice(0, 4000)); await b.close();
})().catch(e => { console.error(String(e).slice(0, 400)); process.exit(1) });
