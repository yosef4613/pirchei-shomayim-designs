return (async()=>{const S=ms=>new Promise(r=>setTimeout(r,ms)),o={log:[]},L=s=>o.log.push(Math.round(performance.now()/1000)+'s '+s);await S(3000);
 const fps=async()=>{let n=0,t0=performance.now();await new Promise(r=>{const f=()=>{n++;if(performance.now()-t0<1000)requestAnimationFrame(f);else r()};requestAnimationFrame(f)});return n};
 try{setPhoneOpen(false)}catch(e){}o.mode0=PlayerProfile.mode;if(PlayerProfile.mode!=='walk')try{exitVehicle()}catch(e){}for(let i=0;i<60&&PlayerProfile.mode!=='walk';i++)await S(100);
 // לחכות שהמיקום יתייצב (היציאה מהרכב מסתיימת)
 let px=PlayerPed.x,py=PlayerPed.y,stable=0;for(let i=0;i<60&&stable<10;i++){await S(200);if(Math.hypot(PlayerPed.x-px,PlayerPed.y-py)<1)stable++;else stable=0;px=PlayerPed.x;py=PlayerPed.y}
 o.fps0=await fps();
 const R=PLAYER_PERSON_RADIUS;let tries=0,reached=false;
 for(;tries<3&&!reached;tries++){PlayerProfile.mode='walk';State.mapQa=false;PlayerPed.x=3716;PlayerPed.y=5100;await S(500);if(Math.abs(PlayerPed.y-5100)>40){L('teleport undone → '+Math.round(PlayerPed.x)+','+Math.round(PlayerPed.y));continue}
  Input.held.add('KeyS');let last=PlayerPed.y,still=0;const t0=performance.now();while(performance.now()-t0<30000){await S(200);if(PlayerPed.y>=5462){reached=true;break}if(Math.abs(PlayerPed.y-last)<0.5){if(++still===10){L('stall '+Math.round(PlayerPed.x)+','+Math.round(PlayerPed.y)+' '+personBlockedAt(PlayerPed.x,PlayerPed.y+R+1,R));break}}else still=0;last=PlayerPed.y}
  Input.held.delete('KeyS');L('walk '+tries+' end y '+Math.round(PlayerPed.y)+' in '+Math.round(performance.now()-t0)+'ms fps '+(await fps()))}
 o.reached=reached;o.atHead=[Math.round(PlayerPed.x),Math.round(PlayerPed.y)];
 try{gameClockSet(7,45);await S(500);const id='S14-ST-D7';S9STORY.start(id);L('start step '+S9STORY.step(id)+' clock '+gameClock().hhmm);
  let lastStep=-1,fOk=0;for(let i=0;i<300;i++){await S(1000);const n=S9STORY.step(id);if(S9STORY.done(id)){L('done · '+gameClock().hhmm);break}if(n!==lastStep){L('step '+n+' · '+gameClock().hhmm+' · ship '+s14ModeOf('ship'));lastStep=n}
   if(!State.phoneOpen){const r=interactNearbyPoi();if(r&&fOk++<3)L('F → '+r+' · '+State.interactionId)}else if(State.interactionId!=='TUG-PIER-HEAD'){setPhoneOpen(false)}
   const b=document.querySelector('[data-s9-step="'+id+'"]');if(b){b.click();L('click step '+n)}}
  o.done=S9STORY.done(id);o.final=gameClock().hhmm}catch(e){o.exc=String(e&&e.stack||e).slice(0,400)}
 try{o.pierErr=PIERX.err()}catch(e){}return o})()
