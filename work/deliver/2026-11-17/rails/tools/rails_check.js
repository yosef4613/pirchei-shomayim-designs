// rails 17.11 — הבדיקה החוסמת של המסילות + צילומים לעצמי (לא לדף): node rails_check.js <game.html> <out.json> [shots_prefix]
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [f, out, shots] = process.argv.slice(2); const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1400, height: 900 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 240)));
  await p.goto('file://' + path.resolve(f) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(2500);
  const q = fs.readFileSync(path.join(__dirname, 'q_rails.js'), 'utf8');
  const R = JSON.parse(await p.evaluate(s => JSON.stringify(window.__TC_DEV.ev(s)), '(()=>{' + q + '\n})()'));
  const spots = [['photo', 6430, 5130, 3.0], ['sea', 6350, 5150, 1.2], ['e4', 5850, 2950, 1.0], ['e6', 5850, 4400, 1.4], ['yard', 5730, 3850, 1.1], ['e3n', 5930, 1850, 1.4]];
  R.drawn = [];
  if (shots) for (const [n, x, y, z] of spots) {
    await p.evaluate(([x, y, z]) => window.__TC_DEV.cam({ x, y, zoom: z }), [x, y, z]); await p.waitForTimeout(2200);
    await p.screenshot({ path: shots + '_' + n + '.png' });
    R.drawn.push([n, await p.evaluate(() => window.__TC_DEV.ev('RJX.drawn'))]);
  }
  R.pageErrors = errs.length; R.pageErrorsHead = errs.slice(0, 4); if (errs.length) { R.ok = false; R.fail.push('page-errors:' + errs.length) }
  fs.writeFileSync(out, JSON.stringify(R, null, 1)); console.log('rails_check', R.ok ? 'PASS' : 'FAIL', R.fail.slice(0, 8).join(' | '), 'errors', errs.length);
  await b.close(); process.exit(0);
})().catch(e => { console.error(String(e).slice(0, 400)); process.exit(1) });
