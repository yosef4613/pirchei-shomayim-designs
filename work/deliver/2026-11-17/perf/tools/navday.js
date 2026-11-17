// navday.js — perf 17.11: השיא של 116 מ"ש "בקבלת משימה — setNavigationTarget" (הממצא של missions, try6367, ‏MB.E.msMax) — מאיפה הוא בא.
// node navday.js <game.html> <out.json> [steps=110]   — דרך התור: bash W/tools_pack/bslot.sh node ...
// Chromium עם --enable-precise-memory-info (כדי לראות איסוף זבל בתוך קריאה: ירידה בערימה). ‎#dev, ‏1280×800.
// עוטף לזמן המדידה בלבד (בתוך הדף): setNavigationTarget (העטיפה החיצונית — הנעילות), ‏recalcNavigation, ‏navPoiRegistry, ‏shortestNodePath, ‏nearestRoadNode,
//   startMission, ‏setTemporaryVehicle, ‏cancelActiveMission, ‏SaveManager.save / log, ‏toast, ‏renderPhone, ‏g77MsgIn, ‏g77CallIn, ‏S9STORY.start / advance, ‏TCSTORY.focus.
// שלבים: (0) הקריאה הראשונה לניווט (קר) ועוד שתיים; (1) 120 יעדים אקראיים (ועוד 20 עם הטלפון פתוח); (2) 30 משימות עבודה: startMission → ביטול;
//   (3) "יום" של לוח המשימות כמו mb_day.js של missions (הצעות, "קבל", סיום, הסיפור) — לכל צעד: הזמן של הלוח (ΔE.ms) ומה רץ בחלון הזה (קריאות ≥ 8 מ"ש,
//   משימות ארוכות ≥ 50 מ"ש של הדפדפן); (4) הדקלים של B6 בצייר השטוח (K34 כבוי לרגע) והשומר TPG.
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
const INSTR = `(()=>{if(window.__ND)return 'again';const N=window.__ND={calls:{},top:[],stack:[],log:[],lt:[]};
 const mem=()=>{try{return performance.memory.usedJSHeapSize}catch(e){return 0}};
 const wrapF=(name,get,set)=>{let f;try{f=get()}catch(e){return 0}if(typeof f!=='function'||f.__nd)return 0;
  const w=function(){const fr={t:performance.now(),h:mem(),ch:[]};N.stack.push(fr);try{return f.apply(this,arguments)}finally{N.stack.pop();
   const d=performance.now()-fr.t,drop=fr.h-mem(),c=N.calls[name]||(N.calls[name]={n:0,ms:0,max:0,o5:0,o20:0,o50:0,gcMax:0});c.n++;c.ms+=d;if(d>c.max)c.max=d;if(d>5)c.o5++;if(d>20)c.o20++;if(d>50)c.o50++;
   const gc=drop>262144?Math.round(drop/104857.6)/10:0;const rec={n:name,ms:+d.toFixed(1),at:Math.round(fr.t),gc,a:String(arguments[0]).slice(0,40),ch:fr.ch.filter(x=>x.ms>=.5).slice(0,10)};
   if(d>c.gcMax&&gc)c.gcMax=d;const par=N.stack[N.stack.length-1];if(par)par.ch.push({n:name,ms:rec.ms,gc});
   if(d>=8){N.log.push(rec);if(N.log.length>600)N.log.shift()}
   if(!par){N.top.push(rec);N.top.sort((a,b)=>b.ms-a.ms);if(N.top.length>14)N.top.length=14}}};
  w.__nd=1;try{set(w)}catch(e){return 0}return 1};
 let k=0;const G=(n)=>k+=wrapF(n,()=>eval(n),f=>{eval(n+'=f')});
 for(const n of ['setNavigationTarget','recalcNavigation','navPoiRegistry','shortestNodePath','nearestRoadNode','startMission','setTemporaryVehicle','cancelActiveMission','toast','renderPhone','g77MsgIn','g77CallIn'])try{G(n)}catch(e){}
 k+=wrapF('SaveManager.save',()=>SaveManager.save,f=>{SaveManager.save=f});k+=wrapF('SaveManager.log',()=>SaveManager.log,f=>{SaveManager.log=f});
 try{k+=wrapF('S9STORY.start',()=>S9STORY.start,f=>{S9STORY.start=f});k+=wrapF('S9STORY.advance',()=>S9STORY.advance,f=>{S9STORY.advance=f})}catch(e){}
 try{k+=wrapF('TCSTORY.focus',()=>TCSTORY.focus,f=>{TCSTORY.focus=f})}catch(e){}
 try{new PerformanceObserver(l=>{for(const e of l.getEntries()){N.lt.push({at:Math.round(e.startTime),ms:Math.round(e.duration)});if(N.lt.length>3000)N.lt.shift()}}).observe({type:'longtask',buffered:true})}catch(e){N.ltErr=String(e)}
 N.wrapped=k;return 'ok '+k})()`;
