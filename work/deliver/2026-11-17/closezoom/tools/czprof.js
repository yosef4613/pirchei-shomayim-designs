// czprof.js <build.html> <out.json> [W=412] [H=860] — closezoom: איפה הולך זמן הציור בזום 16 מול 5.5 (באותו מקום, עמידה, אחרי חימום).
// עוטף בתוך המשחק (‎__TC_DEV.ev — אותו סקופ) את הפונקציות שהציור קורא להן, וסוכם מ"ש מעבד לכל אחת בכל חלון. בלי שינוי בקוד המשחק.
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
const NAMES = ['render', 'wtcGround', 'wtcPass', 'wtcSchedule', 'wtcLayerPass', 'wtcReplaySprites', 'wtcExactLayers', 'wtcLodLayers', 'wtcTrees', 'wtcPropsLive', 'wtcOverLive', 'wtcLiveUnder', 'wtcLiveOver', 'wtcLiveOverRoad',
  'wtcCoolingLive', 'wtcAptLive', 'wtcVignette', 'wldTick', 'wldSkyPaint', 'sbcgFlush', 'renderGroundClassic', 'pgDraw', 'p560Live', 'p560DrawDoors', 'flushRoofs', 'flushCars', 'f2DrawPeople', 'e2DrawVisitors',
  'drawTrafficCars', 'drawPortProps', 'drawPortOverhead', 'drawPlayerPed', 'drawPlayerCar', 'drawParkedCars', 'drawNPCPedestrians', 'drawLanes', 'drawFreightTrains', 'drawFlowTrucks', 'drawNavigationWorld', 'drawSignals',
  'busStopsLive', 'drawBusStopPassengers', 'c34Flush', 'p34Pump', 'wtcBuildTile', 'wtcBuild', 'wtcBuild0', 'wtcEvict', 'g77ZpNext', 'sbcDraw', 'sbcMake', 'drawWho', 'wxDraw', 'wxRain', 'drawWeather', 'k34Take', 'vegDraw', 'vegLive'];
(async () => {
  const [file, out, W0, H0] = process.argv.slice(2); const W = +(W0 || 412), H = +(H0 || 860);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: W, height: H } }); const errs = [];
  p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 900000, polling: 500 });
  const ev = s => p.evaluate(s => Promise.resolve(window.__TC_DEV.ev(s)), s);
  await p.waitForTimeout(4000);
  const wrap = NAMES.map(n => `try{if(typeof ${n}==='function'&&!${n}.__czp){const f0=${n};${n}=function(){const t=performance.now();try{return f0.apply(this,arguments)}finally{const d=performance.now()-t;const e=P.t['${n}']||(P.t['${n}']=[0,0]);e[0]+=d;e[1]++}};${n}.__czp=1;P.w.push('${n}')}}catch(e){P.err.push('${n}:'+e)}`).join('\n');
  const R0 = await ev(`(()=>{if(PlayerProfile.mode!=='walk')TurboCityOnFoot.exitVehicle();const x=PlayerPed.x,y=PlayerPed.y;window.tcStepFig('st-aharon',{x:x+26,y:y+6},{until:900000,src:'cz-prof'});
    const P=window.__CZP={t:{},w:[],err:[],frames:0};${wrap}
    const r0=render;render=function(){P.frames++;return r0.apply(this,arguments)};return {wrapped:P.w.length,err:P.err}})()`);
  const R = { build: path.basename(file), W, H, wrapped: R0, win: [] };
  const win = async (tag, ms) => { await ev('(window.__CZP.t={},window.__CZP.frames=0,1)'); await p.waitForTimeout(ms);
    const o = await ev(`(()=>{const P=window.__CZP,f=Math.max(1,P.frames);return{frames:P.frames,top:Object.entries(P.t).map(([k,v])=>[k,+(v[0]/f).toFixed(2),+(v[1]/f).toFixed(1)]).sort((a,b)=>b[1]-a[1]).slice(0,16),tiles:WTC.tiles.size,built:WTC.stats.built,zoom:Camera.zoom}})()`);
    o.tag = tag; R.win.push(o); console.log(JSON.stringify(o)) };
  await ev('(Camera.zoom=5.5,1)'); await p.waitForTimeout(12000); await win('5.5', 8000);
  await ev('(Camera.zoom=16,1)'); await p.waitForTimeout(16000); await win('16 (1)', 8000); await win('16 (2)', 8000);
  await ev('(Camera.zoom=11,1)'); await p.waitForTimeout(12000); await win('11', 8000);
  R.errs = errs; await b.close(); fs.writeFileSync(out, JSON.stringify(R)); console.log('errs', JSON.stringify(errs));
})().catch(e => { console.error(String(e && e.stack || e).slice(0, 900)); process.exit(1) });
