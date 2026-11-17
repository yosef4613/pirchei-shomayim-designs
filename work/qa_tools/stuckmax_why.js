// stuckmax_why.js — עותק של qa_tools/stuckmax.js (אותה מדידה, אותו פלט), ועוד שדה why לכל רכב שעמד יותר מ-5 שנ׳: מה המנוע אמר ברגע של העמידה הכי ארוכה —
// limit, מי לפניו (lead), מגע (hardBy), האם קיבל כניסה (granted) ולאיזה צומת (gate / junctionLock), על איזו תנועה או נתיב, והמקום. כך מקרה נדיר מסביר את עצמו
// כבר בהרצה שבה הוא קרה, בלי שחזור. (סוכן הכיכרות, 10.11 — הצעה להחליף בו את stuckmax.js בסט המלא.)  node stuckmax_why.js <build> <secs> [tag]
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const [file, secs, tag] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] }); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const pe = []; p.on('pageerror', e => pe.push(String(e).slice(0, 200)));
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' }); await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  const ev = s => p.evaluate(x => window.__TC_DEV.ev(x), s);
  const M = {};
  for (let t = 0; t < 2 * (+secs || 150); t++) { await p.waitForTimeout(500);
    const r = await ev(`(()=>{const W=v=>{const c=v.c2;if(!c)return null;return{t:+SIM.t.toFixed(1),x:Math.round(v.x),y:Math.round(v.y),limit:c.limit||null,lead:c.limitLead||null,gap:c.limitGap!=null?Math.round(c.limitGap):null,hardBy:c.hardBy||null,granted:!!c.granted,gate:c.gate?c.gate.node:null,why:c.why||null,chain:c.chainWant?c.chainWant.node+':'+c.chainWant.why:null,lock:v.junctionLock||null,mv:c.mv?c.mv.id:null,ms:c.mv?Math.round(c.ms):null,lane:c.mv?null:c.lane.id,s:c.mv?null:Math.round(c.s),backout:!!c.backout,laneBack:c.laneBack>0}};
      return[...BUS_VEHICLES.map(b=>['bus',b.id,+(b.stuck||0).toFixed(1),b.edgeId,b.term?1:0,b.dwell>0||b.curbStop?1:0,(b.stuck||0)>5?W(b):null]),...TRAFFIC_CARS.map(c=>['car',c.id+':'+c.asset,+(c.stuck||0).toFixed(1),c.edgeId,0,0,(c.stuck||0)>5?W(c):null])].filter(q=>q[2]>1)})()`);
    for (const q of r) { const k = q[0] + ' ' + q[1]; if (!M[k] || q[2] > M[k].max) M[k] = { max: q[2], edge: q[3], term: q[4], stop: q[5], why: q[6] || (M[k] && M[k].why) || null } } }
  const st = await ev(`({served:BUS_VEHICLES.reduce((a,b)=>a+(b.passengersServed||0),0),rec:BUS_VEHICLES.reduce((a,b)=>a+(b.recoveries2||0)+(b.recoveries||0),0),owned:TERM.bays.filter(q=>q.owner).length})`);
  const long = Object.entries(M).filter(([k, v]) => v.max > 5).map(([k, v]) => [k, v.max, v.edge, v.term ? 'term' : '', v.stop ? 'stop' : '']);
  const why = Object.fromEntries(Object.entries(M).filter(([k, v]) => v.max > 5).map(([k, v]) => [k, v.why]));
  const events = await ev(`CORE2_STATS.events.filter(e=>['junction_backout','lane_backout','merge_backout','hard_block','gate_backout','long_turn_yield','creep_yield','ghost_yield','queue_watchdog','engine_stall','ped_release'].includes(e.name)).slice(-30)`);
  console.log(JSON.stringify({ tag, build: path.basename(file), secs: +secs, over5: long.length, busOver5: long.filter(q => q[0].startsWith('bus')).length, long, st, pe, why, events }));
  await b.close();
})().catch(e => { console.error(String(e).slice(0, 300)); process.exit(1) });
