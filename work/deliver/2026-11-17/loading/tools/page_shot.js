// page_shot.js <page.html> <out.png> [clickSel] [w] [h] — צילום לבדיקה פנימית בלבד
const { chromium } = require('playwright'); const path = require('path');
(async () => { const [f, o, sel, w, h] = process.argv.slice(2); const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: +w || 1280, height: +h || 800 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(f)); await p.waitForTimeout(800); if (sel) { await p.click(sel); await p.waitForTimeout(900) }
  await p.screenshot({ path: o, fullPage: !sel }); console.log('errors', errs.length, errs.join(' | ')); await b.close() })();
