// shot_game.js — fieldcalc: צילומים מהמשחק לבדיקה בעין (לעצמי בלבד — לא לדף ולא לבעלים): node shot_game.js <game.html> <out_prefix>
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const [f, o] = process.argv.slice(2); const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1400, height: 900 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 200)));
  await p.goto('file://' + path.resolve(f) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(2000);
  const cam = (x, y, z) => p.evaluate(([x, y, z]) => { try { perfCamera({ x, y, zoom: z }) } catch (e) { try { State.mapQa = true; Camera.x = x; Camera.y = y; Camera.zoom = z } catch (e2) {} } }, [x, y, z]);
  const shots = [['p6', 8980, 1110, 2.6], ['r', 9030, 1180, 2.6], ['bh12', 7100, 930, 2.0], ['bh45', 8250, 930, 2.0]];
  for (const [n, x, y, z] of shots) { await cam(x, y, z); await p.waitForTimeout(1500); await p.screenshot({ path: o + '_' + n + '.png' }) }
  console.log('errors', errs.length, errs.slice(0, 3).join(' | '));
  await b.close();
})().catch(e => { console.error(String(e).slice(0, 300)); process.exit(1) });
