// stuckmax_bus.js <build> <secs> [tag] — buses (17.11): עותק של qa_tools/stuckmax.js (אותה ספירה בדיוק: over5 / busOver5 / long / st / pe),
// ובנוסף — "ln": אוטובוסי הקווים (LN.bus, ‏074f) לפי המקום ולא לפי v.stuck (‏lnStep מאפס את v.stuck בדרך משלו, ו-BUS_VEHICLES ריק):
// לכל אוטובוס — העמידה הארוכה ביותר (זז פחות מ-3 פיקס׳) בשלב של נסיעה (אותה רשימה כמו LN.aud.frz ב-074f), השלב, המקום וה-waitBy באותו רגע.
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const [file, secs, tag] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] }); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const pe = []; p.on('pageerror', e => pe.push(String(e).slice(0, 200)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' }); await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  const ev = s => p.evaluate(x => window.__TC_DEV.ev(x), s);
  const M = {}, LS = {}, LM = {};
  for (let t = 0; t < 2 * (+secs || 150); t++) { await p.waitForTimeout(500);
    const r = await ev(`({s:[...BUS_VEHICLES.map(b=>['bus',b.id,+(b.stuck||0).toFixed(1),b.edgeId,b.term?1:0,b.dwell>0||b.curbStop?1:0]),...TRAFFIC_CARS.map(c=>['car',c.id+':'+c.asset,+(c.stuck||0).toFixed(1),c.edgeId,0,0])].filter(q=>q[2]>1),
      ln:(typeof LN==='undefined'?[]:LN.bus.filter(B=>B.v).map(B=>[B.no,B.ph,/^(gate|gate10|dep|dep2|out10|turn10|road|ret|ret-wait|in|out|tin|tout|twait|adv)$/.test(B.ph)?1:0,Math.round(B.v.x),Math.round(B.v.y),String(B.waitBy||'').slice(0,40),B.v.c2?'road':'path',+LN.t.toFixed(1)])),br:(typeof S13LB!=='undefined'?S13LB.st:null)})`);
    for (const q of r.s) { const k = q[0] + ' ' + q[1]; if (!M[k] || q[2] > M[k].max) M[k] = { max: q[2], edge: q[3], term: q[4], stop: q[5] } }
    for (const [no, ph, mov, x, y, wb, md, lt] of r.ln) { const S = LS[no];
      if (!S || !mov || Math.hypot(x - S.x, y - S.y) > 3) { LS[no] = { x, y, t: lt }; continue }
      const d = +(lt - S.t).toFixed(1); if (!LM[no] || d > LM[no].max) LM[no] = { max: d, ph, x, y, waitBy: wb, mode: md, bridge: r.br } } }
  const st = await ev(`({served:BUS_VEHICLES.reduce((a,b)=>a+(b.passengersServed||0),0),rec:BUS_VEHICLES.reduce((a,b)=>a+(b.recoveries2||0)+(b.recoveries||0),0),owned:TERM.bays.filter(q=>q.owner).length})`);
  let lnA = null; try { lnA = await ev(`({frz:LN.aud&&LN.aud.frz?{max:LN.aud.frz.max,n:LN.aud.frz.n}:null,yields:LN.stats.yields||0,bsv:(typeof busesAudit==='function'?(()=>{const a=busesAudit();return{first:a.first,bend:a.bend,waitByCleared:a.waitByCleared,err:a.err}})():null),trips:LN.stats.trips,buses:LN.bus.length,inService:LN.bus.filter(b=>b.v).length})`) } catch (e) { lnA = String(e).slice(0, 120) }
  const long = Object.entries(M).filter(([k, v]) => v.max > 5).map(([k, v]) => [k, v.max, v.edge, v.term ? 'term' : '', v.stop ? 'stop' : '']);
  const lnL = Object.entries(LM).map(([no, v]) => [no, v.max, v.ph, v.mode, v.x, v.y, v.waitBy, v.bridge]).sort((a, b) => b[1] - a[1]);
  console.log(JSON.stringify({ tag, build: path.basename(file), secs: +secs, over5: long.length, busOver5: long.filter(q => q[0].startsWith('bus')).length, long, st, pe,
    ln: { over30: lnL.filter(q => q[1] > 30).length, over60: lnL.filter(q => q[1] > 60).length, over180: lnL.filter(q => q[1] >= 180).length, top: lnL.slice(0, 12), audit: lnA } }));
  await b.close();
})().catch(e => { console.error(String(e).slice(0, 300)); process.exit(1) });
