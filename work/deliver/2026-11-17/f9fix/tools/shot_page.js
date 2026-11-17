// shot_page.js — צילום של דף (לעצמי, לבדיקה בעין): node shot_page.js <page.html> <out.png> [width]
const { chromium } = require('playwright'); const path = require('path');
(async () => { const [f, o, w] = process.argv.slice(2); const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: +(w || 1280), height: 900 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e))); await p.goto('file://' + path.resolve(f)); await p.waitForTimeout(500);
  await p.screenshot({ path: o, fullPage: true }); const sw = await p.evaluate(() => document.documentElement.scrollWidth); console.log(JSON.stringify({ errs, scrollWidth: sw })); await b.close() })();
