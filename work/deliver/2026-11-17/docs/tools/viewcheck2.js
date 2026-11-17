// הדף בדפדפן: כל תצוגה (#overview, ‏#roadmap, ‏#decisions ...) — שגיאות, וחיפוש של המחרוזות החדשות של v7.01
const { chromium } = require('playwright'); const path = require('path');
(async () => { const f = process.argv[2]; const b = await chromium.launch(); const out = { views: {}, errs: [] };
  const need = ['S17 — האי מחדש', 'W34', 'D‑698', 'D‑694', 'גיטהב', 'S7F298', 'כמה נשאר (17.11'];
  for (const v of ['overview', 'roadmap', 'decisions', 'new', 'history', 'sources']) {
    const p = await b.newPage({ viewport: { width: 1366, height: 900 } });
    p.on('pageerror', e => out.errs.push(v + ': ' + String(e))); p.on('console', m => { if (m.type() === 'error') out.errs.push(v + ' console: ' + m.text()) });
    await p.goto('file://' + path.resolve(f) + '#' + v); await p.waitForTimeout(2500);
    let txt = ''; for (const fx of p.frames()) { try { txt += await fx.evaluate(() => document.body ? document.body.innerText : '') } catch (e) {} }
    out.views[v] = { len: txt.length, found: need.filter(s => txt.includes(s)) }; await p.close(); }
  await b.close(); console.log(JSON.stringify(out, null, 1)); })().catch(e => { console.error(e); process.exit(1) });
