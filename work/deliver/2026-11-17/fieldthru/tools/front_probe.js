// front_probe.js <build> <secs> <out.json> — fieldthru (המתאם, perf): מכונית שתקועה בחזית הטרמינל (AIR-FRONT) — מי לפניה ולמה. כמו stuckmax (כל 0.5 ש׳),
// וכשמכונית ב-AIR-FRONT תקועה מעל 6 ש׳ — כל השדות שלה, ומי שבתוך 160 פיקס׳ ממנה (מכוניות, אוטובוסים, חונים), פעם אחת לכל מכונית בכל 5 ש׳
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
(async () => {
  const [file, secs, out] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] }); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' }); await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  const ev = s => p.evaluate(x => window.__TC_DEV.ev(x), s); const rec = []; const last = {};
  for (let t = 0; t < 2 * (+secs || 150); t++) { await p.waitForTimeout(500);
    const r = await ev(`(()=>{const o=[];for(const c of TRAFFIC_CARS){if(c.edgeId!=='AIR-FRONT'||!(c.stuck>6))continue;const pick=x=>{const q={};for(const k of Object.keys(x)){const v=x[k];if(v==null||typeof v==='function')continue;if(typeof v==='object'){if(Array.isArray(v)&&v.length<6&&v.every(z=>typeof z!=='object'))q[k]=v;continue}q[k]=v}return q};
      const near=[...TRAFFIC_CARS.filter(d=>d!==c&&Math.hypot(d.x-c.x,d.y-c.y)<160).map(d=>({k:'car',id:d.id,edge:d.edgeId,x:Math.round(d.x),y:Math.round(d.y),stuck:d.stuck,sp:d.speed,ln:d.lane})),...BUS_VEHICLES.filter(d=>Math.hypot(d.x-c.x,d.y-c.y)<160).map(d=>({k:'bus',id:d.id,edge:d.edgeId,x:Math.round(d.x),y:Math.round(d.y),stuck:d.stuck,dwell:d.dwell,curb:!!d.curbStop}))];
      o.push({t:performance.now()/1000|0,car:pick(c),near})}return o})()`);
    for (const q of r) { const k = q.car.id; if (last[k] && t - last[k] < 10) continue; last[k] = t; rec.push(q) } }
  fs.writeFileSync(out, JSON.stringify(rec, null, 1)); console.log('front_probe', rec.length, 'records'); await b.close();
})().catch(e => { console.error(String(e).slice(0, 300)); process.exit(1) });
