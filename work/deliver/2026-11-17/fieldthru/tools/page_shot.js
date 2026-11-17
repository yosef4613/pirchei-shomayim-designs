// page_shot.js <page.html> <outprefix> — צילום לעצמי (לא לדף): רוחב 1000 ו-390, שגיאות, גלילה לרוחב
const { chromium } = require('playwright'); const path = require('path'), fs = require('fs');
(async () => { const [f, o] = process.argv.slice(2); const b = await chromium.launch(); const res = {};
 for (const w of [1000, 390]) { const p = await b.newPage({ viewport: { width: w, height: 900 } }); const errs = []; p.on('pageerror', e => errs.push(String(e)));
  await p.goto('file://' + path.resolve(f)); await p.waitForTimeout(800);
  const sw = await p.evaluate(() => [document.documentElement.scrollWidth, innerWidth]); await p.screenshot({ path: o + '_' + w + '.png', fullPage: true });
  res[w] = { errs, scroll: sw }; await p.close() }
 fs.writeFileSync(o + '.json', JSON.stringify(res)); console.log(JSON.stringify(res)); await b.close() })().catch(e => { console.error(e); process.exit(1) });
