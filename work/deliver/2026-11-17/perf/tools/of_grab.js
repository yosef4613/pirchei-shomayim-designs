// of_grab.js — perf 17.11 (המתאם 16:20): סרטון הפתיחה מהאריח במסך הפתיחה תוקע את התהליכון הראשי 13–28 שנ׳ (leftovers: q_of_tile / q_of_diag).
// node of_grab.js <out.json> <a.html> [b.html …]   — דרך התור. לכל בנייה: ‎#dev → __TCO.open (מסך הפתיחה, כמו q_of_tile) → עד שהאריח מופיע;
// (א) כל מצלמה חיה של הסרטון (TCOF.film().cams — 7): TCCITY.grab קר, עם פרופיל CPU (CDP, כל 200 מיקרו-שנ׳) — הזמן, ומה בתוכו (עצמי / כולל, לפי הפונקציה והשורה);
// (ב) אותן מצלמות שוב (חם); (ג) אם MODE=play: לחיצה על האריח (בתוך הדף), ומדידה של הסרטון: מתי הפריים הראשון, ‏ST.dts / ‏ST.dms (הזמן בין פריימים / הציור), משימות ארוכות, ‏TCCITY.grab בכל פריים.
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
const MODE = process.env.MODE || 'grab';
function top(prof, n) {
  const byId = new Map(prof.nodes.map(x => [x.id, x])); const self = new Map(); const dt = prof.timeDeltas; let tot = 0;
  const parent = new Map(); for (const x of prof.nodes) for (const c of (x.children || [])) parent.set(c, x.id);
  for (let i = 0; i < prof.samples.length; i++) { const d = (dt[i + 1] !== undefined ? dt[i + 1] : 0) / 1000; const nd = byId.get(prof.samples[i]); if (/^\((idle|program|root)\)$/.test(nd.callFrame.functionName)) continue; tot += d; self.set(prof.samples[i], (self.get(prof.samples[i]) || 0) + d) }
  const fk = x => (x.callFrame.functionName || '(anon)') + ':' + (x.callFrame.lineNumber + 1);
  const S = {}, I = {}; for (const [id, ms] of self) { const k = fk(byId.get(id)); S[k] = (S[k] || 0) + ms; const seen = new Set(); let p = id; while (p !== undefined) { const kk = fk(byId.get(p)); if (!seen.has(kk)) { seen.add(kk); I[kk] = (I[kk] || 0) + ms } p = parent.get(p) } }
  const r = o => Object.entries(o).sort((a, b) => b[1] - a[1]).slice(0, n).map(([k, v]) => [k, +v.toFixed(1)]);
  return { busyMs: +tot.toFixed(1), self: r(S), incl: r(I) };
}
(async () => {
  const [out, ...files] = process.argv.slice(2); const all = [];
  for (const file of files) {
    const R = { build: path.basename(file), mode: MODE }; const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
    try {
      const p = await b.newPage({ viewport: { width: 1280, height: 800 } }); const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 200)));
      await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' }); await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 }); await p.waitForTimeout(1500);
      const ev = s => p.evaluate(x => Promise.resolve(window.__TC_DEV.ev(x)).then(v => typeof v === 'string' ? v : JSON.stringify(v)), s);
      R.open = JSON.parse(await ev(`(async()=>{const W=ms=>new Promise(r=>setTimeout(r,ms));__TCO.open('perf');let t=0;while(t<20000&&!document.querySelector('#tcoRoot [data-act="tcofHome"]')){await W(250);t+=250}
        return JSON.stringify({tile:!!document.querySelector('#tcoRoot [data-act="tcofHome"]'),ms:t,mode:TCO.mode,cams:TCOF.film().cams.length,grabSt:Object.assign({},TCCITY.st),warmQ:!!(TCSHOW.ST)})})()`));
      const cdp = await p.context().newCDPSession(p); await cdp.send('Profiler.enable'); await cdp.send('Profiler.setSamplingInterval', { interval: 200 });
      if (MODE === 'grab') {
        R.cold = []; R.warm = [];
        const n = JSON.parse(await ev('JSON.stringify(TCOF.film().cams.length)'));
        for (let i = 0; i < n; i++) { await cdp.send('Profiler.start'); const ms = +(await ev(`(()=>{const c=TCOF.film().cams[${i}];const t=performance.now();TCCITY.grab(c);return String(+(performance.now()-t).toFixed(1))})()`)); const { profile } = await cdp.send('Profiler.stop');
          R.cold.push({ i, ms, prof: top(profile, 14) }); await p.waitForTimeout(400) }
        for (let i = 0; i < n; i++) { const ms = +(await ev(`(()=>{const c=TCOF.film().cams[${i}];const t=performance.now();TCCITY.grab(c);return String(+(performance.now()-t).toFixed(1))})()`)); R.warm.push({ i, ms }); await p.waitForTimeout(150) }
      } else {
        await ev(`(()=>{const M=window.__OFM={lt:[],grabs:[],t0:0,first:0,gaps:[]};try{new PerformanceObserver(l=>{for(const e of l.getEntries())M.lt.push([Math.round(e.startTime),Math.round(e.duration)])}).observe({entryTypes:['longtask']})}catch(e){}
          const g0=TCCITY.grab;TCCITY.grab=function(c){const t=performance.now();try{return g0.apply(this,arguments)}finally{M.grabs.push([Math.round(t),+(performance.now()-t).toFixed(1),c&&Math.round(c.x)+','+Math.round(c.y)])}};
          let last=performance.now();M.iv=setInterval(()=>{const n=performance.now();if(n-last>120)M.gaps.push([Math.round(last),Math.round(n-last)]);last=n},20);return 'ok'})()`);
        await cdp.send('Profiler.start');
        R.click = JSON.parse(await ev(`(async()=>{const W=ms=>new Promise(r=>setTimeout(r,ms)),M=window.__OFM;const b=document.querySelector('#tcoRoot [data-act="tcofHome"]');M.t0=performance.now();setTimeout(()=>b.click(),0);
          let t=0;while(t<60000&&!(TCSHOW.on&&TCSHOW.stats().frames>0)){await W(20);t+=20}M.first=performance.now()-M.t0;await W(12000);const s=TCSHOW.stats();const ST=TCSHOW.ST||{};
          const dts=(ST.dts||[]).slice(),dms=(ST.dms||[]).slice();clearInterval(M.iv);
          return JSON.stringify({firstFrameMs:Math.round(M.first),on:!!TCSHOW.on,t:TCSHOW.on&&+TCSHOW.on.t.toFixed(2),stats:s,dtMax:Math.round(Math.max(0,...dts)),dtOver100:dts.filter(x=>x>100).length,dmsMax:Math.round(Math.max(0,...dms)),frames:dts.length,
            gaps:M.gaps.filter(g=>g[0]>=M.t0-50).map(g=>[g[0]-Math.round(M.t0),g[1]]).slice(0,30),lt:M.lt.filter(x=>x[0]>=M.t0-50).map(x=>[x[0]-Math.round(M.t0),x[1]]).slice(0,30),grabs:M.grabs.map(g=>[g[0]-Math.round(M.t0),g[1],g[2]]).slice(0,60),grabSt:Object.assign({},TCCITY.st)})})()`));
        const { profile } = await cdp.send('Profiler.stop'); R.prof = top(profile, 20);
        await ev(`(()=>{try{window.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',code:'Escape',bubbles:true}))}catch(e){}return 1})()`);
      }
      R.errs = errs.slice(0, 5);
    } catch (e) { R.err = String(e && e.stack || e).slice(0, 400) } finally { await b.close() }
    all.push(R); fs.writeFileSync(out, JSON.stringify(all, null, 1));
    console.log(JSON.stringify(MODE === 'grab' ? { build: R.build, err: R.err, open: R.open, cold: (R.cold || []).map(c => [c.ms, c.prof.self.slice(0, 4), c.prof.incl.slice(0, 6)]), warm: (R.warm || []).map(c => c.ms) } : { build: R.build, err: R.err, click: R.click && Object.assign({}, R.click, { grabs: (R.click.grabs || []).slice(0, 25) }), prof: R.prof && { busy: R.prof.busyMs, self: R.prof.self.slice(0, 8), incl: R.prof.incl.slice(0, 12) } }, null, 1));
  }
})().catch(e => { console.error(String(e && e.stack || e).slice(0, 500)); process.exit(1) });