const PH01 = `(()=>{const N=window.__ND,o={},R=navPoiRegistry(),a=playerActor(),ids=Object.keys(R).filter(k=>!R[k].hidden&&!/^(D5-FK-|ACT-)/.test(k));
 ids.sort((x,y)=>Math.hypot(R[y].x-a.x,R[y].y-a.y)-Math.hypot(R[x].x-a.x,R[x].y-a.y));o.pois=ids.length;o.player=[Math.round(a.x),Math.round(a.y),PlayerProfile.mode];
 const am=PlayerProfile.activeMission;PlayerProfile.activeMission=null;const one=(id,o2)=>{const t=performance.now(),h=performance.memory.usedJSHeapSize;let r;try{r=setNavigationTarget(id,o2||{mission:true})}catch(e){r='err '+String(e).slice(0,80)}
  return{id,ms:+(performance.now()-t).toFixed(2),gc:Math.max(0,Math.round((h-performance.memory.usedJSHeapSize)/104857.6)/10),ok:r===true,pts:State.navigation&&State.navigation.points?State.navigation.points.length:0}};
 o.cold=[one(ids[0]),one(ids[0]),one(ids[1])];
 let s=12345;const rnd=()=>(s=(s*16807)%2147483647)/2147483647;const L=[];for(let i=0;i<120;i++)L.push(one(ids[Math.floor(rnd()*ids.length)],i%2?{mission:true}:{mission:true,silent:true}));
 const ms=L.map(x=>x.ms).sort((x,y)=>x-y),q=p=>ms[Math.min(ms.length-1,Math.floor(p*ms.length))];o.rand={n:L.length,p50:q(.5),p90:q(.9),p99:q(.99),max:ms[ms.length-1],over20:L.filter(x=>x.ms>20).length,top:L.slice().sort((x,y)=>y.ms-x.ms).slice(0,5)};
 try{const op=State.phoneOpen;if(!op&&typeof setPhoneOpen==='function')setPhoneOpen(true);const P=[];for(let i=0;i<20;i++)P.push(one(ids[Math.floor(rnd()*ids.length)]));if(!op&&typeof setPhoneOpen==='function')setPhoneOpen(false);
  const pm=P.map(x=>x.ms).sort((x,y)=>x-y);o.phone={p50:pm[10],max:pm[19],top:P.slice().sort((x,y)=>y.ms-x.ms).slice(0,3)}}catch(e){o.phoneErr=String(e).slice(0,120)}
 State.navigation=null;PlayerProfile.activeMission=am;return JSON.stringify(o)})()`;
const PH2 = `(()=>{const o={calls:[]},am=PlayerProfile.activeMission,ids=Object.keys(MISSION_DEFS).filter(id=>!/^M-ST-/.test(id)&&!MISSION_DEFS[id].retired);let n=0;
 for(const id of ids){if(n>=30)break;PlayerProfile.activeMission=null;State.navigation=null;const t=performance.now(),h=performance.memory.usedJSHeapSize;let er=null;try{startMission(id)}catch(e){er=String(e).slice(0,100)}
  const ms=performance.now()-t,gc=Math.max(0,Math.round((h-performance.memory.usedJSHeapSize)/104857.6)/10);if(!PlayerProfile.activeMission&&!er)continue;n++;
  const t2=performance.now();try{cancelActiveMission()}catch(e){}o.calls.push({id,type:MISSION_DEFS[id].type||'',ms:+ms.toFixed(1),gc,cancel:+(performance.now()-t2).toFixed(1),er})}
 PlayerProfile.activeMission=am;const ms=o.calls.map(x=>x.ms).sort((x,y)=>x-y);o.n=ms.length;o.p50=ms[Math.floor(ms.length/2)];o.max=ms[ms.length-1];o.top=o.calls.slice().sort((x,y)=>y.ms-x.ms).slice(0,6);delete o.calls;return JSON.stringify(o)})()`;
