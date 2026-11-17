// dump_sim.js — fieldthru: הסימולציה של השדה כמו שהיא רצה במשחק (אחרי כל העטיפות) + המדידה של fieldcalc (__TC_FC.report). node dump_sim.js <build> <out.json>
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out, hash] = process.argv.slice(2);   // hash — למשל dev&ft=0 (העולם בלי התוספת של fieldthru)
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await b.newPage({ viewport: { width: 1000, height: 700 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 300)));
  await p.goto('file://' + path.resolve(file) + '#' + (hash || 'dev'), { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(8000);
  const s = await p.evaluate(() => window.__TC_DEV.ev('JSON.stringify({T:S15SIM.T,flights:S15SIM.flights,veh:S15SIM.veh,tows:S15SIM.tows,heli:S15SIM.heli,sched:S15SIM.sched,ngf:S15SIM.ngf,spots:S15D.spots,stands:S15D.stands,parked:S15D.parked,stat:s15StaticList().map(o=>({id:o.id,key:o.key,x:o.x,y:o.y,th:o.th,heli:!!o.heli,al:o.al||null})),keys:Object.keys(S15SIM),fc:(window.__TC_FC&&window.__TC_FC.report)?window.__TC_FC.report():null,fts:(typeof FTS!=="undefined")?{on:FTS.on,n:FTS.n,u:FTS.u,v:FTS.v,err:FTS.err}:null,ftv:(window.__TC_FTV?{log:__TC_FTV.log(),made:__TC_FTV.made(),err:FTV.err}:null),fta:(typeof ftOps==="function")?(()=>{try{return ftOps()}catch(e){return String(e)}})():null,ffr3a:(window.__TC_FIELDFIX&&__TC_FIELDFIX.r3)?(()=>{try{return __TC_FIELDFIX.r3()}catch(e){return String(e)}})():null,ffr3:(typeof FFR3!=="undefined"&&FFR3.build)?(()=>{try{return FFR3.build()}catch(e){return String(e)}})():null,audit:(()=>{try{return s15SimAudit(1)}catch(e){return String(e)}})(),k:(()=>{try{const a=s15kAudit();return{ok:a.ok,n:a.n,pairs:a.pairs.slice(0,12)}}catch(e){return String(e)}})()})'));
  const o = JSON.parse(s); o.errs = errs; fs.writeFileSync(out, JSON.stringify(o)); console.log('ok', s.length, 'errs', errs.length); await b.close();
})().catch(e => { console.error(String(e).slice(0, 400)); process.exit(1) });
