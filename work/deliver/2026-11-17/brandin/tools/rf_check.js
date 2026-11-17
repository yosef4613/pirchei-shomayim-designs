// rf_check.js <page.html> <out.json> [shot.png] — brandin: דף הבדיקה "לפני / אחרי" של המזנונים — ההבדלים (window.__RF) ושגיאות
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => { const [file, out, shot] = process.argv.slice(2); const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1200, height: 900 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 200)));
  await p.goto('file://' + path.resolve(file)); await p.waitForFunction(() => window.__RF, null, { timeout: 120000 });
  const day = await p.evaluate(() => window.__RF); await p.click('#nt'); await p.waitForTimeout(500); const night = await p.evaluate(() => window.__RF);
  if (shot) { await p.click('#nt'); await p.waitForTimeout(300); await p.screenshot({ path: shot, fullPage: true }) }
  const R = { day, night, maxDay: Math.max(...day), maxNight: Math.max(...night), meanDay: day.reduce((a, b) => a + b, 0) / day.length, errs };
  fs.writeFileSync(out, JSON.stringify(R)); console.log(JSON.stringify(R)); await b.close() })().catch(e => { console.error(e); process.exit(2) });
