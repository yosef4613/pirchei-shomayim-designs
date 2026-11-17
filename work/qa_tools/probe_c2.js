// probe_c2.js — מריץ שאילתה אחת בתוך המשחק ומדפיס את התוצאה (בונה S7F266, 8.11; במקום הכלי של הבונה הקודם שלא הגיע בחבילה).
// node probe_c2.js <game.html> <query.js> [out.json]
//   השאילתה: ביטוי JS אחד (כמו tools_pack/style_dump.js) או גוף של פונקציה שמתחיל ב-return (כמו qa_story5.js).
//   התוצאה: מחרוזת — מודפסת כמו שהיא; אחרת — JSON. ‏Promise — מחכים לו.
//   בדפוס של שאר הכלים: Chromium אחד, ‎#dev‎, מחכים ל-__TC_DEV.ready(), ושגיאות הדף נאספות (ל-stderr).
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, qf, out] = process.argv.slice(2);
  if (!file || !qf) { console.error('usage: node probe_c2.js <game.html> <query.js> [out.json]'); process.exit(2) }
  let src = fs.readFileSync(qf, 'utf8');
  const body = src.replace(/^(\s*\/\/[^\n]*\n|\s*\/\*[\s\S]*?\*\/)*/, '');
  if (/^\s*return\b/.test(body)) src = '(()=>{' + src + '\n})()';
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 240)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(+(process.env.PROBE_WAIT_MS || 1500));
  let r;
  try { r = await p.evaluate(s => Promise.resolve(window.__TC_DEV.ev(s)).then(v => typeof v === 'string' ? v : JSON.stringify(v)), src) }
  catch (e) { console.error('probe: השאילתה נכשלה — ' + String(e).slice(0, 600)); await b.close(); process.exit(1) }
  if (out) fs.writeFileSync(out, r); else process.stdout.write(r + '\n');
  if (errs.length) console.error('שגיאות דף: ' + errs.length + ' · ' + errs.slice(0, 4).join(' | '));
  await b.close(); process.exit(0);
})().catch(e => { console.error(String(e).slice(0, 400)); process.exit(1) });
