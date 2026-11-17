return (async()=>{const S=ms=>new Promise(r=>setTimeout(r,ms)),o={jumps:[]};await S(3000);
 try{setPhoneOpen(false)}catch(e){}o.mode0=PlayerProfile.mode;if(PlayerProfile.mode!=='walk')try{exitVehicle()}catch(e){}for(let i=0;i<40&&PlayerProfile.mode!=='walk';i++)await S(100);await S(3000);o.mode1=PlayerProfile.mode;
 const P=PlayerPed;let vx=P.x,vy=P.y;const rec=(k,v,old)=>{if(Math.abs(v-old)>60&&o.jumps.length<8)o.jumps.push({t:Math.round(performance.now()),k,from:Math.round(old),to:Math.round(v),stack:String(new Error().stack).split('\n').slice(3,9).map(s=>s.trim().replace(/\(?file:.*?html:/,'@')).join(' < ')})};
 Object.defineProperty(P,'x',{configurable:true,get(){return vx},set(v){rec('x',v,vx);vx=v}});Object.defineProperty(P,'y',{configurable:true,get(){return vy},set(v){rec('y',v,vy);vy=v}});
 State.mapQa=false;o.jumps.push('teleport');PlayerPed.x=3716;PlayerPed.y=5100;await S(1000);o.after1s=[Math.round(PlayerPed.x),Math.round(PlayerPed.y)];
 const tr=[];Input.held.add('KeyS');for(let i=0;i<40;i++){await S(250);tr.push(Math.round(PlayerPed.y))}Input.held.delete('KeyS');o.trace=tr.join(',');o.end=[Math.round(PlayerPed.x),Math.round(PlayerPed.y)];
 try{o.here=personBlockedAt(PlayerPed.x,PlayerPed.y+4,PLAYER_PERSON_RADIUS);o.dyn=dynamicPersonBlockedAt(PlayerPed.x,PlayerPed.y+5)}catch(e){o.hereErr=String(e)}
 try{o.lockN=TCLOCK.E.n;o.mode=TCSTORY.mode();o.tut=TCTUT.T?TCTUT.T.on:'?'}catch(e){}o.reached=PlayerPed.y>=5455;return o})()
