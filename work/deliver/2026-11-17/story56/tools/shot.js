// story56 · צילום לעצמי (בדיקה בעין בלבד, לא לדף): node shot.js <page.html> <out.png> [width] [height]
const { chromium } = require('playwright'); const path = require('path');
(async () => { const [f, o, w, h] = process.argv.slice(2); const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: +(w || 1200), height: +(h || 900) } });
  await p.goto('file://' + path.resolve(f)); await p.waitForTimeout(400); await p.screenshot({ path: o, fullPage: true }); await b.close() })();
