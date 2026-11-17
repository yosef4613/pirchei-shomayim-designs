// page_shot.js — צילום של דף (לבדיקה בעין בלבד, לא לדף): node page_shot.js <page.html> <out.png> [width] [fullpage=1]
const { chromium } = require('playwright'); const path = require('path');
(async () => { const [f, o, w, fp] = process.argv.slice(2); const b = await chromium.launch({ args: ['--no-sandbox'] }); const p = await b.newPage({ viewport: { width: +w || 1280, height: 900 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e))); await p.goto('file://' + path.resolve(f)); await p.waitForTimeout(1500);
  await p.screenshot({ path: o, fullPage: fp !== '0' }); console.log('errors', errs.length, errs.slice(0, 3).join(' | ')); await b.close() })();
