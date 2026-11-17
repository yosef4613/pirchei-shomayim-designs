// q_south.js — fieldcalc: הים מדרום לשדה (x 6900–10900, ‏y 2550–3850) — ים / יבשה כל 50 פיקס׳, כלי השיט שם לאורך היום (S14 — המכמורות), והסירות של FISH3 עכשיו
return (()=>{const o={};const sea=(x,y)=>{try{return w3IsSea(x,y)?1:0}catch(e){return -1}};
 const rows=[];for(let y=2550;y<=3850;y+=50){let s='';for(let x=6900;x<=10900;x+=50)s+=sea(x,y)===1?'~':(sea(x,y)===0?'#':'?');rows.push(y+' '+s)}o.grid=rows;
 try{o.boats=(FISH3.BOATS||[]).map(b=>[b.id,Math.round(b.x),Math.round(b.y)]).slice(0,40)}catch(e){o.boatsErr=String(e)}
 try{const R=G84_CLOCK.rate||.5,L=[];for(let m=0;m<1440;m+=10){for(const id of['TRAWL-1','TRAWL-2']){const p=S14.poseOf(id,m);if(p&&p.y<4000&&p.x>6500&&p.x<11500)L.push([id,m,Math.round(p.x),Math.round(p.y)])}}o.trawls=L.slice(0,60)}catch(e){o.trawlErr=String(e)}
 try{o.buoys=[];for(const b of (S9DG.buoys||[]))if(b.y>2500&&b.y<3900)o.buoys.push([b.id,Math.round(b.x),Math.round(b.y)]);for(const b of (S14D.buoys||[]))if(b.y>2500&&b.y<3900)o.buoys.push([b.id,Math.round(b.x),Math.round(b.y)])}catch(e){o.buoyErr=String(e)}
 try{o.bshop=BSHOP&&BSHOP.G?{lane:BSHOP.G.lane,stage:BSHOP.G.stage,edge:BSHOP.G.edge}:null}catch(e){}
 return o})()
