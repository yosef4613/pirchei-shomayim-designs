// timeline.js <game.html> <hash> <secs> [out.json] — ציר הזמן של הטעינה: צביעה ראשונה, משימות ארוכות, ומצב MAPBASE / WTC / C34 / השדה / TCO / TCLD כל 300 מ"ש
const { chromium } = require('playwright'); const path = require('path'), fs = require('fs');
(async () => {
  const [f, hash, secs, out] = process.argv.slice(2); const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300))); p.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text().slice(0, 200)) });
  await p.addInitScript(() => { window.__TL = { paint: [], lt: [] }; try { new PerformanceObserver(l => { for (const e of l.getEntries()) __TL.paint.push([e.name, Math.round(e.startTime)]) }).observe({ type: 'paint', buffered: true }) } catch (e) { }
    try { new PerformanceObserver(l => { for (const e of l.getEntries()) __TL.lt.push([Math.round(e.startTime), Math.round(e.duration)]) }).observe({ type: 'longtask', buffered: true }) } catch (e) { } });
  await p.goto('file://' + path.resolve(f) + (hash || ''), { waitUntil: 'commit' });
  const S = [], t0 = Date.now(), Q = `(()=>{const o={};try{o.mode=TCO.mode;o.ui=TCO.ui}catch(e){}try{o.mb=[MAPBASE.next,MAPBASE.total,MAPBASE.done?1:0]}catch(e){}try{o.wtc=[WTC.stats.built,WTC.tiles.size,WTC.stats.fallbackFrames]}catch(e){}
   try{o.c34=[C34G.armed?1:0,typeof C34!=='undefined'?C34.queued():-1]}catch(e){}try{o.apt=APT_OPS.ready?1:0}catch(e){}try{o.lds=G77_LDS.job?[G77_LDS.job.n,G77_LDS.job.total]:0}catch(e){}try{o.ld=window.TCLD?TCLD.state():null}catch(e){}return o})()`;
  while (Date.now() - t0 < +secs * 1000) {
    const s = await p.evaluate(q => { const r = { t: Math.round(performance.now()) }; try { if (window.__TC_DEV) Object.assign(r, window.__TC_DEV.ev(q)) } catch (e) { r.e = String(e).slice(0, 80) } r.ld0 = window.TCLD ? 1 : 0; r.root = (document.getElementById('tcoRoot') || {}).className; return r }, Q).catch(e => ({ err: String(e).slice(0, 100) }));
    S.push(s); await p.waitForTimeout(300) }
  const tl = await p.evaluate(() => window.__TL).catch(() => null);
  const R = { samples: S, tl, errs }; if (out) fs.writeFileSync(out, JSON.stringify(R)); 
  // a compact print: the changes only
  let prev = ''; for (const s of S) { const k = JSON.stringify(Object.assign({}, s, { t: 0 })); if (k !== prev) console.log(JSON.stringify(s)); prev = k }
  console.log('paint', JSON.stringify(tl && tl.paint)); console.log('longtasks>200', JSON.stringify(tl && tl.lt.filter(x => x[1] > 200)));
  console.log('errors', errs.length, errs.slice(0, 5).join(' | ')); await b.close();
})();
