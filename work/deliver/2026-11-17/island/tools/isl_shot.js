// s13_shot.js — כלי של הסוכן "S13": שאילתות בתוך המשחק וצילומים לבדיקה בעין (לעצמי בלבד, לא לבעלים).
// node s13_shot.js <game.html> <outdir> [--q <query.js>]... [--wait <ms>] "<שם>:x,y,zoom[,n]" ...   (n=1 — לילה)
//   --q: קובץ עם ביטוי JS אחד או גוף שמתחיל ב-return; התוצאה נכתבת ל-<outdir>/<שם הקובץ>.json ומודפסת בקיצור.
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const a = process.argv.slice(2); const file = a.shift(), outdir = a.shift(); fs.mkdirSync(outdir, { recursive: true });
  const qs = [], specs = []; let wait = 2500, hide = true, vw = 1280, vh = 800;
  while (a.length) { const s = a.shift(); if (s === '--q') qs.push(a.shift()); else if (s === '--wait') wait = +a.shift(); else if (s === '--ui') hide = false; else if (s === '--vp') { const v = a.shift().split('x'); vw = +v[0]; vh = +v[1] } else specs.push(s) }
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] }); const p = await b.newPage({ viewport: { width: vw, height: vh }, deviceScaleFactor: 1 });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(wait);
  for (const qf of qs) { let src = fs.readFileSync(qf, 'utf8'); const body = src.replace(/^(\s*\/\/[^\n]*\n|\s*\/\*[\s\S]*?\*\/)*/, ''); if (/^\s*return\b/.test(body)) src = '(()=>{' + src + '\n})()';
    let r; try { r = await p.evaluate(s => Promise.resolve(window.__TC_DEV.ev(s)).then(v => typeof v === 'string' ? v : JSON.stringify(v)), src) } catch (e) { r = JSON.stringify({ error: String(e).slice(0, 800) }) }
    fs.writeFileSync(path.join(outdir, path.basename(qf).replace(/\.js$/, '') + '.json'), r || 'null'); console.log(path.basename(qf) + ': ' + String(r).slice(0, +(process.env.QMAX || 3000))) }
  if (specs.length) {
    await p.evaluate(() => window.__TC_DEV.ev(`(()=>{State.mapQa=true;try{G77_ASV.on=false}catch(e){}return 1})()`));
    if (hide) await p.evaluate(() => { const cv = [...document.querySelectorAll('canvas')].sort((a, b) => b.width * b.height - a.width * a.height)[0]; const keep = new Set(); for (let e = cv; e; e = e.parentElement) keep.add(e);
      for (const e of document.body.querySelectorAll('*')) if (!keep.has(e) && !e.contains(cv)) e.style.visibility = 'hidden'; cv.style.visibility = 'visible' });
    for (const s of specs) { const [nm, v] = s.split(':'); const [x, y, z, n] = v.split(',').map(Number);
      await p.evaluate(([x, y, z, n]) => window.__TC_DEV.ev(`(()=>{c34Night(${n ? 1 : 0});try{wtcInvalidate()}catch(e){}State.mapQa=true;Camera.x=${x};Camera.y=${y};Camera.zoom=${z};return 1})()`), [x, y, z, n || 0]);
      await p.waitForTimeout(+(process.env.SHOT_WAIT||1800)); await p.screenshot({ path: path.join(outdir, nm + '.jpg'), type: 'jpeg', quality: 82 }) } }
  console.log('צילומים', specs.length, '· שגיאות דף', errs.length, errs.slice(0, 4).join(' | '));
  await b.close();
})().catch(e => { console.error(String(e).slice(0, 500)); process.exit(1) });
