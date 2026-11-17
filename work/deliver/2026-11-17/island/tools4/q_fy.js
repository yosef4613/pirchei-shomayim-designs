// שאילתה (island4, 2ג-2א): המעבורת עם רכבים במסוף החדש — 3 מחזורים מלאים של הסימולציה עצמה (__TC_SIM_STEP_QA): כמה עלו וירדו בכל צד, ההמתנה הארוכה, ורכבים תקועים בדרכים של E9
return (()=>{const R={};try{const t0=FY.T,s0=JSON.parse(JSON.stringify(FY.stats));let maxW=0,worst=null,maxStuck=0,ws=null;const E9=new Set(['IS-H1','IS-H2','IS-H3','IS-HL1','IS-HL2','IS-HL3','IS-HL4']),seen=new Set();
 for(let k=0;k<230;k++){window.__TC_SIM_STEP_QA({seconds:4,warmup:0,every:4});
  for(const v of FY.cars){const w=(v.fy.wait||0);if(w>maxW){maxW=w;worst=[v.id,v.fy.side,v.fy.st,Math.round(v.x),Math.round(v.y),v.fy.waitBy||v.fy.blkBy||null]}}
  for(const v of [...TRAFFIC_CARS,...BUS_VEHICLES]){if(!E9.has(v.edgeId))continue;seen.add(v.id);if((v.stuck||0)>maxStuck){maxStuck=v.stuck;ws=[v.id,v.edgeId,Math.round(v.x),Math.round(v.y),v.fy?v.fy.st:null]}}}
 R.T=Math.round(FY.T-t0);R.stats=FY.stats;R.s0={boarded:s0.boarded,landed:s0.landed};R.maxWait=+maxW.toFixed(1);R.worst=worst;R.e9cars=seen.size;R.maxStuckE9=+maxStuck.toFixed(1);R.worstE9=ws;
 const a=FY.audit();R.audit={ok:a.ok,issues:a.issues,cars:a.cars,q:a.q,phase:a.phase};R.log=FY.log.slice(-30);R.err=FY.err}catch(e){R.e=String(e&&e.stack||e).slice(0,400)}return R})()
