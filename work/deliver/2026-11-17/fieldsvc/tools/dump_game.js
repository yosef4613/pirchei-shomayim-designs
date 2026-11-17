// dump_game.js — fieldsvc: מצב השדה כפי שהוא רץ במשחק (S15SIM אחרי כל העטיפות) + מדידת השירות של fieldcalc (__TC_FC.svc) + מדידת השירות של fieldsvc (__TC_FS אם קיים)
// שימוש: node dump_game.js <build.html> <out.json> [hash]
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  let [file, out, hash] = process.argv.slice(2);
  try { const R = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'qa', 'redirect.json'), 'utf8')); const k = path.basename(file); if (R[k]) file = path.join(path.dirname(file), R[k]) } catch (e) {}   // תור ארוך: הבקשה שחיכתה בתור רצה על הבנייה האחרונה (נרשם בפלט: build)
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await b.newPage({ viewport: { width: 1000, height: 700 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
  const t0 = Date.now();
  await p.goto('file://' + path.resolve(file) + '#' + (hash || 'dev'), { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 900000, polling: 500 });
  await p.waitForTimeout(8000);
  const s = await p.evaluate(() => window.__TC_DEV.ev(`JSON.stringify({T:S15SIM.T,flights:S15SIM.flights,veh:S15SIM.veh,tows:S15SIM.tows,sched:S15SIM.sched,spots:S15D.spots,pockets:S15D.pockets,stands:S15D.stands,service:S15D.service,
    vt:(typeof S15K_VT!=='undefined')?S15K_VT:null,
    fcsvc:(window.__TC_FC&&__TC_FC.svc)?(()=>{try{return __TC_FC.svc()}catch(e){return String(e)}})():null,
    fcmoves:(window.__TC_FC&&__TC_FC.moves)?(()=>{try{return __TC_FC.moves(1800)}catch(e){return String(e)}})():null,
    fs:(window.__TC_FS&&__TC_FS.report)?(()=>{try{return __TC_FS.report()}catch(e){return String(e)}})():null,fspre:(window.__TC_FS&&__TC_FS.pre)?(()=>{try{return __TC_FS.pre()}catch(e){return String(e)}})():null,
    mem:(performance&&performance.memory)?{used:performance.memory.usedJSHeapSize,total:performance.memory.totalJSHeapSize}:null,
    S15D:S15D,ngf:S15SIM.ngf,moving:[...S15_MOVING],W4:{RR:S15W4.RR,vF:S15W4.vF,vR:S15W4.vR},GR:{PX:S15GR.PX,VK:S15GR.VK},CART:(typeof S15GR_CART!=='undefined')?S15GR_CART:null,
    S6A:(typeof S6A_TYPES!=='undefined')?S6A_TYPES:null,GRT:(typeof S15GR_T!=='undefined')?S15GR_T:null,v4:(typeof S15K!=='undefined')?S15K.v4:null,
    vmax:(typeof s15kVmax==='function')?Object.fromEntries(['PT','BT','BL','CT','FT','WT','LV','GP','MS','AB','SH','SVC','HL','TG'].map(t=>[t,s15kVmax(t)])):null,
    acb:(typeof s15w4AcBoxes==='function')?s15w4AcBoxes():null,
    fsx:(typeof fsvSpot==='function')?(()=>{try{const o={};for(const A of fsvStands()){const r=o[A.f.id]={stand:A.f.home,model:A.f.model,ob:A.ob,off:A.off,x:A.x,y:A.y,th:A.th,span:A.span,L:A.L,need:A.need,sp:{},tm:{}};
      for(const c of ['WT','LV','SVC','GP','FT','CT','AL','HL','BL','BT']){try{r.sp[c]=fsvSpot(A,c)}catch(e){r.sp[c]=String(e).slice(0,80)}try{r.tm[c]=fsvTiming(A,c)}catch(e){}}
      r.old={};for(const k of ['water','lavatory','cleaning','gpu','belt','catering']){try{r.old[k]=fsvOldSpot(A,k)}catch(e){}}try{r.fuel=fsvFuelSpot(A)}catch(e){}try{r.door=fsvDoorR1(A)}catch(e){}
      try{r.cat=s15w4CatSpot({ac:A.f.model,x:A.x,y:A.y,th:A.th,sid:A.f.home,f:A.f})}catch(e){}try{r.cathold=s15w4Hold(A.f.home,A.f.model,A.f.id)}catch(e){}}return o}catch(e){return String(e)}})():null,
    fsdims:(typeof fsvDims==='function')?Object.fromEntries(['WT','LV','SVC','GP','FT','CT','AL','HL'].map(c=>[c,fsvDims(c)])):null})`));
  const o = JSON.parse(s); o.build = path.basename(file); o.errs = errs; o.ms = Date.now() - t0; fs.writeFileSync(out, JSON.stringify(o)); console.log('ok', s.length, 'errs', errs.length, 'ms', o.ms); await b.close();
})().catch(e => { console.error(String(e).slice(0, 400)); process.exit(1) });
