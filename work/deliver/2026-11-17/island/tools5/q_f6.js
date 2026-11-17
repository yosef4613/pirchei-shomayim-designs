// island5: הגאומטריה סביב מעבר הסירות ב-F6 — המסילות, העמודים, המצופים, סירת הנתב, הים
return (()=>{const R={};const BX=[5900,4300,8600,5500];
 const inB=(x,y)=>x>BX[0]&&x<BX[2]&&y>BX[1]&&y<BX[3];
 R.segs=RAIL_SEGS.filter(g=>g.pts.some(p=>inB(p[0],p[1]))).map(g=>{const P=g.pts.filter(p=>inB(p[0],p[1]));const step=Math.max(1,Math.floor(P.length/14));
   let piers=[];try{piers=rlPiers(g).filter(q=>inB(q.x,q.y)).map(q=>[Math.round(q.x),Math.round(q.y)])}catch(e){piers=['err']}
   return{id:g.id,from:g.from,to:g.to,kind:g.kind,track:g.track,n:g.pts.length,len:Math.round(g.len||0),pts:P.filter((p,i)=>i%step===0||i===P.length-1).map(p=>[Math.round(p[0]),Math.round(p[1])]),piers:piers.length>40?piers.filter((p,i)=>i%2===0):piers,np:piers.length}});
 try{R.siding=F56_SIDING.pts.filter((p,i)=>i%6===0).map(p=>[Math.round(p[0]),Math.round(p[1])])}catch(e){R.siding=String(e)}
 try{R.buoys=F56_BUOYS.map(b=>[b.id,b.x,b.y])}catch(e){R.buoys=String(e)}
 try{R.s10v={SPAN:S10V.SPAN,CH:S10V.CH,audit:S10V.audit()}}catch(e){R.s10v=String(e)}
 try{const P=[];for(let t=0;t<900;t+=3){const q=F56LIVE.pilotPose(t*1000);if(q)P.push([Math.round(q.x),Math.round(q.y),q.stop||''])}R.pilot=P}catch(e){R.pilot=String(e)}
 try{const rows=[];for(let y=4300;y<=5500;y+=40){let s='';for(let x=5900;x<=8600;x+=40)s+=w3IsSea(x,y)?'~':'#';rows.push(y+' '+s)}R.sea=rows}catch(e){R.sea=String(e)}
 try{R.nodes=RAIL_NODES.filter(n=>inB(n.x,n.y)).map(n=>[n.id,Math.round(n.x),Math.round(n.y),n.type])}catch(e){}
 try{R.chunks=Object.entries(MAP_CHUNKS||{}).filter(([k,v])=>/^[EFGH][4-8]$/.test(k)).map(([k,v])=>[k,v.kind||v.type||v.t||JSON.stringify(v).slice(0,60)])}catch(e){R.chunks=String(e)}
 try{R.hooks={rail:S9_HOOKS.rail.length,over:S9_HOOKS.over.length,water:S9_HOOKS.water.length}}catch(e){}
 return R})()
