return (async()=>{const out={};const col=x=>{const r=[];let last=null;for(let y=4900;y<=5500;y+=2){let b=null;try{b=personBlockedAt(x,y)}catch(e){b='ERR'}b=b||'ok';if(b!==last){r.push(y+':'+b);last=b}}return r.join(' | ')};
 for(const x of[3702,3716,3730])out['x'+x]=col(x);
 out.R=PLAYER_PERSON_RADIUS;out.AB=ACTIVE_BOUNDS;out.chunk=currentChunkId(3716,5150);
 try{const H=Input.held;PlayerProfile.mode='walk';State.mapQa=false;let y=5100;for(;y>4700&&personBlockedAt(3716,y);y-=4);PlayerPed.x=3716;PlayerPed.y=y;out.start=[3716,y];Camera.x=3716;Camera.y=5300;H.add('KeyS');await new Promise(r=>setTimeout(r,9000));H.delete('KeyS');out.end=[Math.round(PlayerPed.x),Math.round(PlayerPed.y)];out.endBlockNext=personBlockedAt(PlayerPed.x,PlayerPed.y+2)}catch(e){out.walkErr=String(e)}
 try{out.poi=TUG_PIER_POI_dummy}catch(e){}
 return out})()
