return (async()=>{const R={};
 try{R.b7=await (async()=>{const o={};const col=(x,y0,y1)=>{const r=[];let last=null;for(let y=y0;y<=y1;y+=2){let b=null;try{b=personBlockedAt(x,y)}catch(e){b='ERR'}b=b||'ok';let w='';try{w=WATERWALK.isWater(x,y)?'w':'l'}catch(e){}b=b+'/'+w;if(b!==last){r.push(y+':'+b);last=b}}return r.join(' | ')};
 for(const x of[1895,2105,2115,2125])o['x'+x]=col(x,4850,5060);
 const row=(y,x0,x1)=>{const r=[];let last=null;for(let x=x0;x<=x1;x+=2){let b=personBlockedAt(x,y)||'ok';if(b!==last){r.push(x+':'+b);last=b}}return r.join(' | ')};
 o.row4990=row(4990,2000,2250);o.row4970=row(4970,2000,2250);o.row4940=row(4940,2000,2250);
 o.decks=WATERWALK.decks().filter(d=>/B7/.test(d.id)).map(d=>d.id+':'+d.r.join(','));o.roots=o.decks.length;try{o.r2=PIERX.roots([2100,5000,2130,5420]);o.r1=PIERX.roots([1880,5000,1910,5420])}catch(e){}
 return o})()}catch(e){R.b7Err=String(e&&e.stack||e).slice(0,300)}
 try{R.fveh=await (async()=>{const S=ms=>new Promise(r=>setTimeout(r,ms));await S(3000);const out={rows:[],err:[]};
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
 try{out.need=[ui7Need(MISSION_DEFS['M-E3-TAXI']),(PlayerProfile.mode='walk',ui7Need(MISSION_DEFS['M-E3-TAXI']))]}catch(e){out.needErr=String(e)}PlayerProfile.mode='vehicle';try{out.pfv=PFV.st;out.pfvErr=PFV.err()}catch(e){}return out})()}catch(e){R.fvehErr=String(e&&e.stack||e).slice(0,300)}
 try{R.tug=await (async()=>{const S=ms=>new Promise(r=>setTimeout(r,ms)),o={log:[]},L=s=>o.log.push(Math.round(performance.now()/1000)+'s '+s);await S(3000);
 try{o.pierWalk=PIERX.walk()}catch(e){o.pierWalkErr=String(e)}
 try{try{setPhoneOpen(false)}catch(e){}if(PlayerProfile.mode!=='walk')try{exitVehicle()}catch(e){}PlayerProfile.mode='walk';State.mapQa=false;let y=5100;for(;y>4700&&personBlockedAt(3716,y);y-=4);PlayerPed.x=3716;PlayerPed.y=y;o.walkStart=[3716,y];
  Input.held.add('KeyS');await S(9000);Input.held.delete('KeyS');o.walkEnd=[Math.round(PlayerPed.x),Math.round(PlayerPed.y)];o.reachedHead=Math.hypot(PlayerPed.x-3716,PlayerPed.y-5470)<40||PlayerPed.y>=5460;
  // back to the head point itself (F radius 60)
  Input.held.add('KeyW');for(let i=0;i<40&&PlayerPed.y>5475;i++)await S(50);Input.held.delete('KeyW');o.atHead=[Math.round(PlayerPed.x),Math.round(PlayerPed.y)];
  gameClockSet(7,45);await S(500);const id='S14-ST-D7';S9STORY.start(id);L('start step '+S9STORY.step(id)+' clock '+gameClock().hhmm);
  let lastStep=-1;for(let i=0;i<300;i++){await S(1000);const n=S9STORY.step(id);if(S9STORY.done(id)){L('done');break}if(n!==lastStep){L('step '+n+' · '+gameClock().hhmm+' · ship '+s14ModeOf('ship'));lastStep=n}
   if(!State.phoneOpen){const r=interactNearbyPoi();if(i<2)L('F → '+r+' · '+State.interactionId)}else if(State.interactionId!=='TUG-PIER-HEAD'){setPhoneOpen(false)}
   const b=document.querySelector('[data-s9-step="'+id+'"]');if(b){b.click();L('click step '+n)}}
  o.done=S9STORY.done(id);o.final=gameClock().hhmm}catch(e){o.exc=String(e&&e.stack||e).slice(0,400)}return o})()}catch(e){R.tugErr=String(e&&e.stack||e).slice(0,300)}
 return R})()
