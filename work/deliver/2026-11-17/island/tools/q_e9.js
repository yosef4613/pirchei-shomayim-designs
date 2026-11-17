// שאילתה: היבשה של E9 (שלב 2ג-1) — isl17E9Audit, ‏s14Audit (הים, האוניות), הרישום ב-tcLiveAdd, s13Audit
return (()=>{const R={};try{R.e9=__TC_ISL17E9()}catch(e){R.e9Err=String(e)}
 try{R.e9obj={ok:ISL17E9.ok,err:ISL17E9.err,sea:ISL17E9S.ok,seaErr:ISL17E9S.err,live:ISL17LIVE.e9,liveErr:ISL17LIVE.err}}catch(e){R.objErr=String(e)}
 try{const A=s14Audit();R.s14ok=A.ok;R.s14bad=A.rows.filter(q=>!q.ok);R.s14vd=A.rows.filter(q=>/vessels_day|open_sea|buoys/.test(q.id))}catch(e){R.s14Err=String(e)}
 try{R.liveAdd=window.__TC_LIVEADD.audit()}catch(e){R.laErr=String(e)}
 try{const A=s13Audit();R.s13ok=A.ok;R.s13bad=A.checks.filter(q=>!q.ok)}catch(e){R.s13Err=String(e)}
 try{const q=(x,y)=>[x,y,w3IsSea(x,y),personBlockedAt(x,y,3),inActiveRegion(x,y)];R.pts=[q(5400,7500),q(5660,7500),q(5860,7300),q(6300,7726),q(6492,7650),q(4900,7400)]}catch(e){R.ptErr=String(e)}
 try{const S=S14.snapshot?S14.snapshot(16.6*60):null;R.shipAt=[];for(const t of [990,995,1000,1003,1006,1010,1015,1020]){const P=S14.poseOf('ship',t),T=S14.poseOf('TUG-1',t);R.shipAt.push([t,Math.round(P.x),Math.round(P.y),+P.h.toFixed(2),Math.round(T.x),Math.round(T.y)])}}catch(e){R.shipErr=String(e)}
 return R})()
