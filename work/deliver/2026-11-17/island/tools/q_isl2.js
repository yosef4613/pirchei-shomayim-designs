// שאילתה: שלב 2א — H8 (ISL17H8): יבשה / ים בנקודות, האסדה בים, תחנת הגז והמקום, ובדיקת האי; וגם הרכבל (ISL17)
return (()=>{const R={};R.h8ok=ISL17H8.ok;R.h8err=ISL17H8.err;R.gondola=ISL17.ok;R.gErr=ISL17.err;{const t=performance.now()/1000,P=Array.from({length:ISL17.N},(_,k)=>{const p=ISL17.pose(k,t,true);return Math.round(p.x)+','+Math.round(p.y)});R.cabins=ISL17.N;R.distinct=new Set(P).size}
 const pts={'H8 יבשה 9000,6700':[9000,6700],'H8 יבשה 9500,6620':[9500,6620],'האסדה 8975,6250':[8975,6250],'קצה הלפיד 9210,6468':[9210,6468],'ספינת האספקה 8790,6560':[8790,6560],'8600,6560':[8600,6560],'מזרח 9550,6560':[9550,6560],'H9 9300,7100':[9300,7100],'נתיב 8400,5880':[8400,5880]};
 R.sea={};for(const [k,[x,y]] of Object.entries(pts))R.sea[k]=w3IsSea(x,y)?'ים':'יבשה';
 R.walk={gas:personBlockedAt(9500,6788,3),h8:personBlockedAt(9000,6700,3)};R.bld=C4_BUILDINGS.some(b=>b.id==='IS-GAS-B');R.poi=!!S13_POIS['IS-GAS'];
 try{R.f=phoneS13Business?'יש':'אין'}catch(e){}
 try{const A=s13Audit();R.auditOk=A.ok;R.auditBad=A.checks.filter(q=>!q.ok)}catch(e){R.auditErr=String(e)}
 try{R.live={via:(typeof ISL17LIVE!=='undefined'?ISL17LIVE.via+(ISL17LIVE.err?' · '+ISL17LIVE.err:''):'?'),liveAdd:(window.__TC_LIVEADD?__TC_LIVEADD.list():'אין 028z'),liveAudit:(window.__TC_LIVEADD?__TC_LIVEADD.audit():null),mapH8:MAP_ACTIVE_IDS.has('H8'),regions:ACTIVE_REGIONS.length,ids:MAP_ACTIVE_IDS.size,seaPerson:personBlockedAt(8600,6560,3),seaCar:blockedAt(8600,6560,8),seaRig:personBlockedAt(9300,6200,3),landCar:blockedAt(9000,6720,8)}}catch(e){R.liveErr=String(e)}
 R.lifeErr=S13LIFE.err();R.placesErr=S13P.err;R.landErr=S13L.err;try{R.rigErr=S10U.err?S10U.err():null}catch(e){}
 return R})()
