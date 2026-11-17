// zoomcycle.js — perf 17.11: "הכול נעלם ונשאר ירוק בזומים" — שחזור ומדידה בדפדפן אחד (כדי לחסוך בתור bslot).
// node zoomcycle.js <build.html> <out.json> [shotsDir|-] [cycles=20] [W=1920] [H=953] [DPR=1] [narrow=1]
// מה נמדד (בכל פריים, מתוך המשחק — ‎#dev‎, ‏__TC_DEV.ev):
//   dt, הזום, ואריחים: fb = מצוירים חי בפריים (אין אריח ואין כיסוי), mf = מכוסים מהמפה האפויה (MAPBASE), sc = מכוסים מהזום הקודם,
//   fc = מכוסים מהרמה המלאה האחרונה, b = נבנו; ‏gr = חלק הפיקסלים ה"ירוקים" במסך (דגימה 160×80), ‏gy = חלק האפורים (כבישים / גגות).
//   עצים עם וריאציה מחוץ לטווח (TP[0][S.v]) — עם המחסנית. שגיאות דף וקונסול.
//   הזיכרון (אחרי gc) והקנבסים — לפני, באמצע ובסוף הסבבים.
// הסבב: גלגלת החוצה 8 חריצים (עד 0.55), 1.6 שנ׳, גלגלת פנימה 8 חריצים, 1.6 שנ׳. אחרי הסבבים — F4 וקפיצות מצלמה בזום 0.45.
// בסוף (narrow=1) — דף שני במסך צר 412×860 (השגיאה "world tile fallback … is not iterable at tree").
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
const MON = `(()=>{if(window.__PM)return 'again';const M=window.__PM={rows:[],on:true,last:performance.now(),treeBad:[],errs:{},px:true,ph:''};
 const s0=()=>({fb:WTC.stats.fallbackTiles,mf:WTC.stats.mapFilled||0,sc:WTC.stats.scaledTiles||0,b:WTC.stats.built,fc:G77_ZP.stats.fullCover||0});
 const pc=document.createElement('canvas');pc.width=160;pc.height=80;const pg=pc.getContext('2d',{willReadFrequently:true});
 M.pix=()=>{pg.drawImage(cv,0,0,160,80);const d=pg.getImageData(0,0,160,80).data;let g=0,y=0;for(let i=0;i<d.length;i+=4){const r=d[i],G=d[i+1],b=d[i+2];if(G>r+14&&G>b+14)g++;else if(Math.abs(r-G)<14&&Math.abs(G-b)<16&&r>55&&r<215)y++}const n=d.length/4;return[+(g/n).toFixed(3),+(y/n).toFixed(3)]};
 let p=s0();
 const mc0=wtcMapCover;let mf=-1;const mset=new Set(),cnt={l1:0,l1h:0,t:0,p:0};M.cnt=cnt;
 wtcMapCover=function(q,G){const L=q[0];if(L==='L1'){cnt.l1++;if(!(mf===WTC.frame&&mset.has(G.key+'|'+q[1]+'|'+q[2])))cnt.l1h++}else if(L==='T')cnt.t++;else if(L==='P'||L==='O'||L[0]==='X')cnt.p++;
  const r=mc0.apply(this,arguments);if(r&&(L==='M'||L==='L0')){if(mf!==WTC.frame){mf=WTC.frame;mset.clear()}mset.add(G.key+'|'+q[1]+'|'+q[2])}return r};
 const z0=()=>{const Z=window.__TC_PERF17;return[cnt.l1h,cnt.t,cnt.p,Z?Z.n.l1Cover:0,Z?Z.n.staleDrawn:0,WTC.stats.dirtyDropped||0,WTC.epoch]};let pz=z0();
 const tick=()=>{if(!M.on)return;const n=performance.now(),c=s0();let q=[-1,-1];if(M.px){try{q=M.pix()}catch(e){}}
  if(WTC.err){const k=String(WTC.err).slice(0,260);M.errs[k]=(M.errs[k]||0)+1;WTC.err=null}
  const cz=z0();M.rows.push([Math.round(n),+(n-M.last).toFixed(1),+Camera.zoom.toFixed(3),c.fb-p.fb,c.mf-p.mf,c.sc-p.sc,c.b-p.b,c.fc-p.fc,WTC.tiles.size,MAPBASE.done?1:0,q[0],q[1],M.ph,cz[0]-pz[0],cz[1]-pz[1],cz[2]-pz[2],cz[3]-pz[3],cz[4]-pz[4],cz[5]-pz[5],cz[6]-pz[6]]);p=c;pz=cz;M.last=n;requestAnimationFrame(tick)};requestAnimationFrame(tick);
 let wr=0;for(const a of (TurboCity.assets||[])){if(!a||typeof a.id!=='string'||!a.id.startsWith('TP-')||a.__pm)continue;const d0=a.draw;a.__pm=1;wr++;a.draw=function(c,S,t){try{const v=S&&S.v;if(!(v>=0&&v<=3)&&M.treeBad.length<12)M.treeBad.push({id:a.id,v,stack:String(new Error().stack).split('\\n').slice(2,11).map(s=>s.trim().replace(/\\(?file:.*?\\.html:/,'@')).join(' | ')})}catch(e){}return d0.apply(this,arguments)}}M.wrapped=wr;
 return 'ok'})()`;
