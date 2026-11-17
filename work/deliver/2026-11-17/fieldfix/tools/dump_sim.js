// dump_sim.js — fieldfix: הסימולציה של השדה כמו שהיא רצה במשחק (אחרי כל העטיפות: FL-C2, ‏HL-C1, ‏repath, ‏s15k) → JSON לכלי של הטיסות. node dump_sim.js <build> <out.json>
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await b.newPage({ viewport: { width: 1000, height: 700 } });
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  await p.waitForTimeout(6000);
  const s = await p.evaluate(() => window.__TC_DEV.ev('JSON.stringify({T:S15SIM.T,flights:S15SIM.flights,veh:S15SIM.veh,tows:S15SIM.tows,heli:S15SIM.heli,sched:S15SIM.sched,ngf:S15SIM.ngf,spots:S15D.spots,stands:S15D.stands,parked:S15D.parked,bridges:S15D.bridges,stat:s15StaticList().map(o=>({id:o.id,key:o.key,x:o.x,y:o.y,th:o.th,heli:!!o.heli,al:o.al||null})),keys:Object.keys(S15SIM)})'));
  fs.writeFileSync(out, s); console.log('ok', s.length); await b.close();
})().catch(e => { console.error(String(e).slice(0, 400)); process.exit(1) });
