return (async()=>{const S=ms=>new Promise(r=>setTimeout(r,ms)),o={jumps:[]};await S(3000);
 const P=PlayerPed;let vx=P.x,vy=P.y;
 Object.defineProperty(P,'x',{configurable:true,get(){return vx},set(v){if(Math.abs(v-vx)>200&&o.jumps.length<6)o.jumps.push({t:Math.round(performance.now()),from:[Math.round(vx),Math.round(vy)],to:Math.round(v),stack:String(new Error().stack).split('\n').slice(2,9).map(s=>s.trim().replace(/\(file:.*?html:/,'(:')).join(' < ')});vx=v}});
 Object.defineProperty(P,'y',{configurable:true,get(){return vy},set(v){if(Math.abs(v-vy)>200&&o.jumps.length<6)o.jumps.push({t:Math.round(performance.now()),y:1,from:[Math.round(vx),Math.round(vy)],to:Math.round(v),stack:String(new Error().stack).split('\n').slice(2,9).map(s=>s.trim().replace(/\(file:.*?html:/,'(:')).join(' < ')});vy=v}});
 try{setPhoneOpen(false)}catch(e){}if(PlayerProfile.mode!=='walk')try{exitVehicle()}catch(e){}await S(1500);PlayerProfile.mode='walk';PlayerPed.x=3716;PlayerPed.y=5100;
 Input.held.add('KeyS');await S(3000);Input.held.delete('KeyS');o.end=[Math.round(PlayerPed.x),Math.round(PlayerPed.y)];
 try{o.tut={on:TCTUT&&TCTUT.T?TCTUT.T.on:null};o.tco=TCO.mode}catch(e){}return o})()
