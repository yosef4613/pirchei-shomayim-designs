// shots2.js — צילומים לעצמי (לבדיקה בעין). node shots2.js <game.html> <outprefix> <W> <H> <pre-eval-js|-> x,y,zoom,label ...
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const [file, pre, W, H, pe, ...spec] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: +W, height: +H }, deviceScaleFactor: +(process.env.DSF || 1) });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 240)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(1500);
  if (pe && pe !== '-') console.log(await p.evaluate(s => { try { return String(window.__TC_DEV.ev(s)) } catch (e) { return 'ERR ' + e } }, pe));
  for (const s of spec) { const [x, y, z, l] = s.split(','); await p.evaluate(a => window.__TC_DEV.cam(a), { x: +x, y: +y, zoom: +z }); await p.waitForTimeout(+(process.env.SHOT_WAIT || 5000)); await p.screenshot({ path: pre + '_' + l + '.png' }); }
  if (process.env.POST) console.log(await p.evaluate(s => { try { return String(window.__TC_DEV.ev(s)) } catch (e) { return 'ERR ' + e } }, process.env.POST));
  if (errs.length) console.error('שגיאות דף: ' + errs.length + ' · ' + errs.slice(0, 4).join(' | '));
  await b.close();
})().catch(e => { console.error(String(e).slice(0, 400)); process.exit(1) });
