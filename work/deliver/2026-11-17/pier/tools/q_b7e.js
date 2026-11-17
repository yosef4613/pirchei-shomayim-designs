return (async()=>{const S=ms=>new Promise(r=>setTimeout(r,ms)),o={};await S(2500);o.clock=gameClock().hhmm;o.walk=PIERX.walk();
 const col=(x,y0,y1)=>{const r=[];let last=null;for(let y=y0;y<=y1;y+=2){let b=null;try{b=personBlockedAt(x,y)}catch(e){b='ERR'}b=b||'ok';if(b!==last){r.push(y+':'+b);last=b}}return r.join(' | ')};
 for(const x of[2104,2110,2115,2120,2126])o['x'+x]=col(x,4940,5420);
 const row=(y)=>{const r=[];let last=null;for(let x=2060;x<=2170;x+=2){let b=personBlockedAt(x,y)||'ok';if(b!==last){r.push(x+':'+b);last=b}}return r.join(' | ')};
 for(const y of[4990,4996,5002,5010,5030])o['y'+y]=row(y);
 try{o.dyn=[];for(let y=4960;y<=5420;y+=10){const d=dynamicPersonBlockedAt(2115,y);if(d)o.dyn.push(y+':'+d)}}catch(e){o.dynErr=String(e)}
 return o})()
