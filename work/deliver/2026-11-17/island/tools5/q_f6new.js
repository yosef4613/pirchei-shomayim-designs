// island5: הבדיקות של מעבר הסירות החדש ב-F6 — S10V, ‏f56Audit, ‏s16cEastAudit, המטוס האמפיבי, S14 ושגיאות
return (()=>{const R={};const sh=a=>a&&a.checks?{ok:a.ok,bad:a.checks.filter(c=>!c.ok).map(c=>c.name+': '+String(c.detail).slice(0,300)),all:a.checks.map(c=>c.name+(c.ok?' ✓ ':' ✗ ')+String(c.detail).slice(0,200))}:a;
 try{R.s10v=sh(S10V.audit())}catch(e){R.s10v=String(e)}
 try{const a=f56Audit();R.f56={ok:a.ok,issues:a.issues}}catch(e){R.f56=String(e)}
 try{R.s16cEast=s16cEastAudit()}catch(e){R.s16cEast=String(e)}
 try{const a=AMPH.audit();R.amph=a&&a.checks?{ok:a.ok,bad:a.checks.filter(c=>!c.ok).map(c=>(c.id||c.name)+': '+String(c.det||c.detail).slice(0,300)),boats:a.checks.filter(c=>/boat|pilot/.test(c.id||c.name)).map(c=>(c.id||c.name)+(c.ok?' ✓ ':' ✗ ')+String(c.det||c.detail).slice(0,240))}:a}catch(e){R.amph=String(e)}
 try{const a=s14Audit();R.s14=Array.isArray(a)?a.filter(c=>!c.ok).map(c=>c.id+': '+c.det.slice(0,200)):a}catch(e){R.s14=String(e)}
 try{const a=roadAudit();R.road={ok:a.ok,bad:(a.checks||[]).filter(c=>!c.ok).map(c=>c.name+': '+String(c.detail).slice(0,240))}}catch(e){R.road=String(e)}
 try{R.errs={s10v:S10V.err(),s9x:(typeof S9X!=='undefined'?S9X.err:null),f56live:F56LIVE.err(),amph:AMPH.err()}}catch(e){R.errs=String(e)}
 try{R.piers=['EAST-B4','EAST-N1','EAST-C','EAST-S2'].map(id=>{const g=RAIL_SEG_BY_ID[id];return id+':'+rlPiers(g).filter(q=>q.x>6600&&q.x<7400).map(q=>Math.round(q.x)).join(',')})}catch(e){R.piers=String(e)}
 try{const P=[];for(let t=300;t<620;t+=6){const q=F56LIVE.pilotPose(t*1000);if(q)P.push([t,Math.round(q.x),Math.round(q.y)])}R.pilot=P}catch(e){R.pilot=String(e)}
 return R})()
