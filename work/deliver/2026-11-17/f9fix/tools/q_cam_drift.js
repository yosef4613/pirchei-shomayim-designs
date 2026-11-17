return (async()=>{const w=ms=>new Promise(r=>setTimeout(r,ms));const out=[];
 if(!PERF.hud)perfHudToggle();tcF9Show('zones');await w(300);
 const run=async(lbl,f)=>{f();const s=[];for(let i=0;i<8;i++){s.push([Math.round(Camera.x),Math.round(Camera.y),+Camera.zoom.toFixed(2)]);await w(150)}out.push([lbl,s,{mapQa:State.mapQa,held:[...Input.held],follow:typeof Camera.follow!=='undefined'?Camera.follow:null,mode:PlayerProfile.mode}])};
 await run('cam 600,-425',()=>tcF9Cam(600,-425,1.1));
 await run('cam 750,-475 z3',()=>tcF9Cam(750,-475,3));
 await run('cam 600,346',()=>tcF9Cam(600,346,1.1));
 await run('cam 3000,3000',()=>tcF9Cam(3000,3000,1.1));
 return out})()
