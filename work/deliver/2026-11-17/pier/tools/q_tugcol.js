return (async()=>{const S=ms=>new Promise(r=>setTimeout(r,ms)),o={};await S(3000);
 try{o.mode=TCSTORY.mode();o.saveMode=TCSAVE.mode()}catch(e){o.modeErr=String(e)}
 const R=PLAYER_PERSON_RADIUS;const col=(x,y0,y1)=>{const r=[];let last=null;for(let y=y0;y<=y1;y+=2){let b=null;try{b=personBlockedAt(x,y,R)}catch(e){b='ERR'}b=b||'ok';if(b!==last){r.push(y+':'+b);last=b}}return r.join(' | ')};
 o.col3716=col(3716,5080,5480);o.col3700=col(3700,5080,5480);o.col3730=col(3730,5080,5480);
 try{o.zone=[currentChunkId(3716,5100),currentChunkId(3716,5300),currentChunkId(3716,5460)];o.lk=[TCLOCK.lockedAt(3716,5100),TCLOCK.lockedAt(3716,5300)].map(v=>v&&v.name||v)}catch(e){o.zErr=String(e)}
 try{setPhoneOpen(false)}catch(e){}if(PlayerProfile.mode!=='walk')try{exitVehicle()}catch(e){}await S(1500);PlayerProfile.mode='walk';State.mapQa=false;PlayerPed.x=3716;PlayerPed.y=5100;await S(300);PlayerPed.x=3716;PlayerPed.y=5100;
 const n0=JSON.stringify(TCLOCK.E.n);const tr=[];Input.held.add('KeyS');for(let i=0;i<18;i++){await S(500);tr.push(Math.round(PlayerPed.y))}Input.held.delete('KeyS');o.trace=tr.join(',');o.end=[Math.round(PlayerPed.x),Math.round(PlayerPed.y)];o.lockN=[n0,JSON.stringify(TCLOCK.E.n)];
 try{o.here=personBlockedAt(PlayerPed.x,PlayerPed.y+3,R);o.dyn=dynamicPersonBlockedAt(PlayerPed.x,PlayerPed.y+4)}catch(e){o.hereErr=String(e)}
 try{o.cam=[Camera.zoom,State.phoneOpen,State.mapQa,PlayerProfile.mode,State.cutscene||null,typeof CUTS!=='undefined'?Object.keys(CUTS).slice(0,5):null]}catch(e){}
 return o})()
