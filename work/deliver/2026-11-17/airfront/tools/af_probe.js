// af_probe.js <build> <secs> <out.json> [hash] (secs — שניות משחק: SIM.t; ‏FAST=n — עוד n צעדי סימולציה בכל דגימה, להאצה; ‏WALLMAX — תקרת שניות אמת) — airfront: כמו stuckmax (כל 0.5 שנ׳, כל הרכבים), ועל כל מכונית ב-AIR-FRONT / AIR-CONN / AIR-ACC-N שתקועה מעל 4 שנ׳ —
// כל השדות שלה ושל c2 (למה עומדת: limit, ‏limitLead, ‏hardBy), מי שמולה (המוביל / הגוף שנוגע) ומי שבתוך 200 פיקס׳, שעון המשחק, והאירועים של CORE2 עליה. פעם ב-2 שנ׳ לכל מכונית.
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
(async () => {
  const [file, secs, out, hash] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--no-sandbox'] }); const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const pe = []; p.on('pageerror', e => pe.push(String(e).slice(0, 200)));
  await p.goto('file://' + path.resolve(file) + '#' + (hash || 'dev'), { waitUntil: 'commit' }); await p.waitForFunction(() => window.__TC_DEV && window.__TC_DEV.ready(), null, { timeout: 600000, polling: 500 });
  const ev = s => p.evaluate(x => window.__TC_DEV.ev(x), s);
  const geo = await ev(`(()=>{const o={};for(const id of ['AIR-FRONT','AIR-CONN','AIR-ACC-N']){const e=byEdge[id];if(!e)continue;o[id]={a:e.a,b:e.b,cls:e.cls,pts:(e.points||e.pts||[]).map(p=>[Math.round(p.x??p[0]),Math.round(p.y??p[1])])};try{o[id].l0=lane2(id,1,0);o[id].l1=lane2(id,1,1)}catch(x){}}return JSON.parse(JSON.stringify(o,(k,v)=>typeof v==='number'?Math.round(v*10)/10:v))})()`).catch(e => String(e));
  const M = {}, rec = [], last = {}, t0 = Date.now();
  const SNAP = `(()=>{const F=new Set(['AIR-FRONT','AIR-CONN','AIR-ACC-N']);const R=v=>Math.round(v);const o=[];
   const c2of=c=>{const q=c&&c.c2;if(!q)return null;return{limit:q.limit,lead:q.limitLead,gap:q.limitGap!=null?+(+q.limitGap).toFixed(1):null,hardBy:q.hardBy,blockT:+(q.blockT||0).toFixed(1),stuckT:+(q.stuckT||0).toFixed(1),s:q.s!=null?+q.s.toFixed(1):null,lane:q.lane?q.lane.id:null,k:q.lane?q.lane.k:null,stopS:q.lane&&q.lane.stopS!=null?+q.lane.stopS.toFixed(1):null,len:q.lane&&q.lane.len!=null?+q.lane.len.toFixed(1):null,mv:q.mv?q.mv.id||q.mv.node:null,gate:q.gate?(q.gate.id||q.gate.node||1):null,granted:!!q.granted,why:q.why||null,next:q.nextKey||null,lc:!!q.laneChanging,laneBack:q.laneBack||0,backout:!!q.backout,profile:q.profile,cooldown:q.cooldown||0}};
   const brief=d=>({id:d.id,asset:d.asset,x:R(d.x),y:R(d.y),h:d.heading!=null?+d.heading.toFixed(2):null,edge:d.edgeId,sp:d.speed!=null?+(+d.speed).toFixed(1):null,stuck:d.stuck!=null?+(+d.stuck).toFixed(1):null,ghost:d.ghost||0,wait:!!d.wait,c2:c2of(d),cl:d.cl?{ph:d.cl.ph,where:d.cl.where,by:d.cl.by,wt:d.cl.wt}:null,s16:d.s16p||d.s16||null,lnph:d.ln?d.ln.ph:null,dwell:d.dwell||0,curb:d.curbStop?(d.curbStop.id||1):null,taxi:d.taxiRoute?{arrived:!!d.taxiRoute.arrived,hold:!!d.taxiRoute.hold}:null,evt:d.evt?d.evt.ph:null,mode:d.c5?d.c5.mode:null,logi:d.logi?d.logi.m:null});
   const all=[...TRAFFIC_CARS,...BUS_VEHICLES];
   const FZ=(window.__AFZ=window.__AFZ||{});const tnow=SIM.t;
   for(const c of [...TRAFFIC_CARS,...BUS_VEHICLES.filter(b=>TRAFFIC_CARS.indexOf(b)<0)]){if(!F.has(c.edgeId)){delete FZ[c.id];continue}
    const z=FZ[c.id];if(!z||Math.abs(z.x-c.x)>1||Math.abs(z.y-c.y)>1){FZ[c.id]={x:c.x,y:c.y,t:tnow}}c.__afz=tnow-FZ[c.id].t}
   for(const c of [...TRAFFIC_CARS,...BUS_VEHICLES.filter(b=>TRAFFIC_CARS.indexOf(b)<0)]){if(!F.has(c.edgeId)||!(c.stuck>4||(c.__afz>8&&!(c.cl&&c.cl.ph!=='road'&&c.cl.ph!=='wander'))))continue;
    const near=all.filter(d=>d!==c&&Math.hypot(d.x-c.x,d.y-c.y)<200).map(brief);
    const pk=PARKED_CARS.filter(d=>Math.hypot(d.x-c.x,d.y-c.y)<90).map(d=>({id:d.id,x:R(d.x),y:R(d.y)}));
    const peds=(typeof NPC_PEDESTRIANS!=='undefined'?NPC_PEDESTRIANS:[]).filter(d=>Math.hypot(d.x-c.x,d.y-c.y)<60).map(d=>({id:d.id,x:R(d.x),y:R(d.y),st:d.state||d.mode||null}));
    const evs=(CORE2_STATS.events||[]).filter(e=>e.id===c.id||e.to===c.id||e.blocker===c.id).slice(-6);
    const keys=Object.keys(c).filter(k=>c[k]!=null&&typeof c[k]!=='function');
    const raw={};for(const k of keys){const v=c[k];if(typeof v!=='object')raw[k]=v;else if(Array.isArray(v))raw[k]='arr'+v.length;else raw[k]='obj:'+Object.keys(v).slice(0,8).join(',')}
    o.push({frozen:+(c.__afz||0).toFixed(1),ln:c.ln?{no:c.ln.no,ph:c.ln.ph,target:c.ln.target,at:c.ln.at,wait:c.ln.wait,dir:c.ln.dir}:null,clk:(typeof APT_OPS!=='undefined'?APT_OPS.clk:null),simT:+SIM.t.toFixed(1),car:brief(c),raw,near,pk,peds,evs})}
   const st=[...BUS_VEHICLES.map(b=>['bus',b.id,+(b.stuck||0).toFixed(1),b.edgeId,Math.round(b.x),Math.round(b.y)]),...TRAFFIC_CARS.map(c=>['car',c.id+':'+c.asset,+(c.stuck||0).toFixed(1),c.edgeId,Math.round(c.x),Math.round(c.y)])].filter(q=>q[2]>1);
   return{o,st,simT:+SIM.t.toFixed(1)}})()`;
  let simT = 0; const FAST = +(process.env.FAST || 0), WALLMAX = +(process.env.WALLMAX || 1500); const T0 = await ev('SIM.t');
  const FF = `(()=>{const L=SIM_LOOP,H=L.h;for(let i=0;i<${FAST};i++){simInterpSnapshot();simStep(H,L.simNow+H*1000);L.simNow+=H*1000}simInterpPost();return 1})()`;
  for (let t = 0; simT - T0 < (+secs || 150) && Date.now() - t0 < WALLMAX * 1000; t++) { await p.waitForTimeout(500);
    if (FAST) { try { await ev(FF) } catch (e) { pe.push('ff: ' + String(e).slice(0, 200)) } }
    let r; try { r = await ev(SNAP) } catch (e) { pe.push('probe: ' + String(e).slice(0, 200)); continue }
    simT = r.simT;
    for (const q of r.st) { const k = q[0] + ' ' + q[1]; if (!M[k] || q[2] > M[k].max) M[k] = { max: q[2], edge: q[3], x: q[4], y: q[5], at: r.simT } }
    for (const q of r.o) { const k = q.car.id; if (last[k] && t - last[k] < 4) continue; last[k] = t; q.wall = +((Date.now() - t0) / 1000).toFixed(1); rec.push(q) } }
  const long = Object.entries(M).filter(([k, v]) => v.max > 5).map(([k, v]) => [k, v.max, v.edge, v.x, v.y, v.at]);
  const res = { build: path.basename(file), secs: +secs, simT0: T0, simT, wall: +((Date.now() - t0) / 1000).toFixed(0), fast: FAST, over5: long.length, front: long.filter(q => q[2] === 'AIR-FRONT').length, long, pe, geo, rec };
  fs.writeFileSync(out, JSON.stringify(res, null, 1));
  console.log(JSON.stringify({ build: res.build, game: +(simT - T0).toFixed(0), wall: res.wall, fast: FAST, over5: res.over5, front: res.front, long, recs: rec.length, pe: pe.length }));
  await b.close();
})().catch(e => { console.error(String(e).slice(0, 300)); process.exit(1) });
