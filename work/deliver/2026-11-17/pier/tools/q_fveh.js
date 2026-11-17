return (async()=>{const S=ms=>new Promise(r=>setTimeout(r,ms));await S(3000);const out={rows:[],err:[]};
 const SPEC=['ground-training','runway-observation','tower-view','shift','forklift'];
 const reg=navPoiRegistry();const closeAll=()=>{try{if(typeof G77_FF!=='undefined'&&G77_FF.open)g77FfClose()}catch(e){}try{setPhoneOpen(false)}catch(e){}try{if(PlayerProfile.mode==='vehicle'&&State.phoneOpen)setPhoneOpen(false)}catch(e){}State.interactionId=null};
 const opened=()=>{const o=[];try{if(State.phoneOpen)o.push('phone:'+(State.interactionId||'?'))}catch(e){}try{if(typeof G77_FF!=='undefined'&&G77_FF.open)o.push('ff')}catch(e){}try{if(typeof PLACE!=='undefined'&&PLACE.on)o.push('place:'+(PLACE.on.app||'?')+'/'+(PLACE.on.id||'?'))}catch(e){}return o.join(',')};
 const seen=new Set();
 for(const [id,d] of Object.entries(MISSION_DEFS)){if(d.walk||C4_JOBS.includes(id)||SPEC.includes(d.type)||d.retired)continue;const pid=d.start||d.pickup;if(!pid||seen.has(pid))continue;seen.add(pid);const p=reg[pid];if(!p){out.err.push(id+': אין '+pid);continue}
  const row={job:id,poi:pid,chunk:p.chunk||currentChunkId(p.x,p.y),x:Math.round(p.x),y:Math.round(p.y)};
  try{closeAll();PlayerProfile.activeMission=null;PlayerProfile.mode='walk';PlayerPed.x=p.x;PlayerPed.y=p.y;await S(30);let r=false;try{r=interactNearbyPoi()}catch(e){row.footErr=String(e).slice(0,80)}row.foot=(r?'T':'F')+' '+opened();closeAll();
   // the nearest drivable point
   let best=null;for(let rad=0;rad<=200&&!best;rad+=8){const n=Math.max(1,Math.round(rad/4));for(let k=0;k<n*2;k++){const a=k/(n*2)*Math.PI*2,x=p.x+Math.cos(a)*rad,y=p.y+Math.sin(a)*rad;try{if(!blockedAt(x,y,PLAYER_COLLISION_RADIUS)&&pointRoad(x,y)){best=[x,y,rad];break}}catch(e){}}}
   if(!best){row.veh='אין כביש עד 200';}else{PlayerProfile.mode='vehicle';PlayerCar.x=best[0];PlayerCar.y=best[1];PlayerCar.speed=0;PlayerPed.x=best[0];PlayerPed.y=best[1];await S(30);let r2=false;try{r2=interactNearbyPoi()}catch(e){row.vehErr=String(e).slice(0,80)}row.veh=(r2?'T':'F')+' '+opened()+' @'+best[2];closeAll()}}catch(e){row.exc=String(e).slice(0,120)}
  out.rows.push(row)}
 try{out.need=[ui7Need(MISSION_DEFS['M-E3-TAXI']),(PlayerProfile.mode='walk',ui7Need(MISSION_DEFS['M-E3-TAXI']))]}catch(e){out.needErr=String(e)}PlayerProfile.mode='vehicle';try{out.pfv=PFV.st;out.pfvErr=PFV.err()}catch(e){}return out})()
