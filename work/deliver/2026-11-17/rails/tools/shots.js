// rails 17.11 — צילומים קרובים של כל צומת שנבנה (לבדיקה בעין שלי בלבד — לא לדף ולא לבעלים): node shots.js <game.html> <prefix>
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const [f, o] = process.argv.slice(2); const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 900, height: 600 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 200)));
  await p.goto('file://' + path.resolve(f) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(2000);
  const spots = [['sea', 6440, 5135, 3.2], ['e4x', 5850, 2852, 3.0], ['e4t', 5900, 3015, 3.0], ['e4n', 5850, 3190, 3.0], ['e3', 5935, 1800, 3.0], ['e6', 5850, 4312, 3.0], ['e5a', 5735, 3720, 2.6], ['e5b', 5735, 4080, 2.6]];
  for (const [n, x, y, z] of spots) { await p.evaluate(([x, y, z]) => window.__TC_DEV.cam({ x, y, zoom: z }), [x, y, z]); await p.waitForTimeout(1800); await p.screenshot({ path: o + '_' + n + '.png' }) }
  console.log('shots', spots.length, 'errors', errs.length, errs.slice(0, 2).join(' | '));
  await b.close();
})().catch(e => { console.error(String(e).slice(0, 300)); process.exit(1) });
