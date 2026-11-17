// shots.js — צילומים לעצמי בלבד (לבדיקה בעין; לא לדף). node shots.js <game.html> <outprefix> x,y,zoom[,label] ...
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const [file, pre, ...spec] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 240)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(1500);
  for (const s of spec) { const [x, y, z, l] = s.split(','); await p.evaluate(a => window.__TC_DEV.cam(a), { x: +x, y: +y, zoom: +z }); await p.waitForTimeout(+(process.env.SHOT_WAIT || 4000)); await p.screenshot({ path: pre + '_' + (l || (x + '_' + y + '_' + z)) + '.png' }); }
  if (errs.length) console.error('שגיאות דף: ' + errs.length + ' · ' + errs.slice(0, 4).join(' | '));
  await b.close();
})().catch(e => { console.error(String(e).slice(0, 400)); process.exit(1) });
