// plan_shot.js — צילום של הציור (רק לעצמי — לבדוק שהטקסט בתוך המסגרות). node plan_shot.js <plan.html> <out.png>
const { chromium } = require('playwright'); const path = require('path');
(async () => { const [f, o] = process.argv.slice(2); const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1100, height: 900 } });
  await p.goto('file://' + path.resolve(f)); await p.waitForTimeout(500); await p.screenshot({ path: o, fullPage: true }); await b.close() })().catch(e => { console.error(e); process.exit(1) });
