// בדיקת דף ההשוואה בדפדפן: 0 שגיאות, שלוש הספריות הישנות עלו, המדידה רצה; צילום לבדיקה פנימית בלבד.
// node page_check.js <page.html> <out.png> <out.json>
const { chromium } = require('playwright'); const path = require('path'), fs = require('fs');
(async () => { const [f, png, js] = process.argv.slice(2); const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1200, height: 900 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300))); p.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text().slice(0, 300)) });
  const reqs = []; p.on('request', r => { if (!r.url().startsWith('file:')) reqs.push(r.url()) });
  const t0 = Date.now(); await p.goto('file://' + path.resolve(f)); await p.waitForFunction(() => window.__res, null, { timeout: 120000 }); const load = Date.now() - t0;
  await p.waitForTimeout(1500); await p.click('#benchBtn'); await p.waitForFunction(() => window.__bench, null, { timeout: 180000 });
  const r = await p.evaluate(() => ({ res: window.__res, bench: window.__bench, errsText: document.getElementById('errs').textContent, imgs: document.images.length, h: document.body.scrollHeight }));
  await p.screenshot({ path: png, fullPage: true }); const out = { load, errs, reqs, ...r }; fs.writeFileSync(js, JSON.stringify(out, null, 1)); console.log(JSON.stringify(out).slice(0, 1500)); await b.close() })();
