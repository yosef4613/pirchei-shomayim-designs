// rails 17.11 — איפה רכבת נוגעת ברכבת (אותה סחיפה כמו rlSweepAudit, עם המקום)
return (()=>{const out=[];const T0=Math.max(...RL_TRAINS.map(t=>t.cycle))*2;
 for(let t=0;t<T0&&out.length<12;t+=.5){const snap=RL_TRAINS.filter(T=>!T.err).map(T=>({T,cars:rlCars(rlState(T,t*1000))}));
  for(let i=0;i<snap.length;i++)for(const a of snap[i].cars)for(let j=i+1;j<snap.length;j++)for(const c of snap[j].cars){if(c.x>G76_VIS_X||a.x>G76_VIS_X)continue;if(rlObbHit(rlObb(a),rlObb(c),3))out.push({t,a:a.id,ax:Math.round(a.x),ay:Math.round(a.y),b:c.id,bx:Math.round(c.x),by:Math.round(c.y),ra:snap[i].cars.length&&rlState(snap[i].T,t*1000).R.legs.map(l=>l[0]).join(','),rb:rlState(snap[j].T,t*1000).R.legs.map(l=>l[0]).join(',')})}}
 return out})()
