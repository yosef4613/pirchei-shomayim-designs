// per-vehicle longest hold over N s (sampled each 0.5 s): buses and cars; where the long ones were. node stuckmax.js <build> <secs> [tag]
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const [file, secs, tag] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] }); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const pe = []; p.on('pageerror', e => pe.push(String(e).slice(0, 200)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' }); await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  const ev = s => p.evaluate(x => window.__TC_DEV.ev(x), s);
  const M = {};
  for (let t = 0; t < 2 * (+secs || 150); t++) { await p.waitForTimeout(500);
    const r = await ev(`[...BUS_VEHICLES.map(b=>['bus',b.id,+(b.stuck||0).toFixed(1),b.edgeId,b.term?1:0,b.dwell>0||b.curbStop?1:0]),...TRAFFIC_CARS.map(c=>['car',c.id+':'+c.asset,+(c.stuck||0).toFixed(1),c.edgeId,0,0])].filter(q=>q[2]>1)`);
    for (const q of r) { const k = q[0] + ' ' + q[1]; if (!M[k] || q[2] > M[k].max) M[k] = { max: q[2], edge: q[3], term: q[4], stop: q[5] } } }
  const st = await ev(`({served:BUS_VEHICLES.reduce((a,b)=>a+(b.passengersServed||0),0),rec:BUS_VEHICLES.reduce((a,b)=>a+(b.recoveries2||0)+(b.recoveries||0),0),owned:TERM.bays.filter(q=>q.owner).length})`);
  const long = Object.entries(M).filter(([k, v]) => v.max > 5).map(([k, v]) => [k, v.max, v.edge, v.term ? 'term' : '', v.stop ? 'stop' : '']);
  console.log(JSON.stringify({ tag, build: path.basename(file), secs: +secs, over5: long.length, busOver5: long.filter(q => q[0].startsWith('bus')).length, long, st, pe }));
  await b.close();
})().catch(e => { console.error(String(e).slice(0, 300)); process.exit(1) });
