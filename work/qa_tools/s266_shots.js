// s266_shots.js — צילומים לבדיקה בעין של הבונה בלבד (D‑477; לא לבעלים): המשחק עצוב, רק העולם, deviceScaleFactor 1.
// node s266_shots.js <game.html> <outdir> "<שם>:x,y,zoom[,n]" ...   (n=1 — לילה; בלי n — יום)
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, outdir, ...specs] = process.argv.slice(2); fs.mkdirSync(outdir, { recursive: true });
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 800 }, deviceScaleFactor: 1 });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 200)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(2500);
  await p.evaluate(() => window.__TC_DEV.ev(`(()=>{State.mapQa=true;try{G77_ASV.on=false}catch(e){}return 1})()`));
  await p.evaluate(() => { const cv = [...document.querySelectorAll('canvas')].sort((a, b) => b.width * b.height - a.width * a.height)[0]; const keep = new Set(); for (let e = cv; e; e = e.parentElement) keep.add(e);
    for (const e of document.body.querySelectorAll('*')) if (!keep.has(e) && !e.contains(cv)) e.style.visibility = 'hidden'; cv.style.visibility = 'visible' });
  for (const s of specs) {
    const [nm, v] = s.split(':'); const [x, y, z, n] = v.split(',').map(Number);
    await p.evaluate(([x, y, z, n]) => window.__TC_DEV.ev(`(()=>{c34Night(${n ? 1 : 0});try{wtcInvalidate()}catch(e){}State.mapQa=true;Camera.x=${x};Camera.y=${y};Camera.zoom=${z};return 1})()`), [x, y, z, n || 0]);
    await p.waitForTimeout(1600);
    await p.screenshot({ path: path.join(outdir, nm + '.jpg'), type: 'jpeg', quality: 84 });
  }
  console.log('shots', specs.length, '· שגיאות דף', errs.length, errs.slice(0, 3).join(' | '));
  await b.close();
})().catch(e => { console.error(e); process.exit(1) });