const PH4 = `(()=>{const T=window.__TC_PERFX&&window.__TC_PERFX.tpv,cv=document.createElement('canvas');cv.width=cv.height=96;const c=cv.getContext('2d'),o={b6:B6_TREES.length,vars:{},ok:0,thr:0,first:null};
 for(const t of B6_TREES)o.vars[t.variant]=(o.vars[t.variant]||0)+1;const k0=(typeof K34C!=='undefined')?K34C.on:null;if(k0!==null)K34C.on=false;
 try{for(const t of B6_TREES){try{TurboCity.draw(c,t.asset,0,0,{mode:'runtime',targetWidth:30,variant:t.variant||0,time:0});o.ok++}catch(e){o.thr++;o.first=o.first||String(e).slice(0,140)}}
  const g0=T&&T.guard;o.gthr=0;for(const v of [4,5,7,-1,NaN,1.5])try{TurboCity.draw(c,'TP-UR-01',0,0,{mode:'runtime',variant:v,time:0})}catch(e){o.gthr++;o.gfirst=o.gfirst||String(e).slice(0,140)}
  o.guardHits=T&&T.guard!=null?T.guard-g0:null;o.where=T&&T.where?T.where.slice(0,2):null;o.tpv=T?{fixed:T.fixed,wrapped:T.wrapped}:null}finally{if(k0!==null)K34C.on=k0}
 try{o.wtcErr=WTC.err?String(WTC.err).slice(0,300):null}catch(e){}return JSON.stringify(o)})()`;
