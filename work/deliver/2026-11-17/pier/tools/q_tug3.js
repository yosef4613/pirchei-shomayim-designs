return (async()=>{const S=ms=>new Promise(r=>setTimeout(r,ms)),o={runs:[]};await S(3000);
 try{o.pw=PIERX.walk().ok}catch(e){}
 try{setPhoneOpen(false)}catch(e){}if(PlayerProfile.mode!=='walk')try{exitVehicle()}catch(e){}for(let i=0;i<40&&PlayerProfile.mode!=='walk';i++)await S(100);await S(3000);
 const R=PLAYER_PERSON_RADIUS;
 for(let run=0;run<4;run++){const r={stalls:[]};o.runs.push(r);PlayerProfile.mode='walk';State.mapQa=false;PlayerPed.x=3716;PlayerPed.y=5100;await S(300);PlayerPed.x=3716;PlayerPed.y=5100;r.clock=gameClock().hhmm;
  Input.held.add('KeyS');let last=5100,still=0;const tr=[];for(let i=0;i<45;i++){await S(200);const y=Math.round(PlayerPed.y),x=Math.round(PlayerPed.x);tr.push(y);if(Math.abs(y-last)<1){still++;if(still===2&&r.stalls.length<4){const s={at:[x,y]};for(const [dx,dy] of[[0,R+1],[0,R+3],[-3,R+1],[3,R+1]]){try{s['p'+dx+'_'+dy]=personBlockedAt(x+dx,y+dy,R)}catch(e){}try{s['d'+dx+'_'+dy]=dynamicPersonBlockedAt(x+dx,y+dy)}catch(e){}}
     try{s.near=(typeof NPC_PEDESTRIANS!=='undefined'?NPC_PEDESTRIANS:[]).filter(p=>Math.hypot(p.x-x,p.y-y)<30).map(p=>p.id+'@'+Math.round(p.x)+','+Math.round(p.y)).slice(0,5)}catch(e){}r.stalls.push(s)}}else still=0;last=y;if(y>=5490)break}
  Input.held.delete('KeyS');r.trace=tr.filter((v,i)=>i%3===0).join(',');r.end=[Math.round(PlayerPed.x),Math.round(PlayerPed.y)];r.reached=PlayerPed.y>=5455;await S(4000)}
 return o})()
