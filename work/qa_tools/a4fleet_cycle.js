// a4fleet_cycle.js — עודכן 11.11 (סוכן המיזוג, לפי המתאם): רכב ב-TRAFFIC_CARS שאינו ברשת הכבישים (roadVehicles2 — למשל משאית של קו אספקה שעומדת במפרץ, c5.mode='bay') לא נספר כ"עומד בשדרה";
// הוא נרשם בנפרד ב-offRoadStill (עם המצב והאתר). מקור: deliver/2026-11-10/merge/tools/a4fleet_cycle_m.js; הגרסה הקודמת: _to_delete/a4fleet_cycle_1111_before_roadonly.js.
// 4.11 00:30 · a4fleet_cycle — the fire engine and the ambulance of A4: every dispatch goes out, comes back and parks; no one stands still (the owner 00:25: the engine stuck half out, the emergency red, the avenue blocked)
// node a4fleet_cycle.js <game.html> <out.json> [sim_seconds=900]  — fast-forward of the simulation (simStep), a sample every 2 s
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out, secs] = process.argv.slice(2); const T = +(secs || 900);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  const r = await p.evaluate((T) => window.__TC_DEV.ev(`(()=>{const L=SIM_LOOP,H=L.h;if(L.simNow==null)L.simNow=performance.now();
    const step=s=>{const n=Math.round(s/H);for(let i=0;i<n;i++){simStep(H,L.simNow+H*1000);L.simNow+=H*1000}};
    const o={samples:[],stuck:[],trips:{fire:0,ems:0},parkedBack:{fire:0,ems:0},carsStill:[]};const last={},still={};
    for(let t=0;t<${T};t+=2){step(2);
     for(const name of ['fire','ems']){const m=A4_FLEET_STATE[name].active;if(!m){if(last[name]&&last[name].phase==='inbound')o.parkedBack[name]++;last[name]=null;continue}
      const k=name;const pv=last[k];if(!pv||pv.trip!==m.trip)o.trips[name]++;
      const mv=pv&&pv.trip===m.trip?Math.hypot(m.x-pv.x,m.y-pv.y):99;
      still[k]=(mv<0.5&&!m.scene&&!m.offsite)?(still[k]||0)+2:0;
      if(still[k]===90)o.stuck.push({t,name,phase:m.phase,x:Math.round(m.x),y:Math.round(m.y),d:Math.round(m.d),blocked:m.blocked,priority:m.priority});
      last[k]={trip:m.trip,x:m.x,y:m.y,phase:m.phase};
      if(t%20===0)o.samples.push({t,name,phase:m.phase,x:Math.round(m.x),y:Math.round(m.y),pr:!!m.priority,sc:!!m.scene,off:!!m.offsite})}
     const RV=new Set(roadVehicles2());for(const c of TRAFFIC_CARS){if(!A4_CLW_EDGES.includes(c.edgeId))continue;if(!RV.has(c)){const s=(Math.abs(c.speed||0)<0.3)?((still['o'+c.id]||0)+2):0;still['o'+c.id]=s;if(s===90)(o.offRoadStill=o.offRoadStill||[]).push({t,id:c.id,edge:c.edgeId,x:Math.round(c.x),y:Math.round(c.y),mode:c.c5&&c.c5.mode,site:c.logi&&c.logi.site,clock:(typeof gameClockHHMM==='function'?gameClockHHMM():null)});continue}const s=still['c'+c.id]=(Math.abs(c.speed||0)<0.3)?(still['c'+c.id]||0)+2:0;if(s===90)o.carsStill.push({t,id:c.id,edge:c.edgeId,x:Math.round(c.x),y:Math.round(c.y)})}}
    o.ok=!o.stuck.length&&!o.carsStill.length&&o.trips.fire>0;return o})()`), T);
  fs.writeFileSync(out, JSON.stringify(r, null, 1));
  console.log(JSON.stringify({ offRoadStill: r.offRoadStill || [], ok: r.ok, trips: r.trips, parkedBack: r.parkedBack, stuck: r.stuck.slice(0, 5), carsStill: r.carsStill.slice(0, 5) }));
  await b.close(); process.exit(r.ok ? 0 : 1);
})().catch(e => { console.error(e); process.exit(2) });
