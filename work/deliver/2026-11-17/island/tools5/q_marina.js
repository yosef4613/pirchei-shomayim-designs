// island5: המרינה ב-½ D9 וסגירת האגן העליון — הבדיקות והשגיאות
return (()=>{const R={};
 try{R.e9land=isl17E9Audit()}catch(e){R.e9land=String(e)}
 try{R.mar=ISL17MAR.ok?ISL17MAR.audit():{err:ISL17MAR.err,off:ISL17MAR.off}}catch(e){R.mar=String(e)}
 try{R.errs={e9:ISL17E9.err,mar:ISL17MAR.err,life:S13LIFE.err(),s13l:S13L.err,ft:ISL17FT.err,live:ISL17LIVE}}catch(e){R.errs=String(e)}
 try{const a=roadAudit();R.road={ok:a.ok,bad:(a.checks||[]).filter(c=>!c.ok).map(c=>c.name+': '+String(c.detail).slice(0,300))}}catch(e){R.road=String(e)}
 try{const a=s14Audit();R.s14=a.filter(c=>!c.ok).map(c=>c.id+': '+c.det.slice(0,240))}catch(e){R.s14=String(e)}
 try{R.water=S13D.water.map(P=>P.map(p=>p.join(',')).join(' '))}catch(e){}
 try{const P=[];for(let t=0;t<900;t+=20){const q=S13LIFE.fbPose(t);P.push([t,Math.round(q.x),Math.round(q.y),q.stop||''])}R.fb=P}catch(e){R.fb=String(e)}
 try{R.pts=[[4440,7540],[4500,7416],[4600,7700],[5900,7150],[6300,7160],[5860,7250]].map(([x,y])=>[x,y,w3IsSea(x,y)?'sea':'land',personBlockedAt(x,y,3)||'-',inActiveRegion(x,y)])}catch(e){R.pts=String(e)}
 return R})()
