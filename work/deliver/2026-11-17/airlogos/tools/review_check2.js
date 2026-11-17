// review_check2.js <page.html> <shotdir> <out.json> — דף הסקירה: ציוני העיצוב — מחכה לסיום החישוב, סופר לפי ציון ולפי מנוע, דוגמאות,
//  וצילומים (פנימיים בלבד) של כל ציון בכל אזור — לבדיקה בעין.
const { chromium } = require('playwright'); const path = require('path'), fs = require('fs');
(async () => { const [f, sd, out] = process.argv.slice(2); fs.mkdirSync(sd, { recursive: true }); const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1300, height: 1000 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 200))); await p.goto('file://' + path.resolve(f));
  const t0 = Date.now(); await p.waitForFunction('typeof scDone!=="undefined"&&scDone===true', null, { timeout: 600000, polling: 1000 }); const secs = (Date.now() - t0) / 1000;
  const R = await p.evaluate(() => { const by = {}, ex = {}; for (const k in SC) { const api = k.split('|')[0], s = SC[k].s; by[api] = by[api] || { full: 0, mid: 0, simple: 0 }; by[api][s]++; (ex[api + ':' + s] = ex[api + ':' + s] || []).length < 6 && ex[api + ':' + s].push(k.split('|')[1]) } return { n: Object.keys(SC).length, by, ex, fail: (window.__FAIL || []).length } });
  R.secs = secs; R.errs = errs;
  for (const t of ['city', 'airport', 'port', 'island', 'lib']) { await p.click('#tabs button[data-t="' + t + '"]'); await p.waitForTimeout(300);
    for (const d of ['full', 'mid', 'simple']) { const btn = await p.$('button[data-d="' + d + '"]'); if (!btn) continue; await btn.click(); await p.waitForTimeout(900); await p.evaluate(() => window.scrollTo(0, 560)); await p.waitForTimeout(700); await p.screenshot({ path: path.join(sd, t + '_' + d + '.png') }) } }
  fs.writeFileSync(out, JSON.stringify(R, null, 1)); console.log(JSON.stringify({ n: R.n, by: R.by, secs, fail: R.fail, errs: errs.length })); await b.close() })().catch(e => { console.error(e); process.exit(2) });
