// czab.js <build.html> <out.json> [W=1920] [H=953] — closezoom: השוואה מבוקרת של זמן הציור (render, מ"ש מעבד בתוך המשחק) באותו מקום:
// 5.5 מול 16, עמידה והליכה, ובזום 16 — SBC כבוי / פועל לסירוגין (4 חלונות), אחרי חימום (האריחים והתמונות של האנשים כבר נבנו).
// לכל חלון: חציון, p25, p90 של render, ‏dt, והזיכרון (קנבסים, SBC, ‏P34, ‏P34G) אחרי gc.
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
const MEM = `(()=>{try{window.gc&&window.gc()}catch(e){}const cm=window.__TC_CANVAS_MEM?window.__TC_CANVAS_MEM():null;return{heap:performance.memory?+(performance.memory.usedJSHeapSize/1048576).toFixed(1):null,canvas:cm&&cm.mb,sbc:+(SBC.bytes/1048576).toFixed(1),p34:window.P34?P34.stats().MB:null,p34g:+(P34G.bytes/1048576).toFixed(1),tiles:WTC.tiles.size}})()`;
(async () => {
  const [file, out, W0, H0] = process.argv.slice(2); const W = +(W0 || 1920), H = +(H0 || 953);
  const b = await chromium.launch({ args: ['--js-flags=--expose-gc', '--enable-precise-memory-info'] });
  const p = await b.newPage({ viewport: { width: W, height: H } }); const errs = [];
  p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 900000, polling: 500 });
  const ev = s => p.evaluate(s => Promise.resolve(window.__TC_DEV.ev(s)), s);
  await p.waitForTimeout(4000);
  await ev(`(()=>{if(PlayerProfile.mode!=='walk')TurboCityOnFoot.exitVehicle();const x=PlayerPed.x,y=PlayerPed.y;window.tcStepFig('st-aharon',{x:x+26,y:y+6},{until:900000,src:'cz-ab'});window.tcStepFig('st-shimon',{x:x-26,y:y+8},{until:900000,src:'cz-ab'});
   const M=window.__CZAB={rt:[],on:false};const r0=render;render=function(){const t=performance.now();try{return r0.apply(this,arguments)}finally{if(M.on)M.rt.push(+(performance.now()-t).toFixed(2))}};return 1})()`);
  await p.mouse.move(W / 2, H / 2);
  const R = { build: path.basename(file), W, H, win: [] };
  const win = async (tag, ms, walk) => {
    await ev('(window.__CZAB.rt=[],window.__CZAB.on=true,1)'); const t0 = Date.now();
    if (walk) { while (Date.now() - t0 < ms) { await p.keyboard.down('KeyD'); await p.waitForTimeout(1200); await p.keyboard.up('KeyD'); await p.keyboard.down('KeyA'); await p.waitForTimeout(1200); await p.keyboard.up('KeyA') } }
    else await p.waitForTimeout(ms);
    const rt = await ev('(window.__CZAB.on=false,window.__CZAB.rt)'); const s = rt.slice().sort((a, b) => a - b), q = f => s.length ? s[Math.min(s.length - 1, Math.floor(f * s.length))] : null;
    const o = { tag, n: s.length, p25: q(.25), med: q(.5), p90: q(.9), fps: +(s.length / (ms / 1000)).toFixed(1), mem: await ev(MEM) }; R.win.push(o); console.log(JSON.stringify(o));
  };
  const zoom = z => ev(`(Camera.zoom=${z},1)`);
  await zoom(5.5); await p.waitForTimeout(12000); await win('5.5 עמידה', 8000); await win('5.5 הליכה (חימום)', 5000, true); await win('5.5 הליכה', 7000, true);
  await zoom(16); await ev('(TCCZ.sbcOff=true,1)'); await p.waitForTimeout(16000);
  await win('16 עמידה · SBC כבוי', 8000); await ev('(TCCZ.sbcOff=false,1)'); await p.waitForTimeout(6000); await win('16 עמידה · SBC פועל', 8000);
  await ev('(TCCZ.sbcOff=true,1)'); await p.waitForTimeout(3000); await win('16 עמידה · SBC כבוי (2)', 8000); await ev('(TCCZ.sbcOff=false,1)'); await p.waitForTimeout(3000); await win('16 עמידה · SBC פועל (2)', 8000);
  await ev('(TCCZ.sbcOff=true,1)'); await win('16 הליכה (חימום)', 5000, true); await win('16 הליכה · SBC כבוי', 7000, true);
  await zoom(5.5); await p.waitForTimeout(16000); await win('5.5 עמידה (שוב)', 8000);
  R.errs = errs; R.cz = await ev('__TC_CZ.stats()'); await b.close(); fs.writeFileSync(out, JSON.stringify(R)); console.log('errs', JSON.stringify(errs));
})().catch(e => { console.error(String(e && e.stack || e).slice(0, 900)); process.exit(1) });
