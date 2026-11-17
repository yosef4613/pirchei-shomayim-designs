return (async()=>{const R={};
 try{R.tug=await (async()=>{const S=ms=>new Promise(r=>setTimeout(r,ms)),o={log:[]},L=s=>o.log.push(Math.round(performance.now()/1000)+'s '+s);await S(3000);
 try{o.pierWalk=PIERX.walk()}catch(e){o.pierWalkErr=String(e)}
 try{try{setPhoneOpen(false)}catch(e){}if(PlayerProfile.mode!=='walk'){try{exitVehicle()}catch(e){}for(let i=0;i<40&&PlayerProfile.mode!=='walk';i++)await S(100);await S(3000)}PlayerProfile.mode='walk';o.modeAfterExit=PlayerProfile.mode;State.mapQa=false;let y=5100;for(;y>4700&&personBlockedAt(3716,y);y-=4);PlayerPed.x=3716;PlayerPed.y=y;await S(300);PlayerPed.x=3716;PlayerPed.y=y;o.walkStart=[3716,y];o.posCheck=[Math.round(PlayerPed.x),Math.round(PlayerPed.y)];
  Input.held.add('KeyS');await S(9000);Input.held.delete('KeyS');o.walkEnd=[Math.round(PlayerPed.x),Math.round(PlayerPed.y)];o.reachedHead=Math.hypot(PlayerPed.x-3716,PlayerPed.y-5470)<40||PlayerPed.y>=5460;
  // back to the head point itself (F radius 60)
  Input.held.add('KeyW');for(let i=0;i<40&&PlayerPed.y>5475;i++)await S(50);Input.held.delete('KeyW');o.atHead=[Math.round(PlayerPed.x),Math.round(PlayerPed.y)];
  gameClockSet(7,45);await S(500);const id='S14-ST-D7';S9STORY.start(id);L('start step '+S9STORY.step(id)+' clock '+gameClock().hhmm);
  let lastStep=-1;for(let i=0;i<300;i++){await S(1000);const n=S9STORY.step(id);if(S9STORY.done(id)){L('done');break}if(n!==lastStep){L('step '+n+' · '+gameClock().hhmm+' · ship '+s14ModeOf('ship'));lastStep=n}
   if(!State.phoneOpen){const r=interactNearbyPoi();if(i<2)L('F → '+r+' · '+State.interactionId)}else if(State.interactionId!=='TUG-PIER-HEAD'){setPhoneOpen(false)}
   const b=document.querySelector('[data-s9-step="'+id+'"]');if(b){b.click();L('click step '+n)}}
  o.done=S9STORY.done(id);o.final=gameClock().hhmm}catch(e){o.exc=String(e&&e.stack||e).slice(0,400)}return o})()}catch(e){R.tugErr=String(e&&e.stack||e).slice(0,300)}
 try{R.f2=await (async()=>{const S=ms=>new Promise(r=>setTimeout(r,ms)),o={log:[]},L=s=>o.log.push(Math.round(performance.now()/1000)+'s '+s);
 await S(4000);o.qa=PF2.qa();o.pier=PIERX.walk();o.pierErr=PIERX.err();
 try{if(PlayerProfile.mode!=='vehicle'){L('mode '+PlayerProfile.mode)}try{setPhoneOpen(false)}catch(e){}PlayerProfile.mode='vehicle';PlayerProfile.activeMission=null;PlayerCar.x=6300;PlayerCar.y=1232;PlayerCar.heading=0;PlayerCar.speed=0;
  startMission('M-F2-PICKUP');const m=PlayerProfile.activeMission;if(!m){o.fail='לא התחילה';return o}L('started '+m.id+' stage '+m.stage+' flight '+m.f2.flight+' s15 '+JSON.stringify(m.f2.s15)+' tReady-now '+(m.f2.tReady-APT_OPS.clk).toFixed(1));
  PlayerCar.x=6440;PlayerCar.y=1232;PlayerCar.heading=0;PlayerCar.speed=0;
  let t0=performance.now(),last='';for(let i=0;i<900;i++){await S(1000);const mm=PlayerProfile.activeMission;PlayerCar.speed=0;if(!mm){L('mission ended (no active)');break}
   const w=F2_PICKUP.walker,s=mm.stage+' | '+(w?('walker '+Math.round(w.x)+','+Math.round(w.y)+' '+w.state):'no walker')+' | rem '+Math.round(mm.timeRemaining);if(s.split('|')[0]!==last.split('|')[0]||(w&&!last.includes('walker'))||i%30===0)L(s);last=s;
   if(mm.stage==='drive'){L('boarded · dest '+mm.f2.dest);const t=navPoiRegistry()[mm.f2.dest];PlayerCar.x=t.x;PlayerCar.y=t.y;PlayerCar.speed=0;await S(1500);L('after teleport: active '+(PlayerProfile.activeMission?PlayerProfile.activeMission.stage:'none'));break}}
  o.done=PlayerProfile.progression?.completedMissions?.slice(-3);o.persist=PlayerProfile.worldPersistent?.airportTerminal;o.st=PF2.st;o.err=PF2.err()}catch(e){o.exc=String(e&&e.stack||e).slice(0,500)}
 return o})()}catch(e){R.f2Err=String(e&&e.stack||e).slice(0,300)}
 try{R.pfv=PFV.st;R.pfvErr=PFV.err();R.pf2=PF2.qa();R.pierErr=PIERX.err()}catch(e){R.endErr=String(e)}
 return R})()
