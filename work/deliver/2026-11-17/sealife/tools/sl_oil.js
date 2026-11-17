// sl_oil.js <game.html> <out.json> [shotDir] — sealife: שרשרת הנפט — השלבים, הכמות נשמרת, F, ועצירה כשהמכלית ריקה; צילומים לבדיקה עצמית
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out, shotDir] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] }); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 900000, polling: 500 });
  await p.waitForTimeout(1500); const ev = s => p.evaluate(x => window.__TC_DEV.ev(x), s);
  const tot = `(()=>{const s=window.__TC_OIL.S;return s.ship+s.ref[0]+s.ref[1]+s.buf[0]+s.buf[1]+s.bal.__plant})()`;
  await ev(`(()=>{const S=window.__TC_OIL.S;S.bal.__plant=0;const o=window.__TC_OIL.step;return 1})()`);
  const r = { tl: [] }; const T0 = await ev(`(()=>{const s=window.__TC_OIL.S;return{sum:s.ship+s.ref[0]+s.ref[1]+s.buf[0]+s.buf[1],plant:s.dayPlant,day:s.day}})()`);
  for (let t = 0; t <= 300; t += 20) { const s = await ev(`window.__TC_OIL.state()`); r.tl.push([t, s.ph, s.arm, s.q, s.toRef, s.toBuf, s.ship, s.ref.join('/'), s.buf.join('/'), s.boost, s.plant]); await ev(`window.__TC_SIM_STEP_QA({seconds:20,warmup:0,every:20})`) }
  const T1 = await ev(`(()=>{const s=window.__TC_OIL.S;return{sum:s.ship+s.ref[0]+s.ref[1]+s.buf[0]+s.buf[1],plant:s.dayPlant,day:s.day}})()`);
  r.conserve = { before: Math.round(T0.sum), after: Math.round(T1.sum), plant: Math.round(T1.plant - T0.plant), sameDay: T0.day === T1.day, diff: Math.round(T0.sum - T1.sum - (T1.plant - T0.plant)) };
  r.pumping = r.tl.some(x => x[1] === 'pump' && x[3] > 2000);
  if (shotDir) for (const [nm, x, y, z] of [['oil_pier', 2728, 5440, 1.0], ['oil_pipe', 2728, 4700, .7], ['oil_term', 2960, 4620, 1.2], ['oil_ref', 2760, 3600, 1.0], ['oil_far', 2728, 4800, .4]]) { await ev(`perfCamera({x:${x},y:${y},zoom:${z}})`); await p.waitForTimeout(1800); await p.screenshot({ path: path.join(shotDir, nm + '.png') }) }
  r.card = await ev(`(()=>{try{State.interactionId='C6-OIL-CTRL';const h=phoneBusinessBase();return{has:/הזרמת הנפט/.test(h),len:h.length}}catch(e){return{err:String(e)}}})()`);
  /* המכלית כמעט ריקה: עצירה, ניקוז, ניתוק — ואז משאבות הדחף */
  await ev(`(()=>{const S=window.__TC_OIL.S;S.ship=900;S.ref=[9000,8000];return 1})()`);
  r.tl2 = []; for (let t = 0; t <= 200; t += 20) { const s = await ev(`window.__TC_OIL.state()`); r.tl2.push([t, s.ph, s.arm, s.q, s.ship, s.boost, s.qBoost, s.buf.join('/'), s.ref.join('/')]); await ev(`window.__TC_SIM_STEP_QA({seconds:20,warmup:0,every:20})`) }
  r.emptyOk = r.tl2.some(x => x[1] === 'empty' && x[2] === 0 && x[3] === 0) && r.tl2.some(x => x[5] && x[6] > 0);
  /* המחזור (הבקר 17.11 סעיף 1): ריקה → המתנה → מטען חדש → idle; בבדיקה — מקצרים את ההמתנה ומתחילים מסוף הטעינה */
  r.tl3 = []; await ev(`(()=>{const S=window.__TC_OIL.S;S.pt=1e4;return 1})()`);
  for (let t = 0; t <= 120; t += 20) { await ev(`window.__TC_SIM_STEP_QA({seconds:20,warmup:0,every:20})`); const s = await ev(`window.__TC_OIL.state()`); r.tl3.push([t, s.ph, s.ship, s.loads]); if (s.ph === 'refill') await ev(`(()=>{const S=window.__TC_OIL.S;S.ship=Math.max(S.ship,window.__TC_OIL.CAP.ship-50);return 1})()`) }
  r.refillOk = r.tl3.some(x => x[1] === 'refill') && r.tl3.some(x => x[3] >= 1 && x[2] >= 71900);
  r.s5 = await ev(`(()=>{try{const w=window.__TC_LOGI13.table().streams.find(x=>x[0]==='S5');return{st:w[2],fuel:window.__TC_OIL.state().fuel}}catch(e){return{err:String(e)}}})()`);
  r.err = await ev(`window.__TC_OIL.err()`); r.ok = r.pumping && Math.abs(r.conserve.diff) <= 2 && r.card.has && r.emptyOk && r.refillOk && r.s5.st === 'run' && !r.err && !errs.length;
  fs.writeFileSync(out, JSON.stringify({ r, errs }, null, 1)); console.log(JSON.stringify(r).slice(0, 5000)); console.log('errs', JSON.stringify(errs)); await b.close();
})().catch(e => { console.error(String(e).slice(0, 300)); process.exit(1) });
