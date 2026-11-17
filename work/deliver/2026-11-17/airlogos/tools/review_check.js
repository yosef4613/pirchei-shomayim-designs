// review_check.js <page.html> <shotdir> — הדף לבעלים: נטען, כל לשונית מציירת, כמה קנבסים נכשלו ("לא צויר"), שגיאות דף. צילומים — פנימיים בלבד.
const { chromium } = require('playwright'); const path = require('path'), fs = require('fs');
(async () => { const [f, sd] = process.argv.slice(2); fs.mkdirSync(sd, { recursive: true }); const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1300, height: 900 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 200))); await p.goto('file://' + path.resolve(f)); await p.waitForTimeout(1500); const R = {};
  for (const t of ['city', 'airport', 'island', 'port', 'al', 'lib', 'post']) { await p.click('#tabs button[data-t="' + t + '"]'); await p.waitForTimeout(600);
    // לגלול עד הסוף כדי שכל הכרטיסים יצוירו
    const n = await p.evaluate(async () => { const H = document.body.scrollHeight; for (let y = 0; y < H; y += 700) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 30)) } window.scrollTo(0, 0); await new Promise(r => setTimeout(r, 300));
      let fail = 0, all = 0, blank = 0; const msgs = {}; for (const c of document.querySelectorAll('canvas')) { all++; const g = c.getContext('2d'), d = g.getImageData(0, 0, Math.min(40, c.width), Math.min(20, c.height)).data; let s = 0; for (let i = 3; i < d.length; i += 4) s += d[i]; if (!s) blank++ }
      for (const c of document.querySelectorAll('canvas[data-f]')) { } return { all, blank, cards: document.querySelectorAll('.card').length, fail: (window.__FAIL||[]).length, ex: (window.__FAIL||[]).slice(0,5) } });
    const fails = await p.evaluate(() => { const o = []; const T = CanvasRenderingContext2D.prototype; return o });
    R[t] = n; await p.screenshot({ path: path.join(sd, t + '.png') }) }
  R.errs = errs; console.log(JSON.stringify(R)); await b.close() })().catch(e => { console.error(e); process.exit(2) });
