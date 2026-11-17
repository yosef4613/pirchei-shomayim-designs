// airline_check.js <page> <shotdir> — דף חברות התעופה: נטען בלי שגיאות, מספר הקנבסים, סימון נשמר אחרי טעינה מחדש, העתקה. צילומים — פנימיים.
const { chromium } = require('playwright'); const path = require('path'), fs = require('fs');
(async () => { const [f, sd] = process.argv.slice(2); fs.mkdirSync(sd, { recursive: true }); const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 1280, height: 1000 } }); const p = await ctx.newPage();
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 200))); const url = 'file://' + path.resolve(f); await p.goto(url); await p.waitForTimeout(800);
  const R = await p.evaluate(() => ({ cos: document.querySelectorAll('.co').length, cvs: document.querySelectorAll('canvas').length, blank: [...document.querySelectorAll('canvas')].filter(c => { const d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data; for (let i = 3; i < d.length; i += 400) if (d[i]) return false; return true }).length }));
  await p.screenshot({ path: path.join(sd, 'a1.png') }); await p.evaluate(() => window.scrollTo(0, 1600)); await p.screenshot({ path: path.join(sd, 'a2.png') });
  await p.click('#now .co:first-child .mk button.redo'); await p.fill('#now .co:first-child textarea', 'בדיקה'); await p.waitForTimeout(200); await p.reload(); await p.waitForTimeout(600);
  R.kept = await p.evaluate(() => JSON.parse(document.getElementById('out').value)); await p.click('#cp'); await p.waitForTimeout(300); R.cpm = await p.textContent('#cpm');
  await p.click('#zm'); await p.waitForTimeout(300); await p.screenshot({ path: path.join(sd, 'a3.png') }); await p.click('#clr');
  R.errs = errs; console.log(JSON.stringify(R)); await b.close() })().catch(e => { console.error(e); process.exit(2) });
