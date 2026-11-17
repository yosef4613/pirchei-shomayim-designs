// zoom_shots.js — perf 17.11: צילומים לעצמי (לא לדף) בזמן זום החוצה ופנימה בגלגלת, כדי לראות מה זה ה"ירוק".
// node zoom_shots.js <build.html> <outdir> [w=1920] [h=953] [dpr=1]
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, outdir, W = '1920', H = '953', DPR = '1'] = process.argv.slice(2);
  fs.mkdirSync(outdir, { recursive: true });
  const b = await chromium.launch({ args: ['--js-flags=--expose-gc', '--enable-precise-memory-info'] });
  const p = await b.newPage({ viewport: { width: +W, height: +H }, deviceScaleFactor: +DPR });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
  p.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text().slice(0, 300)) });
  const t0 = Date.now();
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  console.log('ready after', Math.round((Date.now() - t0) / 1000), 's');
  await p.waitForTimeout(4000);
  const ev = s => p.evaluate(s => window.__TC_DEV.ev(s), s);
  const st = () => ev("JSON.stringify({z:+Camera.zoom.toFixed(3),x:Math.round(Camera.x),y:Math.round(Camera.y),tiles:WTC.tiles.size,fb:WTC.stats.fallbackTiles,mf:WTC.stats.mapFilled||0,sc:WTC.stats.scaledTiles||0,built:WTC.stats.built,ev:WTC.stats.evicted,mb:MAPBASE.done,err:WTC.err&&WTC.err.slice(0,200)})");
  console.log('start', await st());
  await p.mouse.move(+W / 2, +H / 2);
  await p.screenshot({ path: path.join(outdir, 's00_start.png') });
  // out: 12 wheel notches, quickly
  for (let i = 0; i < 12; i++) { await p.mouse.wheel(0, 100); await p.waitForTimeout(30) }
  for (let k = 1; k <= 8; k++) { await p.waitForTimeout(150); await p.screenshot({ path: path.join(outdir, 's1' + k + '_out.png') }); console.log('out', k, await st()) }
  for (let i = 0; i < 12; i++) { await p.mouse.wheel(0, -100); await p.waitForTimeout(30) }
  for (let k = 1; k <= 8; k++) { await p.waitForTimeout(150); await p.screenshot({ path: path.join(outdir, 's2' + k + '_in.png') }); console.log('in', k, await st()) }
  // jump: far camera move (F4 map mode)
  console.log(await ev("(()=>{if(!State.mapQa)toggleMapQa();Camera.zoom=.45;Camera.x=7600;Camera.y=5600;return 'f4'})()"));
  for (let k = 1; k <= 8; k++) { await p.waitForTimeout(150); await p.screenshot({ path: path.join(outdir, 's3' + k + '_jump.png') }); console.log('jump', k, await st()) }
  console.log('errors', errs.length, errs.slice(0, 6).join(' | '));
  await b.close();
})().catch(e => { console.error(String(e).slice(0, 600)); process.exit(1) });
