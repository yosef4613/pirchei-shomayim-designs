return (async()=>{const S=ms=>new Promise(r=>setTimeout(r,ms)),o={log:[]},L=s=>o.log.push(Math.round(performance.now()/1000)+'s '+s);await S(3000);
 try{o.pierWalk=PIERX.walk()}catch(e){o.pierWalkErr=String(e)}
 try{try{setPhoneOpen(false)}catch(e){}if(PlayerProfile.mode!=='walk'){try{exitVehicle()}catch(e){}await S(2500)}PlayerProfile.mode='walk';o.modeAfterExit=PlayerProfile.mode;State.mapQa=false;let y=5100;for(;y>4700&&personBlockedAt(3716,y);y-=4);PlayerPed.x=3716;PlayerPed.y=y;await S(300);PlayerPed.x=3716;PlayerPed.y=y;o.walkStart=[3716,y];o.posCheck=[Math.round(PlayerPed.x),Math.round(PlayerPed.y)];
  Input.held.add('KeyS');await S(9000);Input.held.delete('KeyS');o.walkEnd=[Math.round(PlayerPed.x),Math.round(PlayerPed.y)];o.reachedHead=Math.hypot(PlayerPed.x-3716,PlayerPed.y-5470)<40||PlayerPed.y>=5460;
  // back to the head point itself (F radius 60)
  Input.held.add('KeyW');for(let i=0;i<40&&PlayerPed.y>5475;i++)await S(50);Input.held.delete('KeyW');o.atHead=[Math.round(PlayerPed.x),Math.round(PlayerPed.y)];
  gameClockSet(7,45);await S(500);const id='S14-ST-D7';S9STORY.start(id);L('start step '+S9STORY.step(id)+' clock '+gameClock().hhmm);
  let lastStep=-1;for(let i=0;i<300;i++){await S(1000);const n=S9STORY.step(id);if(S9STORY.done(id)){L('done');break}if(n!==lastStep){L('step '+n+' · '+gameClock().hhmm+' · ship '+s14ModeOf('ship'));lastStep=n}
   if(!State.phoneOpen){const r=interactNearbyPoi();if(i<2)L('F → '+r+' · '+State.interactionId)}else if(State.interactionId!=='TUG-PIER-HEAD'){setPhoneOpen(false)}
   const b=document.querySelector('[data-s9-step="'+id+'"]');if(b){b.click();L('click step '+n)}}
  o.done=S9STORY.done(id);o.final=gameClock().hhmm}catch(e){o.exc=String(e&&e.stack||e).slice(0,400)}return o})()
