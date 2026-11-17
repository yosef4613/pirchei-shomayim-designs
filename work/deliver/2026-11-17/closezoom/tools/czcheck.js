// czcheck.js <build.html> <out.json> [shotsDir|-] [cycles=10] [W=1920] [H=953] [DPR=1]
// closezoom 17.11 — בדפדפן אחד: (1) השחקן ברגל ליד שתי דמויות סיפור (tcStepFig); (2) בכל זום — 1.15 / 5.5 / 11 / 16 — הליכה 4 שנ׳: dt של פריימים
// (חציון, p95, מקסימום, מעל 50 / 100 מ"ש), הזיכרון אחרי gc (ערימה + קנבסים), P34G / P34 / TCCZ; (3) זום הלוך וחזור 5.5 ↔ 16 בגלגלת × cycles —
// "קפיצות ירוק" בשיטה של perf (zc_sum: חלק ירוק במסך מעל היציב +0.12 והאפור יורד); (4) עלייה לרכב בזום 16 — חזרה ל-5.5 בלי קפיצה; (5) __TC_CZ.qa();
// שגיאות דף / קונסול. צילומים — לבדיקה עצמית בלבד.
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
const MEM = `(()=>{try{window.gc&&window.gc();window.gc&&window.gc()}catch(e){}const cm=window.__TC_CANVAS_MEM?window.__TC_CANVAS_MEM('by'):null;
 return {heapMB:performance.memory?+(performance.memory.usedJSHeapSize/1048576).toFixed(1):null,canvasMB:cm&&cm.mb,canvases:cm&&cm.live,tiles:WTC.tiles.size,p34g:+(P34G.bytes/1048576).toFixed(1),p34:window.P34?P34.stats():null,sbcMB:+(SBC.bytes/1048576).toFixed(1),c34MB:(window.C34&&C34.stats)?C34.stats().MB:null,by:cm&&cm.by?cm.by:null,wtc:(typeof wtcMem==='function')?wtcMem():null}})()`;
const MON = `(()=>{const M=window.__CZM={rows:[],on:true,last:performance.now(),ph:'',rt:0};const r0=render;render=function(){const t=performance.now();try{return r0.apply(this,arguments)}finally{M.rt=performance.now()-t}};const pc=document.createElement('canvas');pc.width=160;pc.height=80;const pg=pc.getContext('2d',{willReadFrequently:true});
 const pix=()=>{pg.drawImage(cv,0,0,160,80);const d=pg.getImageData(0,0,160,80).data;let g=0,y=0;for(let i=0;i<d.length;i+=4){const r=d[i],G=d[i+1],b=d[i+2];if(G>r+14&&G>b+14)g++;else if(Math.abs(r-G)<14&&Math.abs(G-b)<16&&r>55&&r<215)y++}const n=d.length/4;return[+(g/n).toFixed(3),+(y/n).toFixed(3)]};
 let fb=WTC.stats.fallbackTiles;const tick=()=>{if(!M.on)return;const n=performance.now();let q=[-1,-1];try{q=pix()}catch(e){}const f=WTC.stats.fallbackTiles;M.rows.push([Math.round(n),+(n-M.last).toFixed(1),+Camera.zoom.toFixed(3),f-fb,q[0],q[1],M.ph,PlayerProfile.mode,+M.rt.toFixed(2)]);fb=f;M.last=n;requestAnimationFrame(tick)};requestAnimationFrame(tick);return 'ok'})()`;
