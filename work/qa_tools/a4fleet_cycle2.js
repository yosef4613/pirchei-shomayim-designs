// a4fleet_cycle2.js — עודכן 11.11 (סוכן המיזוג, לפי המתאם): רכב ב-TRAFFIC_CARS שאינו ברשת הכבישים (roadVehicles2 — למשל משאית של קו אספקה שעומדת במפרץ, c5.mode='bay') לא נספר כ"עומד בשדרה";
// הוא נרשם בנפרד ב-offRoadStill (עם המצב והאתר). מקור: deliver/2026-11-10/merge/tools/a4fleet_cycle2_m.js; הגרסה הקודמת: _to_delete/a4fleet_cycle2_1111_before_roadonly.js.
// 4.11 07:00 · a4fleet_cycle2 — like a4fleet_cycle, and stricter (the builder 06:5x: a vehicle of the fleet "trembled" in place near J06_42 and was not counted as standing;
// one run had 2 trips instead of 4): a vehicle of the fleet that does not get 5 px further in 100 s (net, not at a scene, not off site) is stuck; and the trips must be at least 3 of each.
// The 100 s window is longer than the longest planned wait of the fleet (p577l: up to 90 s before the station).
// node a4fleet_cycle2.js <game.html> <out.json> [sim_seconds=900]
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const [file, out, secs] = process.argv.slice(2); const T = +(secs || 900);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  await p.goto('file://' + path.resolve(file) + '#dev', { waitUntil: 'commit' });
  await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  const r = await p.evaluate((T) => window.__TC_DEV.ev(`(()=>{const L=SIM_LOOP,H=L.h;if(L.simNow==null)L.simNow=performance.now();
    const step=s=>{const n=Math.round(s/H);for(let i=0;i<n;i++){simStep(H,L.simNow+H*1000);L.simNow+=H*1000}};
    const W=50,MIN_TRIPS=3;   /* 50 samples of 2 s = 100 s */
    const o={samples:[],stuck:[],trips:{fire:0,ems:0},parkedBack:{fire:0,ems:0},carsStill:[]};const last={},still={},hist={fire:[],ems:[]},flagged={};
    for(let t=0;t<${T};t+=2){step(2);
     for(const name of ['fire','ems']){const m=A4_FLEET_STATE[name].active;if(!m){if(last[name]&&last[name].phase==='inbound')o.parkedBack[name]++;last[name]=null;hist[name]=[];continue}
      const pv=last[name];if(!pv||pv.trip!==m.trip){o.trips[name]++;hist[name]=[]}
      const H_=hist[name];H_.push({x:m.x,y:m.y,free:!m.scene&&!m.offsite});if(H_.length>W+1)H_.shift();
      if(H_.length===W+1&&H_.every(q=>q.free)){const a=H_[0];const net=Math.hypot(m.x-a.x,m.y-a.y);const key=name+':'+m.trip;
        if(net<5&&!flagged[key]){flagged[key]=1;o.stuck.push({t,name,phase:m.phase,x:Math.round(m.x),y:Math.round(m.y),net:+net.toFixed(1),d:Math.round(m.d),blocked:m.blocked,priority:m.priority})}}
      last[name]={trip:m.trip,x:m.x,y:m.y,phase:m.phase};
      if(t%20===0)o.samples.push({t,name,phase:m.phase,x:Math.round(m.x),y:Math.round(m.y),pr:!!m.priority,sc:!!m.scene,off:!!m.offsite})}
     const RV=new Set(roadVehicles2());for(const c of TRAFFIC_CARS){if(!A4_CLW_EDGES.includes(c.edgeId))continue;if(!RV.has(c)){const s=(Math.abs(c.speed||0)<0.3)?((still['o'+c.id]||0)+2):0;still['o'+c.id]=s;if(s===90)(o.offRoadStill=o.offRoadStill||[]).push({t,id:c.id,edge:c.edgeId,x:Math.round(c.x),y:Math.round(c.y),mode:c.c5&&c.c5.mode,site:c.logi&&c.logi.site,clock:(typeof gameClockHHMM==='function'?gameClockHHMM():null)});continue}const s=still['c'+c.id]=(Math.abs(c.speed||0)<0.3)?(still['c'+c.id]||0)+2:0;if(s===90)o.carsStill.push({t,id:c.id,edge:c.edgeId,x:Math.round(c.x),y:Math.round(c.y)})}}
    o.minTrips=MIN_TRIPS;o.ok=!o.stuck.length&&!o.carsStill.length&&o.trips.fire>=MIN_TRIPS&&o.trips.ems>=MIN_TRIPS;return o})()`), T);
  fs.writeFileSync(out, JSON.stringify(r, null, 1));
  console.log(JSON.stringify({ offRoadStill: r.offRoadStill || [], ok: r.ok, trips: r.trips, parkedBack: r.parkedBack, stuck: r.stuck.slice(0, 5), carsStill: r.carsStill.slice(0, 5) }));
  await b.close(); process.exit(r.ok ? 0 : 1);
})().catch(e => { console.error(e); process.exit(2) });