const MEM = `(()=>{try{window.gc&&window.gc();window.gc&&window.gc()}catch(e){}const cm=window.__TC_CANVAS_MEM?window.__TC_CANVAS_MEM('by'):null;
 return {heapMB:performance.memory?+(performance.memory.usedJSHeapSize/1048576).toFixed(1):null,canvasMB:cm&&cm.mb,canvases:cm&&cm.live,cby:cm&&cm.by,tiles:WTC.tiles.size,pool:WTC.pool.length,wtcMem:wtcMem(),mapbase:{done:MAPBASE.done,total:MAPBASE.total,next:MAPBASE.next,builds:MAPBASE.builds,err:MAPBASE.lastError},wtcErr:WTC.err&&WTC.err.slice(0,400),evicted:WTC.stats.evicted,built:WTC.stats.built}})()`;
async function openGame(b, file, W, H, DPR, errs) {
  const p = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: DPR });
  p.on('pageerror', e => errs.push('page: ' + String(e).slice(0, 400)));
  p.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text().slice(0, 400)) });
  const t0 = Date.now();
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 900000, polling: 500 });
  return { p, readyS: Math.round((Date.now() - t0) / 1000) };
}
(async () => {
  const a = process.argv.slice(2);
  const [file, out] = a; const shots = a[2] && a[2] !== '-' ? a[2] : null; const cycles = +(a[3] || 20), W = +(a[4] || 1920), H = +(a[5] || 953), DPR = +(a[6] || 1), narrow = (a[7] || '1') === '1';
  if (shots) fs.mkdirSync(shots, { recursive: true });
  const R = { build: path.basename(file), W, H, DPR, cycles, t: new Date().toISOString() };
  const b = await chromium.launch({ args: ['--js-flags=--expose-gc', '--enable-precise-memory-info'] });
  const errs = []; R.errs = errs;
  const { p, readyS } = await openGame(b, file, W, H, DPR, errs); R.readyS = readyS;
  const ev = s => p.evaluate(s => window.__TC_DEV.ev(s), s);
  const ph = s => ev("window.__PM&&(window.__PM.ph=" + JSON.stringify(s) + ")");
  const shot = async n => { if (shots) { try { await p.screenshot({ path: path.join(shots, n + '.png') }) } catch (e) { } } };
  await p.waitForTimeout(3000);
  R.start = await ev("({cam:[Math.round(Camera.x),Math.round(Camera.y),+Camera.zoom.toFixed(3)],dpr,mapbase:{done:MAPBASE.done,total:MAPBASE.total},wtc:{maxTiles:WTC.maxTiles,T:WTC.T,tiles:WTC.tiles.size,lodZoom:WTC.lodZoom,mapFill:WTC.mapFill},zp:G77_ZP.on,zq:WTC_ZQ.on,glg:GLG.active})");
  // extra in-game queries before the zoom cycles (env QX = comma separated files, the probe_c2 format: an expression or a body that starts with return)
  R.qx = {};
  for (const f of String(process.env.QX || '').split(',').filter(Boolean)) {
    let src = fs.readFileSync(f, 'utf8'); const body = src.replace(/^(\s*\/\/[^\n]*\n|\s*\/\*[\s\S]*?\*\/)*/, ''); if (/^\s*return\b/.test(body)) src = '(()=>{' + src + '\n})()';
    try { R.qx[path.basename(f)] = await p.evaluate(s => Promise.resolve(window.__TC_DEV.ev(s)).then(v => v), src) } catch (e) { R.qx[path.basename(f)] = { err: String(e).slice(0, 400) } }
  }
  await p.waitForTimeout(1500);
  R.mon = await ev(MON);
  R.mem0 = await ev(MEM);
  await p.mouse.move(W / 2, H / 2);
  await shot('c00_start');
  const wheel = async (dir, n) => { for (let i = 0; i < n; i++) { await p.mouse.wheel(0, dir * 100); await p.waitForTimeout(40) } };
  R.memAt = {};
  for (let k = 1; k <= cycles; k++) {
    await ph('out' + k); await wheel(1, 8);
    if (k === 1 || k === cycles) { await p.waitForTimeout(60); await shot('c' + k + '_out_0'); }
    await p.waitForTimeout(1600); if (k === 1 || k === cycles) await shot('c' + k + '_out_1');
    await ph('in' + k); await wheel(-1, 8);
    if (k === 1 || k === cycles) { await p.waitForTimeout(60); await shot('c' + k + '_in_0'); }
    await p.waitForTimeout(1600); if (k === 1 || k === cycles) await shot('c' + k + '_in_1');
    if (k === Math.ceil(cycles / 2) || k === cycles) R.memAt[k] = await ev(MEM);
  }
  // F4 and jumps (the minimap click / far camera moves) at the far zoom
  await ph('f4');
  R.f4 = await ev("(()=>{if(!State.mapQa)toggleMapQa();Camera.zoom=.45;return [Math.round(Camera.x),Math.round(Camera.y)]})()");
  await p.waitForTimeout(2500);
  const J = [[7600, 5600], [1200, 600], [5200, 2100], [8800, 3000], [3000, 4700], [600, 6400], [6600, 800], [1800, 4500], [4200, 3000]];
  for (let i = 0; i < J.length; i++) {
    await ph('jump' + i); await ev(`(()=>{Camera.x=${J[i][0]};Camera.y=${J[i][1]};return 1})()`);
    await p.waitForTimeout(80); if (i < 3) await shot('j' + i + '_0'); await p.waitForTimeout(1800); if (i < 3) await shot('j' + i + '_1');
  }
  await ph('f4in'); await ev("(()=>{Camera.zoom=1.15;return 1})()"); await p.waitForTimeout(80); await shot('j_in_0'); await p.waitForTimeout(1800); await shot('j_in_1');
  await ph('end');
  R.memEnd = await ev(MEM);
  R.treeBad = await ev("window.__PM.treeBad"); R.tpv = await ev("(window.__TC_PERFX&&window.__TC_PERFX.tpv)||null"); R.wrapped = await ev("window.__PM.wrapped"); R.wtcErrs = await ev("window.__PM.errs");
  R.rows = await ev("(()=>{window.__PM.on=false;return window.__PM.rows})()");
  R.cols = ['t', 'dt', 'zoom', 'fb', 'mf', 'sc', 'b', 'fc', 'tiles', 'mbDone', 'green', 'gray', 'phase', 'l1hole', 'tHole', 'pHole', 'l1Cover', 'staleDrawn', 'dirtyDropped', 'epoch'];
  R.perf17 = await ev("window.__TC_PERF17?{n:window.__TC_PERF17.n,err:window.__TC_PERF17.err,map:window.__TC_PERF17.map.size}:null");
  R.zpStats = await ev("({...G77_ZP.stats,stepMs:G77_ZP.stepMs})");
  R.wtcStats = await ev("({...WTC.stats})");
  await p.close();
  if (narrow) {
    const e2 = []; R.narrowErrs = e2;
    const { p: q, readyS: r2 } = await openGame(b, file, 412, 860, 1, e2); R.narrowReadyS = r2;
    const ev2 = s => q.evaluate(s => window.__TC_DEV.ev(s), s);
    await q.waitForTimeout(2500);
    R.narrowMon = await ev2(MON);
    R.narrowStart = await ev2("({cam:[Math.round(Camera.x),Math.round(Camera.y),+Camera.zoom.toFixed(3)],wtcErr:WTC.err&&WTC.err.slice(0,600)})");
    await q.mouse.move(206, 430);
    for (let k = 0; k < 3; k++) { for (let i = 0; i < 8; i++) { await q.mouse.wheel(0, 100); await q.waitForTimeout(40) } await q.waitForTimeout(1500); for (let i = 0; i < 8; i++) { await q.mouse.wheel(0, -100); await q.waitForTimeout(40) } await q.waitForTimeout(1500) }
    R.narrowEnd = await ev2("({cam:[Math.round(Camera.x),Math.round(Camera.y),+Camera.zoom.toFixed(3)],wtcErr:WTC.err&&WTC.err.slice(0,900),errs:window.__PM.errs,treeBad:window.__PM.treeBad})");
    await q.close();
  }
  await b.close();
  fs.writeFileSync(out, JSON.stringify(R));
  // summary
  const rows = R.rows || [], by = {};
  for (const r of rows) { const k = String(r[12]).replace(/\d+$/, ''); const o = by[k] || (by[k] = { n: 0, fb: 0, mf: 0, sc: 0, fc: 0, b: 0, maxDt: 0, over50: 0, over100: 0, gMax: 0, fbFrames: 0, mfFrames: 0 }); o.n++; o.fb += r[3]; o.mf += r[4]; o.sc += r[5]; o.fc += r[7]; o.b += r[6]; if (r[1] > o.maxDt) o.maxDt = r[1]; if (r[1] > 50) o.over50++; if (r[1] > 100) o.over100++; if (r[10] > o.gMax) o.gMax = r[10]; if (r[3]) o.fbFrames++; if (r[4]) o.mfFrames++ }
  console.log(JSON.stringify({ qx: R.qx, readyS: R.readyS, start: R.start, mem0: R.mem0 && { heap: R.mem0.heapMB, canvas: R.mem0.canvasMB, tiles: R.mem0.tiles }, memAt: Object.fromEntries(Object.entries(R.memAt).map(([k, v]) => [k, { heap: v.heapMB, canvas: v.canvasMB, tiles: v.tiles, pool: v.pool }])), memEnd: R.memEnd && { heap: R.memEnd.heapMB, canvas: R.memEnd.canvasMB, err: R.memEnd.wtcErr }, by, treeBad: (R.treeBad || []).slice(0, 3), wtcErrs: R.wtcErrs, narrow: R.narrowEnd, errs: errs.slice(0, 8), narrowErrs: (R.narrowErrs || []).slice(0, 5) }, null, 1));
})().catch(e => { console.error(String(e && e.stack || e).slice(0, 900)); process.exit(1) });
