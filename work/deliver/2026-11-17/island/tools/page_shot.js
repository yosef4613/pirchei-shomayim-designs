// page_shot.js — צילום של דף לבדיקה בעין (לעצמי בלבד): node page_shot.js <page.html> <out.jpg> [width] [fullPage=1]
const { chromium } = require('playwright'); const path = require('path');
(async () => { const [f, out, w, full] = process.argv.slice(2); const b = await chromium.launch({ args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: +(w || 1400), height: 900 } }); await p.goto('file://' + path.resolve(f)); await p.waitForTimeout(500);
  await p.screenshot({ path: out, type: 'jpeg', quality: 80, fullPage: full !== '0' }); await b.close() })();