(async () => {
  const a = process.argv.slice(2); const [file, out] = a; const shots = a[2] && a[2] !== '-' ? a[2] : null; const cycles = +(a[3] || 10), W = +(a[4] || 1920), H = +(a[5] || 953), DPR = +(a[6] || 1);
  if (shots) fs.mkdirSync(shots, { recursive: true });
  const R = { build: path.basename(file), W, H, DPR, t: new Date().toISOString() }; const errs = []; R.errs = errs;
  const b = await chromium.launch({ args: ['--js-flags=--expose-gc', '--enable-precise-memory-info'] });
  const p = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: DPR });
  p.on('pageerror', e => errs.push('page: ' + String(e).slice(0, 400))); p.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text().slice(0, 400)) });
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 900000, polling: 500 });
  const ev = s => p.evaluate(s => Promise.resolve(window.__TC_DEV.ev(s)), s);
  const shot = async n => { if (shots) { try { await p.screenshot({ path: path.join(shots, n + '.png') }) } catch (e) { } } };
  await p.waitForTimeout(4000);
  R.start = await ev(`(()=>{const o={mode:PlayerProfile.mode,cam:[Math.round(Camera.x),Math.round(Camera.y),+Camera.zoom.toFixed(2)]};if(PlayerProfile.mode!=='walk'){try{TurboCityOnFoot.exitVehicle()}catch(e){o.exitErr=String(e)}}o.mode2=PlayerProfile.mode;return o})()`);
  await p.waitForTimeout(1500);
  R.place = await ev(`(()=>{const o={};const x=PlayerPed.x,y=PlayerPed.y;try{const f1=window.tcStepFig('st-aharon',{x:x+26,y:y+6},{until:600000,src:'cz-qa'});const f2=window.tcStepFig('st-shimon',{x:x-26,y:y+8},{until:600000,src:'cz-qa'});o.f1=!!f1;o.f2=!!f2}catch(e){o.err=String(e)}o.pl=[Math.round(x),Math.round(y)];o.cz=window.__TC_CZ?__TC_CZ.stats():null;return o})()`);
  R.mon = await ev(MON); R.mem0 = await ev(MEM);
  await p.mouse.move(W / 2, H / 2);
  const ph = s => ev("window.__CZM&&(window.__CZM.ph=" + JSON.stringify(s) + ")");
  const zoomTo = z => ev(`(()=>{Camera.zoom=${z};return +Camera.zoom.toFixed(3)})()`);
  R.levels = {};
  for (const z of [1.15, 5.5, 8, 11]) {   // 16:25: the foot max is 11
    if (z === '16s') await ev('(TCCZ.sbcOff=false,1)');
    await ph('lv' + z); await zoomTo(z === '16s' ? 16 : z); await p.waitForTimeout(1500); await shot('z' + z + '_stand');
    await p.keyboard.down('KeyD'); await p.waitForTimeout(1800); await shot('z' + z + '_walk'); await p.keyboard.up('KeyD');
    await p.keyboard.down('KeyA'); await p.waitForTimeout(1800); await p.keyboard.up('KeyA'); await p.waitForTimeout(10500);   // perf: the stale copies of the tiles of the previous zoom live up to 15 s — the memory after them
    if (z === '16s') await ev('(TCCZ.sbcOff=true,1)');
    R.levels[z] = { mem: await ev(MEM), cz: await ev('__TC_CZ.stats()'), zoom: await ev('+Camera.zoom.toFixed(3)'), figs: await ev("(window.__TC_SACT&&__TC_SACT.figs().map(f=>({id:f.id,por:f.por})))||null") };
  }
  // the wheel: 5.5 ↔ 16 on foot (10 notches = ×3.1), cycles times
  await zoomTo(5.5); await p.waitForTimeout(1200); R.memW0 = await ev(MEM);
  const wheel = async (dir, n) => { for (let i = 0; i < n; i++) { await p.mouse.wheel(0, dir * 100); await p.waitForTimeout(40) } };
  for (let k = 1; k <= cycles; k++) { await ph('in' + k); await wheel(-1, 12); await p.waitForTimeout(1400); if (k === 1) await shot('wheel_in'); await ph('out' + k); await wheel(1, 10); await p.waitForTimeout(1400) }
  R.afterWheel = await ev('+Camera.zoom.toFixed(3)'); R.memW1 = await ev(MEM);
  await ph('in-max'); await wheel(-1, 14); await p.waitForTimeout(1200); R.footMaxWheel = await ev('+Camera.zoom.toFixed(3)');
  // into a vehicle at the close zoom — back to 5.5 softly
  await ph('veh'); R.veh = await ev(`(()=>{const z0=+Camera.zoom.toFixed(3);try{PlayerPed.x=PlayerCar.x+14;PlayerPed.y=PlayerCar.y+4;TurboCityOnFoot.enterVehicle()}catch(e){return{err:String(e)}}return{z0,mode:PlayerProfile.mode}})()`);
  const zs = []; for (let i = 0; i < 12; i++) { await p.waitForTimeout(80); zs.push(await ev('+Camera.zoom.toFixed(3)')) } R.veh.zs = zs; await shot('veh_after');
  await p.waitForTimeout(800); R.veh.final = await ev('+Camera.zoom.toFixed(3)');
  await wheel(-1, 14); await p.waitForTimeout(500); R.veh.wheelMax = await ev('+Camera.zoom.toFixed(3)');
  await ph('end');
  R.qa = await ev('__TC_CZ.qa()'); R.stats = await ev('__TC_CZ.stats()'); R.memEnd = await ev(MEM);
  R.rows = await ev('(()=>{window.__CZM.on=false;return window.__CZM.rows})()'); R.cols = ['t', 'dt', 'zoom', 'fb', 'green', 'gray', 'phase', 'mode', 'renderMs'];
  await b.close(); fs.writeFileSync(out, JSON.stringify(R));
  // summary
  const by = {}; for (const r of R.rows) { const k = /^lv/.test(String(r[6])) ? String(r[6]) : String(r[6]).replace(/\d+$/, ''); (by[k] = by[k] || []).push(r) }
  const pct = (A, q) => { const s = A.slice().sort((x, y) => x - y); return s.length ? s[Math.min(s.length - 1, Math.floor(q * s.length))] : 0 };
  const sum = {}; let gj = 0;
  for (const [k, L] of Object.entries(by)) { const dts = L.map(r => r[1]); const tail = L.slice(-8), g0 = pct(tail.map(r => r[4]), .5), y0 = pct(tail.map(r => r[5]), .5); const j = L.filter(r => r[4] - g0 > .12 && r[5] < y0 - .05).length; if (/^(in|out)$/.test(k)) gj += j;
    const rts = L.map(r => r[8] || 0); sum[k] = { n: L.length, rMed: pct(rts, .5), rP90: pct(rts, .9), med: pct(dts, .5), p95: pct(dts, .95), max: Math.max(...dts), o50: dts.filter(d => d > 50).length, o100: dts.filter(d => d > 100).length, live: L.reduce((s, r) => s + r[3], 0), greenJump: j } }
  console.log(JSON.stringify({ start: R.start, place: R.place, mem0: R.mem0, levels: Object.fromEntries(Object.entries(R.levels).map(([z, v]) => [z, { heap: v.mem.heapMB, canvas: v.mem.canvasMB, p34g: v.mem.p34g, p34: v.mem.p34 && v.mem.p34.MB, sbc: v.mem.sbcMB, c34: v.mem.c34MB, by: v.mem.by, face: v.cz.n.face, figs: v.cz.n.figs, zoom: v.zoom }])),
    memW0: R.memW0 && { heap: R.memW0.heapMB, canvas: R.memW0.canvasMB }, memW1: R.memW1 && { heap: R.memW1.heapMB, canvas: R.memW1.canvasMB }, afterWheel: R.afterWheel, footMaxWheel: R.footMaxWheel, veh: R.veh,
    phases: sum, greenJumpWheel: gj, qa: R.qa, stats: R.stats, memEnd: { heap: R.memEnd.heapMB, canvas: R.memEnd.canvasMB, sbc: R.memEnd.sbcMB, c34: R.memEnd.c34MB, p34g: R.memEnd.p34g, by: R.memEnd.by }, errs: errs.slice(0, 8) }, null, 1));
})().catch(e => { console.error(String(e && e.stack || e).slice(0, 900)); process.exit(1) });
