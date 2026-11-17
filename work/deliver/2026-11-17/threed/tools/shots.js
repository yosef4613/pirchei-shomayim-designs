// צילומים לבדיקה פנימית בלבד (לא לדף): node shots.js <html> <outdir> <tag>
const { chromium } = require('playwright'); const path = require('path'), fs = require('fs');
(async () => {
  const [f, od, tag] = process.argv.slice(2); fs.mkdirSync(od, { recursive: true });
  const b = await chromium.launch({ args: ['--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] }); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 400))); p.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') errs.push(m.type() + ': ' + m.text().slice(0, 300)) });
  const reqs = []; p.on('request', r => { if (!/^(file|data|blob):/.test(r.url())) reqs.push(r.url()) });
  const t0 = Date.now(); await p.goto('file://' + path.resolve(f)); try { await p.waitForFunction('window.TD&&window.TD.ready', null, { timeout: 300000 }) } catch (e) { await p.screenshot({ path: path.join(od, tag + '_fail.png') }); console.log(JSON.stringify({ fail: String(e).slice(0, 200), errs, reqs })); await b.close(); process.exit(3) } const ready = Date.now() - t0;
  const res = { ready, errs, reqs, shots: [] };
  const views = [
    ['game_full', 'TD.teleport(65,42,-Math.PI/2);TD.zoom(6.2)'],
    ['game_car', 'TD.teleport(57.9,40,-Math.PI/2);TD.zoom(16)'],
    ['game_sig', 'TD.teleport(60,6,-Math.PI/2);TD.zoom(11)'],
    ['chase', 'TD.teleport(57.9,60,-Math.PI/2);TD.setMode("chase")'],
    ['free', 'TD.setMode("free")'],
    ['night', 'TD.setMode("game");TD.teleport(65,42,-Math.PI/2);TD.zoom(7);TD.setNight(true)'],
    ['low', 'TD.setNight(false);TD.setLow(true);TD.zoom(9)'],
  ];
  for (const [n, js] of views) { await p.evaluate(js); const f0 = await p.evaluate('TD.frames()'); await p.waitForFunction(x => TD.frames() > x + 3, f0, { timeout: 120000 }).catch(() => {}); await p.waitForTimeout(800); const o = path.join(od, tag + '_' + n + '.png'); await p.screenshot({ path: o }); res.shots.push(o) }
  // מדידה: 5 שניות במבט המשחק, איכות מלאה
  await p.evaluate('TD.setLow(false);TD.setMode("game");TD.zoom(9)');
  res.fps = await p.evaluate(() => new Promise(r => { let n = 0, t0 = performance.now(); (function f(t) { n++; if (t - t0 < 5000) requestAnimationFrame(f); else r(+(n * 1000 / (t - t0)).toFixed(1)) })(t0) }));
  res.stats = await p.evaluate('__TD()'); res.heapMB = await p.evaluate(() => Math.round(performance.memory.usedJSHeapSize / 1048576)); res.imgs = await p.evaluate('document.images.length');
  fs.writeFileSync(path.join(od, tag + '.json'), JSON.stringify(res, null, 1)); console.log(JSON.stringify(res)); await b.close();
})();
