// labshot.js <page.html> <outDir> — closezoom: צילום לבדיקה עצמית בלבד (לא לדף) של דף הניסוי, ושגיאות הדף
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out] = process.argv.slice(2); fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch(); const errs = [];
  for (const [W, H, tag] of [[1400, 1500, 'wide'], [412, 900, 'narrow']]) {
    const p = await b.newPage({ viewport: { width: W, height: H } });
    p.on('pageerror', e => errs.push(tag + ' page: ' + String(e).slice(0, 300))); p.on('console', m => { if (m.type() === 'error') errs.push(tag + ' console: ' + m.text().slice(0, 300)) });
    await p.goto('file://' + path.resolve(file)); await p.waitForTimeout(2500);
    await p.screenshot({ path: path.join(out, tag + '_a.png'), fullPage: tag === 'wide' });
    await p.waitForTimeout(2600); await p.screenshot({ path: path.join(out, tag + '_b.png'), fullPage: tag === 'wide' });
    if (tag === 'wide') { await p.click('button[data-m="front"]'); await p.waitForTimeout(1200); await p.screenshot({ path: path.join(out, 'front.png'), fullPage: true });
      const st = await p.evaluate(() => ({ cz: window.__LAB.TCCZ.n, err: window.__LAB.TCCZ.err, p34err: window.P34X && P34X.err, stats: P34.stats(), sw: document.documentElement.scrollWidth })); console.log(JSON.stringify(st)) }
    else { const sw = await p.evaluate(() => document.documentElement.scrollWidth); console.log('narrow scrollWidth', sw) }
    await p.close();
  }
  console.log('errs', JSON.stringify(errs)); await b.close();
})().catch(e => { console.error(e); process.exit(1) });
