// מדידת דף תלת־ממד בכרומיום (בלי מסך — WebGL בתוכנה, SwiftShader: קרוב ל"מחשב חלש מאוד").
// node measure.js <url> <out.png> <out.json> [waitExpr] [w] [h]
const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const [url, png, js, waitExpr, w, h] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: +w || 1280, height: +h || 800 } });
  const errs = [], reqs = [];
  p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
  p.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text().slice(0, 300)) });
  p.on('request', r => { const u = r.url(); if (!u.startsWith('file:') && !u.startsWith('data:') && !u.startsWith('blob:') && !u.startsWith('http://127.0.0.1')) reqs.push(u.slice(0, 120)) });
  const t0 = Date.now();
  await p.goto(url, { waitUntil: 'load', timeout: 180000 });
  const tLoad = Date.now() - t0;
  let tReady = null;
  try { await p.waitForFunction(waitExpr || 'true', null, { timeout: 180000, polling: 200 }); tReady = Date.now() - t0 } catch (e) { errs.push('ready timeout') }
  await p.waitForTimeout(2500);
  const fps = await p.evaluate(() => new Promise(res => { let n = 0, t0 = performance.now(), worst = 0, last = t0; function f(t) { n++; worst = Math.max(worst, t - last); last = t; if (t - t0 < 5000) requestAnimationFrame(f); else res({ fps: +(n * 1000 / (t - t0)).toFixed(1), worstMs: +worst.toFixed(0) }) } requestAnimationFrame(f) }));
  const mem = await p.evaluate(() => performance.memory ? Math.round(performance.memory.usedJSHeapSize / 1048576) : null);
  const gl = await p.evaluate(() => { const c = document.createElement('canvas').getContext('webgl2'); if (!c) return null; const d = c.getExtension('WEBGL_debug_renderer_info'); return d ? c.getParameter(d.UNMASKED_RENDERER_WEBGL) : c.getParameter(c.RENDERER) });
  const extra = await p.evaluate(() => window.__TD ? window.__TD() : null).catch(() => null);
  await p.screenshot({ path: png });
  const out = { url: url.slice(0, 160), tLoad, tReady, fps, heapMB: mem, gl, imgs: await p.evaluate(() => document.images.length), errs, reqs, extra };
  fs.writeFileSync(js, JSON.stringify(out, null, 1)); console.log(JSON.stringify(out));
  await b.close();
})();
