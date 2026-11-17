return (async()=>{const S=ms=>new Promise(r=>setTimeout(r,ms)),o={log:[],cands:[],runs:[]},L=s=>o.log.push(Math.round(performance.now()/1000)+'s '+s);await S(4000);
 /* F מתוך רכב מהשמירה הנקייה: עבודה שמתחילה מתוך רכב ולא דורשת רישיון — F ברכב עומד בכביש הקרוב, "התחל" בכרטיס, ונסיעה עד הסוף */
 const reg=navPoiRegistry(),closeAll=()=>{try{setPhoneOpen(false)}catch(e){}State.interactionId=null};
 o.clean={money:PlayerProfile.money,done:(PlayerProfile.progression?.completedMissions||[]).length,lic:(PlayerProfile.licenses||[]).length,mode:PlayerProfile.mode,active:!!PlayerProfile.activeMission};
 const road=(p)=>{for(let rad=0;rad<=200;rad+=8){const n=Math.max(1,Math.round(rad/4));for(let k=0;k<n*2;k++){const a=k/(n*2)*Math.PI*2,x=p.x+Math.cos(a)*rad,y=p.y+Math.sin(a)*rad;try{if(!blockedAt(x,y,PLAYER_COLLISION_RADIUS)&&pointRoad(x,y))return[x,y,rad]}catch(e){}}}return null};
 for(const [id,d] of Object.entries(MISSION_DEFS)){if(!PFV.needsVehicle(d)||d.retired||d.type==='airport-pickup')continue;if(d.license&&!licenseOwned(d.license))continue;try{if(d5MissionHidden(id))continue}catch(e){}const p=reg[d.start||d.pickup];if(!p)continue;o.cands.push(id+'/'+(d.type||'pd'))}
 const want=o.cands.map(s=>s.split('/')[0]).filter(id=>{const d=MISSION_DEFS[id],p=reg[d.start||d.pickup];return !!road(p)&&!!PFV.placeFor(p,reg)}).slice(0,3);o.want=want;
 for(const id of want){const d=MISSION_DEFS[id],p=reg[d.start||d.pickup],r={id,type:d.type||'pickup-dropoff'};o.runs.push(r);
  try{closeAll();PlayerProfile.activeMission=null;PlayerProfile.mode='vehicle';const b=road(p);if(!b){r.fail='אין כביש';continue}PlayerCar.x=b[0];PlayerCar.y=b[1];PlayerCar.speed=0;PlayerPed.x=b[0];PlayerPed.y=b[1];r.at=b[2];await S(600);
   r.hud=(()=>{try{return hudGoalText()}catch(e){return 'ERR '+e}})();
   const f=interactNearbyPoi();await S(400);r.F=f;r.opened=State.phoneOpen?State.interactionId:null;
   const btn=document.querySelector('[data-mission-start="'+id+'"]');r.btn=!!btn;r.need=(()=>{try{return ui7Need(d)}catch(e){return 'ERR'}})();
   if(btn)btn.click();else startMission(id);await S(500);const m=PlayerProfile.activeMission;r.started=!!m&&m.id===id;if(!r.started){r.fail='לא התחילה';continue}
   L(id+' started · stage '+m.stage);
   for(let i=0;i<60&&PlayerProfile.activeMission;i++){const mm=PlayerProfile.activeMission;let tid=null;
    if(mm.stage==='pickup')tid=d.pickup;else if(mm.stage==='dropoff')tid=d.dropoff;else if(mm.stage==='route')tid=d.stops[mm.routeIndex];else if(mm.stage==='bus-route'){try{tid=busPlayerStops(mm)[mm.busStopIndex].id}catch(e){}}
    const t=tid&&reg[tid];if(!t){r.stuck='stage '+mm.stage;break}PlayerCar.x=t.x;PlayerCar.y=t.y;PlayerCar.speed=0;PlayerCar.collisions=mm.startCollisions||0;
    for(let k=0;k<12&&PlayerProfile.activeMission&&PlayerProfile.activeMission.stage===mm.stage&&(mm.stage!=='route'||PlayerProfile.activeMission.routeIndex===mm.routeIndex);k++){await S(500);PlayerCar.x=t.x;PlayerCar.y=t.y;PlayerCar.speed=0}
    L(id+' → '+(PlayerProfile.activeMission?PlayerProfile.activeMission.stage+(PlayerProfile.activeMission.routeIndex!=null?' #'+PlayerProfile.activeMission.routeIndex:''):'done'))}
   r.done=(PlayerProfile.progression.completedMissions||[]).includes(id);r.money=PlayerProfile.money;if(PlayerProfile.activeMission){r.left=PlayerProfile.activeMission.stage;try{missionFail('qa')}catch(e){}}}catch(e){r.exc=String(e&&e.stack||e).slice(0,300)}}
 o.pfv=PFV.st;o.err=PFV.err();o.ok=o.runs.length>0&&o.runs.every(r=>r.F&&r.opened&&r.started&&r.done);return o})()
