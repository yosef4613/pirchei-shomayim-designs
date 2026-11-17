// the plan page in the browser: opens, page / console errors, the number at the top (the status chip and the opening-screen KPI); 1366 light and 390 dark
const { chromium } = require('playwright'); const path = require('path');
(async () => { const f = process.argv[2]; const b = await chromium.launch(); const out = [];
  for (const [scheme, w] of [['light', 1366], ['dark', 390]]) {
    const p = await b.newPage({ viewport: { width: w, height: 900 }, colorScheme: scheme }); const errs = [];
    p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()) });
    const t0 = Date.now(); await p.goto('file://' + path.resolve(f)); await p.waitForTimeout(1500);
    const fr = p.frames().find(x => x !== p.mainFrame() && x.url().startsWith("about:srcdoc")) || p.mainFrame();
    let h1 = null; for (const fx of p.frames()) { try { await fx.waitForSelector('.view h1', { timeout: 60000 }); h1 = fx; break; } catch (e) {} }
    const o = await (h1 || fr).evaluate(() => { const v = document.querySelector('.view'); const chip = v && v.querySelector('.band .chip');
      return { title: document.title, h1: (v.querySelector('h1') || {}).textContent, chip: chip ? chip.textContent.slice(0, 220) : '', kpi: (v.querySelector('.kpi b') || {}).textContent,
               sub: [...v.querySelectorAll('.band p.sub')].map(x => x.textContent.slice(0, 200)), img: document.querySelectorAll('img').length } });
    out.push({ scheme, w, ms: Date.now() - t0, frames: p.frames().length, errs, ...o }); await p.close(); }
  await b.close(); console.log(JSON.stringify(out, null, 1)); })().catch(e => { console.error(e); process.exit(1) });