(async () => {
  const [file, out, nS] = process.argv.slice(2); const STEPS = +(nS || 110); const R = { build: path.basename(file), steps: STEPS };
  const b = await chromium.launch({ args: ['--enable-precise-memory-info'] }); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300))); p.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text().slice(0, 240)) });
  const t0 = Date.now(); await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 }); R.readyS = Math.round((Date.now() - t0) / 1000);
  await p.waitForTimeout(1500);
  const ev = s => p.evaluate(x => Promise.resolve(window.__TC_DEV.ev(x)).then(v => typeof v === 'string' ? v : JSON.stringify(v)), s);
  const J = async s => { const r = await ev(s); try { return JSON.parse(r) } catch (e) { return { raw: String(r).slice(0, 400) } } };
  const ONLY4 = process.env.ND_ONLY === 'ph4';   // only (4) — for the base build (without TPV / TPG)
  R.instr = await ev(INSTR);
  if (!ONLY4) { R.ph01 = await J(PH01); R.ph2 = await J(PH2) }
  // (3) the day of the board
  R.init = ONLY4 ? { mb: false, only4: true } : await J(`(()=>{const MB=window.__TC_MB;if(!MB)return JSON.stringify({mb:false});MB.force(true);try{__TC_STORY.jump('1-3')}catch(e){}window.__MBD={offers:0,acc:0,later:0,done:0,go:0,goT:-1};gameClockSet(6,0);
    return JSON.stringify({mb:true,ms:MB.E.ms,ticks:MB.E.ticks,msMax:MB.E.msMax})})()`);
  const rows = []; let prev = await J(`JSON.stringify({ms:window.__TC_MB?__TC_MB.E.ms:0,ticks:window.__TC_MB?__TC_MB.E.ticks:0,t:performance.now()})`);
  for (let i = 0; i < STEPS && R.init.mb; i++) {
    const h = 6 + Math.floor(i * 5 / 60), mi = (i * 5) % 60;
    await ev(`gameClockSet(${h % 24},${mi})`); await p.waitForTimeout(1100);
    const r = await J(`(()=>{const MB=window.__TC_MB,D=window.__MBD,N=window.__ND,P=${JSON.stringify(prev)},o={i:${i}};const now=performance.now();
     o.dms=+(MB.E.ms-P.ms).toFixed(1);o.dt=MB.E.ticks-P.ticks;o.msMax=+MB.E.msMax.toFixed(1);
     if(o.dms>15){o.calls=N.log.filter(x=>x.at>=P.t-50).map(x=>({n:x.n,ms:x.ms,gc:x.gc,a:x.a,ch:x.ch}));o.lt=N.lt.filter(x=>x.at>=P.t-50).slice(0,6)}
     let S=null;try{S=MB.state()}catch(e){o.err=String(e).slice(0,100)}
     if(S){if(${i}>0&&${i}%18===0){const it=S.items.find(q=>q.key[0]==='z')||S.items[0];if(it){const id=it.key.slice(2);if(it.key[0]==='z'){if(S9STORY.step(id)<1)MB.act('acc',it.key);let g=0;while(!S9STORY.done(id)&&g++<12)S9STORY.advance(id)}else{MB.E.jobsDone.push(id);PlayerProfile.progression.completedMissions.push(id)}D.done++;o.did='done '+it.key}}
      if(S.offer){D.offers++;if(D.offers%2){MB.act('acc',S.offer);D.acc++;o.did=(o.did||'')+' acc '+S.offer}else{MB.act('later',S.offer);D.later++;o.did=(o.did||'')+' later '+S.offer}}
      if(!PlayerProfile.activeMission&&${i}%9===4){const it=S.items.find(q=>q.key[0]==='j');if(it){MB.act('go',it.key);if(PlayerProfile.activeMission){D.go++;D.goT=${i};o.did=(o.did||'')+' go '+it.key}}}
      if(PlayerProfile.activeMission&&D.goT>=0&&${i}-D.goT>=3){try{cancelActiveMission()}catch(e){}D.goT=-1;o.did=(o.did||'')+' cancel'}
      if(${i}>0&&${i}%12===0){try{__TC_STORY.skip()}catch(e){}}}
     o.next={ms:MB.E.ms,ticks:MB.E.ticks,t:performance.now()};return JSON.stringify(o)})()`);
    prev = r.next || prev; delete r.next; rows.push(r);
  }
  R.day = { steps: rows.length, msMax: rows.length ? Math.max(...rows.map(r => r.msMax || 0)) : null, spikes: rows.filter(r => r.dms > 15).slice(0, 12), stepMs: rows.map(r => r.dms), D: await J(`JSON.stringify(window.__MBD||null)`) };
  R.calls = await J(`JSON.stringify(Object.fromEntries(Object.entries(window.__ND.calls).map(([k,c])=>[k,{n:c.n,avg:+(c.ms/c.n).toFixed(2),max:+c.max.toFixed(1),o5:c.o5,o20:c.o20,o50:c.o50,gcMax:+c.gcMax.toFixed(1)}])))`);
  R.top = await J(`JSON.stringify(window.__ND.top)`);
  R.longtasks = await J(`(()=>{const L=window.__ND.lt;const ms=L.map(x=>x.ms).sort((a,b)=>b-a);return JSON.stringify({n:L.length,top:ms.slice(0,10),over100:L.filter(x=>x.ms>100).length})})()`);
  R.ph4 = await J(PH4);
  R.errs = errs.slice(0, 12); R.nErrs = errs.length; R.sec = Math.round((Date.now() - t0) / 1000);
  fs.writeFileSync(out, JSON.stringify(R, null, 1));
  console.log(JSON.stringify({ readyS: R.readyS, instr: R.instr, cold: R.ph01 && R.ph01.cold, rand: R.ph01 && R.ph01.rand && { p50: R.ph01.rand.p50, p90: R.ph01.rand.p90, max: R.ph01.rand.max, over20: R.ph01.rand.over20 }, phone: R.ph01 && R.ph01.phone && { p50: R.ph01.phone.p50, max: R.ph01.phone.max },
    start: R.ph2 && { n: R.ph2.n, p50: R.ph2.p50, max: R.ph2.max, top: (R.ph2.top || []).slice(0, 3) }, day: { msMax: R.day.msMax, spikes: R.day.spikes.length, D: R.day.D }, top: (R.top || []).slice(0, 4).map(x => x.n + ' ' + x.ms + (x.gc ? ' gc' + x.gc : '')), longtasks: R.longtasks, ph4: R.ph4, nErrs: R.nErrs, errs: R.errs.slice(0, 4) }, null, 1));
  await b.close(); process.exit(0);
})().catch(e => { console.error(String(e && e.stack || e).slice(0, 600)); process.exit(1) });
