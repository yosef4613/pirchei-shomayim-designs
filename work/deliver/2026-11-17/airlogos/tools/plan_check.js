// plan_check.js <page.html> <shot.png> — הדף של הציור נטען בלי שגיאות, והגלריה מצוירת (צילום — לבדיקה פנימית בלבד)
const { chromium } = require('playwright'); const path = require('path');
(async () => { const [f, shot] = process.argv.slice(2); const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1200, height: 900 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e))); await p.goto('file://' + path.resolve(f)); await p.waitForTimeout(800);
  const n = await p.evaluate(() => document.querySelectorAll('#gal canvas').length); await p.click('#nt'); await p.waitForTimeout(300);
  const imgs = await p.evaluate(() => document.querySelectorAll('img').length);
  await p.screenshot({ path: shot, fullPage: true }); console.log(JSON.stringify({ canvases: n, imgs, errs })); await b.close() })().catch(e => { console.error(e); process.exit(2) });
