// run_js.js — f9fix: מריץ קוד בתוך המשחק (#dev) ושומר את התוצאה: node run_js.js <game.html> <code.js> <out.json>
// הקוד: גוף שמחזיר ערך / Promise (כמו q_f9_checks.js). שגיאות בדף — בשדה pageErrors.
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => { const [file, code, out] = process.argv.slice(2); const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 1280, height: 800 } }); const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' }); await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 }); await p.waitForTimeout(2000);
  const src = fs.readFileSync(code, 'utf8'); const expr = src.trim().replace(/^return\s+/, ''); let r; try { r = await p.evaluate(x => Promise.resolve(window.__TC_DEV.ev(x)), expr) } catch (e) { r = { evalError: String(e).slice(0, 500) } }
  const o = { result: r, pageErrors: errs }; fs.writeFileSync(out, JSON.stringify(o, null, 1)); console.log(JSON.stringify(o).slice(0, 3000)); await b.close() })();
