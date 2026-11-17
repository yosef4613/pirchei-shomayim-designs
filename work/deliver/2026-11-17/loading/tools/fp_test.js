// fp_test.js <game.html> <out.json> — "נטען מיד": מתי מסך הטעינה נצבע לראשונה מול הסקריפט הגדול (בלוק 12), בלי האטה ועם האטה פי 4 של המעבד.
// מודד: הזמן שבו ‎#tcldRoot נכנס לדף, ה-first-paint / first-contentful-paint, המשימות הארוכות (longtask — הגדולה היא בלוק 12), ה-rAF הראשון, ומתי TCLD.hooked.
const { chromium } = require('playwright'); const path = require('path'), fs = require('fs');
(async () => {
  const [f, out] = process.argv.slice(2); const b = await chromium.launch(); const R = { runs: [] };
  for (const rate of [1, 4]) {
    const ctx = await b.newContext({ viewport: { width: 1280, height: 800 } }); const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 200)));
    const cdp = await ctx.newCDPSession(p); if (rate > 1) await cdp.send('Emulation.setCPUThrottlingRate', { rate });
    await p.addInitScript(() => {
      const L = window.__FP = { paint: [], lt: [], scripts: [], tcld: null, raf: null, hooked: null, shot: null };
      try { new PerformanceObserver(l => { for (const e of l.getEntries()) L.paint.push([e.name, Math.round(e.startTime)]) }).observe({ type: 'paint', buffered: true }) } catch (e) { }
      try { new PerformanceObserver(l => { for (const e of l.getEntries()) L.lt.push([Math.round(e.startTime), Math.round(e.duration)]) }).observe({ type: 'longtask', buffered: true }) } catch (e) { }
      new MutationObserver(ms => { for (const m of ms) for (const n of m.addedNodes) { if (n.nodeName === 'SCRIPT') L.scripts.push([L.scripts.length + 1, Math.round(performance.now()), (n.textContent || '').length]); if (n.id === 'tcldRoot' && !L.tcld) L.tcld = Math.round(performance.now()) } }).observe(document, { childList: true, subtree: true });
      requestAnimationFrame(() => { L.raf = Math.round(performance.now()) });
      const iv = setInterval(() => { if (window.TCLD && TCLD.hooked) { L.hooked = Math.round(performance.now()); clearInterval(iv) } }, 50);
    });
    const t0 = Date.now(); await p.goto('file://' + path.resolve(f), { waitUntil: 'commit' });
    // the picture at the first chance the page lets us (it waits for the main thread — so it shows what is on the screen while block 12 is running only if the browser painted before it)
    let shotAt = null; try { await p.waitForSelector('#tcldRoot.on', { timeout: 120000 }); await p.screenshot({ path: out.replace(/\.json$/, '_x' + rate + '.png'), timeout: 120000 }); shotAt = Date.now() - t0 } catch (e) { }
    await p.waitForFunction(() => window.__FP && __FP.hooked, null, { timeout: 240000 }).catch(() => { });
    const L = await p.evaluate(() => Object.assign({}, window.__FP, { nav: Math.round(performance.timing.responseEnd - performance.timing.navigationStart), tcldState: window.TCLD ? { first: TCLD.st.paint0, view: TCLD.state().view } : null }));
    const big = L.lt.slice().sort((a, b2) => b2[1] - a[1])[0] || null, fcp = (L.paint.find(x => x[0] === 'first-contentful-paint') || [])[1];
    const run = { rate, tcldIn: L.tcld, fcp, paint: L.paint, raf: L.raf, hooked: L.hooked, bigTask: big, paintedBeforeBig: !!(big && fcp != null && fcp <= big[0]), scripts: L.scripts.slice(0, 14), shotAt, errs };
    R.runs.push(run); console.log(JSON.stringify(run)); await ctx.close();
  }
  fs.writeFileSync(out, JSON.stringify(R, null, 1)); await b.close();
})().catch(e => { console.log('CRASH', e); process.exit(2) });
